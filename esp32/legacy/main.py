print("main.py: 开始加载")
import machine
import time
import _thread
from machine import Pin, PWM
from umqttsimple import MQTTClient
import network
import ujson
import sys
import dht  # 添加DHT模块导入

# 配置WiFi信息
WIFI_SSID = "你的WiFi名称"  # 留档脱敏：请填入真实值
WIFI_PASSWORD = "你的WiFi密码"  # 留档脱敏：请填入真实值

# --- MQTT 核心配置与变量 ---
MQTT_BROKER = "192.168.137.1"  # 电脑移动热点（本地连接* 2）IPv4
MQTT_PORT = 1883  # 默认MQTT端口
CLIENT_ID = "esp32_lipreading_iot"  # 客户端ID
SUBSCRIBE_TOPIC = b"lip_reading/iot"  # 仅订阅此主题
PUBLISH_ENV_TOPIC = b"lip_reading/environment"  # 发布温湿度数据的常规主题
PUBLISH_SRC_TOPIC = b"lip_reading/src_text"  # 指令5触发的温湿度发布主题

# 全局变量
mqtt_client = None  # MQTT客户端实例
last_connect_time = 0
connect_interval = 5  # MQTT重连间隔(秒)
last_sensor_read_time = 0
sensor_read_interval = 5  # 传感器读取间隔(秒)
FAN_HUMIDITY_ON = 85   # 湿度达到该值时自动开启风扇
FAN_HUMIDITY_OFF = 82  # 湿度低于该值时自动关闭（滞回，避免反复开关）
DHT_READ_TIMEOUT_MS = 2500
fan_manual_mode = None  # None=湿度自动控制, 'on'=指令强制开, 'off'=指令临时关（湿度<85后恢复自动）
fan_is_running = False  # 当前风扇运行状态
last_valid_temperature = None
last_valid_humidity = None
dht_read_busy = False
dht_worker_active = False
dht_fail_count = 0

# 配置引脚
led1 = Pin(12, Pin.OUT)  # D12引脚 - 可能用于状态指示
led2 = Pin(13, Pin.OUT)  # D13引脚 - 可能用于状态指示
relay = Pin(14, Pin.OUT)  # D14引脚 - 控制继电器
dht_sensor = dht.DHT11(Pin(27))  # D27引脚 - 连接DHT11传感器

# RGB灯引脚配置（添加部分）
RED_PIN = 26    # 红色LED引脚
GREEN_PIN = 25  # 绿色LED引脚
BLUE_PIN = 33   # 蓝色LED引脚

room_led1 = Pin(15, Pin.OUT)
room_led2 = Pin(2, Pin.OUT)
room_led3 = Pin(4, Pin.OUT)
room_led4 = Pin(18, Pin.OUT)
room_led5 = Pin(19, Pin.OUT)
room_led6 = Pin(5, Pin.OUT)


def pwm_set_duty(pwm, value):
    value = max(0, min(1023, value))
    try:
        pwm.duty(value)
    except AttributeError:
        pwm.duty_u16(int(value * 65535 / 1023))


def create_pwm(pin_num, freq=1000):
    pin = Pin(pin_num)
    try:
        return PWM(pin, freq=freq, duty=0)
    except TypeError:
        pwm = PWM(pin, freq=freq)
        pwm_set_duty(pwm, 0)
        return pwm


# RGB PWM对象（添加部分）
red_pwm = create_pwm(RED_PIN)
green_pwm = create_pwm(GREEN_PIN)
blue_pwm = create_pwm(BLUE_PIN)
print("main.py: 硬件初始化完成")

# 连接WiFi
def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)

    # 不要 active(False) 重置 WiFi，ESP32 上会直接重启
    if not sta_if.active():
        sta_if.active(True)
        time.sleep_ms(500)

    if sta_if.isconnected():
        print('WiFi已连接，网络配置:', sta_if.ifconfig())
        return sta_if

    print('正在连接WiFi: {}'.format(WIFI_SSID))
    try:
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    except OSError as e:
        print('WiFi connect 出错:', e)

    timeout = 20
    while not sta_if.isconnected() and timeout > 0:
        print('等待WiFi... 剩余{}秒'.format(timeout))
        time.sleep(1)
        timeout -= 1

    if sta_if.isconnected():
        print('WiFi连接成功，网络配置:', sta_if.ifconfig())
    else:
        print('WiFi连接失败，请检查热点名称、密码和2.4GHz频段')
    return sta_if


def print_wifi_status(sta_if):
    if sta_if.isconnected():
        print('WiFi状态: 已连接', sta_if.ifconfig())
    else:
        print('WiFi状态: 未连接')
    
# 初始化继电器状态（默认关闭）
relay.value(0)

# --- RGB灯控制函数（添加部分）---
def set_rgb_color(red, green, blue):
    """设置RGB灯颜色，参数范围0-1023"""
    # 限制输入范围
    red = max(0, min(1023, red))
    green = max(0, min(1023, green))
    blue = max(0, min(1023, blue))
    
    # 设置PWM占空比（注意有些LED是共阳极，需要取反）
    pwm_set_duty(red_pwm, red)
    pwm_set_duty(green_pwm, green)
    pwm_set_duty(blue_pwm, blue)
    
def rgb_off():
    """关闭RGB灯"""
    pwm_set_duty(red_pwm, 0)
    pwm_set_duty(green_pwm, 0)
    pwm_set_duty(blue_pwm, 0)

# 预设颜色（添加部分）
def rgb_nuan():
    set_rgb_color(210, 105, 30)
    


# --- 设备控制函数 ---
def fan_start():
    led1.value(0)
    led2.value(1)
    time.sleep_ms(50)
    relay_on()
    time.sleep_ms(150)
    print("风扇启动（继电器已打开）")

def fan_stop():
    led1.value(0)
    led2.value(0)
    relay_off()
    print("风扇停止（继电器已关闭）")


def should_fan_run(humidity, fresh=True):
    # 指令优先级高于传感器
    if fan_manual_mode == 'on':
        return True
    if fan_manual_mode == 'off':
        return False
    # 自动模式：仅由湿度控制
    if not fresh or humidity is None:
        return False
    if fan_is_running:
        return humidity >= FAN_HUMIDITY_OFF
    return humidity >= FAN_HUMIDITY_ON


def resume_auto_if_cmd_off_cleared(humidity, fresh):
    """指令关闭后，湿度降到85%以下时恢复自动湿度控制。"""
    global fan_manual_mode
    if (
        fresh
        and fan_manual_mode == 'off'
        and humidity is not None
        and humidity < FAN_HUMIDITY_ON
    ):
        fan_manual_mode = None
        print("湿度低于{}%，恢复自动湿度控制".format(FAN_HUMIDITY_ON))
        return True
    return False


def sync_fan(humidity, reason="", fresh=True):
    global fan_is_running
    target = should_fan_run(humidity, fresh)
    if target == fan_is_running:
        return
    fan_is_running = target
    mode_text = fan_manual_mode if fan_manual_mode is not None else 'auto'
    if target:
        fan_start()
        print(reason or "风扇启动：湿度={}%，模式={}".format(humidity, mode_text))
    else:
        fan_stop()
        print(reason or "风扇停止：湿度={}%，模式={}".format(humidity, mode_text))

def relay_on():
    relay.value(1)  # 打开继电器（假设高电平触发）
    
def relay_off():
    relay.value(0)  # 关闭继电器

# --- 传感器数据采集函数 ---
def read_dht_sensor():
    global last_valid_temperature, last_valid_humidity, dht_read_busy, dht_worker_active, dht_fail_count

    if dht_read_busy or dht_worker_active:
        return last_valid_temperature, last_valid_humidity, False

    result = {"temp": None, "hum": None, "done": False, "error": None}

    def _worker():
        global dht_worker_active
        try:
            dht_sensor.measure()
            result["temp"] = dht_sensor.temperature()
            result["hum"] = dht_sensor.humidity()
        except Exception as e:
            result["error"] = e
        result["done"] = True
        dht_worker_active = False

    dht_read_busy = True
    dht_worker_active = True
    try:
        _thread.start_new_thread(_worker, ())
        deadline = time.ticks_add(time.ticks_ms(), DHT_READ_TIMEOUT_MS)
        while not result["done"] and time.ticks_diff(deadline, time.ticks_ms()) > 0:
            time.sleep_ms(20)

        if not result["done"]:
            dht_fail_count += 1
            print("DHT11读取超时，使用上次有效数据")
            return last_valid_temperature, last_valid_humidity, False

        if result["error"] is not None:
            dht_fail_count += 1
            print("读取DHT11传感器时出错：{}".format(result["error"]))
            return last_valid_temperature, last_valid_humidity, False

        dht_fail_count = 0
        last_valid_temperature = result["temp"]
        last_valid_humidity = result["hum"]
        return result["temp"], result["hum"], True
    finally:
        dht_read_busy = False


def mqtt_disconnect():
    global mqtt_client
    if mqtt_client is not None and mqtt_client.sock:
        try:
            mqtt_client.sock.close()
        except OSError:
            pass
        mqtt_client.sock = None


def mqtt_try_connect():
    global mqtt_client, last_connect_time
    mqtt_disconnect()
    print("连接MQTT服务器 {}:{} ...".format(MQTT_BROKER, MQTT_PORT))
    mqtt_client.connect(clean_session=True)
    mqtt_client.sock.settimeout(5)
    mqtt_client.subscribe(SUBSCRIBE_TOPIC)
    print("已订阅 {}，等待消息...".format(SUBSCRIBE_TOPIC))
    last_connect_time = time.time()


def mqtt_safe_check_msg():
    if mqtt_client is None or not mqtt_client.sock:
        return
    try:
        mqtt_client.check_msg()
    except OSError as e:
        print("MQTT check_msg错误：{}".format(e))
        mqtt_disconnect()


def mqtt_safe_publish(topic, message):
    if mqtt_client is None or not mqtt_client.sock:
        return False
    try:
        mqtt_client.publish(topic, message)
        return True
    except OSError as e:
        print("MQTT publish错误：{}".format(e))
        mqtt_disconnect()
        return False

# --- MQTT 消息回调函数 (仅处理 lip_reading/iot 主题) ---
def mqtt_callback(topic, msg):
    global fan_manual_mode
    try:
        # 确保只处理目标主题的消息
        if topic != SUBSCRIBE_TOPIC:
            return
            
        msg_str = msg.decode('utf-8').strip()
        print("Received from {}: {}".format(topic, msg_str))

        # 根据接收到的数字执行不同操作
        if msg_str == "1":
            fan_manual_mode = 'on'
            print("执行操作1：指令强制启动风扇（优先于湿度）")
            sync_fan(last_valid_humidity, "MQTT指令1：强制开启", fresh=True)
            
        elif msg_str == "2":
            fan_manual_mode = 'off'
            print("执行操作2：指令强制停止风扇（湿度<{}%后恢复自动）".format(FAN_HUMIDITY_ON))
            sync_fan(last_valid_humidity, "MQTT指令2：强制关闭", fresh=True)
            
        elif msg_str == "3":
            fan_manual_mode = 'on'
            print("执行操作3：指令强制开继电器/风扇")
            sync_fan(last_valid_humidity, "MQTT指令3：强制开启", fresh=True)
            
        elif msg_str == "4":
            fan_manual_mode = 'off'
            print("执行操作4：指令强制关继电器/风扇（湿度<{}%后恢复自动）".format(FAN_HUMIDITY_ON))
            sync_fan(last_valid_humidity, "MQTT指令4：强制关闭", fresh=True)
            
        elif msg_str == "5":
            # 读取当前温湿度并发送中文描述到lip_reading/src_text
            temperature, humidity, _fresh = read_dht_sensor()
            if temperature is not None and humidity is not None:
                # 构建中文描述消息（直接字符串形式，便于阅读）
                chinese_message = f"当前环境温度：{temperature}摄氏度，相对湿度：百分之{humidity}"
                # 发布中文消息到指定主题
                if mqtt_client is not None:
                    mqtt_client.publish(PUBLISH_SRC_TOPIC, chinese_message.encode('utf-8'))
                print(f"已发送中文温湿度到{str(PUBLISH_SRC_TOPIC)}：{chinese_message}")
            else:
                error_msg = "无法获取有效温湿度数据"
                if mqtt_client is not None:
                    mqtt_client.publish(PUBLISH_SRC_TOPIC, error_msg.encode('utf-8'))
                print(error_msg)
        
        # RGB灯控制（添加部分）
        elif msg_str == "6":
            print("执行操作6：RGB暖色")
            rgb_nuan()
            
        elif msg_str == "7":
            print("执行操作7：关闭")
            rgb_off()
        elif msg_str == "8":
            room_led1.value(1)  #柜子灯
        elif msg_str == "9":
            room_led1.value(0)
            
        elif msg_str == "10":
            room_led2.value(1)#床后灯  
        elif msg_str == "11":
            room_led2.value(0)  
            
        elif msg_str == "12":#床下前
            room_led3.value(1)  
        elif msg_str == "13":
            room_led3.value(0)
            
        elif msg_str == "14":#床头灯
            room_led4.value(1)  
        elif msg_str == "15":
            room_led4.value(0)
            
        elif msg_str == "16":
            room_led5.value(1) #上左灯
        elif msg_str == "17":
            room_led5.value(0)
            
        elif msg_str == "18":
            room_led6.value(1)  #厕所灯
        elif msg_str == "19":
            room_led6.value(0)   
        else:
            print(f"未知指令：{msg_str}，忽略处理")
            
    except Exception as e:
        sys.print_exception(e)
        print(f"处理消息时出错：{e}")

# --- 主循环 ---
def main():
    global mqtt_client, last_connect_time, last_sensor_read_time, fan_is_running, fan_manual_mode

    print('ESP32 程序启动')
    fan_stop()
    fan_is_running = False
    fan_manual_mode = None
    # 连接WiFi (替换为你的WiFi信息)
    wlan = connect_wifi()
    print_wifi_status(wlan)
    
    # 初始化MQTT客户端
    mqtt_client = MQTTClient(CLIENT_ID, MQTT_BROKER, MQTT_PORT, keepalive=120)
    mqtt_client.set_callback(mqtt_callback)  # 设置回调函数
    
    wifi_check_interval = 30
    last_wifi_check_time = time.time()

    while True:
        try:
            current_time = time.time()
            if current_time - last_wifi_check_time > wifi_check_interval:
                if not wlan.isconnected():
                    print('WiFi已断开，尝试重新连接...')
                    try:
                        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
                    except OSError as e:
                        print('WiFi重连出错:', e)
                else:
                    print_wifi_status(wlan)
                last_wifi_check_time = current_time

            # 检查MQTT连接，断开则重连
            if (mqtt_client.sock is None) and (current_time - last_connect_time > connect_interval):
                try:
                    mqtt_try_connect()
                except OSError as e:
                    print("MQTT连接错误：{}".format(e))
                    mqtt_disconnect()
                    last_connect_time = time.time()
            
            # 检查并处理新消息
            mqtt_safe_check_msg()
            
            # 定期读取传感器数据并发布
            if current_time - last_sensor_read_time > sensor_read_interval:
                temperature, humidity, fresh = read_dht_sensor()

                if fresh:
                    resume_auto_if_cmd_off_cleared(humidity, fresh)

                if fresh and fan_manual_mode is None:
                    sync_fan(
                        humidity,
                        "湿度联动：湿度{}%，{}风扇".format(
                            humidity,
                            "开启" if should_fan_run(humidity, True) else "关闭"
                        ),
                        fresh=True,
                    )
                elif (fan_manual_mode is None) and fan_is_running and not fresh:
                    if (
                        last_valid_humidity is not None
                        and last_valid_humidity >= FAN_HUMIDITY_OFF
                    ):
                        print("传感器读取失败，但湿度仍偏高，保持风扇运行")
                    else:
                        sync_fan(
                            humidity,
                            "传感器读取失败，自动关闭风扇",
                            fresh=False,
                        )

                if temperature is not None and humidity is not None:
                    message = ujson.dumps({
                        "temperature": temperature,
                        "humidity": humidity,
                        "timestamp": current_time
                    })
                    if mqtt_safe_publish(PUBLISH_ENV_TOPIC, message):
                        print("发布温湿度数据：温度={}°C，湿度={}%".format(temperature, humidity))

                last_sensor_read_time = current_time
            
            # 短暂延时，降低CPU占用
            time.sleep_ms(100)
            
        except Exception as e:
            sys.print_exception(e)
            print("主循环错误：{}".format(e))
            time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        sys.print_exception(e)
        print("main.py 运行失败，请把上面的报错发出来")



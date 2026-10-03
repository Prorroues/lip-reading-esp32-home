print("main.py: 开始加载")
import machine
import time
from machine import Pin, PWM
from umqttsimple import MQTTClient
import network
import ujson
import sys

# 配置WiFi信息（须与眼镜、电脑在同一局域网）
from config import WIFI_SSID, WIFI_PASSWORD, MQTT_BROKER, MQTT_PORT  # 真实配置放 config.py（不进版本库）

# --- MQTT 核心配置与变量 ---
CLIENT_ID = "esp32_lipreading_iot"
SUBSCRIBE_TOPIC = b"esp32/" + CLIENT_ID.encode() + b"/command"
SUBSCRIBE_MSG_TOPIC = b"esp32/" + CLIENT_ID.encode() + b"/message"
SUBSCRIBE_CONFIG_TOPIC = b"esp32/" + CLIENT_ID.encode() + b"/config"
PUBLISH_STATUS_TOPIC = b"esp32/" + CLIENT_ID.encode() + b"/status"

mqtt_client = None
last_connect_time = 0
connect_interval = 5
fan_is_running = False

led1 = Pin(12, Pin.OUT)
led2 = Pin(13, Pin.OUT)
relay = Pin(14, Pin.OUT)

RED_PIN = 26
GREEN_PIN = 25
BLUE_PIN = 33

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
        print("  PWM duty({}) OK".format(value))
    except AttributeError:
        u16 = int(value * 65535 / 1023)
        pwm.duty_u16(u16)
        print("  PWM duty_u16({}) OK".format(u16))


def create_pwm(pin_num, freq=1000):
    pin = Pin(pin_num)
    try:
        return PWM(pin, freq=freq, duty=0)
    except TypeError:
        pwm = PWM(pin, freq=freq)
        pwm_set_duty(pwm, 0)
        return pwm


red_pwm = create_pwm(RED_PIN)
green_pwm = create_pwm(GREEN_PIN)
blue_pwm = create_pwm(BLUE_PIN)
print("main.py: 硬件初始化完成")


def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.active():
        sta_if.active(True)
        time.sleep_ms(500)

    if sta_if.isconnected():
        print("WiFi已连接，网络配置:", sta_if.ifconfig())
        return sta_if

    print("正在连接WiFi: {}".format(WIFI_SSID))
    try:
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    except OSError as e:
        print("WiFi connect 出错:", e)

    timeout = 20
    while not sta_if.isconnected() and timeout > 0:
        print("等待WiFi... 剩余{}秒".format(timeout))
        time.sleep(1)
        timeout -= 1

    if sta_if.isconnected():
        print("WiFi连接成功，网络配置:", sta_if.ifconfig())
    else:
        print("WiFi连接失败，请检查热点名称、密码和2.4GHz频段")
    return sta_if


def print_wifi_status(sta_if):
    if sta_if.isconnected():
        print("WiFi状态: 已连接", sta_if.ifconfig())
    else:
        print("WiFi状态: 未连接")


relay.value(0)


def set_rgb_color(red, green, blue):
    red = max(0, min(1023, red))
    green = max(0, min(1023, green))
    blue = max(0, min(1023, blue))
    print("RGB PWM: R:{} G:{} B:{}".format(red, green, blue))
    pwm_set_duty(red_pwm, red)
    pwm_set_duty(green_pwm, green)
    pwm_set_duty(blue_pwm, blue)


def rgb_off():
    pwm_set_duty(red_pwm, 0)
    pwm_set_duty(green_pwm, 0)
    pwm_set_duty(blue_pwm, 0)


def rgb_nuan():
    set_rgb_color(210, 105, 30)


def fan_start():
    global fan_is_running
    led1.value(0)
    led2.value(1)
    time.sleep_ms(50)
    relay.value(1)
    time.sleep_ms(150)
    fan_is_running = True
    print("风扇启动（继电器已打开）")


def fan_stop():
    global fan_is_running
    led1.value(0)
    led2.value(0)
    relay.value(0)
    fan_is_running = False
    print("风扇停止（继电器已关闭）")


def mqtt_disconnect():
    global mqtt_client
    if mqtt_client is not None:
        try:
            if mqtt_client.sock:
                mqtt_client.publish(PUBLISH_STATUS_TOPIC, b"offline")
                mqtt_client.sock.close()
        except OSError:
            pass
        mqtt_client.sock = None


def mqtt_try_connect():
    global mqtt_client, last_connect_time
    mqtt_disconnect()
    print("连接MQTT服务器 {}:{} ...".format(MQTT_BROKER, MQTT_PORT))
    mqtt_client.set_last_will(PUBLISH_STATUS_TOPIC, b"offline", retain=False, qos=0)
    mqtt_client.connect(clean_session=True)
    mqtt_client.sock.settimeout(5)
    mqtt_client.subscribe(SUBSCRIBE_TOPIC)
    mqtt_client.subscribe(SUBSCRIBE_MSG_TOPIC)
    mqtt_client.subscribe(SUBSCRIBE_CONFIG_TOPIC)
    print("已订阅 {} / {} / {}".format(SUBSCRIBE_TOPIC, SUBSCRIBE_MSG_TOPIC, SUBSCRIBE_CONFIG_TOPIC))
    mqtt_safe_publish(PUBLISH_STATUS_TOPIC, b"online")
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


def mqtt_callback(topic, msg):
    try:
        msg_str = msg.decode("utf-8").strip()
        print("Received from {}: {}".format(topic, msg_str))

        if topic == SUBSCRIBE_MSG_TOPIC:
            print("[设备消息] {}".format(msg_str))
            return

        if topic == SUBSCRIBE_CONFIG_TOPIC:
            print("已忽略配置消息（传感器自动化已移除）: {}".format(msg_str))
            return

        if topic != SUBSCRIBE_TOPIC:
            return

        if msg_str == "1" or msg_str == "3":
            print("执行指令{}：打开风扇".format(msg_str))
            fan_start()
        elif msg_str == "2" or msg_str == "4":
            print("执行指令{}：关闭风扇".format(msg_str))
            fan_stop()
        elif msg_str == "5":
            print("指令5已忽略：温湿度传感器已移除")
        elif msg_str == "6":
            print("执行操作6：RGB暖色")
            rgb_nuan()
        elif msg_str == "7":
            print("执行操作7：关闭RGB")
            rgb_off()
        elif msg_str == "20":
            print("执行操作20：RGB暖色")
            rgb_nuan()
        elif msg_str.startswith("{"):
            print("收到JSON指令: {}".format(msg_str))
            try:
                rgb_data = ujson.loads(msg_str)
                if rgb_data.get("cmd") == 21:
                    r = rgb_data.get("r", 0)
                    g = rgb_data.get("g", 0)
                    b = rgb_data.get("b", 0)
                    set_rgb_color(r, g, b)
                    print("执行操作21：自定义RGB R:{} G:{} B:{}".format(r, g, b))
                else:
                    print("JSON cmd={}".format(rgb_data.get("cmd")))
            except Exception as e:
                print("RGB JSON解析失败: {}".format(e))
        elif msg_str == "8":
            room_led1.value(1)
        elif msg_str == "9":
            room_led1.value(0)
        elif msg_str == "10":
            room_led2.value(1)
        elif msg_str == "11":
            room_led2.value(0)
        elif msg_str == "12":
            room_led3.value(1)
        elif msg_str == "13":
            room_led3.value(0)
        elif msg_str == "14":
            room_led4.value(1)
        elif msg_str == "15":
            room_led4.value(0)
        elif msg_str == "16":
            room_led5.value(1)
        elif msg_str == "17":
            room_led5.value(0)
        elif msg_str == "18":
            room_led6.value(1)
        elif msg_str == "19":
            room_led6.value(0)
        else:
            print("未知指令：{}，忽略处理".format(msg_str))

    except Exception as e:
        sys.print_exception(e)
        print("处理消息时出错：{}".format(e))


def main():
    global mqtt_client, last_connect_time, fan_is_running

    print("ESP32 程序启动")
    fan_stop()
    fan_is_running = False
    wlan = connect_wifi()
    print_wifi_status(wlan)

    mqtt_client = MQTTClient(CLIENT_ID, MQTT_BROKER, MQTT_PORT, keepalive=120)
    mqtt_client.set_callback(mqtt_callback)

    wifi_check_interval = 30
    last_wifi_check_time = time.time()

    while True:
        try:
            current_time = time.time()
            if current_time - last_wifi_check_time > wifi_check_interval:
                if not wlan.isconnected():
                    print("WiFi已断开，尝试重新连接...")
                    try:
                        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
                    except OSError as e:
                        print("WiFi重连出错:", e)
                else:
                    print_wifi_status(wlan)
                last_wifi_check_time = current_time

            if (mqtt_client.sock is None) and (current_time - last_connect_time > connect_interval):
                try:
                    mqtt_try_connect()
                except OSError as e:
                    print("MQTT连接错误：{}".format(e))
                    mqtt_disconnect()
                    last_connect_time = time.time()

            mqtt_safe_check_msg()
            time.sleep_ms(100)

        except Exception as e:
            sys.print_exception(e)
            print("主循环错误：{}".format(e))
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.print_exception(e)
        print("main.py 运行失败，请把上面的报错发出来")


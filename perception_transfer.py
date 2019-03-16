# -*- coding:utf-8 -*-


import time
import random
import paho.mqtt.client as mqtt
import auto_read_conf as epc


def conf_read():
    colony_frame_auto = epc.Colony_Frame_Auto()
    colony_frame_auto.colony_frame_fb(fb='EPC-simple.conf')
    list_body = colony_frame_auto.colony_frame_slave('PERCEPTION_FRAME')
    print(list_body)
    return [list_body['info_server_ip'], int(list_body['info_server_port'])]


def test(host, port):
    client = mqtt.Client()
    client.connect(host, port, 60)

    # temperature sensor 温度传感器
    # humidity sensor 湿度传感器

    analog_temperature = random.randint(10, 35)
    analog_humidity = round(random.uniform(0, 1), 2)
    time.sleep(1)
    client.publish("server", "from T:{}C H:{}%".format(analog_temperature, analog_humidity*100))

    print("server", "from T:{}C H:{}%".format(analog_temperature, str(analog_humidity*100)[:2]), 0)
    # client.loop_forever() 阻塞则使用该方法


if __name__ == '__main__':
    conf_list = conf_read()
    while 1:
        test(conf_list[0], conf_list[1])

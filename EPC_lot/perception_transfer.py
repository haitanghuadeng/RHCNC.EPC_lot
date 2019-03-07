# -*- coding:utf-8 -*-


import random
import paho.mqtt.client as mqtt
import EPC_lot.auto_read_conf as epc


def conf_read():
    colony_frame_auto = epc.Colony_Frame_Auto()
    colony_frame_auto.colony_frame_fb(fb='EPC-simple.conf')
    list_body = colony_frame_auto.colony_frame_slave('PERCEPTION_FRAME')
    print(list_body)
    return [list_body['info_server_ip'], int(list_body['info_server_port'])]


def test(HOST, PORT):
    client = mqtt.Client()
    client.connect(HOST, PORT, 60)
    analog_number = random.randint(1, 10)
    client.publish("server", f"hello 模拟测试{analog_number}", 0)
    print("server", f"hello 模拟测试{analog_number}", 0)
    # client.loop_forever() 阻塞则使用该方法


if __name__ == '__main__':
    conf_list = conf_read()
    for i in range(7):
        test(conf_list[0], conf_list[1])

# -*- coding:utf-8 -*-


import paho.mqtt.client as mqtt
import datetime
import EPC_lot.auto_read_conf as epc

mqttClient = mqtt.Client()


def conf_read():
    colony_frame_auto = epc.Colony_Frame_Auto()
    colony_frame_auto.colony_frame_fb(fb='EPC-simple.conf')
    list_body = colony_frame_auto.colony_frame_slave('PERCEPTION_FRAME')
    print(list_body)
    return [list_body['info_server_ip'], int(list_body['info_server_port'])]


# 连接MQTT服务器
def on_mqtt_connect(MQTTHOST, MQTTPORT):
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()


# publish 消息
def on_publish(topic, payload, qos):
    mqttClient.publish(topic, payload, qos)


# 消息处理函数
def on_message_come(lient, userdata, msg):
    print(
        f"\n --- 本地时间：{datetime.datetime.now().strftime('%b-%d-%Y %H:%M:%S')} \n || 主题：{msg.topic} 消息内容：{str(msg.payload)} 服务质量：{str(msg.qos)}",
        end=' ')

# subscribe 消息


def on_subscribe():
    mqttClient.subscribe("server", 1)
    mqttClient.on_message = on_message_come  # 消息到来处理函数


def main():
    conf_list = conf_read()
    on_mqtt_connect(conf_list[0], conf_list[1])
    on_publish("server", "Hello Python!", 1)
    on_subscribe()
    while True:
        pass


if __name__ == '__main__':
    main()

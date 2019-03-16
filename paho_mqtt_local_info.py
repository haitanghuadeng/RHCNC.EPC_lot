# -*- coding:utf-8 -*-


import os
import json
import time
import redis
import datetime
# import _thread
import paho.mqtt.client as mqtt
import auto_read_conf as epc


body = {}
mqttClient = mqtt.Client(client_id='localtime:123456')
colony_frame_auto = epc.Colony_Frame_Auto()
colony_frame_auto.colony_frame_fb(fb='EPC-simple.conf')
read_conf = colony_frame_auto.colony_frame_slave('SUBSCRIPTION_INFO_LASTING_FRAME')


def conf_read():
    list_body = colony_frame_auto.colony_frame_slave('PERCEPTION_FRAME')
    print(list_body)
    return [list_body['info_server_ip'], int(list_body['info_server_port'])]


# 连接MQTT服务器
def on_mqtt_connect(mqtthost, mqttport):
    mqttClient.connect(mqtthost, mqttport, 60)
    mqttClient.loop_start()


# publish 消息
def on_publish(topic, payload, qos):
    mqttClient.publish(topic, payload, qos)
    # on_publish("server", "Hello Python!", 1)


# 消息处理函数
def on_message_come(msg):
    body[f"{datetime.datetime.now().strftime('%b-%d-%Y >>> %H:%M:%S.%f')}"] = \
        [f"topic >>> {msg.topic} ", f"info_body >>> {msg.payload[:]} ", f"server_quality >>> {str(msg.qos)}"]
    print(f"{datetime.datetime.now().strftime('%b-%d-%Y >>> %H:%M:%S.%f')}",
          f"topic:{msg.topic} ",
          f"info_body:{str(msg.payload)} ",
          f"server_quality:{str(msg.qos)}")


def on_subscribe():
    mqttClient.subscribe([("server", 0), ('server-1', 0), ('server-2', 0), ('server-3', 0)])
    mqttClient.on_message = on_message_come  # 消息到来处理函数


def main():
    """
    main() 本地消息持久化
    :return: 默认返回None
    """

    conf_list = conf_read()
    on_mqtt_connect(conf_list[0], conf_list[1])

    list_body = colony_frame_auto.colony_frame_slave('SUBSCRIPTION_INFO_LASTING_FRAME')
    file_name = list_body['local_lasting_path'] + 'info.json'

    on_subscribe()
    while True:
        time.sleep(1)
        if len(body) > 6:

                write_bodys = json.dumps(body, sort_keys=True, indent=4,  separators=(',', ': '))

                if os.path.exists(file_name) is True:
                    if os.path.getsize(file_name) < 102400:
                        with open(file_name, 'r+') as f:
                            temporary = f.read()
                            if temporary == '':
                                read_body = None
                            else:
                                read_body = {**json.loads(temporary), **body}

                        with open(file_name, 'w+') as f:
                            if not read_body:
                                read_bodys = {**body}
                            else:
                                read_bodys = {**read_body, **body}

                            write_bodys = json.dumps(read_bodys, sort_keys=True, indent=4, separators=(',', ': '))
                            f.write(write_bodys)
                    else:
                        break
                else:
                    with open(file_name, 'w+') as f:
                        f.write(write_bodys)
                    print(r'-set up {}\{}'.format(os.getcwd(), file_name))

        pass


def run_main():
    """
    # subscription_lasting为'NO'时，则直接输出结果，不进行lasting处理。

    :return: 默认返回None
    """

    conf_list = conf_read()
    on_mqtt_connect(conf_list[0], conf_list[1])
    on_subscribe()

    while True:
        pass


def run_db(database, userpass=''):
    """
    run_db()函数，针对数据库持久化开发。将立于1.2版本至1.3版本中，适用于公开版本。
    :return: 默认返回None
    """
    database_sites = database.split(':')
    database_ip = database_sites[0]
    database_port = database_sites[1]

    if userpass:
        userpass = userpass
    else:
        pass
    # 默认用户为root
    rdp = redis.ConnectionPool(host=database_ip, port=database_port, password=userpass)
    rdc = redis.StrictRedis(connection_pool=rdp)
    conf_list = conf_read()
    on_mqtt_connect(conf_list[0], conf_list[1])

    on_subscribe()
    while 1:
        time.sleep(1)
        key = []
        for i in body.keys():
            key.append(i)
        try:
            rdc.set(key[-1], body[key[-1]])
        except IndexError:
            pass


if __name__ == '__main__':
    """
    启动架构后，将优先读取conf文件
    这将为自动化提供策略
    
    # 优先级
    # subscription_lasting
    #       --- 1. io_subscription_lasting  YES | NO
    #       --- 2. subscription_database_lasting  YES | NO
    # 若subscription_lasting选项为'YES'，则启用消息持久化。作为父级。
    # 若父级为'YES'，则子级io_subscription_lasting成为第一优先策略(无视后序策略)。'YES'则本地持久化，'NO'则数据库持久化。
    # 若父级为'YES'和io_subscription_lasting为'NO'，则子级subscription_database_lasting成为同级第一策略。 ↓
    # 'YES'则数据库持久化。
    # 'NO'则不启用本地持久化和数据库持久化，这将同时修改conf中的父级及其下的选项，全部默认为NO。
    
    """

    if read_conf['subscription_lasting'] == 'YES':
        if read_conf['io_subscription_lasting'] != 'NO':
            main()
        else:
            if read_conf['subscription_database_lasting'] != 'NO':
                database_site = read_conf['subscription_database_lasting']
                username = read_conf['database_user']
                user_password = read_conf['database_password']
                run_db(database_site, user_password)
            else:
                # 将conf文件中的[SUBSCRIPTION_LASTING_FRAME]修正为NO
                # 开发……
                pass
    else:
        run_main()

    # mqttClient.loop_forever()

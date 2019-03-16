# -*- coding:utf-8 -*-


import os
import re
import json
import redis
import EMQ_monitoring as Mon
import auto_read_conf as epc
import EPC_error.EPC_Error as Error


class Ssh_Sub:

    def __init__(self, userpass=''):
        self.command = {}
        self.return_list = {}
        self.client_id_topic = {}
        self.epcssh = Mon.EpcSsh()
        self.ip = self.epcssh.conf_read()
        self.colony_frame_auto = epc.Colony_Frame_Auto()
        self.colony_frame_auto.colony_frame_fb(fb='EPC-simple.conf')
        self.read_conf = self.colony_frame_auto.colony_frame_slave('SUBSCRIPTION_INFO_LASTING_FRAME')
        self.database = self.read_conf['subscription_database_lasting']
        self.database_site = self.database.split(':')
        self.database_ip = self.database_site[0]
        self.database_port = self.database_site[1]
        if userpass is '':
            self.userpass = userpass
        else:
            self.userpass = self.read_conf['SUBSCRIPTION_INFO_LASTING_FRAME']['database_password']
        self.rdp = redis.ConnectionPool(host=self.database_ip, port=self.database_port, password=self.userpass, db=1)
        self.rdc = redis.StrictRedis(connection_pool=self.rdp)

    def ssh_command(self):
        if self.read_conf['subscription_pull_auto'] == 'YES':

            sub_file_name = self.read_conf['subscription_pull_path'] + 'sub_pull.json'
            self.command = {'emqx_ctl subscriptions list'}

            try:
                self.return_list = self.epcssh.epc_ssh(
                    hostname=self.ip,
                    username='root',
                    password='',
                    user_info=self.command)
            except TimeoutError as e:
                print(e)
                print('通信断裂，建立在连接之上的指令集无法传输。')
                quit()
            self.epcssh.epc_close()
            self.command = 'emqx_ctl subscriptions list'
            return_up = self.return_list[self.command]
            if return_up is []:
                quit()
            return_down = re.split('\n', return_up)[:-1]
            print(return_down)

            for i in return_down:
                i = i.split(' -> ')
                if i[0] in self.client_id_topic.keys():
                    self.client_id_topic[i[0]] = [*self.client_id_topic[i[0]], i[1]]
                else:
                    self.client_id_topic[i[0]] = [i[1]]
            print(self.client_id_topic)

            if self.read_conf['subscription_pull_auto_local'] == 'NO':
                # 使用self.client_id_topic变量，该变量dict()类型将存储临时键值对。
                for i in self.client_id_topic.keys():
                    if self.rdc.get(i) is None:
                        self.rdc.set(i, '{}'.format(self.client_id_topic.get(i)))
                    else:
                        redis_get = eval(self.rdc.get(i).decode())
                        # print(redis_get)
                        self.rdc.set(i, '{}'.format(list({*redis_get, *self.client_id_topic.get(i)})))
            else:
                if os.path.exists(sub_file_name) is True:
                    with open(sub_file_name, 'r+') as f:
                        read_json = json.loads(f.read())
                        if read_json == '':
                            read_body = None
                        else:
                            read_body = {**read_json}

                    with open(sub_file_name, 'w+') as f:
                        read_bodys = {**read_body}
                        if read_body:
                            for i in self.client_id_topic.keys():
                                if i in read_body.keys():
                                    if self.client_id_topic[i] == read_body[i]:
                                        pass
                                    else:
                                        self.client_id_topic[i] = list(set(self.client_id_topic[i] + read_body[i]))
                                else:
                                    read_bodys[i] = self.client_id_topic[i]
                        else:
                            read_bodys = {**self.client_id_topic}

                        write_bodys = json.dumps(read_bodys, sort_keys=True, indent=4, separators=(',', ': '))
                        f.write(write_bodys)
                else:
                    write_bodys = json.dumps(self.client_id_topic, sort_keys=True, indent=4, separators=(',', ': '))
                    with open(sub_file_name, 'w+') as f:
                        f.write(write_bodys)
                    print(r'-set up {}\{}'.format(os.getcwd(), sub_file_name))

        elif self.read_conf['subscription_pull_auto'] == 'NO':
            pass
        else:
            try:
                raise Error.Conf_Key_Error('SUBSCRIPTION_INFO_LASTING_FRAME主框架 - 子项subscription_pull_auto未知配置！')
            except Error.Conf_Key_Error as e:
                print(e)


if __name__ == '__main__':
    ssh_sub = Ssh_Sub()
    ssh_sub.ssh_command()

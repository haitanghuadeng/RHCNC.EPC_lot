# -*- coding:utf-8 -*-


import paramiko
import auto_read_conf as epc


class EpcSsh:

    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.colony_frame_auto = epc.Colony_Frame_Auto()
        self.colony_frame_auto.colony_frame_fb(fb='EPC-simple.conf')

    def epc_ssh(
            self,
            hostname='127.0.0.1',
            port=22,
            username=None,
            password=None,
            user_info=None):
        """
        :param hostname: 默认项为目标主机IP地址
        :param port: 默认端口为22(ssh)
        :param username: 默认为空
        :param password: 默认为空
        :param user_info: 默认为None, 如果为True则保持连接。
            根据user_info所存储的类型进而回调，多指令请存放到{}，None则默认使用'emqx_ctl status'(不支持emqtt2.x版本)
        :return: 单命令回弹，{}则返回每条命令所执行的结果，以键值对方式返回
        """

        self.client.connect(hostname, port, username, password)

        if user_info:
            if type(user_info) is set:
                command_info = {}

                for i in user_info:
                    stdin, stdout, stderr = self.client.exec_command(i)
                    result = stdout.read().decode('utf-8')
                    command_info[i] = result

                return command_info

            else:
                while True:
                    user_info = input('>>> ')
                    stdin, stdout, stderr = self.client.exec_command(user_info)
                    result = stdout.read().decode('utf-8')
                    print(result)

        else:
            stdin, stdout, stderr = self.client.exec_command('emqx_ctl status')
            result = stdout.read().decode('utf-8')
            return result

    def conf_read(self):
        list_body = self.colony_frame_auto.colony_frame_slave('PERCEPTION_FRAME')
        return list_body['info_server_ip']

    def epc_close(self):

        self.client.close()

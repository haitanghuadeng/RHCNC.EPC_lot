# -*- coding:utf-8 -*-


import paramiko
import EPC_lot.auto_read_conf as epc


class EpcSsh:

    def __init__(self):

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

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
        :param user_info: 默认为None, 如果为True则保持连接
        :return:
        """

        self.client.connect(hostname, port, username, password)

        if user_info:
            while True:
                user_info = input('>>> ')
                # if user_info is 'q' or 'quit':
                #     break

                stdin, stdout, stderr = self.client.exec_command(user_info)
                result = stdout.read().decode('utf-8')
                print(result)

        else:
            stdin, stdout, stderr = self.client.exec_command('emqx_ctl status')
            result = stdout.read().decode('utf-8')
            return result

    def conf_read(self):
        colony_frame_auto = epc.Colony_Frame_Auto()
        colony_frame_auto.colony_frame_fb(fb='EPC-simple.conf')
        list_body = colony_frame_auto.colony_frame_slave('PERCEPTION_FRAME')
        return list_body['info_server_ip']

    def epc_close(self):

        self.client.close()


if __name__ == '__main__':
    epcssh = EpcSsh()
    ip = epcssh.conf_read()
    epcssh.epc_ssh(
        hostname=ip,
        username='root',
        password=None,
        user_info=True)
    epcssh.epc_close()

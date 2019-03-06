# -*- coding:utf-8 -*-


import paramiko


class EpcSsh():

    def __init__(self):

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def epc_ssh(self, hostname='127.0.0.1', port=22, username=None, password=None, user_info=None):
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
            while 1:
                user_info = input('>>> ')
                # if user_info is 'q' or 'quit':
                #     break

                stdin, stdout, stderr = self.client.exec_command(user_info)
                result = stdout.read().decode('utf-8')
                print(result)

        else:
            stdin, stdout, stderr = self.client.exec_command('emqx_ctl status')
            result = stdout.read().decode('utf-8')
            print(result)
            return result

    def epc_close(self):

        self.client.close()


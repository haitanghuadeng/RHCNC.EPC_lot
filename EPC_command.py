# -*- coding:utf-8 -*-


from EMQ_monitoring import *


class Command:

    def __init__(self):
        self.epcssh = EpcSsh()
        self.ip = self.epcssh.conf_read()

    def test(self, command_type):
            self.epcssh.epc_ssh(
                    hostname=self.ip,
                    username='root',
                    password='',
                    user_info=command_type)
            self.epcssh.epc_close()


if __name__ == '__main__':
    command_types = {'emqx_ctl status', 'uname -a'}
    command = Command()
    command.test(command_types)

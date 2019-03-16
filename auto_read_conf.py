# -*- coding:utf-8 -*-


import os
import configparser
from EPC_error import EPC_Error as Emq
from collections import Iterable


class Colony_Frame_Auto:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.sections()
        self.fb = None

    def colony_frame_fb(self, fb=None):

        """
        colony_frame_fb()方法：
            作用返回当前指定配置文件的area范围
        """

        if not fb:
            pass
        else:
            if os.path.exists(fb) is True:
                self.config.read(fb)
            else:
                raise Emq.FilepathError('未找到该文件！{}'.format(fb))

        frame_area_name = [i for i in self.config]

        return frame_area_name

    def colony_frame_slave(self, master=None):

        """
        colony_frame_slave()方法：
            作用获得当前指定配置文件的指定框架及子选项和参数
        """
        temporary_dict = {}
        if master is None:
            # 默认master 获得当前架构配置文件的所有项
            # 默认主框架为 DEFAULT
            master = [i for i in self.config]
            print("所有项：", master)

            for i in master:

                if self.config.has_section(i) is True:

                    if i == 'DEFAULT':
                        pass

                    else:
                        print("主框架：{}".format(i))
                        temporary = self.config[i]

                        for k in temporary:
                            temporary_dict[k] = self.config[i][k]
                            print('---{} = {}'.format(k, self.config[i][k]))

                else:
                    print('主框架：{}'.format(i))

        else:

            assign_master = self.config[master]
            for i in assign_master:
                temporary_dict[i] = self.config[master][i]

        return temporary_dict

    def colony_frame_change_request(self, change_name=None):

        """
        colony_frame_change_request()方法：
            集群架构变更请求，选择主框架名称将其修改
            change_name关系：将第一个变量名(主框架名)修改为第二个变量名
        """
        if change_name is None:
            pass
        else:
            change_name = tuple(change_name)
            if isinstance(change_name, Iterable):

                if self.config.has_section(change_name[0]) is True:
                    temporary = {}
                    print('\n变更请求：{}'.format(change_name[0]))

                    for i in self.config[change_name[0]]:
                        temporary[i] = self.config[change_name[0]][i]
                        print('---选项{}, 参数{}'.format(i, self.config[change_name[0]][i]))

                    del self.config[change_name[0]]

                    self.config.add_section(change_name[1])
                    print('变更主框架名称！')

                    for i in temporary.keys():
                        self.config[change_name[1]][i] = temporary[i]

                    print('转移完成！\n当前主架构体：{}'.format(self.config.sections()))
                else:

                    raise ValueError('{}参数并未在配置文件中找到！Error[2]错误！'.format(change_name[0]))

            else:

                raise ValueError('colony_frame_change_request()方法:\n\t参数change_name需要提供一个可迭代对象！Error[1]错误！')

    def colony_customized(self, frame_master, frame_slave):
        """
        colony_customized()方法，为conf文件提供可添加的选项，配合colony_customized_create()方法，
        定制化批量部署架构服务
        :param frame_master: 主框架建立
        :param frame_slave: 主框架-子项建立
        """
        # self.config[]
        pass

    def colony_frame_info(self, fb=None):

        """
        配置持久化操作，colony_frame_info()方法应放到执行代码尾部
        """

        if fb is None:
            self.config.write(open('EPC-simple.conf', 'w+'))
        else:
            self.config.write(open(fb, 'w+'))


if __name__ == '__main__':
    #     Colony_Frame_Auto() 对象将会初始化configparser.ConfigParser()对象
    colony_frame_auto = Colony_Frame_Auto()
    colony_frame_auto.colony_frame_fb(fb='EPC-simple.conf')
    colony_frame_auto.colony_frame_slave()
    #     colony_frame_auto.colony_frame_change_request(change_name=('AGE', 'YEAR'))
    #     colony_frame_info()方法，将所有操作进行持久化。
    colony_frame_auto.colony_frame_info()

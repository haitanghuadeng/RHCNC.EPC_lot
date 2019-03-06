# -*- coding:utf-8 -*-


import os
import configparser


class Customized_Conf():

    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.sections()

    def colony_customized_create(self, file_name='EMQ-simple', advanced=None):
        """
        colony_customized_create()方法，定制化生产emq架构服务
        file_name形参：指定conf文件名称，将会初始化生成该文件
        advanced形参：指定EPC_lot框架的配置文件范围，作用范围决定该文件生成的配置参数数量

        逻辑架构：
        主框架 |
                EMQ框架 | 自动化框架 | 集群框架 | 扩展框架

        物理架构：
        从框架 |
                IP集群框架 | 订阅持久化架构 | 消息持久化架构 | 可视化架构


        emq_frame 承载消息服务器的开启，监控开启
        auto_frame 承载了节点循时管理，集群列表管理
        colony_frame 承载了集群架构的高级特性(例如：MCL最小耦合路径损耗)
        extend_frame 承载了可定制化的框架
        ip_colony_frame 承载了集群框架的网络层
        subscription_lasting_frame 承载了订阅持久化架构的一系列配置(包括当前架构的地位：Pc/Server)
        info_lasting_frame 承载了EPC_lot架构的消息持久化方面，根据订阅持久化的策略，而去决定消息持久化的地位。
            这之间也确定了持久化的位置，以及对DB的方法。
        visual_frame 承载了可视化架构方面的支持，YES/NO将决定是否开启WEB框架，这将是由tornado提供。

        若advanced形参为：None
            该方法只提供如下几种

        主(逻辑)架构：
        主框架 |
                EMQ框架 | 自动化框架 | 集群框架 | 扩展框架

        从(物理)架构：
        从框架 |
                IP集群框架 | 可视化架构

        """
        __master_frame = [
            'EMQ_FRAME',
            'AUTO_FRAME',
            'COLONY_FRAME',
            'EXTEND_FRAME']
        __slave_frame = [
            'IP_COLONY_FRAME',
            'VISUAL_FRAME']
        emq_frame = {'emq_server': 'YES', 'emq_service_monitoring': 'YES'}
        auto_frame = {'node_find': '60s', 'colony_find': 'YES'}
        colony_frame = {'MCL_status': 'NO'}
        extend_frame = {'customized_frame': 'YES'}
        ip_colony_frame = {'ip_find_list': 'NO'}
        subscription_lasting_frame = {
            'subscription_lasting': 'NO',
            'Client_subscription': 'YES',
            'Server_subscription': 'NO'}
        info_lasting_frame = {
            'info_lasting': 'NO',
            '#info_path': '#local/global',
            'info_path': 'NO',
            '#DB_info': '#mysql/127.0.0.1:3306  | NO',
            'DB_info': 'NO'}
        visual_frame = {'visual_frame': 'YES'}

        def file_():

            if '.conf' in file_name:

                if not os.path.exists(f'{file_name}'):

                    with open(f'{file_name}', 'w+') as f:
                        pass
                else:
                    exit()

                return f'{file_name}'
            else:

                if not os.path.exists(f'{file_name}.conf'):

                    with open(f'{file_name}.conf', 'w+') as f:
                        pass
                else:
                    exit()

                return f'{file_name}.conf'

        """
        advanced 默认为None，则使用精简化conf文件
        advanced 如果为True，则使用标准conf文件
        --------------------------------------
        当前部署的服务器如果为主，那么建议使用标准conf文件
        """

        for i in __master_frame:
            self.config.add_section(i)
        for i in __slave_frame:
            self.config.add_section(i)

        self.config['EMQ_FRAME'] = {**emq_frame}
        self.config['AUTO_FRAME'] = {**auto_frame}
        self.config['COLONY_FRAME'] = {**colony_frame}
        self.config['EXTEND_FRAME'] = {**extend_frame}
        self.config['IP_COLONY_FRAME'] = {**ip_colony_frame}
        self.config['VISUAL_FRAME'] = {**visual_frame}

        if advanced is None:
            pass

        else:
            more_config = ['SUBSCRIPTION_LASTING_FRAME', 'INFO_LASTING_FRAME']
            for i in more_config:
                self.config.add_section(i)

            self.config['SUBSCRIPTION_LASTING_FRAME'] = {**subscription_lasting_frame}
            self.config['INFO_LASTING_FRAME'] = {**info_lasting_frame}

        self.config.write(open(f'{file_()}', 'w+'))


if __name__ == '__main__':
    customized_conf = Customized_Conf()
    customized_conf.colony_customized_create(advanced=True)


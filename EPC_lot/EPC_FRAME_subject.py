# -*- coding:utf-8 -*-


import os
import configparser


class Customized_Conf:

    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.sections()

    def colony_customized_create(self, file_name='EPC-simple', advanced=None):
        """
        colony_customized_create()方法，定制化生产emq架构服务
        file_name形参：指定conf文件名称，将会初始化生成该文件
        advanced形参：指定EPC_lot框架的配置文件范围，作用范围决定该文件生成的配置参数数量

        逻辑架构：
        主框架 |
                EMQ框架 | 自动化框架 | 集群框架 | 扩展框架 | 感知层框架 | 粒度级别架构

        物理架构：
        从框架 |
                IP集群框架 | 订阅_消息持久化架构 | 可视化架构


        emq_frame 承载消息服务器的开启，监控开启
        auto_frame 承载了节点循时管理，集群列表管理。
        colony_frame 承载了集群架构的高级特性(例如：MCL最小耦合路径损耗)
        extend_frame 承载了可定制化的框架
        perception_frame 承载了拟态传感器的测试目标，将消息服务器存放至此。
            EPC架构将进行感知层之上的测试时，只需要填写EMQ消息服务器端ip、端口即可。默认心跳为60。
            同时，监听的ip层同样也是存在于此。
            承载可寻址和亲缘关系。
        granularity_level_frame 承载了粒度级别框架，EPC将会对通过EMQ转发的架构进行粒度滤载。根据已设定完成的conf中，读取对应策略。
            默认监听的每个主题设定粒度是5

        ip_colony_frame 承载了集群框架的网络层
        subscription_lasting_frame 承载了订阅持久化架构的一系列配置(包括当前架构的地位：Pc/Server)
        visual_frame 承载了可视化架构方面的支持，YES/NO将决定是否开启WEB框架，这将是由tornado提供。

        若advanced形参为：None
            该方法只提供如下几种

        主(逻辑)架构：
        主框架 |
                EMQ框架 | 自动化框架 | 集群框架 | 扩展框架 | 感知层框架

        从(物理)架构：
        从框架 |
                IP集群框架 | 可视化架构

        """
        __master_frame = [
            'EMQ_FRAME',
            'AUTO_FRAME',
            'COLONY_FRAME',
            'EXTEND_FRAME',
            'PERCEPTION_FRAME',
            'granularity_level_FRAME']
        __slave_frame = [
            'IP_COLONY_FRAME',
            'VISUAL_FRAME']

        emq_frame = {'emq_server': 'YES', 'emq_service_monitoring': 'YES'}
        auto_frame = {'node_find': '60s', 'colony_find': 'YES', }
        colony_frame = {'MCL_status': 'NO'}
        extend_frame = {'customized_frame': 'YES'}
        perception_frame = {'info_server_ip': '127.0.0.1', 'info_server_port': '1883'}
        granularity_level_frame = {'granularity_level': '0 <= float/int <= 10 ',
                                   'granularity_level_scope': '100/0.1'}
        ip_colony_frame = {'ip_colony_find': 'NO'}
        subscription_info_lasting_frame = {
            'addressable_topic': 'YES',
            'subscription_lasting': 'NO',
            'io_subscription_lasting': 'NO',
            '#subscription_database_lasting': '127.0.0.1:3306  | NO',
            'subscription_database_lasting': 'NO',
            '#database_user': 'root',
            '#database_password': '',
            'local_lasting_path': 'EPC_json\\',
            '# ============================': '',
            'subscription_pull_auto': 'YES',
            'subscription_pull_auto_local': 'YES',
            'subscription_pull_path': 'EPC_json\\'}
        visual_frame = {'visual_frame': 'YES'}

        def file_():

            if '.conf' in file_name:

                if not os.path.exists(file_name):
                    with open(file_name, 'w+'):
                        pass

                else:
                    exit()

                return file_name
            else:

                if not os.path.exists('{}.conf'.format(file_name)):
                    with open('{}.conf'.format(file_name), 'w+'):
                        pass

                else:
                    exit()

                return '{}.conf'.format(file_name)

        """
        advanced 默认为None，则使用精简化conf文件
        advanced 如果为True，则使用标准conf文件
        --------------------------------------
        当前部署的服务器如果为主，那么建议使用标准conf文件
        """

        for i, k in zip(__master_frame, __slave_frame):
            self.config.add_section(i)
            self.config.add_section(k)

        self.config['EMQ_FRAME'] = {**emq_frame}
        self.config['AUTO_FRAME'] = {**auto_frame}
        self.config['COLONY_FRAME'] = {**colony_frame}
        self.config['EXTEND_FRAME'] = {**extend_frame}
        self.config['PERCEPTION_FRAME'] = {**perception_frame}
        self.config['IP_COLONY_FRAME'] = {**ip_colony_frame}
        self.config['VISUAL_FRAME'] = {**visual_frame}

        if advanced:
            more_config = ['SUBSCRIPTION_INFO_LASTING_FRAME']
            for i in more_config:
                self.config.add_section(i)

            self.config['SUBSCRIPTION_INFO_LASTING_FRAME'] = {**subscription_info_lasting_frame}
            self.config['GRANULARITY_LEVEL_FRAME'] = {**granularity_level_frame}

        self.config.write(open(file_(), 'w+'))


if __name__ == '__main__':
    customized_conf = Customized_Conf()
    customized_conf.colony_customized_create(advanced=True)

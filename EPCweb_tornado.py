# -*- coding:utf-8 -*-


import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
import EMQ_monitoring as epc
from tornado.options import define, options
from tornado.web import RequestHandler

define('port', default=80, help=' Run Help!', type=int)


class MainHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('main.html')

    def post(self, *args, **kwargs):
        pass


class ApacheHandler(RequestHandler):
    def get(self):
        epcssh = epc.EpcSsh()
        ip = epcssh.conf_read()
        server_info = epcssh.epc_ssh(hostname=ip, username='root', password='1234.com')
        epcssh.epc_close()
        self.render('Apache.html', server_info=server_info)

    def post(self, *args, **kwargs):
        epcssh = epc.EpcSsh()
        ip = epcssh.conf_read()
        server_info = epcssh.epc_ssh(hostname=ip, username='root', password='1234.com')
        epcssh.epc_close()
        self.render('Apache.html', server_info=server_info)


class TomcatHandler(RequestHandler):
    def get(self):
        self.render('tomcat.html')

    def post(self):
        self.render('show_view_charts.html')


applications = tornado.web.Application(
    handlers=[
        (r'/main', MainHandler),
        (r'/apache', ApacheHandler),
        (r'/tomcat', TomcatHandler),],
    template_path='templates',
)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(applications)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

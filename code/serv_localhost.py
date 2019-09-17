import os

import tornado.ioloop
import tornado.web

from tornado.ioloop import IOLoop


from web_handlers import HandlerDatabase


class WebApplication(tornado.web.Application):
    def __init__(self, configuration, helper):
        current_path = os.path.dirname(os.path.abspath(__file__))
        web_resources = current_path + '/web_resources'

        handlers = [
            (r'/database', HandlerDatabase, dict(configuration=configuration, helper=helper))
        ]

        settings = {
            'static_path': web_resources,
            'template_path': 'web_templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class ServLocalhost:
    def __init__(self, configuration, helper):
        self.configuration = configuration
        self.config = configuration.config
        self.helper = helper

        self.name = 'serv_localhost'
        # no conflict with main server
        port = self.config[self.name]['server_port']
        address = '127.0.0.1'

        ws_app = WebApplication(self.configuration, self.helper)
        server = tornado.httpserver.HTTPServer(ws_app)

        self.helper.log_add_text(self.name, 'Start ' + self.name + 'at address ' + address + ' port:' + str(port))
        server.listen(port, address=address)
        IOLoop.instance().start()

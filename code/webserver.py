#!/usr/bin/env python
import os

import threading
import tornado.web
import tornado.websocket
import tornado.httpserver
from tornado import gen
from tornado.ioloop import IOLoop

from random import randint

from web_handlers import HandlerCamera
from web_handlers import HandlerCameraStream
from web_handlers import HandlerConfig
from web_handlers import HandlerIndexPage
from web_handlers import HandlerPreview
from web_handlers import HandlerSend
from web_handlers import HandlerShutdown
from web_handlers import HandlerWebSockets


def current_modus_updated(current_modus, helper, m_modus):
    try:
        new_modus = {}
        # do not remove next line as this is needed to avoid reference changes !
        new_modus = helper.copy_modus(m_modus, new_modus)
        if helper.is_different_modus(current_modus, new_modus):
            current_modus = helper.copy_modus(new_modus, current_modus)
        else:
            pass
    except Exception as e:
        print(e)
    return current_modus

@gen.coroutine
def generate_message_to_sockets(configuration, helper, m_modus):
    current_modus = configuration.default_mode()
    while True:
        msg = current_modus_updated(current_modus, helper, m_modus)
        yield [con.write_message(msg) for con in HandlerWebSockets.connections]
        yield gen.sleep(1.0)


class WebApplication(tornado.web.Application):
    def __init__(self, l_lock, configuration, helper, q_message, m_video):
        current_path = os.path.dirname(os.path.abspath(__file__))
        web_resources = current_path + '/web_resources'
        output_folder = configuration.output_folder()

        handlers = [
            (r'/', HandlerIndexPage, dict(configuration=configuration, helper=helper)),
            (r'/actioncam/(.*)', tornado.web.StaticFileHandler, {'path': web_resources}),
            (r'/camera', HandlerCamera, dict(l_lock=l_lock, configuration=configuration, q_message=q_message)),
            (r'/camera/stream.jpeg', HandlerCameraStream, dict(m_video=m_video)),
            (r'/config', HandlerConfig, dict(configuration=configuration)),
            (r'/preview', HandlerPreview, dict(configuration=configuration, helper=helper)),
            (r'/send', HandlerSend, dict(configuration=configuration, helper=helper)),
            (r'/recordings/(.*)', tornado.web.StaticFileHandler, {'path': output_folder}),
            (r'/shutdown', HandlerShutdown, dict(helper=helper, l_lock=l_lock, q_message=q_message)),
            (r'/websockets', HandlerWebSockets, dict(helper=helper, ))
        ]

        settings = {
            'static_path': web_resources,
            'template_path': 'web_templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class WebServer:
    def __init__(self, l_lock, configuration, helper, q_message, m_modus, m_video):
        self.configuration = configuration
        self.config = configuration.config
        self.helper = helper
        self.m_modus = m_modus

        self.name = 'webserver'

        port = self.config[self.name]['server_port']
        ws_app = WebApplication(l_lock, configuration, self.helper, q_message,  m_video)
        server = tornado.httpserver.HTTPServer(ws_app)

        self.log('Start web server at port:' + str(port))
        server.listen(port)
        IOLoop.current().spawn_callback(generate_message_to_sockets, self.configuration, self.helper, self.m_modus)
        IOLoop.instance().start()

    def log(self, text):
        self.helper.log_add_text(self.name, text)

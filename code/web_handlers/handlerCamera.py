import tornado.web
import json


class HandlerCamera(tornado.web.RequestHandler):
    def initialize(self, l_lock, configuration, q_message):
        self.configuration = configuration
        self.l_lock = l_lock
        self.q_message = q_message

    def post(self, *args):
        # todo check if valid
        camera_mode = tornado.escape.json_decode(self.request.body)
        with self.l_lock:
            self.q_message.put(camera_mode)
        self.write(json.dumps({'status': 'set mode to ' + camera_mode}))
        self.finish()

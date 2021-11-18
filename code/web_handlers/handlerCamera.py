import tornado.web
import json


class HandlerCamera(tornado.web.RequestHandler):
    def initialize(self, l_lock, configuration, q_message):
        self.configuration = configuration
        self.config = self.configuration.config["camera"]
        self.debug = self.configuration.config['debug']

        self.l_lock = l_lock
        self.q_message = q_message

    def post(self, *args):
        camera_mode = tornado.escape.json_decode(self.request.body)
        if camera_mode.startswith("camera_mode:"):
            new_modus = camera_mode.split(":")[1]
        else:
            new_mods = "bad"
        if self.debug:
            print("HandlerCamera:" + camera_mode)
            print("HandlerCamera:" + new_modus)
        if new_modus in self.config["modes"]:
            with self.l_lock:
                self.q_message.put(camera_mode)
            self.write(json.dumps({'status': 'set mode to ' + camera_mode}))
        else:
            self.write(json.dumps({'status': 'mode declined'}))
        self.finish()

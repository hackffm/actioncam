import tornado.web


class HandlerShutdown(tornado.web.RequestHandler):
    def initialize(self, helper, l_lock, q_message):
        self.helper = helper
        self.lock = l_lock
        self.q_message = q_message

    def get(self):
        try:
            self.lock.acquire()
            self.q_message.put('do:shutdown')
            self.lock.release()
        except Exception as e:
            print(e)
        infos = self.helper.state_updated()
        self.render("shutdown.html", title="Shutdown", items=infos)

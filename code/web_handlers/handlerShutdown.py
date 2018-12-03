import tornado.web


class HandlerShutdown(tornado.web.RequestHandler):
    def initialize(self, l_lock, q_message):
        self.q_message = q_message
        self.lock = l_lock

    def get(self):
        try:
            self.lock.acquire()
            self.q_message.put('do:shutdown')
            self.lock.release()
        except Exception as e:
            print(e)
        infos = ['time', 'recordings']
        self.render("shutdown.html", title="Shutdown", items=infos)

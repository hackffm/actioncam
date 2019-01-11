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
        state = self.helper.state_load()
        dt_start = state['dt_start']
        dt_diff = str(self.helper.datetime_diff_from_string(dt_start))
        infos = []
        infos.append('started:' + dt_start)
        infos.append('Now: ' + str(self.helper.now()))
        infos.append('seconds running: ' + dt_diff)
        self.render("shutdown.html", title="Shutdown", items=infos)

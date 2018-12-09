import tornado.web


class HandlerIndexPage(tornado.web.RequestHandler):
    def initialize(self, configuration, helper):
        self.configuration = configuration
        self.helper = helper

    def get(self):
        ip = self.helper.interfaces_first()
        self.render("index.html", ip=ip)

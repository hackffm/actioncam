import tornado.web


class HandlerIndexPage(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
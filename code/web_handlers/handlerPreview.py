import tornado.web


class HandlerPreview(tornado.web.RequestHandler):
    def initialize(self, configuration, helper):
        self.configuration = configuration
        self.helper = helper

        self.config = configuration.config

    def get(self):
        items = self.helper.preview_files()
        self.render("preview.html", title="Previews", items=items)


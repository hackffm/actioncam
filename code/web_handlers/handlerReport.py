import tornado.web


class HandlerReport(tornado.web.RequestHandler):
    def initialize(self, configuration, helper):
        self.configuration = configuration
        self.helper = helper

        self.config = configuration.config

    def get(self):
        items = self.helper.report_all()
        self.helper.log_add_text('test', str(len(items)))
        self.render("report.html", title="Previews", items=items)


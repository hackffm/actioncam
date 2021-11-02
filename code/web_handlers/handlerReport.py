import tornado.web


class HandlerReport(tornado.web.RequestHandler):
    def initialize(self, configuration, helper):
        self.configuration = configuration
        self.helper = helper
        self.name = 'HandlerReport'
        self.config = configuration.config

    def get(self):
        try:
            items = self.helper.report_all()
            self.render("report.html", title="Report", items=items)
        except Exception as e:
            self.log(str(e))

    def log(self, text):
        self.helper.log_add_text(self.name, text)


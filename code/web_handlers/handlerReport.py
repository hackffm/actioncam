import tornado.web

from local_services import Compress

class HandlerReport(tornado.web.RequestHandler):
    def initialize(self, configuration, helper):
        self.configuration = configuration
        self.helper = helper
        self.name = 'HandlerReport'
        self.config = configuration.config
        self.compress = Compress(configuration, helper)

    def get(self):
        try:
            items_compressed = self.compress.get_compressed()
            self.render("report.html", title="Report", items_comp=items_compressed)
        except Exception as e:
            self.log(str(e))

    def log(self, text):
        self.helper.log_add_text(self.name, text)


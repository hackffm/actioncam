import tornado.web


class HandlerSend(tornado.web.RequestHandler):
    def initialize(self, configuration, helper):
        self.configuration = configuration
        self.config = configuration.config
        self.helper = helper

    def get(self):
        sended = self.helper.report_csv('mail')
        sendedHtml = sended.to_html(border=0)
        self.render("send.html", title="Send", htmlSend=sendedHtml)

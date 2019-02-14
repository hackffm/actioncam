import json
import tornado.websocket


class HandlerWebSockets(tornado.websocket.WebSocketHandler):
    connections = set()
    
    def initialize(self, helper):
        self.helper = helper
    
    def log(self, text):
        self.helper.log_add_text('handlerWebsockets', text)
           
    def writeMessage(self, msg):
        [con.write_message(msg) for con in HandlerWebSockets.connections]
        return 
        
    # -- default events--------------------------#
    def open(self):
        self.connections.add(self)
        message = {"actioncam": "welcome", "camera": "", "idle": 0, "info": "none"}
        self.writeMessage(json.dumps(message))
        self.log('new connection was opened')
        return

    # currently we don't expect messages from the webfrontend
    def on_message(self, message):
        self.log('from WebSocket: ', message)

    def on_close(self):
        self.connections.remove(self)
        self.log('connection closed')

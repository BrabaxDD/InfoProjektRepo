from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync


class gamePlayerSocketConsumer(WebsocketConsumer):
    def __init__(self):
        self.firstMessage = True
        self.gameServerName = ""
        self.tmpGroupName = "test"

    def connect(self):
        #        async_to_sync(self.channel_layer.group_add)(
        #            self.tmpGroupName, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        pass
#        async_to_sync(self.channel_layer.group_discard)(
#            self.tmpGroupName, self.channel_name)

    def receive(self, text_data):
        if self.firstMessage:
            text_data_json = json.loads(text_data)
            self.gameServerName = text_data_json["serverName"]
        positionx = text_data_json["posx"]
        positiony = text_data_json["posy"]
#        async_to_sync(self.channel_layer.group_send)(
#            self.tmpGroupName,
#            {
#                "type": "position",
#                "posx": positionx,
#                "posy": positiony
#            }
#        )

    def position(self, event):
        posx = event["posx"]
        posy = event["posy"]
        self.send(text_data=json.dumps({
            "positionx": posx,
            "positiony": posy,
        }))

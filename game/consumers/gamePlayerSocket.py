from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync


class gamePlayerSocketConsumer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.firstMessage = True
        self.gameServerName = ""
        self.tmpGroupName = "test"
        self.player_ID = "opfer"

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.tmpGroupName, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        pass
        async_to_sync(self.channel_layer.group_discard)(
            self.tmpGroupName, self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        messageType = text_data_json["type"]
        if messageType == "action":
            up = text_data_json["up"]
            down = text_data_json["down"]
            left = text_data_json["left"]
            right = text_data_json["right"]

            async_to_sync(self.channel_layer.group_send)(
                self.tmpGroupName,
                {
                    "type": "action",
                    "ID": self.player_ID,
                    "up": up,
                    "down": down,
                    "left": left,
                    "right": right,
                }
            )
        if messageType == "login":
            ID = text_data_json["ID"]
            self.player_ID = ID
            async_to_sync(self.channel_layer.group_send)(
                self.tmpGroupName, {"type": "login", "ID": ID})

    def position(self, event):
        if event["ID"] == self.player_ID:
            posx = event["posx"]
            posy = event["posy"]
            self.send(text_data=json.dumps({
                "type": "position",
                "ID": self.player_ID,
                "posx": posx,
                "posy": posy,
            }))
    def login(self,event):
        pass
    def action(self,event):
        pass

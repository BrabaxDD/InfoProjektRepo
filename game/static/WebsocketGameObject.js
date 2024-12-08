import GameObject from "./GameObject.js"

export default class websocketGameObjectClient extends GameObject {
    constructor(serverName) {
        this.serverName = serverName
        this.webSocket = new WebSocket('ws://' + window.location.host + '/game/login')
        this.webSocket.onmessage == function(e) {
            data = JSON.parse(e.data)
            type = data.type
            switch(type){
                case position:
                




            }

        }
    }
}

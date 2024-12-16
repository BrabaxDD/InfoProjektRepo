import { start } from "./game.js"
import GameObject from "./GameObject.js"

export default class WebsocketGameObjectClient extends GameObject{
    constructor(scene) {
        super(scene)

        this.webSocketHost = new WebSocket('ws://' + window.location.host + '/game/server')
        this.webSocket = new WebSocket('ws://' + window.location.host + '/game/login')
        this.webSocket.onmessage = function(e) {
            let data = JSON.parse(e.data)
            let type = data.type
            if(type == "position"){
                    this.scene.eventBus.triggerEvent("position", {type:data.entityType, ID: data.ID , posx:data.posx , posy:data.posy})
            }
            

        }
    }

    updateToServer(){
        //console.log("Server update")
        this.webSocket.send(JSON.stringify({type: "action", up: this.scene.gameObjects[0].up, down: this.scene.gameObjects[0].down, left: this.scene.gameObjects[0].left, right: this.scene.gameObjects[0].right, actiontype: "movement"}))
    }

    loginToServer(serverName){
        console.log(this.scene.gameObjects)
        console.log("PLAYER ID:")
        console.log(this.scene.mainPlayerID)
        console.log("LOGGIN IN TO SERVER: "+serverName)
        this.webSocket.send(JSON.stringify({type: "login", ID:this.scene.mainPlayerID, serverID:serverName}))
        while (this.webSocket.readyState != this.webSocket.OPEN){
            this.sleep(10)
        }
        start()
    }
    
    loginToServerHost(serverName){
        console.log("SETTUING UP NEW SERVER: "+serverName)
        this.webSocketHost.send(JSON.stringify({type : "startserver", serverID : serverName}))
    }
    
    generateItem(object){
        console.log("Generating Item: "+ object)
        this.webSocket.send(JSON.stringify({type : "generateItem", itemID : object}))
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
        }
}

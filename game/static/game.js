import GameSceneFactory from './GameSceneFactory.js';
import Player from './Player.js';
import Scene from './Scene.js';
import SceneSwitcher from './SceneSwitcher.js';
import WebsocketGameObjectClient from './WebsocketGameObject.js';

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
ctx.font = 60
//const webSocketHost = new WebSocket('ws://' + window.location.host + '/game/server')
//const webSocket = new WebSocket('ws://' + window.location.host + '/game/login')


/*webSocket.onmessage = function(e) {
    const data = JSON.parse(e.data)
    //console.log("")
    //console.log(data)
    if (!isStarted){
        return
    }
    //console.log(data)

    scene.eventBus.triggerEvent("position", {type:data.entityType, ID: data.ID , posx:data.posx , posy:data.posy})
    /*if(data.type == "position" && data.entityType == "Player"){
        scene.gameObjects[scene.playerIndex].posx = data.posx
        scene.gameObjects[scene.playerIndex].posy = data.posy
    }
}*/


// Canvas dimensions
const canvasWidth = canvas.width;
const canvasHeight = canvas.height;




window.addEventListener('keydown', (e) => {
    //keys[e.key] = true;
    scene.eventBus.triggerEvent("keydown", {key:e.key, status:true})
});

window.addEventListener('keyup', (e) => {
    //keys[e.key] = false;
    scene.eventBus.triggerEvent("keydown", {key:e.key, status:false})
});




function websocket() { }

function gameLoop() {
    ctx.clearRect(0, 0, canvasWidth, canvasHeight); // Clear the canvas
    scene.process()
    scene.render()
    if (isStarted){
            if (frameCount >= 1){
                websocketGameObjectClient.updateToServer()
                frameCount = 0
            }
        frameCount += 1
    }
    requestAnimationFrame(gameLoop); // Call the next frame
}


let factory = new GameSceneFactory(canvas, null)
let scene = factory.buildGameScene("mainMenu")
let playerID = 1000
var frameCount = 0
var isDelayed = false
var isStarted = false
// Start the game loop
gameLoop();


function sayHello() {
    webSocket.send(JSON.stringify({ 'posx': scene.gameObjects[0].posx, 'posy': scene.gameObjects[0].posy }))
    //    webSocket.send(JSON.stringify({'login':true, 'server_id': input}))
}


document.getElementById('clickMeButton').addEventListener('click', sayHello);

canvas.addEventListener('click',(event) => {
    scene.eventBus.triggerEvent("click_on_canvas")
});








export function getMainPlayerID(){
    return scene.mainPlayerID
}

export function switchScene(sceneToSwitch){
    console.log("NEW SCENE")
    scene = factory.buildGameScene(sceneToSwitch) 
    //webSocketHost = new WebSocket('ws://' + window.location.host + '/game/server')
    //webSocket = new WebSocket('ws://' + window.location.host + '/game/login')

}

export function start(){
    isStarted = true
}
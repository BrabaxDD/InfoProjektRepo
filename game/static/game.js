import GameSceneFactory from './GameSceneFactory.js';
import Player from './Player.js';
import Scene from './Scene.js';
import SceneSwitcher from './SceneSwitcher.js';

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
ctx.font = 60
const webSocketHost = new WebSocket('ws://' + window.location.host + '/game/server')
const webSocket = new WebSocket('ws://' + window.location.host + '/game/login')


webSocket.onmessage = function(e) {
    const data = JSON.parse(e.data)
    console.log("")
    console.log(data)
    if (data.ID === playerID){
            if(data.type == "position" && data.entityType == "Player"){
                scene.gameObjects[scene.playerIndex].posx = data.posx
                scene.gameObjects[scene.playerIndex].posy = data.posy
            }
    }
}

// Canvas dimensions
const canvasWidth = canvas.width;
const canvasHeight = canvas.height;


const keys = {}; // Object to track key states

window.addEventListener('keydown', (e) => {
    keys[e.key] = true;
});

window.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});




function websocket() { }

function gameLoop() {
    ctx.clearRect(0, 0, canvasWidth, canvasHeight); // Clear the canvas
    scene.process()
    scene.render()
    if (isStarted){
        if(isDelayed == true){
            if (frameCount >= 5){
                updateToServer()
                frameCount = 0
            }
        }
        if (frameCount >= 200){
            isDelayed = true
        }
        frameCount += 1
    }
    requestAnimationFrame(gameLoop); // Call the next frame
}


let factory = new GameSceneFactory(canvas, keys)
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

export function switchScene(sceneToSwitch){
    console.log("NEW SCENE")
    scene = factory.buildGameScene(sceneToSwitch) 
    //webSocketHost = new WebSocket('ws://' + window.location.host + '/game/server')
    //webSocket = new WebSocket('ws://' + window.location.host + '/game/login')

}


function updateToServer(){
    console.log("Server update")
    webSocket.send(JSON.stringify({type: "action", up: scene.gameObjects[0].up, down: scene.gameObjects[0].down, left: scene.gameObjects[0].left, right: scene.gameObjects[0].right}))
}

export function loginToServer(serverName){
    let d = new Date()
    playerID = d.getTime().toString()
    console.log("PLAYER ID:")
    console.log(playerID)
    console.log("LOGGIN IN TO SERVER: "+serverName)
    webSocket.send(JSON.stringify({type: "login", ID:playerID, serverID:serverName}))
    isStarted = true
}

export function loginToServerHost(serverName){
    console.log("SETTUING UP NEW SERVER: "+serverName)
    webSocketHost.send(JSON.stringify({type : "startserver", serverID : serverName}))
}

export function generateItem(object){
    console.log("Generating Item: "+ object)
    webSocket.send(JSON.stringify({type : "generateItem", itemID : object}))
}

import GameSceneFactory from './GameSceneFactory.js';
import Player from './Player.js';
import Scene from './Scene.js';
import SceneSwitcher from './SceneSwitcher.js';
import Tree from './tree.js';
import Zombie from "./zombie.js";

export const font = "20px Arial"

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
ctx.font = font
const webSocketHost = new WebSocket('ws://' + window.location.host + '/game/server')
const webSocket = new WebSocket('ws://' + window.location.host + '/game/login')


webSocket.onmessage = function(e) {
    const data = JSON.parse(e.data)
    //console.log("")
    //console.log(data)


    if (data.type == "InventoryUpdate"){
        console.log(e)
        console.log(data)
        scene.eventBus.triggerEvent("inventory",data.Inventory)
    }

    if (data.type == "position"){
        scene.eventBus.triggerEvent("position", {type:data.entityType, ID: data.ID , posx:data.posx , posy:data.posy})
    }

    if (data.type == "newGameObject"){
        
        if (data.entityType == "Tree"){
            const t = new Tree(scene,data.ID)
            scene.addObject(t)
            console.log(scene.gameObjects)
        }
        if (data.entityType == "Player"){
            let player = new Player(100,100,20,20, 'blue', 5,scene, data.ID)
            scene.addObject(player)
        }
        if (data.entityType == "Zombie"){
            const z = new Zombie(scene,data.ID)
            scene.addObject(z)
            console.log("new Zombie")
            console.log(scene.gameObjects)
        }
        
    }
    
    /*if(data.type == "position" && data.entityType == "Player"){
        scene.gameObjects[scene.playerIndex].posx = data.posx
        scene.gameObjects[scene.playerIndex].posy = data.posy
    }*/
}

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
        if(isDelayed == true){
            if (frameCount >= 1){
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


let factory = new GameSceneFactory(canvas, null)
let scene = factory.buildGameScene("mainMenu")
let loginID = -100
var frameCount = 0
var isDelayed = false
var isStarted = false
// Start the game loop
gameLoop();



canvas.addEventListener('click',(event) => {
    scene.eventBus.triggerEvent("click_on_canvas")
});

canvas.addEventListener("mousedown", (event) => {
    scene.eventBus.triggerEvent("mouseDown",{status:true})
});
canvas.addEventListener("mouseup", (event) => {
    scene.eventBus.triggerEvent("mouseDown",{status:false})
});

export function switchScene(sceneToSwitch){
    console.log("NEW SCENE")
    scene = factory.buildGameScene(sceneToSwitch) 
    //webSocketHost = new WebSocket('ws://' + window.location.host + '/game/server')
    //webSocket = new WebSocket('ws://' + window.location.host + '/game/login')

}


function updateToServer(){
    //console.log("Server update")
    webSocket.send(JSON.stringify({type: "action", up: scene.gameObjects[scene.playerIndex].up, down: scene.gameObjects[scene.playerIndex].down, left: scene.gameObjects[scene.playerIndex].left, right: scene.gameObjects[scene.playerIndex].right, actiontype: "movement"}))
}

export function loginToServer(serverName){
    
    console.log("PLAYER ID:")
    console.log(scene.mainPlayerID)
    console.log("LOGGIN IN TO SERVER: "+serverName)
    let d = new Date()
    loginID = Math.floor(Math.random() * 3000000001)
    webSocket.send(JSON.stringify({type: "login", ID:loginID, serverID:serverName}))
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

export function getMainPlayerID(){
    return scene.mainPlayerID
}

export function hit(){
    console.log("HIT")
    webSocket.send(JSON.stringify({type:"action", actiontype:"hit",direction:100}))
}

export function addTestInv(){
    scene.eventBus.triggerEvent("inventory",{"items": [{"size": 99, "itemID": "Stick", "tags": []}, {itemID:"Stick",size:3,tags:{}}, {itemID:2, size:5, tags:{}}, {itemID:"Stick", size:5, tags:{}}, {itemID:"Stick", size:8, tags:{}},{"size": 99, "itemID": "Stick", "tags": []}, {itemID:"Stick",size:3,tags:{}}, {itemID:2, size:5, tags:{}}, {itemID:"Stick", size:5, tags:{}}, {itemID:"Stick", size:8, tags:{}}]})
}

import GameSceneFactory from './GameSceneFactory.js';
import Player from './Player.js';
import Scene from './Scene.js';
import SceneSwitcher from './SceneSwitcher.js';

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
//const webSocket = new WebSocket('ws://' + window.location.host + '/game/login')
const webSocket = new WebSocket('ws://' + window.location.host + '/game/server')


webSocket.onmessage = function(e) {
    const data = JSON.parse(e.data)

    scene.gameObjects[0].posx = data.posx
    scene.gameObjects[0].posy = data.posy
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
    requestAnimationFrame(gameLoop); // Call the next frame
}


let factory = new GameSceneFactory(canvas, keys)
let scene = factory.buildGameScene("mainMenu")
loginToServer()
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

export default function switchScene(sceneToSwitch){
    console.log("NEW SCENE")
    scene = factory.buildGameScene(sceneToSwitch) 
}


function updateToServer(){
    webSocket.send(JSON.stringify({ type: "action", up: scene.gameObjects[0].up, down: scene.gameObjects[0].down, left: scene.gameObjects[0].left, right: scene.gameObjects[0].right}))
}

function loginToServer(){
    webSocket.send(JSON.stringify({ type: "login", ID:1000}))
}
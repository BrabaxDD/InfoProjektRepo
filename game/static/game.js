import GameSceneFactory from './GameSceneFactory.js';
import Player from './Player.js'; 
import Scene from './Scene.js';
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const webSocket = new WebSocket('ws://' + window.location.host + '/game/login')
//const webSocketServer = new WebSocket('ws://' + window.location.host + '/game/server')

webSocket.onmessage = function(e) {const data = JSON.parse(e.data)
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




function websocket(){}

function gameLoop() {
    ctx.clearRect(0, 0, canvasWidth, canvasHeight); // Clear the canvas
    scene.process()
    scene.render()
    requestAnimationFrame(gameLoop); // Call the next frame
}

let factory = new GameSceneFactory(canvas,keys)
let player = new Player(100,100,20,20, 'blue', 5, canvas, keys)
let scene = factory.buildGameScene("mainMenu")
// Start the game loop
gameLoop();


function sayHello(){
    webSocket.send(JSON.stringify({'posx':scene.gameObjects[0].posx, 'posy': scene.gameObjects[0].posy}))
    webSocket.send(JSON.stringify({'login':true, 'server_id': input}))
}


document.getElementById('clickMeButton').addEventListener('click', sayHello);

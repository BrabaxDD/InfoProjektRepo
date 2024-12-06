import Player from './Player.js'; 
import Scene from './Scene.js';
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const webSocket = new WebSocket('ws://' + window.location.host + '/game/login')
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
    //getPlayer().render(ctx); // Draw the character
    requestAnimationFrame(gameLoop); // Call the next frame
}

let player = new Player(100,100,20,20, 'blue', 5, canvas, keys)
let scene = new Scene()
scene.addObject(player)
// Start the game loop
gameLoop();


function sayHello(){
    webSocket.send(JSON.stringify({'posx':scene.gameObjects[0].posx, 'posy': scene.gameObjects[0].posy}))
}


document.getElementById('clickMeButton').addEventListener('click', sayHello);

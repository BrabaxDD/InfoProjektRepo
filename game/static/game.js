import Player from './Player.js'; 

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const webSocket = new WebSocket('ws://' + window.location.host + '/game')
webSocket.onmessage = function(e) {const data = JSON.parse(e.data)
    getPlayer().x = data.positionx 
    getPlayer().y = data.positiony 
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
    getPlayer().moveCharacter(keys); // Update character position
    getPlayer().drawCharacter(ctx); // Draw the character
    requestAnimationFrame(gameLoop); // Call the next frame
}

let player = new Player(100,100,20,20, "blue", 5, canvas)
// Start the game loop
gameLoop();


function sayHello(){
    webSocket.send(JSON.stringify({'positionx': getPlayer().x,'positiony': getPlayer().y}))
}

function getPlayer(){
    return player
}

document.getElementById('clickMeButton').addEventListener('click', sayHello);
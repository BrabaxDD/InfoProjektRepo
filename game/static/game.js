const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const webSocket = new WebSocket('ws://' + window.location.host + '/game')
webSocket.onmessage = function(e) {const data = JSON.parse(e.data)
        character.x = data.positionx 
        character.y = data.positiony 
}

// Canvas dimensions
const canvasWidth = canvas.width;
const canvasHeight = canvas.height;
let character = {
    x: 50,       // Starting X position
    y: 200,      // Starting Y position
    width: 50,   // Width of the character
    height: 50,  // Height of the character
    color: 'blue', // Character color
    speed: 5     // Movement speed
};


const keys = {}; // Object to track key states

window.addEventListener('keydown', (e) => {
    keys[e.key] = true;
});

window.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

function moveCharacter() {
    if (keys['ArrowUp'] && character.y > 0) {
        character.y -= character.speed; // Move up
    }
    if (keys['ArrowDown'] && character.y < canvasHeight - character.height) {
        character.y += character.speed; // Move down
    }
    if (keys['ArrowLeft'] && character.x > 0) {
        character.x -= character.speed; // Move left
    }
    if (keys['ArrowRight'] && character.x < canvasWidth - character.width) {
        character.x += character.speed; // Move right
    }
}


function drawCharacter() {
    ctx.fillStyle = character.color;
    ctx.fillRect(character.x, character.y, character.width, character.height);
}
function websocket(){}

function gameLoop() {
    ctx.clearRect(0, 0, canvasWidth, canvasHeight); // Clear the canvas
    moveCharacter(); // Update character position
    drawCharacter(); // Draw the character
    requestAnimationFrame(gameLoop); // Call the next frame
}

// Start the game loop
gameLoop();


function sayHello(){
    webSocket.send(JSON.stringify({'positionx': character.x,'positiony': character.y}))
}


import GameSceneFactory from './GameSceneFactory.js';
import WebsocketGameObjectClient from "./WebsocketGameObject.js"
import DOMHandler from './DOMHandler.js';
import AudioHandler from './sounds/AudioHandler.js';

export const DOM = new DOMHandler()
export let settings = undefined
export let websocketObject = undefined

const audioHandler = new AudioHandler()
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let frameCount = 0
let isDelayed = false
let factory = undefined
let isStarted = false
let scene = undefined


//Define all Listeners For the DOM
window.addEventListener('keydown', (e) => {
    //keys[e.key] = true;
    scene.eventBus.triggerEvent("keydown", { key: e.key, status: true })
});

window.addEventListener('keyup', (e) => {
    //keys[e.key] = false;
    scene.eventBus.triggerEvent("keydown", { key: e.key, status: false })
});

window.addEventListener("wheel", (e) => {
    scene.eventBus.triggerEvent("wheel", e.wheelDelta)
})

canvas.addEventListener('click', () => {
    scene.eventBus.triggerEvent("click_on_canvas")
});

canvas.addEventListener("mousedown", () => {
    scene.eventBus.triggerEvent("mouseDown", { status: true })
});
canvas.addEventListener("mouseup", () => {
    scene.eventBus.triggerEvent("mouseDown", { status: false })
});

export function switchScene(sceneToSwitch) {
    websocketObject.getServers()
    scene = factory.buildGameScene(sceneToSwitch)
    websocketObject.setScene(scene)

}

export function start() {
    isStarted = true
}

async function starupGame() {
    settings = await loadSettings()
    websocketObject = new WebsocketGameObjectClient(undefined)
    factory = new GameSceneFactory(canvas, null, undefined, audioHandler)
    scene = factory.buildGameScene("mainMenu")
    DOM.updateDOMControls()

    // Start the game loop
    gameLoop();
}

async function loadSettings() {
    try {
        const response = await fetch(`/static/settings/settings.txt`);
        if (!response.ok) throw new Error("Network response was not ok");

        const settingsText = await response.text();
        const settings = settingsText
            .trim() // Remove any leading/trailing whitespace
            .split("\n") // Split into lines
            .reduce((acc, line) => {
                const [key, value] = line.split(":").map(part => part.trim()); // Split by colon and trim whitespace
                if (key && value) {
                    acc[key] = value; // Add key-value pair to the result object
                }
                return acc;
            }, {}); // Initialize an empty object to accumulate results

        console.log("Settings:", settings);
        ctx.font = settings.font
        return settings;
    } catch (error) {
        console.error("Error loading settings file:", error);
        return null;
    }
}

function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
    scene.process()
    scene.render()
    if (isStarted) {
        if (frameCount >= 1) {
            websocketObject.updateToServer()
            frameCount = 0
        }

        frameCount += 1
    }

    requestAnimationFrame(gameLoop); // Call the next frame
}



//Startup Game
starupGame()




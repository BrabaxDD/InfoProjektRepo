import EventBus from "./EventBus.js"
import SceneSwitcher from "./SceneSwitcher.js"
import TileMap from "./images/TileMap.js"
import ImageLoader from "./images/ImageLoader.js"
import Camera from "./Camera.js"

export default class Scene {
    constructor(canvasObjectScene, mapName) {
        this.eventBus = new EventBus()
        this.sceneSwitcher = new SceneSwitcher(this)
        this.gameObjects = []
        this.toAdd = []
        this.toDelete = []
        this.mousex = 0
        this.mousey = 0
        this.canvas = canvasObjectScene
        
        this.camera = new Camera(this)


        // Initialize the image loader
        this.imageLoader = new ImageLoader();

        this.map = new TileMap(this, 32, mapName)
        this.mainPlayerID = 0


        this.eventBus.registerListner("keydown", this)
        this.eventBus.registerListner("mouseDown", this)

        this.canvas.addEventListener('mousemove', (event) => {
            // Get the bounding rectangle of the canvas
            const rect = this.canvas.getBoundingClientRect();

            // Calculate mouse position relative to the canvas
            this.mousex = event.clientX - rect.left;
            this.mousey = event.clientY - rect.top;
        });

        this.keys = {}; // Object to track key states
        this.mouseDown = false
        this.mouseJustDown = false
    }

    addObject(object) {
        this.toAdd.push(object);
        console.log("added object to scene: " + object.constructor.name);
        if (object.constructor.name == "Player" && this.mainPlayerID == 0) {
            this.mainPlayerID = object.playerID
            this.playerIndex = this.gameObjects.length + this.toAdd.length - 1
            console.log(object)
            console.log(object.playerID)
            console.log("Main Player ID: "+this.mainPlayerID + "  Player Index in Game objects: " + this.playerIndex)
            console.log(this.gameObjects)
            this.camera.setLockedPlayer(object)
        }
        console.log(this.toAdd)
    }

    render() {
        //console.log(this.gameObjects)
        this.map.render()

        this.camera.render()


        let len = this.gameObjects.length;
        for (let i = 0; i < len; i++) {
            //if (i != this.playerIndex && i!= this.tileMapIndex){
            this.gameObjects[i].render();
            //}

        }
    }

    process() {
        let len = this.gameObjects.length
        for (let i = 0; i < len; i++) {
            this.gameObjects[i].process();
        }


        if (this.toDelete.length != 0) {
            this.gameObjects = this.gameObjects.filter(function(el) {
                return toDelete.indexOf(el) < 0;
            });
            this.toDelete = [];
        }

        let len_add = this.toAdd.length
        if (len_add != 0) {
            for (let i = 0; i < len_add; i++) {
                this.gameObjects.push(this.toAdd[i]);
            }
            this.toAdd = [];
        }

        this.camera.process()

    }

    setMainPlayerID(ID) {
        this.mainPlayerID = ID
    }

    event(eventString, eventObject) {
        if (eventString == "keydown") {
            this.keys[eventObject.key] = eventObject.status;
        }
        if (eventString == "mouseDown") {
            if (this.mouseDown == false && eventObject.status == true) {
                this.eventBus.triggerEvent("mouseJustDown", { status: true })

            }

            this.mouseDown = eventObject.status

        }
    }

}

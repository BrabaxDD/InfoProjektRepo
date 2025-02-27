import EventBus from "./EventBus.js"
import SceneSwitcher from "./SceneSwitcher.js"
import TileMap from "./images/TileMap.js"
import ImageLoader from "./images/ImageLoader.js"
import Camera from "./Camera.js"
import Inventory from "./GUI_elements/Inventory.js"
import { settings } from "./game.js"
import CraftingMenu from "./GUI_elements/CraftingMenu.js"
import ErrorHandler from "./ErrorHandler.js"
import RespawnScreen from "./GUI_elements/RespawnScreen.js"

export default class Scene {
    constructor(canvasObjectScene, mapName, audioHandler) {
        this.eventBus = new EventBus()
        this.sceneSwitcher = new SceneSwitcher(this)
        this.errorHandler = new ErrorHandler(this)
        this.audioHandler = audioHandler
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
        this.eventBus.registerListner("deletedGameObject", this)
        this.eventBus.registerListner("createInv", this)
        this.eventBus.registerListner("createCraftMenu", this)
        this.eventBus.registerListner("eventBoxClicked", this)
        this.eventBus.registerListner("playSound", this)
        this.eventBus.registerListner("startWalkingLoop", this)
        this.eventBus.registerListner("stopWalkingLoop", this)
        this.eventBus.registerListner("playerDead", this)
        this.eventBus.registerListner("respawn", this)

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

        this.playerInv = undefined
        this.craftMenu = undefined

        this.playerDead = false
        this.respawnMenu = new RespawnScreen(this)
    }

    addObject(object) {
        this.toAdd.push(object);
        console.log("added object to scene: " + object.constructor.name);
        if (object.constructor.name == "Player" && this.mainPlayerID == 0) {
            this.mainPlayerID = object.playerID
            this.eventBus.triggerEvent("playerSet", this.mainPlayerID)
            this.playerIndex = this.gameObjects.length + this.toAdd.length - 1
            console.log("Main Player ID: " + this.mainPlayerID + "  Player Index in Game objects: " + this.playerIndex)
            //console.log(this.gameObjects)
            this.camera.setLockedPlayer(object)
        }
    }

    removeObject(object) {
        this.toDelete.push(object)
        console.log("removed an object from scene: " + object.constructor.name)

    }

    render() {
        //console.log(this.gameObjects)
        if (this.playerDead){
            this.respawnMenu.render()
            return
        }
        this.map.render()

        this.camera.render()


        let len = this.gameObjects.length;
        for (let i = 0; i < len; i++) {
            //if (i != this.playerIndex && i!= this.tileMapIndex){
            if (this.gameObjects[i] === this.inv || this.gameObjects[i] === this.craftMenu) {
                continue
            }
            this.gameObjects[i].render();
            //}

        }

        if (this.playerInv != undefined) {
            this.playerInv.render()
        }

        if (this.craftMenu != undefined) {
            this.craftMenu.render()
        }

    }

    process() {
        if (this.playerDead){
            this.respawnMenu.process()
            return
        }
        let len = this.gameObjects.length
        for (let i = 0; i < len; i++) {
            this.gameObjects[i].process();
        }


        if (this.toDelete.length != 0) {
            this.gameObjects = this.gameObjects.filter(el =>
                this.toDelete.indexOf(el) < 0
            );
           // console.log(this.gameObjects)
            this.toDelete = [];

            const length = this.gameObjects.length
            for (let i = 0; i < length; i++) {
                if (this.gameObjects[i].constructor.name == "Player" && this.gameObjects[i].playerID == this.mainPlayerID) {
                    this.playerIndex = i
                }
            }
            //console.log(this.gameObjects)
        }

        let len_add = this.toAdd.length
        if (len_add != 0) {
            for (let i = 0; i < len_add; i++) {
                this.gameObjects.push(this.toAdd[i]);
            }
            this.toAdd = [];

            for (let i = 0; i < length; i++) {
                if (this.gameObjects[i].constructor.name == "Player" && this.gameObjects[i].playerID == this.mainPlayerID) {
                    this.playerIndex = i
                }
            }
        }

        this.camera.process()

    }

    setMainPlayerID(ID) {
        this.mainPlayerID = ID
    }

    event(eventString, eventObject) {
        if (eventString == "createInv") {
            this.playerInv = new Inventory(this)
            this.addObject(this.playerInv)
        }

        if (eventString == "createCraftMenu") {
            const recipes = [
                { name: "Wood", image: "wooden-stick.png", requires:"7 Sticks", produces: "3 Wood"},
                { name: "Stone Axe", image: "stone-axe.png" },
                { name: "Iron Sword", image: "iron-sword.png" },
            ];
            this.craftMenu = new CraftingMenu(this, 50, 50, recipes)
            this.addObject(this.craftMenu)
        }

        if (eventString == "keydown") {
            this.keys[eventObject.key] = eventObject.status;
        }

        if (eventString == "mouseDown") {
            if (this.mouseDown == false && eventObject.status == true) {
                this.eventBus.triggerEvent("mouseJustDown", { status: true })

            }

            this.mouseDown = eventObject.status
        }

        if (eventString == "deletedGameObject") {
            //console.log(eventObject)
            const length = this.gameObjects.length
            for (let i = 0; i <= length; i++) {
                if (this.gameObjects[i].ID === eventObject.ID) {
                    //console.log("OBJECT TO DELETE: ID: ", eventObject.ID, " Type: ", eventObject.type)
                    //console.log("OBJECT THAT IS DELETED: Typ: " + this.gameObjects[i].constructor.name)
                    this.removeObject(this.gameObjects[i])
                    //console.log(this.gameObjects[i])
                    break
                }
            }

        }

        if (eventString == "eventBoxClicked"){
            this.removeObject(eventObject.box)
        }

        if (eventString == "playSound"){
            this.audioHandler.play(eventObject)
        }

        if (eventObject == "startWalkingLoop"){
            this.audioHandler.loop(Walk)
        }

        if (eventObject == "stopWalkingLoop"){
            this.audioHandler.stopLoop()
        }

        if (eventString == "playerDead"){
            this.playerDead = true
            this.respawnMenu.respawnButton.unlockButton()
        }
        if (eventString == "respawn"){
            this.playerDead = false
            this.respawnMenu.respawnButton.lockButton()
        }
    }

}

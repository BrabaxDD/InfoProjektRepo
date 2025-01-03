import GameObject from "./GameObject.js"
import { hit } from "./game.js"
import { addTestInv } from "./game.js"
import Inventory from "./GUI_elements/Inventory.js"
import { font } from "./game.js"


export default class Player extends GameObject {
    constructor(x, y, width, height, color, speed, scene, playerID) {
        super(scene)
        this.posx = x
        this.posy = y
        this.width = width
        this.height = height
        this.color = color
        this.speed = speed
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")
        //this.keys = keys
        //this.scene.eventBus.registerListner("test", this)
        this.scene.eventBus.registerListner("position", this)
        this.scene.eventBus.registerListner("healthUpdate", this)
        this.up = false
        this.down = false
        this.left = false
        this.right = false
        this.playerID = playerID
        this.onCooldown = 0

        this.hp = null

        this.inventory = new Inventory(this.scene)
        this.scene.addObject(this.inventory)
    }

    process() {
        if (this.scene.keys['ArrowUp']) {
            this.up = true
            if (this.posy > 0) { }
            //this.posy -= this.speed; // Move up
        } else {
            this.up = false
        }


        if (this.scene.keys['ArrowDown']) {
            this.down = true
            if (this.posy < this.canvas.height - this.height) {
                //this.posy += this.speed; // Move down
            }
        } else {
            this.down = false
        }

        if (this.scene.keys['ArrowLeft']) {
            this.left = true
            if (this.posx > 0) {
                //this.posx -= this.speed; // Move left
            }
        } else { this.left = false }

        if (this.scene.keys['ArrowRight']) {
            this.right = true
            if (this.posx < this.canvas.width - this.width) {
                //this.posx += this.speed; // Move right
            }
        }
        else {
            this.right = false
        }

        if(this.scene.keys['h'] == true){
            if (this.onCooldown >= 10){
                hit()
                //addTestInv()
                this.onCooldown = 0
            }
            
            this.onCooldown ++
            
        }
    }

    render() {
        this.ctx.fillStyle = "blue";
        this.ctx.fillRect(this.posx, this.posy, this.width, this.height);

        
        this.ctx.font = font;
        this.ctx.fillStyle = 'black';
        this.ctx.textBaseline = 'left';
        
        this.ctx.fillText("Health: " + this.hp, 100 ,100);
    }
   event(eventString, eventObject) {
        if (eventString == "position" && eventObject.type == "Player" && eventObject.ID == this.playerID ) {
            this.posx = eventObject.posx
            this.posy = eventObject.posy
        }
        if(eventString == "healthUpdate" && eventObject.type == "Player" && eventObject.ID == this.playerID){
            console.log("HEALTH UUPDATATET" + eventObject.HP)
            console.log(eventObject)
            this.hp = eventObject.HP
        }
    }
}

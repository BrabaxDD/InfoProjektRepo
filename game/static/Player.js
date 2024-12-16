import GameObject from "./GameObject.js"


export default class Player extends GameObject {
    constructor(x, y, width, height, color, speed, keys, scene, playerID) {
        super(scene)
        this.posx = x
        this.posy = y
        this.width = width
        this.height = height
        this.color = color
        this.speed = speed
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")
        this.keys = keys
        //this.scene.eventBus.registerListner("test", this)
        this.scene.eventBus.registerListner("position", this)
        this.up = false
        this.down = false
        this.left = false
        this.right = false
        this.playerID = playerID
    }

    process() {
        if (this.keys['ArrowUp']) {
            this.up = true
            if (this.posy > 0) { }
            //this.posy -= this.speed; // Move up
        } else {
            this.up = false
        }


        if (this.keys['ArrowDown']) {
            this.down = true
            if (this.posy < this.canvas.height - this.height) {
                //this.posy += this.speed; // Move down
            }
        } else {
            this.down = false
        }

        if (this.keys['ArrowLeft']) {
            this.left = true
            if (this.posx > 0) {
                //this.posx -= this.speed; // Move left
            }
        } else { this.left = false }

        if (this.keys['ArrowRight']) {
            this.right = true
            if (this.posx < this.canvas.width - this.width) {
                //this.posx += this.speed; // Move right
            }
        }
        else {
            this.right = false
        }
    }

    render() {
        this.ctx.fillStyle = "blue";
        this.ctx.fillRect(this.posx, this.posy, this.width, this.height);
    }
   event(eventString, eventObject) {
        if (eventString == "position" && eventObject.type == "Player" && eventObject.ID == this.playerID) {
            this.posx = eventObject.posx
            this.posy = eventObject.posy
        }
    }
}

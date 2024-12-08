import GameObject from "./GameObject.js"


export default class Player extends GameObject {
    constructor(x, y, width, height, color, speed, keys, scene) {
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
        this.scene.eventBus.registerListner("test", this)
    }

    process() {
        if (this.keys['ArrowUp'] && this.posy > 0) {
            this.posy -= this.speed; // Move up
        }
        if (this.keys['ArrowDown'] && this.posy < this.canvas.height - this.height) {
            this.posy += this.speed; // Move down
        }
        if (this.keys['ArrowLeft'] && this.posx > 0) {
            this.posx -= this.speed; // Move left
        }
        if (this.keys['ArrowRight'] && this.posx < this.canvas.width - this.width) {
            this.posx += this.speed; // Move right
        }
    }

    render() {
        this.ctx.fillStyle = "blue";
        this.ctx.fillRect(this.posx, this.posy, this.width, this.height);
    }
   event(eventString, eventObject) {
        if (eventString == "test") {
            this.posx = 400
            this.posy = 400
        }
    }
}

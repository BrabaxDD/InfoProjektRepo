import GameObject from "./GameObject.js"

export default class Wall extends GameObject {
    constructor(scene, ID) {
        super(scene)
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")
        this.scene.eventBus.registerListner("position", this)
        this.scene.eventBus.registerListner("wallInformation", this)
        this.ID = ID
        this.posx = 0
        this.posy = 0
        this.posx2 = 0
        this.posy2 = 0
        this.thickness = 10
    }

    render() {
        this.ctx.fillStyle = "black";
        this.ctx.beginPath()
        this.ctx.moveTo(this.posx, this.posy)
        this.ctx.lineTo(this.posx2, this.posy2)
        this.ctx.strokeStyle = "black"
        this.ctx.lineWidth = this.thickness
        this.ctx.stroke()

    }

    process() { }

    event(eventString, eventObject) {
        if (eventString == "position" && eventObject.type == "Wall" && eventObject.ID == this.ID) {
            this.posx = eventObject.posx
            this.posy = eventObject.posy
        }
        if (eventString == "wallInformation") {
            if (eventObject.wallID == this.ID) {
                this.posx2 = eventObject.posx2
                this.posy2 = eventObject.posy2
                this.thickness = eventObject.thickness
            }
        }
    }
}
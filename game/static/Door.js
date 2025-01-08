import GameObject from "./GameObject.js"

export default class Door extends GameObject {
    constructor(scene, ID) {
        super(scene)
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")
        this.scene.eventBus.registerListner("position", this)
        this.ID = ID
        this.posx = 0
        this.posy = 0
        this.posx2 = 0
        this.posy2 = 0
        this.thickness = 10
    }

    render() {
        this.ctx.fillStyle = "brown";
        this.ctx.beginPath()
        this.ctx.moveTo(this.posx - (this.scene.camera.posx - this.scene.camera.cameraWidth/2), this.posy - (this.scene.camera.posy- this.scene.camera.cameraHeight/2))
        this.ctx.lineTo(this.posx2 - (this.scene.camera.posx - this.scene.camera.cameraWidth/2), this.posy2- (this.scene.camera.posy- this.scene.camera.cameraHeight/2))
        this.ctx.strokeStyle = "brown"
        this.ctx.lineWidth = this.thickness
        this.ctx.stroke()

    }

    process() { }

    event(eventString, eventObject) {
        if (eventString == "position" && eventObject.type == "Door" && eventObject.ID == this.ID) {
            this.posx = eventObject.posx
            this.posy = eventObject.posy
        }
    }
}

import GameObject from "./GameObject.js"
import { font } from "./game.js"

export default class Tree extends GameObject{
    constructor(scene, ID){
        super(scene)
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")
        this.scene.eventBus.registerListner("position", this)
        this.ID = ID
        this.posx = 0
        this.posy = 0
    }

    render(){
        this.ctx.fillStyle = "green";
        this.ctx.fillRect(this.posx - (this.scene.camera.posx - this.scene.camera.cameraWidth/2) , this.posy - (this.scene.camera.posy- this.scene.camera.cameraHeight/2), 10, 10);

        this.ctx.font = font;
        this.ctx.fillStyle = 'black';
        this.ctx.textBaseline = 'left';
        
    }

    process(){}

    event(eventString, eventObject){
        if (eventString == "position" && eventObject.type == "Tree" && eventObject.ID == this.ID) {
            this.posx = eventObject.posx
            this.posy = eventObject.posy
        }
    }
}
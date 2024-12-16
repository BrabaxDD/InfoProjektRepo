import GameObject from "./GameObject.js"

export default class Tree extends GameObject{
    constructor(scene){
        super(scene)
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")
        this.scene.eventBus.registerListner("position", this)
    }

    render(){
        this.ctx.fillStyle = "green";
        this.ctx.fillRect(this.posx, this.posy, 10, 10);
        
    }

    process(){}

    event(eventString, eventObject){
        if (eventString == "position" && eventObject.type == "Tree") {
            this.posx = eventObject.posx
            this.posy = eventObject.posy
        }
    }
}
import GameObject from "./GameObject.js"
export default class ButtonGameObject extends GameObject {
    constructor(posx, posy, widthButton, heightButton, eventString, scene) {
        super(scene)
        this.posx = posx
        this.posy = posy
        this.widhtButton = widthButton
        this.heightButton = heightButton
        this.eventString = eventString
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")
    }
    process() {
        if (this.scene.mousex >  this.posx && this.scene.mousex < this.posx + this.widhtButton && 
            this.scene.mousey >  this.posy && this.scene.mousey < this.posy + this.heightButton){
            this.scene.eventBus.triggerEvent("test",null)
        } 


    }
    render() {
        this.ctx.fillStyle = "blue";
        this.ctx.fillRect(this.posx,this.posy,this.widhtButton,this.heightButton)
    }



}

import GameObject from "../GameObject.js"

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
        this.scene.eventBus.registerListner("click_on_canvas", this)
        this.is_hovered = false
    }
    process() {
        if (this.scene.mousex >  this.posx && this.scene.mousex < this.posx + this.widhtButton && 
            this.scene.mousey >  this.posy && this.scene.mousey < this.posy + this.heightButton){
            this.is_hovered = true
            
        } 
        else{
            this.is_hovered = false
        }


    }
    render() {
        this.ctx.fillStyle = "blue";
        if (this.is_hovered == true){
            this.ctx.fillStyle = "red"
        }
        this.ctx.fillRect(this.posx,this.posy,this.widhtButton,this.heightButton)
    }

    buttonPresed(){
        this.scene.eventBus.triggerEvent("test",null)
    }

    event(eventString, eventObject){
        if (eventString == "click_on_canvas" && this.is_hovered == true) {
            this.buttonPresed()
        }
    }

}

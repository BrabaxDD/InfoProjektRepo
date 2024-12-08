import GameObject from "../GameObject.js"

export default class ButtonGameObject extends GameObject {
    constructor(posx, posy, widthButton, heightButton, eventString, scene, text) {
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
        this.text = text
        this.textSize = 60
        this.textColor = "black"
        text.ButtonPrimaryColor = "green"
        

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
        this.ctx.fillStyle = this.ButtonPrimaryColor;
        if (this.is_hovered == true){
            this.ctx.fillStyle = this.ButtonScondaryColor
        }
        this.ctx.fillRect(this.posx,this.posy,this.widhtButton,this.heightButton)

        this.ctx.fillStyle = this.textColor;
        this.ctx.strokeStyle = this.textColor;
        this.ctx.font = this.textSize;
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        
        this.ctx.fillText(this.text, this.posx+(this.widhtButton / 2), this.posy+(this.heightButton / 2));
        //this.ctx.strokeText(text, this.posx+(this.widhtButton / 2), this.posy+(this.heightButton / 2));
    }

    buttonPresed(){
        this.scene.eventBus.triggerEvent("test",null)
    }

    event(eventString, eventObject){
        if (eventString == "click_on_canvas" && this.is_hovered == true) {
            this.buttonPresed()
        }
    }

    setTextSize(size){
        this.text
    }

    setTextColor(color){
        this.textColor = color
    }

    setButtonColorPrimary(color){
        this.ButtonPrimaryColor = color
    }

    setButtonColorSecondary(color){
        this.ButtonScondaryColor
    }

}

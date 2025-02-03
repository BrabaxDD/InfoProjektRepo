import { settings } from "../game.js";
import GameObject from "../GameObject.js";

export default class AlertBox extends GameObject{
    constructor(scene, posx, posy, widt, heig, text){
        super(scene)

        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")
        
        this.scene.eventBus.registerListner("click_on_canvas", this)

        this.posx = posx
        this.posy = posy

        this.widthBox = widt
        this.heightBox = heig

        this.text = text
    }

    process(){
        if (this.scene.mousex > this.posx && this.scene.mousex < this.posx + this.widthBox &&
            this.scene.mousey > this.posy && this.scene.mousey < this.posy + this.heightBox) {
            this.isHovered = true

        }
        else {
            this.isHovered = false
        }
    }

    render(){
        this.ctx.fillStyle = settings.alertColor;
        this.ctx.globalAlpha = 1;
        this.ctx.fillRect(this.posx, this.posy, this.widthBox, this.heightBox);
        this.ctx.fillStyle = "black";
        this.ctx.lineWidth = 5
        this.ctx.strokeRect(this.posx, this.posy, this.widthBox, this.heightBox);

        this.ctx.fillStyle = "black";
        this.ctx.textBaseline = 'middle';
        this.ctx.font = settings.font;
        this.ctx.fillText(this.text, this.posx + this.widthBox/2 , this.posy + this.heightBox/2);
    }

    event(eventString, eventObject){
        if (eventString == "click_on_canvas"){
            if(this.isHovered){
                 this.scene.eventBus.triggerEvent("eventBoxClicked", {box:this})
            }
        }
    }
}
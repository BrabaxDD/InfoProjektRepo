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

        this.lineheight = settings.textLineHeight

        this.text = this.updateWidth(text, widt - 20)
        this.textHeigt = this.calculateHeight()
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
        for (var i = 0; i<this.text.length; i++)
            this.ctx.fillText(this.text[i], this.posx + (this.widthBox-20)/2, this.posy+ this.heightBox/2+ (i*this.lineheight) );
    }

    event(eventString, eventObject){
        if (eventString == "click_on_canvas"){
            if(this.isHovered){
                 this.scene.eventBus.triggerEvent("eventBoxClicked", {box:this})
                 this.scene.eventBus.triggerEvent("buttonPressed")
            }
        }
    }

    updateWidth(str, maxWidth) {
        
        let result = '';
        let currentLine = '';
        
        for (let word of str.split(' ')) {
            let testLine = currentLine.length > 0 ? currentLine + ' ' + word : word;
            let textWidth = this.ctx.measureText(testLine).width;
            
            if (textWidth > maxWidth) {
                result += (result.length > 0 ? '\n' : '') + currentLine;
                currentLine = word;
            } else {
                currentLine = testLine;
            }
        }
        
        result += (result.length > 0 ? '\n' : '') + currentLine;
        console.log(result)
        return result.split('\n');
    }

    calculateHeight(){
        return this.text.length * this.lineheight
    }
}
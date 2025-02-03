import { settings } from "../game.js";
import GameObject from "../GameObject.js";

export default class TextBox extends GameObject {
    constructor(scene, x, y, maxWidth, text) {
        super(scene)

        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")
        this.scene.eventBus.registerListner("position", this)

        this.textColor = settings.textBoxColor
        this.posx = x
        this.posy = y
        this.maxWidth = maxWidth
        this.lineheight = settings.textLineHeight
        this.text = this.updateWidth(text, maxWidth)
        this.textHeigt = this.calculateHeight()
    }

    render() {
        this.ctx.fillStyle = this.textColor;
        this.ctx.textBaseline = 'middle';
        this.ctx.font = settings.font;

        for (var i = 0; i<this.text.length; i++)
            this.ctx.fillText(this.text[i], this.posx + this.maxWidth/2, this.posy + (i*this.lineheight) );
    }

    process() {}

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
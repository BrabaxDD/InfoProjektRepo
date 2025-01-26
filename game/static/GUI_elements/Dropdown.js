
import { font } from "../game.js"
import GameObject from "../GameObject.js"


export default class Dropdown extends GameObject {
    constructor(scene, options, x, y, widthDropdown, heightDropdown, defaultText) {
        super(scene)
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")

        this.scene.eventBus.registerListner("click_on_canvas", this)
        this.scene.eventBus.registerListner("runningServers", this)
        this.scene.eventBus.registerListner("wheel", this)


        this.options = options; 
        this.defaultText = defaultText
        this.posx = x; 
        this.posy = y; 
        this.widthDrop = widthDropdown
        this.heightDrop = heightDropdown; 
        this.isOpen = false; 
        this.selectedIndex = -1; 

        this.offsetY = 0

    }

    // draw the dropdown menu
    render() {
        // draw main dropdown button
        this.ctx.fillStyle = "#f0f0ff";
        this.ctx.fillRect(this.posx, this.posy, this.widthDrop, this.heightDrop);
        this.ctx.strokeStyle = "#000";
        this.ctx.strokeRect(this.posx, this.posy, this.widthDrop, this.heightDrop);

        this.ctx.fillStyle = "#000";
        this.ctx.font = font;
        this.ctx.textBaseline = "middle";

        const text = this.selectedIndex >= 0 ? this.options[this.selectedIndex] : this.defaultText;
        this.ctx.fillText(text, this.posx + this.widthDrop / 2, this.posy + this.heightDrop / 2);

        if (this.isOpen) {
            // draw dropdown options
            for (let i = 0; i < this.options.length; i++) {
                const optiony = this.posy + (i + 1) * this.heightDrop + this.offsetY;
                if (optiony >= this.posy + this.heightDrop) {
                    //highlight hovered button
                    if (this.scene.mousex >= this.posx &&
                        this.scene.mousex <= this.posx + this.widthDrop &&
                        this.scene.mousey >= optiony &&
                        this.scene.mousey <= optiony + this.heightDrop) {
                        this.ctx.fillStyle = "#f0f0ff"
                    }
                    else {
                        this.ctx.fillStyle = "#f0f0f0"
                    }
                    this.ctx.fillRect(this.posx, optiony, this.widthDrop, this.heightDrop);
                    this.ctx.strokeStyle = "#000";
                    this.ctx.strokeRect(this.posx, optiony, this.widthDrop, this.heightDrop);
                    this.ctx.fillStyle = "#000";
                    this.ctx.fillText(this.options[i], this.posx + this.widthDrop / 2, optiony + this.heightDrop / 2);
                }
            }
        }
    }

    process() { }

    // handle click events
    event(eventString, eventObject) {
        if (eventString == "runningServers") {
            this.options = eventObject
        }

        if (eventString == "wheel") {
            if (!this.isOpen) {
                return
            }
            if (eventObject < 40) {
                if (this.offsetY * (-1) < this.heightDrop * this.options.length - this.heightDrop * 2) {
                    this.offsetY -= this.heightDrop / 2
                }
            }
            else if (eventObject >= 40) {
                if (this.offsetY < 0) {
                    this.offsetY += this.heightDrop / 2
                }
            }
        }

        if (eventString == "click_on_canvas") {
            const mousex = this.scene.mousex
            const mouseY = this.scene.mousey

            if (this.isOpen) {
                // Check if an option was clicked
                for (let i = 0; i < this.options.length; i++) {
                    const optionY = this.posy + (i + 1) * this.heightDrop + this.offsetY;
                    if (optionY > this.posy + this.heightDrop &&
                        mousex >= this.posx &&
                        mousex <= this.posx + this.widthDrop &&
                        mouseY >= optionY &&
                        mouseY <= optionY + this.heightDrop) {
                        this.selectedIndex = i;
                        console.log(`Option selected: ${this.options[i]}`);
                        this.scene.eventBus.triggerEvent("optionSelected", this.options[i])
                        break;
                    }
                }
                this.isOpen = false;
            } else {
                // Toggle dropdown if main button clicked
                if (
                    this.scene.mousex > this.posx && this.scene.mousex < this.posx + this.widthDrop &&
                    this.scene.mousey > this.posy && this.scene.mousey < this.posy + this.heightDrop

                ) {
                    this.isOpen = true;
                    console.log("THTHAAHT")
                }
            }


        }
    }

}
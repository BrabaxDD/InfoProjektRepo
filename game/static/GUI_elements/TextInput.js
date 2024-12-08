import GameObject from "../GameObject.js";

export default class CanvasTextInput extends GameObject{
    constructor(scene) {
        super(scene)
        this.canvas = this.scene.canvas;
        this.ctx = this.canvas.getContext('2d');
        this.inputText = ''; 
        this.isFocused = false;
        this.storedText = null; 
        
        this.posx = 100
        this.posy = 50
        this.widthBox = 200
        this.heightBox = 30;

        this.scene.eventBus.registerListner("click_on_canvas",this)
        
        window.addEventListener('keydown', (e) => this.handleKeyDown(e));
    }

    
    event(eventString, eventObject) {
        if (eventString == "click_on_canvas"){
            this.isFocused = true;
            console.log("CKUCJE")
            if (this.scene.mousex >  this.posx && this.scene.mousex < this.posx + this.widthBox && 
                this.scene.mousey >  this.posy && this.scene.mousey < this.posy + this.heightBox){
                this.isFocused = true;
                
            } 
            else{
                this.isFocused = false;
            }
        }
        
    }

    process(){
        
    }

    handleKeyDown(event) {
        if (!this.isFocused) return;

        if (event.key === 'Enter') {
            this.storedText = this.inputText; 
            console.log('Stored Text:', this.storedText);
            this.inputText = ''; 
        } else if (event.key === 'Backspace') {
            this.inputText = this.inputText.slice(0, -1); 
        } else if (event.key.length === 1) {
            this.inputText += event.key; 
        }
        this.render();
    }

   
    render() {
       
        this.ctx.strokeStyle = this.isFocused ? 'blue' : 'black';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(this.posx, this.posy, this.widthBox, this.heightBox);
        

        this.ctx.font = '16px Arial';
        this.ctx.fillStyle = 'black';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(this.inputText, this.posx + (this.widthBox/2), this.posy + (this.heightBox / 2));

        // Optional: Draw stored text for debugging
        if (this.storedText !== null) {
            this.ctx.fillStyle = 'gray';
            this.ctx.fillText(`Stored: ${this.storedText}`, this.posx, this.posy + this.heightBox + 20);
        }
    }
}


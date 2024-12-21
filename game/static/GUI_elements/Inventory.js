import GameObject from "../GameObject.js"
import { font } from "../game.js"
import InventorySlot from "./InventorySlot.js"

export default class Inventory extends GameObject{
    constructor(scene){
        super(scene)
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")

        this.content = [{itemID:"Stick",size:3,tags:{}}, {itemID:2, size:5, tags:{}}] //All item stacks
        this.scene.eventBus.registerListner("inventory",this)
        this.scene.eventBus.registerListner("mouseJustDown",this)
        //this.scene.eventBus.registerListner("click_on_canvas",this)

        this.isVisible = false

        this.imageLoader = this.scene.imageLoader

        

        this.invWidth = 400
        this.invHeight = 200
        this.borderWidth = 10
        this.bufferSize = 10
        this.textBoderSize = 40

        this.posx = 0
        this.posy = 0 + this.textBoderSize

        this.imageLoader.load(
            "blankItem.png",
            (image) => {
                this.dummyItem = image
            },
            (error) => {
                console.error(`Error loading tile image: ${fileName}`, error);
            }
        );

        this.textSize = font
        
        this.imageSize = 64

        this.isHovered = false

        this.atackPosx = 0
        this.atackPosy = 0
        this.buttons = []
        this.isALLInizialised = false
        this.initializeImages()

        

    }


    async initializeImages() {
        this.imagesIndex = {
            Stick: "stick.png"
        };
    
        this.images =  await this.loadAllImages(this.imagesIndex)
        console.log(this.images)
        this.updateButtons()
        console.log(this.images);
         
    }

    async loadAllImages(imagesIndex) {
        const images = {};
        const keys = Object.keys(imagesIndex);
    
        const loadPromises = keys.map(key => {
            return new Promise((resolve, reject) => {
                this.imageLoader.load(
                    imagesIndex[key],
                    (image) => {
                        images[key] = image;
                        resolve(); // Resolve this image's loading
                    },
                    (error) => {
                        console.error(`Error loading image: ${imagesIndex[key]}`, error);
                        reject(error); // Reject if there is an error
                    }
                );
            });
        });
    
        // Wait for all the images to be loaded
        await Promise.all(loadPromises);
    
        console.log(images);
    
        return images
    }
    

    event(eventString, eventObject){
        if (eventString == "inventory"){
            console.log("eventObject: " + eventObject.items)
            this.content = eventObject.items
        }
        if (eventString == "mouseJustDown"){
            this.mouseJustDown = true
        }
    }

    updateButtons(){
        this.buttons = []
        let len = this.content.length
        for (let i = 0; i<len; i++){
            let image = this.dummyItem

            let c = this.content[i].itemID; // Get the item ID
            if (this.images[c]) {
                image = this.images[c];
            }
            this.buttons.push(new InventorySlot(this.scene, this.posx,this.posy, this.imageSize, image, this.content[i]))
        }
    }

    processButtons(){
        let len = this.buttons.length
        for (let i = 0; i<len; i++){
            this.buttons[i].posx = this.posx + (i * this.imageSize) + this.bufferSize*i + this.borderWidth
            this.buttons[i].posy = this.posy + this.borderWidth
        }
    }

    printInventory(){
        let leng = this.content.length
        for (let i = 0; i<= leng; i++){
            console.log(this.content[i])
        }
    }

    areButtonsHovered(){
        let is = false
        let len = this.buttons.length
        for (let i = 0; i<len; i++){
            if (this.buttons[i].isHovered){
                is = true
            }
        }
        return is
    }

    render(){
        if (this.isVisible){
            if (!this.isHovered){
                this.ctx.fillStyle = "green";
            }
            else{
                this.ctx.fillStyle = "yellow"
            }
            this.ctx.globalAlpha = 0.4;
            this.ctx.fillRect(this.posx, this.posy, this.invWidth, this.invHeight);
            this.ctx.globalAlpha = 1;
            this.ctx.fillStyle = "red";
            this.ctx.globalAlpha = 0.4;
            this.ctx.fillRect(this.posx, this.posy-this.textBoderSize, this.invWidth, this.textBoderSize);
            this.ctx.globalAlpha = 1;
            this.ctx.font = this.textSize;
            this.ctx.fillStyle = 'black';
            this.ctx.textBaseline = 'middle';
            
            this.ctx.fillText("Inventory",this.posx + this.invWidth/2,this.posy-15);

            let len = this.buttons.length
            for (let i = 0; i<len; i++){
                this.buttons[i].render()    
            }
        }
    }

    process(){
        //In the are of the 
        if (this.isVisible && this.scene.mousex >  this.posx && this.scene.mousex < this.posx + this.invWidth && 
            this.scene.mousey >  this.posy - this.textBoderSize && this.scene.mousey < this.posy + this.invHeight && !this.areButtonsHovered()){
            this.isHovered = true
            
        } 

        if(this.mouseJustDown){
            this.atackPosx = this.scene.mousex-this.posx
            this.atackPosy = this.scene.mousey-this.posy
            this.mouseJustDown = false
        }

        if (this.isHovered && this.scene.mouseDown){
                this.posx = this.scene.mousex - this.atackPosx
                this.posy = this.scene.mousey - this.atackPosy
        }

        else{
            this.isHovered = false
        }
        if (this.scene.keys["e"] == true){
            this.isVisible = true
        }
        else{
            this.isVisible = false
        }
        if(this.isVisible){
            this.processButtons()
            let len = this.buttons.length
            for (let i = 0; i<len; i++){
                this.buttons[i].process()    
            }
        }
    }

}
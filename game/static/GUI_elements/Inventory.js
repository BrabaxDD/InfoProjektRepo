import GameObject from "../GameObject.js"
import { font } from "../game.js"

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

        this.posx = 0
        this.posy = 0

        this.invWidth = 400
        this.invHeight = 200
        this.borderWidth = 10
        this.bufferSize = 10

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

        this.initializeImages()

        this.images = this.loadAllImages(this.imagesIndex)

        console.log(this.imagesIndex)

    }

    async initializeImages() {
        this.imagesIndex = {
            Stick: "stick.png"
        };
    
        this.images = await this.loadAllImages(this.imagesIndex); // Wait for images to load
        console.log("Images loaded:", this.images);
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
    
        console.log(images); // Log all loaded images
        console.log("images Stick:", images.Stick);
    
        return images; // Return the loaded images object
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

    printInventory(){
        let leng = this.content.length
        for (let i = 0; i<= leng; i++){
            console.log(this.content[i])
        }
    }

    render(){
        if (this.isVisible){
            this.ctx.fillStyle = "green";
            this.ctx.fillRect(this.posx, this.posy, this.invWidth, this.invHeight);
            this.ctx.font = this.textSize;
            this.ctx.fillStyle = 'black';
            this.ctx.textBaseline = 'middle';

            let len = this.content.length
            for (let i = 0; i<len; i++){
                let image = this.dummyItem
                
                try{
                    let c = this.content[i].itemID; // Get the item ID
                    if (this.images[c]) {
                        image = this.images[c];
                    }
                }
                catch(error){
                }
                this.ctx.drawImage(
                    image,
                    this.posx + (i * this.imageSize) + this.bufferSize*i + this.borderWidth,
                    this.posy + this.borderWidth,
                    this.imageSize,
                    this.imageSize
                );
                this.ctx.fillStyle = 'yellow';
                this.ctx.textBaseline = 'left';
                this.ctx.font = this.textSize*3;
                this.ctx.fillText(this.content[i].size, this.borderWidth + this.posx + (this.imageSize * (i+1)+ (i*this.bufferSize))-5, this.posy + this.borderWidth + this.imageSize);
            }
        }
    }

    process(){
        if (this.isVisible && this.scene.mousex >  this.posx && this.scene.mousex < this.posx + this.invWidth && 
            this.scene.mousey >  this.posy && this.scene.mousey < this.posy + this.invHeight){
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
    }

}
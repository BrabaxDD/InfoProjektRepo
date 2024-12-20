import GameObject from "../GameObject.js"

export default class Inventory extends GameObject{
    constructor(scene){
        super(scene)
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")

        this.content = [{itemID:1,size:3,tags:{}}, {itemID:2, size:5, tags:{}}] //All item stacks
        this.scene.eventBus.registerListner("inventory",this)
        //this.scene.eventBus.registerListner("click_on_canvas",this)

        this.isVisible = false

        this.imageLoader = this.scene.imageLoader

        this.posx = 0
        this.posy = 0

        this.invWidth = 400
        this.invHeight = 200

        this.imageLoader.load(
            "blankItem.png",

            (image) => {
                // Draw the image once it's loaded
                this.dummyItem = image
            },
            (error) => {
                console.error(`Error loading tile image: ${fileName}`, error);
            }
        );

        this.isHovered = false
    }

    event(eventString, eventObject){
        if (eventString == "inventory"){
            console.log("eventObject: " + eventObject.items)
            this.content = eventObject.items
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
            this.ctx.fillText(this.content, this.posx + (this.invWidth/2), this.posy + (this.invHeight / 2));
            let len = this.content.length
            for (let i = 0; i<len; i++){
                this.ctx.drawImage(
                    this.dummyItem,
                    this.posx + i * 32,
                    this.posy + 32,
                    32,
                    32
                );
                this.ctx.fillStyle = 'yellow';
                this.ctx.textBaseline = 'left';
                this.ctx.font = this.textSize*3;
                this.ctx.fillText(this.content[i].size, this.posx + 30 * (i+1), this.posy + 100 + 60);
            }
        }
    }

    process(){
        if (this.isVisible && this.scene.mousex >  this.posx && this.scene.mousex < this.posx + this.invWidth && 
            this.scene.mousey >  this.posy && this.scene.mousey < this.posy + this.invHeight){
            this.isHovered = true
            
        } 

        if (this.isHovered && this.scene.mouseDown){
                this.posx = this.scene.mousex - this.invWidth/2
                this.posy = this.scene.mousey - this.invHeight/2
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
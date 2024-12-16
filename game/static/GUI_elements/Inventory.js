import GameObject from "../GameObject.js"

export default class Inventory extends GameObject{
    constructor(scene){
        super(scene)
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")

        this.content = []//[{itemID:1,size:3,tags:{}}, {itemID:2, size:5, tags:{}}] //All item stacks
        this.scene.eventBus.registerListner("inventory",this)

        this.isVisible = false

        this.imageLoader = this.scene.imageLoader

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
    }

    event(eventString, eventObject){
        if (eventString == "inventory"){
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
            this.ctx.fillRect(0, 100, 400, 200);
            this.ctx.font = this.textSize;
            this.ctx.fillStyle = 'black';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(this.content, 0 + (400/2), 100 + (200 / 2));
            let len = this.content.length
            for (let i = 0; i<len; i++){
                this.ctx.drawImage(
                    this.dummyItem,
                    i * 32,
                    100 + 32,
                    32,
                    32
                );
                this.ctx.fillStyle = 'yellow';
                this.ctx.textBaseline = 'left';
                this.ctx.font = this.textSize*3;
                this.ctx.fillText(this.content[i].size, 30 * (i+1), 100 + 60);
            }
        }
    }

    process(){
        if (this.scene.keys["e"] == true){
            this.isVisible = true
        }
        else{
            this.isVisible = false
        }
    }

}
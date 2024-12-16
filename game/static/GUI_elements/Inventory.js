import GameObject from "../GameObject.js"

export default class Inventory extends GameObject{
    constructor(scene){
        super(scene)
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")

        this.content = ["HALLo", "GAWADo"] //All item stacks
        this.scene.eventBus.registerListner("inventory",this)

        this.isVisible = false
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
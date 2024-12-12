import GameObject from "../GameObject.js"

export default class Inventory extends GameObject{
    constructor(scene){
        super(scene)
        this.content = {} //All item stacks
        this.scene.eventBus.registerListener("inventory",this)
    }

    event(eventString, eventObject){
        if (eventString == "inventory"){
            this.content = eventObject.items
        }
    }

}
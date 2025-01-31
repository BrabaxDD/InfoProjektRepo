import GameObject from "./GameObject.js";
import AlertBox from "./GUI_elements/AlertBox.js";

export default class ErrorHandler extends GameObject{
    constructor(scene){
        super(scene)
        
        this.scene.eventBus.registerListner("alert", this)
        this.scene.eventBus.registerListner("error", this)
    }

    event(eventString, eventObject){
        if (eventString == "alert"){
            let b = new AlertBox(this.scene, this.scene.canvas.width/2 - 200 , this.scene.canvas.height/2 - 100 , 400, 200, eventObject.text)
            this.scene.addObject(b)
        }

    }

}
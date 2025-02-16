import { settings } from "../game.js";
import GameObject from "../GameObject.js";
import ButtonGameObject from "./Button.js";
import TextBox from "./TextBox.js";

export default class RespawnScreen extends GameObject{
    constructor(scene){
        super(scene)

        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")

        this.textBox = new TextBox(this.scene,this.canvas.width/2,this.canvas/3,this.canvas.width/3, "YOU DIED")

        this.respawnButton = new ButtonGameObject(this.canvas.width/2, this.canvas.height/3*2, 200,56, "respawn", {}, this.scene, "RESPAWN")
    }

    process(){
        this.textBox.process()
        this.respawnButton.process()
    }

    render(){
        this.ctx.fillStyle = settings.respawnScreenColor;
        this.ctx.globalAlpha = 0.9;
        this.ctx.fillRect(0,0, this.canvas.width, this.canvas.height);
        this.ctx.globalAlpha = 1;
        this.ctx.fillStyle = "black";
        
        this.textBox.render()
        this.respawnButton.render()
    }
}
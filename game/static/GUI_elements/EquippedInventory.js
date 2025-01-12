import GameObject from "../GameObject.js"
import { font } from "../game.js"
import { sendCombineStacksRequest } from "../game.js"
import InventorySlot from "./InventorySlot.js"
import { addTestInv } from "../game.js"
import ButtonGameObject from "./Button.js"
import { sendCraftingRequest } from "../game.js"

export default class EquippedInventory extends GameObject {
    constructor(scene, posx, posy) {
        super(scene)

        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")

        this.posx = posx
        this.posy = posy
        this.invWidth = 100
        this.invHeight = 100
    }

    render() {
        this.ctx.globalAlpha = 0.4;
        this.ctx.fillRect(this.posx, this.posy, this.invWidth, this.invHeight);
        this.ctx.globalAlpha = 1;


    }

    process() {

    }

}

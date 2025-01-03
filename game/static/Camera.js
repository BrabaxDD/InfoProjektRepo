import GameObject from "./GameObject.js"

export default class Camera extends GameObject{
    constructor(scene){
        super(scene)

        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")

        this.posx = this.canvas.width/2
        this.posy = this.canvas.height/2

        this.lockedPlayer = null
    }

    setLockedPlayer(player){
        this.lockedPlayer = player
    }

    process(){
        if (this.lockedPlayer != null){
            this.posx = this.lockedPlayer.posx
            this.posy = this.lockedPlayer.posy
        }
    }
    
    render(){
        this.ctx.globalAlpha = 0.4;
        this.ctx.fillRect(this.posx+5, this.posy+5, 10,10);
        this.ctx.globalAlpha = 1;
    }
}
import GameObject from "../GameObject.js";

export default class extends GameObject{
    constructor(scene, tileSize){
        super(scene)
        this.tileSize = tileSize
        this.scene = scene
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")

        this.wall = this.#image("Wand.png")
        console.log("Tile Map initialized")

        this.map = [
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
          ];
    }

    #image(fileName) {
        const img = new Image();
        img.src = `/images/${fileName}`;
        return img;
      }

    // 0 - Wand

    

    process(){
    console.log("Is Here")
    }

    render(){
        let length = this.map.length
        for (let row = 0; row < length; row++) {
            let width = this.map[row].length
            for (let column = 0; column < width; column++) {
                const tile = this.map[row][column];
                let image = null;
                switch (tile) {
                    case 0:
                        image = this.wall;
                        break;
                    
                    }

                if (image != null)
                    this.ctx.drawImage(
                    image,
                    column * this.tileSize,
                    row * this.tileSize,
                    this.tileSize,
                    this.tileSize
                );
            }
        }  
    }
}
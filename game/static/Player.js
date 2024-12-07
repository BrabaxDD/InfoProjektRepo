export default class Player {
    constructor(x, y, width,height, color, speed, canvas, keys) {
      this.posx = x
      this.posy = y
      this.width = width
      this.height = height
      this.color = color
      this.speed = speed
      this.canvas = canvas
      this.ctx = this.canvas.getContext("2d")
      this.keys = keys
    }

    process() {
        if (this.keys['ArrowUp'] && this.posy > 0) {
            this.posy -= this.speed; // Move up
        }
        if (this.keys['ArrowDown'] && this.posy < this.canvas.height - this.height) {
            this.posy += this.speed; // Move down
        }
        if (this.keys['ArrowLeft'] && this.posx > 0) {
            this.posx -= this.speed; // Move left
        }
        if (this.keys['ArrowRight'] && this.posx < this.canvas.width - this.width) {
            this.posx += this.speed; // Move right
        }
    }

    render() {
        this.ctx.fillStyle = "blue";
        this.ctx.fillRect(this.posx, this.posy, this.width, this.height);
    }
    
  }

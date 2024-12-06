export default class Player {
    constructor(x, y, width,height, color, speed, canvas, keys) {
      this.yPos = x
      this.yPos = y
      this.width = width
      this.height = height
      this.color = color
      this.speed = speed
      this.canvas = canvas
      this.ctx = this.canvas.getContext("2d")
      this.keys = keys
    }

    process() {
        if (this.keys['ArrowUp'] && this.y > 0) {
            this.y -= this.speed; // Move up
        }
        if (this.keys['ArrowDown'] && this.y < this.canvas.height - this.height) {
            this.y += this.speed; // Move down
        }
        if (this.keys['ArrowLeft'] && this.x > 0) {
            this.x -= this.speed; // Move left
        }
        if (this.keys['ArrowRight'] && this.x < this.canvas.width - this.width) {
            this.x += this.speed; // Move right
        }
    }

    render() {
        this.ctx.fillStyle = "blue";
        this.ctx.fillRect(this.x, this.y, this.width, this.height);
    }
    
  }
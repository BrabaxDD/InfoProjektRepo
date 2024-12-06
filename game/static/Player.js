export default class Player {
    constructor(x, y, width,height, color, speed, canvas) {
      this.yPos = x
      this.yPos = y
      this.width = width
      this.height = height
      this.color = color
      this.speed = speed
      this.canvas = canvas
    }

    moveCharacter(keys) {
        if (keys['ArrowUp'] && this.y > 0) {
            this.y -= this.speed; // Move up
        }
        if (keys['ArrowDown'] && this.y < this.canvas.height - this.height) {
            this.y += this.speed; // Move down
        }
        if (keys['ArrowLeft'] && this.x > 0) {
            this.x -= this.speed; // Move left
        }
        if (keys['ArrowRight'] && this.x < this.canvas.width - this.width) {
            this.x += this.speed; // Move right
        }
    }

    drawCharacter(ctx) {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }
    
  }
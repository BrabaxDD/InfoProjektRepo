import EventBus from "./EventBus.js"


export default class Scene {
    constructor(canvasObjectScene) {
        this.eventBus = new EventBus()
        this.gameObjects = []
        this.toAdd = []
        this.toDelete = []
        this.mousex = 0
        this.mousey = 0
        this.canvas = canvasObjectScene
        this.canvas.addEventListener('mousemove', (event) => {
            // Get the bounding rectangle of the canvas
            const rect = this.canvas.getBoundingClientRect();

            // Calculate mouse position relative to the canvas
            this.mousex = event.clientX - rect.left;
            this.mousey = event.clientY - rect.top;
        });



    }

    addObject(object) {
        this.toAdd.push(object);
        console.log("objekt zu sap hinzugeügt: " + object);
    }

    render() {
        let len = this.gameObjects.length;
        for (let i = 0; i < len; i++) {
            this.gameObjects[i].render();
        }
    }

    process() {
        let len = this.gameObjects.length
        for (let i = 0; i < len; i++) {
            this.gameObjects[i].process();
        }


        if (this.toDelete.length != 0) {
            this.gameObjects = this.gameObjects.filter(function(el) {
                return toDelete.indexOf(el) < 0;
            });
            this.toDelete = [];
        }

        let len_add = this.toAdd.length
        if (len_add != 0) {
            for (let i = 0; i < len_add; i++) {
                this.gameObjects.push(this.toAdd[i]);
            }
            this.toAdd = [];
        }

    }
}

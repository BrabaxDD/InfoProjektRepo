import GameObject from "../GameObject.js"
import { font } from "../game.js"
import { sendCombineStacksRequest } from "../game.js"
import InventorySlot from "./InventorySlot.js"
import { addTestInv } from "../game.js"
import ButtonGameObject from "./Button.js"

export default class Inventory extends GameObject {
    constructor(scene) {
        super(scene)
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")

        this.content = [{ "size": 99, "itemID": "Stick", "tags": [] }, { itemID: "Stick", size: 3, tags: {} }, { itemID: 2, size: 5, tags: {} }, { itemID: "Stick", size: 5, tags: {} }, { itemID: "Stick", size: 8, tags: {} }, { "size": 99, "itemID": "Stick", "tags": [] }, { itemID: "Stick", size: 3, tags: {} }, { itemID: 2, size: 5, tags: {} }, { itemID: "Stick", size: 5, tags: {} }, { itemID: "Stick", size: 8, tags: {} }] //All item stacks
        this.scene.eventBus.registerListner("inventory", this)
        this.scene.eventBus.registerListner("combineStacks", this)
        this.scene.eventBus.registerListner("selectAll", this)
        this.scene.eventBus.registerListner("splitStack", this)
        this.scene.eventBus.registerListner("mouseJustDown", this)
        //this.scene.eventBus.registerListner("click_on_canvas",this)

        this.isVisible = false

        this.imageLoader = this.scene.imageLoader

        this.imageLoader.load(
            "blankItem.png",
            (image) => {
                this.dummyItem = image
            },
            (error) => {
                console.error(`Error loading tile image: ${fileName}`, error);
            }
        );

        this.textSize = font

        this.imageSize = 64


        this.borderWidth = 15
        this.bufferSize = 10
        this.textBoderSize = 40
        this.widthInSLots = 5
        this.updateDimensions(this.widthInSLots)

        this.posx = 0
        this.posy = 0 + this.textBoderSize

        this.isHovered = false

        this.atackPosx = 0
        this.atackPosy = 0
        this.buttons = []
        this.isALLInizialised = false
        this.initializeImages()

        this.combineSelectedButton = new ButtonGameObject(this.posx, this.posy + this.invHeight, this.invWidth, 40, "combineStacks", {}, this.scene, "COMBINE SELECTED")
        this.selectAllButton = new ButtonGameObject(this.posx, this.posy + this.invHeight + 40, this.invWidth, 40, "selectAll", {}, this.scene, "ALL")
        this.splitButton = new ButtonGameObject(this.posx, this.posy + this.invHeight + 80, this.invWidth, 40, "splitStack", {}, this.scene, "SPLIT SELECTED STACK")
    }


    async initializeImages() {
        this.imagesIndex = {
            Stick: "stick.png"
        };

        this.images = await this.loadAllImages(this.imagesIndex)
        console.log(this.images)
        this.updateButtons(this.content)
        console.log(this.images);

    }

    async loadAllImages(imagesIndex) {
        const images = {};
        const keys = Object.keys(imagesIndex);

        const loadPromises = keys.map(key => {
            return new Promise((resolve, reject) => {
                this.imageLoader.load(
                    imagesIndex[key],
                    (image) => {
                        images[key] = image;
                        resolve(); // Resolve this image's loading
                    },
                    (error) => {
                        console.error(`Error loading image: ${imagesIndex[key]}`, error);
                        reject(error); // Reject if there is an error
                    }
                );
            });
        });

        // Wait for all the images to be loaded
        await Promise.all(loadPromises);

        console.log(images);

        return images
    }


    event(eventString, eventObject) {
        if (eventString == "inventory") {
            console.log("eventObject: " + eventObject.items)
            this.content = eventObject.items
            this.updateButtons()
            this.updateDimensions(this.widthInSLots)
        }
        if (eventString == "mouseJustDown") {
            this.mouseJustDown = true
        }
        if (eventString == "combineStacks") {
            console.log("Combining")
            this.combineSelected()
        }
        if (eventString == "selectAll") {
            let len = this.buttons.length
            for (let i = 0; i < len; i++) {
                this.buttons[i].isSelected = !this.buttons[i].isSelected
            }
        }
        if (eventString == "splitStack") {
            let sel = this.getSelected()
            if (sel.length == 1) {
                console.log("Splitting Stack")
                this.splitStack(sel[0].itemStack)
            }
        }
    }

    //regenerates the inventory slot buttons according to the content of the inv 
    updateButtons() {
        this.buttons = []
        let len = this.content.length
        for (let i = 0; i < len; i++) {
            let image = this.dummyItem

            let c = this.content[i].itemID; // Get the item ID
            if (this.images[c]) {
                image = this.images[c];
            }
            this.buttons.push(new InventorySlot(this.scene, this.posx, this.posy, this.imageSize, image, this.content[i]))
        }
        this.updateDimensions(this.widthInSLots)
    }

    //updates the Position and checks status of buttons
    processButtons() {
        let len = this.buttons.length
        for (let i = 1; i <= len; i++) {
            let level = Math.ceil(i / this.widthInSLots)
            this.buttons[i - 1].posx = this.posx + ((i - 1) * this.imageSize) + this.bufferSize * (i - 1) + this.borderWidth - (level - 1) * ((this.invWidth) - 2 * this.bufferSize)
            this.buttons[(i - 1)].posy = this.posy + this.borderWidth + (level - 1) * this.imageSize + this.bufferSize * (level - 1)
        }
        this.combineSelectedButton.posx = this.posx
        this.combineSelectedButton.posy = this.posy + this.invHeight

        this.selectAllButton.posx = this.posx
        this.selectAllButton.posy = this.posy + this.invHeight + 40

        this.splitButton.posx = this.posx
        this.splitButton.posy = this.posy + this.invHeight + 80
    }

    printInventory() {
        let leng = this.content.length
        for (let i = 0; i <= leng; i++) {
            console.log(this.content[i])
        }
    }

    areButtonsHovered() {
        let is = false
        let len = this.buttons.length
        for (let i = 0; i < len; i++) {
            if (this.buttons[i].isHovered) {
                is = true
            }
        }
        return is
    }

    splitStack(stack) {
        //Takes an Item stack as input
        this.content = this.content.filter(e => e !== stack)
        const size1 = Math.ceil(stack.size / 2)
        const size2 = stack.size - size1
        this.content.push({ itemID: stack.itemID, size: size1, tags: {} })
        if (size2 > 0) {
            this.content.push({ itemID: stack.itemID, size: size2, tags: {} })
        }
        this.updateButtons()
    }

    combineSelected() {
        let selected = []
        let buttonsCopy = []
        let len = this.buttons.length
        for (let i = 0; i < len; i++) {
            if (this.buttons[i].isSelected) {
                selected.push(this.buttons[i])
                this.content = this.content.filter(e => e !== this.buttons[i].itemStack)
            } else {
                buttonsCopy.push(this.buttons[i])
            }
        }
        len = selected.length
        for (let i = 0; i < len; i++) {
            selected[i].isSelected = false
        }
        let s = {}
        len = selected.length
        if (selected.length == 2) {
            console.log(selected)
            sendCombineStacksRequest(selected[0].itemStack.stackID, selected[1].itemStack.stackID)
        }


        for (let i = 0; i < len; i++) {
            if (s[selected[i].itemStack.itemID]) {
                s[selected[i].itemStack.itemID] += selected[i].itemStack.size
            } else {
                s[selected[i].itemStack.itemID] = selected[i].itemStack.size
            }
        }
        console.log(s)
        console.log(buttonsCopy)
        len = s.length

        const keys = Object.keys(s)
        keys.forEach(element => {
            console.log(keys)
            this.content.push({ itemID: element, size: s[element], tags: {} })

        });
        this.buttons = {}
        this.buttons = buttonsCopy
        this.updateButtons()


    }

    render() {
        if (this.isVisible) {
            if (!this.isHovered) {
                this.ctx.fillStyle = "green";
            }
            else {
                this.ctx.fillStyle = "yellow"
            }
            this.ctx.globalAlpha = 0.4;
            this.ctx.fillRect(this.posx, this.posy, this.invWidth, this.invHeight);
            this.ctx.globalAlpha = 1;
            this.ctx.fillStyle = "red";
            this.ctx.globalAlpha = 0.4;
            this.ctx.fillRect(this.posx, this.posy - this.textBoderSize, this.invWidth, this.textBoderSize);
            this.ctx.globalAlpha = 1;
            this.ctx.font = this.textSize;
            this.ctx.fillStyle = 'black';
            this.ctx.textBaseline = 'middle';

            this.ctx.fillText("Inventory", this.posx + this.invWidth / 2, this.posy - 15);

            let len = this.buttons.length
            for (let i = 0; i < len; i++) {
                this.buttons[i].render()
            }

            this.combineSelectedButton.render()
            this.selectAllButton.render()
            if (this.getSelected().length != 1) {
                this.splitButton.setButtonColorPrimary("grey")
            }
            else {
                this.splitButton.setButtonColorPrimary("green")
            }
            this.splitButton.render()
        }
    }

    process() {
        //In the are of the 
        if (this.isVisible && this.scene.mousex > this.posx && this.scene.mousex < this.posx + this.invWidth &&
            this.scene.mousey > this.posy - this.textBoderSize && this.scene.mousey < this.posy + this.invHeight && !this.areButtonsHovered()) {
            this.isHovered = true

        }

        if (this.mouseJustDown) {
            this.atackPosx = this.scene.mousex - this.posx
            this.atackPosy = this.scene.mousey - this.posy
            this.mouseJustDown = false
        }

        if (this.isHovered && this.scene.mouseDown) {
            this.posx = this.scene.mousex - this.atackPosx
            this.posy = this.scene.mousey - this.atackPosy
        }

        else {
            this.isHovered = false
        }
        if (this.scene.keys["e"] == true) {
            this.isVisible = true
        }
        else {
            this.isVisible = false
        }
        if (this.scene.keys["t"] == true) {
            addTestInv()
        }

        if (this.isVisible) {
            //update Positions
            this.processButtons()

            //check status of buttons
            let len = this.buttons.length
            for (let i = 0; i < len; i++) {
                this.buttons[i].process()
            }
            this.combineSelectedButton.process()
            this.selectAllButton.process()
            this.splitButton.process()

        }
    }

    updateDimensions(widthInSLots) {
        this.invWidth = this.imageSize * widthInSLots + this.bufferSize * (widthInSLots - 1) + 2 * this.borderWidth
        // Damit auf den nächst größeren Int runden 
        let heightInSlots = Math.ceil(this.content.length / widthInSLots)
        this.invHeight = this.imageSize * heightInSlots + this.bufferSize * (heightInSlots - 1) + 2 * this.borderWidth
    }

    getSelected() {
        let selected = []
        let len = this.buttons.length
        for (let i = 0; i < len; i++) {
            if (this.buttons[i].isSelected) {
                selected.push(this.buttons[i])
            }
        }
        return selected
    }

}

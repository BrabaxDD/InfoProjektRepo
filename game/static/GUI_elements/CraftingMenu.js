import { settings } from "../game.js";
import ButtonGameObject from "./Button.js";

export default class CraftingMenu {
    constructor(scene,posx, posy, recipes) {
        this.scene = scene;
        this.canvas = this.scene.canvas
        this.ctx = this.scene.canvas.getContext("2d")

        this.scene.eventBus.registerListner("click_on_canvas", this)
        this.scene.eventBus.registerListner("increaseQuantity", this)
        this.scene.eventBus.registerListner("decreaseQuantity", this)

        this.recipes = recipes;
        this.selectedRecipe = null;
        this.craftQuantity = 1;

        this.isVisible = false
        this.menuWidth = 200
        this.textBoderSize = 40
        this.menuHeight = 600
        this.posx = posx
        this.posy = posy

        this.recipeButtons = [];
        this.craftButton = new ButtonGameObject(
            400, 300, 100, 50, "CraftRequest", {}, this.scene, "Craft"
        );
        this.quantityButtons = {
            increase: new ButtonGameObject(this.posx+(200-50), this.posy, 50, 50, "increaseQuantity", {}, this.scene, "+"),
            decrease: new ButtonGameObject(this.posx, this.posy, 50, 50, "decreaseQuantity", {}, this.scene, "-"),
        };

        this.setupRecipeButtons();
    }

    setupRecipeButtons() {
        this.recipes.forEach((recipe, index) => {
            const button = new ButtonGameObject(
                this.posx, this.posy + index * 60 + 60, this.menuWidth, 50, "selectRecipe", recipe, this.scene, recipe.name
            );
            this.recipeButtons.push(button);
        });
    }

    process() {
        if (this.isVisible) {
            this.recipeButtons.forEach(button => button.process());
            this.craftButton.process();
            this.quantityButtons.increase.process();
            this.quantityButtons.decrease.process();
        }

        if (this.scene.keys[settings.craftMenuKey]) {
            this.isVisible = true
        }
        else {
            this.isVisible = false
        }
    }

    render() {
        if (this.isVisible) {
            this.ctx.fillStyle = settings.primaryColor;
            this.ctx.globalAlpha = 0.4;
            this.ctx.fillRect(this.posx, this.posy, this.menuWidth, this.menuHeight);
            this.ctx.globalAlpha = 1;
            this.ctx.font = settings.font;

            this.ctx.fillStyle = settings.inventoryTopColor;
            this.ctx.globalAlpha = 0.4;
            this.ctx.fillRect(this.posx, this.posy - this.textBoderSize, this.menuWidth, this.textBoderSize);
            this.ctx.globalAlpha = 1;

            this.ctx.fillStyle = 'black';
            this.ctx.textBaseline = 'middle';

            this.ctx.fillText("Crafting Menu", this.posx + this.menuWidth / 2, this.posy - 15);
            const ctx = this.ctx

            // Render recipe list
            this.recipeButtons.forEach(button => button.render());

            // Render craft quantity controls
            ctx.fillStyle = "black";
            ctx.font = settings.font;
            ctx.fillText(`Quantity: ${this.craftQuantity}`, this.posx + this.menuWidth/2, this.posy + 25);

            this.quantityButtons.increase.render();
            this.quantityButtons.decrease.render();

            // Render craft button
            this.craftButton.render();

            // Render selected recipe
            if (this.selectedRecipe) {
                ctx.fillText(`Selected: ${this.selectedRecipe.name}`, 250, 50);
            }
        }
    }

    event(eventString, eventObject) {
        if (eventString === "click_on_canvas") {
            this.recipeButtons.forEach(button => {
                if (button.is_hovered) {
                    this.selectedRecipe = button.eventObject;
                }
            });

            if (this.craftButton.is_hovered && this.selectedRecipe) {
                console.log(`Crafting ${this.craftQuantity} of ${this.selectedRecipe.name}`);
                for (let i = 0; i<this.craftQuantity; i++){
                    this.scene.eventBus.triggerEvent("CraftRequest", { recipe: this.selectedRecipe.name })
                }
            }
        }

        if (eventString == "increaseQuantity"){
            this.craftQuantity++;
        }

        
        if (eventString == "decreaseQuantity" && this.craftQuantity > 1){
            this.craftQuantity--
        }
    }
}

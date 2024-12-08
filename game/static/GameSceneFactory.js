import Player from "./Player.js";
import Scene from "./Scene.js";
import ButtonGameObject from "./Button.js"

export default class GameSceneFactory{
    constructor (canvas, keys){
        this.canvas = canvas
        this.keys = keys
    }

    buildGameScene(wichSceneToRender ){ //Das ist das Startfeld
        let scene = new Scene(this.canvas);
        switch (wichSceneToRender) {
            case "mainMenu":
            case 0:
                let player = new Player(100,100,20,20, 'blue', 5, this.keys,scene)
                let button = new ButtonGameObject(200,200,50,50,"testButtonPress",scene)
                scene.addObject(player)
                scene.addObject(button)
                break;
        }
        return scene
    }

}

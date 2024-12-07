import Player from "./Player.js";
import Scene from "./Scene.js";

export default class GameSceneFactory{
    constructor (canvas, keys){
        this.canvas = canvas
        this.keys = keys
    }

    buildGameScene(wichSceneToRender ){ //Das ist das Startfeld
        let scene = new Scene();
        switch (wichSceneToRender) {
            case "mainMenu":
            case 0:
                let player = new Player(100,100,20,20, 'blue', 5, this.canvas, this.keys)
                scene.addObject(player)
                break;
        }
        return scene
    }

}
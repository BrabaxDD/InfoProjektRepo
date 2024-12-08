import Player from "./Player.js";
import Scene from "./Scene.js";
import ButtonGameObject from "./GUI_elements/Button.js"
import GameObject from "./GameObject.js";

export default class GameSceneFactory extends GameObject{
    constructor (canvas, keys,sceneObject){
        super(sceneObject)
        this.canvas = canvas
        this.keys = keys
        
    }

    buildGameScene(wichSceneToRender ){ //Das ist das Startfeld
        let scene = new Scene(this.canvas);
        switch (wichSceneToRender) {
            case "mainMenu":
            case 0:
                let player = new Player(100,100,20,20, 'blue', 5, this.keys,scene)
                let button = new ButtonGameObject(200,200,50,50,"switchScene",{sceneToSwitch:"optionsMenu"},scene,"Test Button")
                console.log(button.eventObject.sceneToSwitch)
                let logBut = new ButtonGameObject(100,100,50,50, "loginToServer",{}, scene, "Login")
                scene.addObject(player)
                scene.addObject(logBut)
                scene.addObject(button)
                break;
            case "optionsMenu":
            case 1:
                let b2 = new ButtonGameObject(this.canvas.width/2,this.canvas.width/2,100,50,"switchScene",{sceneToSwitch:0},scene,"Andere Scene")
                scene.addObject(b2)
                break;
        }
        return scene
    }

}

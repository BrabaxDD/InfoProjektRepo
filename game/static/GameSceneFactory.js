import Player from "./Player.js";
import Scene from "./Scene.js";
import ButtonGameObject from "./GUI_elements/Button.js"
import GameObject from "./GameObject.js";
import CanvasTextInput from "./GUI_elements/TextInput.js";
import TileMap from "./images/TileMap.js";

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
                
                let button = new ButtonGameObject(this.canvas.width/2-100,this.canvas.height/3-28,200,56,"switchScene",{sceneToSwitch:"hostOrLogin"},scene,"Play")
                scene.addObject(button)

                let button2 = new ButtonGameObject(this.canvas.width/2-100,this.canvas.height/3 * 2-28,200,56,"switchScene",{sceneToSwitch:"optionsMenu"},scene,"Options")
                scene.addObject(button2)


                let lotTest = new ButtonGameObject(this.canvas.width/3-100,this.canvas.height/5-28,200,56,"loginToServer",{sceneToSwitch:2},scene,"Login (test for message)")
                scene.addObject(lotTest)

                let HostTest = new ButtonGameObject(this.canvas.width/3*2-100,this.canvas.height/5 -28,200,56,"loginToServerHost",{},scene,"Login as host ((test for message))")
                scene.addObject(HostTest)

                console.log(button.eventObject.sceneToSwitch)

                
                console.log("Fertige Scene")
                
                break;

            case "optionsMenu":
            case 1:
                let b2 = new ButtonGameObject(this.canvas.width/2-100,this.canvas.height/3 * 2-28,200,56,"switchScene",{sceneToSwitch:0},scene,"Back To Main Menu")
                scene.addObject(b2)

                break;

            case "game":
            case 2:
                let player = new Player(100,100,20,20, 'blue', 5, this.keys,scene)
                scene.addObject(player)
                
                break;
            
            case "hostOrLogin":
            case 3:
                let input = new CanvasTextInput(scene, this.canvas.width/2-100, this.canvas.height/2 - 15,200,30)
                scene.addObject(input)

                let logBut = new ButtonGameObject(this.canvas.width/3-100,this.canvas.height/5*4-28,200,56, "switchScene",{sceneToSwitch:2}, scene, "Login (to game)")
                scene.addObject(logBut)
                let logButHost = new ButtonGameObject(this.canvas.width/3*2-100,this.canvas.height/5*4-28,200,56, "switchScene",{sceneToSwitch:2}, scene, "Host (to game)")
                scene.addObject(logButHost)
        }
        return scene
    }

}

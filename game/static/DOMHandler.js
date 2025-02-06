import {settings} from "./game.js"

export default class DOMHandler {
    constructor() {

    }

    updateDOMServerName(name) {
        const textBox = document.querySelectorAll('.text-box')[0];
        textBox.innerHTML = `<p>Current Server:<b> ${name}</b></p>`;
    }

    updateDOMConnectionStatus(status) {
        const textBox = document.querySelectorAll('.text-box')[1];
        textBox.innerHTML = `<p>Current Status of connection: <b>${status}</b></p>`;
    }

    updateDOMControls() {
        const textBox = document.querySelectorAll('.text-box')[2];
        textBox.innerHTML = `<pre>Controls:

        Foreward:   ${settings.forwardKey}
        Backward:   ${settings.backKey}
        Left:       ${settings.leftKey}
        Right:      ${settings.rightKey} 

        Inventory:  ${settings.invKey}
        Hit:        ${settings.hitKey}
        Interact:   ${settings.interactKey}
        Craft:      ${settings.craftMenuKey}
        
        </pre>`;
    }

}

export default class DOMHandler {
    constructor() {

    }

    updateDOMServerName(name) {
        const textBox = document.querySelectorAll('.text-box')[0];
        textBox.innerHTML = `<p>Current Server: ${name}</p>`;
    }

    updateDOMConnectionStatus(status) {
        const textBox = document.querySelectorAll('.text-box')[1];
        textBox.innerHTML = `<p>Current Status of connection: ${status}</p>`;
    }

}
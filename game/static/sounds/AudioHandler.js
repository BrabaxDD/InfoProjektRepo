export default class AudioHandler {
    constructor() {
        this.cache = new Map();
        this.onLoop = false
        this.allAudios = {
            Ruby: "Ruby_22.wav",
            Click: "click.wav",
            Walk : "GrassFootsteps.wav"
        };

        this.loadAllSounds().then(() => {
            console.log("All sounds loaded!");

            console.log(this.allAudios)

            // Play a sound when ready
            this.play(this.allAudios.Ruby)
        }).catch(error => {
            console.error("Error loading sounds:", error);
        });
    }

    play(name, volume = 1) {
        const audio = this.getAudio(name);
        if (audio) {
            audio.volume = volume;
            audio.currentTime = 0; // Restart audio 
            audio.play();
        } else {
            console.error(`Audio not found: ${name}`);
        }
        return audio
    }

    async loop(name) {
        this.onLoop = true
        audio = this.play(name)
        while (this.onLoop) {
            await new Promise((resolve) => {
                audio.onended = () => {
                    resolve()  // Resolve the promise when the audio ends
                    audio = this.play(name)
                };
            })
        }
        if (!this.onLoop){
            audio.stop()
        }
    }


    loadAllSounds() {
        return Promise.all(
            Object.entries(this.allAudios).map(([key, fileName]) =>
                this.load(fileName)
                    .then(audio => this.cache.set(key, audio))
                    .catch(error => console.error(`Error loading sound: ${fileName}`, error))
            )
        );
    }

    load(fileName) {
        return new Promise((resolve, reject) => {
            if (this.cache.has(fileName)) {
                return resolve(this.cache.get(fileName));
            }

            const audio = new Audio(`/static/sounds/${fileName}`);

            audio.oncanplaythrough = () => {
                this.cache.set(fileName, audio);
                resolve(audio);
            };

            audio.onerror = (e) => {
                console.error(`Failed to load audio: ${fileName}`, e);
                reject(e);
            };
        });
    }

    getAudio(name) {
        return this.cache.get(name) || null;
    }

    stopLoop(){
        this.onLoop = false
    }
}

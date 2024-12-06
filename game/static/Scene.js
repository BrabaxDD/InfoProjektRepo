export default class Scene{
    constructor() {
        this.gameObjects = []
        this.toAdd = []
        this.toDelete = []
        
      }

    addObject (object){
        this.toAdd.push(object);
        console.log("objekt zu sap hinzugeügt: " + object);
    }

    render(){
      for(let i = 0; i<this.gameObjects.length; i++){
          this.gameObjects[i].render();
      }
    }
    
    process(){
      for(let i = 0; i<this.gameObjects.length; i++){
          this.gameObjects[i].process();
      }


      if(this.toDelete.length != 0){          
          this.gameObjects = this.gameObjects.filter( function( el ) {
            return toDelete.indexOf( el ) < 0;
          } );
          this.toDelete = [];
      }

      if(this.toAdd.length != 0){
        for(let i = 0; i<this.toAdd.length; i++){
            this.gameObjects.push(this.toAdd[i]);
        }
        this.toAdd = [];
      }

    }
}

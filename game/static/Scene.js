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
      let len = this.gameObjects.length;
      for(let i = 0; i<len; i++){
          this.gameObjects[i].render();
      }
    }
    
    process(){
      let len = this.gameObjects.length
      for(let i = 0; i< len; i++){
          this.gameObjects[i].process();
      }

      
      if(this.toDelete.length != 0){          
          this.gameObjects = this.gameObjects.filter( function( el ) {
            return toDelete.indexOf( el ) < 0;
          } );
          this.toDelete = [];
      }

      let len_add = this.toAdd.length
      if(len_add != 0){
        for(let i = 0; i<len_add; i++){
            this.gameObjects.push(this.toAdd[i]);
        }
        this.toAdd = [];
      }

    }
}

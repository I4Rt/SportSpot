from config import *

from mainController import *


if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', port=4999, debug=False) # how to use model with out running app at host?
        
        
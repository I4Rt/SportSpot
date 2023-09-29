from config import *

from mainController import *
from tools.KafkaSingleton import *

if __name__ == "__main__":
    with app.app_context():
        app.run(host='0.0.0.0', port=4998, debug=True) # how to use model with out running app at host?
        
        
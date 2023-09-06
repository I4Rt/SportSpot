from config import *

from mainController import *

from system.streaming.StreamBase import StreamBase
import warnings

if __name__ == "__main__":
    print('App is running')
    #warnings.simplefilter('ignore')
    with app.app_context():
        StreamBase.init()
        app.run(host='0.0.0.0', port=5002, debug=False) # how to use model with out running app at host?
        
        
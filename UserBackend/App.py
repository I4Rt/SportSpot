from config import *
from model import *
from controllers import mainController
from model.data.Sector import Sector
from model.data.Task import *
from model.data.Result import *
from system.kafka.KafkaSingleton import *

from system.streaming.StreamBase import StreamBase

if __name__ == "__main__":
    print('App is running')
    with app.app_context():
        KafkaSender.setInstance(app.config["senderTopic"], app.config["kafkaServer"])
        #StreamBase.init()
        db.create_all()
        app.run(host='0.0.0.0', debug=True)
        
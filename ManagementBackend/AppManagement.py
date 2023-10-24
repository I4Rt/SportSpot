from config import *
from model import *
from model.data.Sector import Sector
from model.data.Task import *
from model.data.Result import *
from model.Threads.TaskRunner import TaskRunner
from model.Threads.SideTaskProcessor import SideTaskProcessor
from model.Threads.AgregatedDataSender import AgregatedDataSender

from system.streaming.StreamBase import StreamBase
from system.kafka.KafkaSingleton import *
from model.Threads.DataReciever import *
import warnings

if __name__ == "__main__":
    print('App is running')
    warnings.simplefilter('ignore')
    with app.app_context():
        SideDataHolder.getInstance().getSavedChangedTasks()
        
        DataReciever().start()
        StreamBase.init()
        TaskRunner().start()
        
        SideTaskProcessor().start()
        AgregatedDataSender().start()
        
        

        app.run(host='0.0.0.0', port=5001, debug=False)
        
        
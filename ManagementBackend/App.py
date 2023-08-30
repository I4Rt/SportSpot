from config import *
from model import *
from model.data.Sector import Sector
from model.data.Task import *
from model.data.Result import *
from model.Threads.TaskRunner import TaskRunner

from system.streaming.StreamBase import StreamBase

import warnings

if __name__ == "__main__":
    print('App is running')
    warnings.simplefilter('ignore')
    with app.app_context():
        StreamBase.init()
        TaskRunner().start()
        
        #db.create_all()
        # for i in Task.getAll():
        #     i.delete()
        app.run(host='0.0.0.0', port=5001, debug=False)
        
        
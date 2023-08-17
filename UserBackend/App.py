from config import *
from model import *
from controllers import mainController
from model.data.Sector import Sector
from model.data.Task import *
from model.data.Result import *
if __name__ == "__main__":
    print('App is running')
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', debug=True)
        
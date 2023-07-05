from config import *
from controllers import mainController


if __name__ == "__main__":
    print('App is running')
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', debug=True)
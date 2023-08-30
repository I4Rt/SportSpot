from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from config import *
class SessionFabric:
    
    @classmethod
    def getSession(cls):
        """Provide a transactional scope around a series of operations."""
        session_factory = sessionmaker(bind=create_engine(app.config['SQLALCHEMY_DATABASE_URI']))
        Session = scoped_session(session_factory)
        try:
            yield Session()
            Session.commit()
        except:
            Session.rollback()
            raise
        finally:
            Session.close()

## 系统
from flask_sqlalchemy import SQLAlchemy

## 实现

def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner
    
@singleton
class connect(object):
    def __init__(self):
        self.db = SQLAlchemy()


db = connect().db


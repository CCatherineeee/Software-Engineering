
import os
DB_URI = 'mysql+pymysql://root:mysqlroot@39.107.51.181:3306/Education_Management_System'
# 'mysql+pymysql://用户名称:密码@localhost:端口/数据库名称'
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SECRET_KEY = '123123'
AVATAR_UPLOAD_FOLDER = os.getcwd()+'/static/avatar/'
CLASSFILE_UPLOAD_FOLDER = os.getcwd()+'/static/classFile/'
EXPERIMENT_UPLOAD_FOLDER = os.getcwd()+'/static/experimentFile/'
SQLALCHEMY_POOL_RECYCLE = 30
SQLALCHEMY_POOL_SIZE = 300
SQLALCHEMY_TRACK_MODIFICATIONS = True


# from flask import Flask
from flask import Flask, request, jsonify
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from flask_cors import CORS  # 解决跨域的问题
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json

import config
import dbManage

from Model import Model

# from Routers.ManageAccount.register import registerRoute
from Routers.ManageAccount.login import loginRoute
from Routers.ManageAccount.addUser import addUserRoute
from Routers.ManageAccount.getUserInfo import getUserInfoRoute
from Routers.ManageAccount.deleteUser import deleteUserRoute
from Routers.ManageAccount.editUserInfo import editUserInfoRoute
from Routers.ManageAccount.auth.authManage import auth
from Routers.ManageCourse.addCourse import addCourseRoute
from Routers.ManageClass.manageClass import manageClassRoute

login_manager = LoginManager()
login_manager.session_protection = 'strong' #安全等级
app = Flask(__name__)
CORS(app, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api

app.config.from_object(config)

dbManage.db.init_app(app)

# app.register_blueprint(registerRoute)

app.register_blueprint(loginRoute)
app.register_blueprint(addUserRoute)
app.register_blueprint(getUserInfoRoute)
app.register_blueprint(deleteUserRoute)
app.register_blueprint(editUserInfoRoute)
app.register_blueprint(auth)
app.register_blueprint(addCourseRoute)
app.register_blueprint(manageClassRoute)

@app.before_first_request
def initdb():
    dbManage.db.create_all()
    if not Model.Admin.query.filter(Model.Admin.name == "admin").first():
        admin = Model.Admin(admin_id="0000000", admin_pwd="admin", name="admin",
                               email="0000000@tongji.edu.cn")
        dbManage.db.session.add(admin)  # 添加数据
        dbManage.db.session.commit()


@app.route('/')  # 接口地址
def home():
    return "home"

def create_app():
    login_manager = LoginManager()
    login_manager.session_protection = 'strong' #安全等级


    app = Flask(__name__)
    CORS(app, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api

    app.config.from_object(config)

    dbManage.db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(loginRoute)
    app.register_blueprint(auth)
    app.register_blueprint(addUserRoute)
    app.register_blueprint(getUserInfoRoute)
    app.register_blueprint(deleteUserRoute)
    app.register_blueprint(editUserInfoRoute)
    app.register_blueprint(addCourseRoute)
    app.register_blueprint(manageClassRoute)


###########3 web 服务器 ################
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)

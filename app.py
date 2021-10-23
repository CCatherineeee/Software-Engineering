# from flask import Flask
from flask import Flask, request, jsonify
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from flask_cors import CORS  # 解决跨域的问题
from flask_sqlalchemy import SQLAlchemy
import json

import dbManage
import config
from Model import Entity

from Routers.ManageAccount.register import registerRoute
from Routers.ManageAccount.login import loginRoute
from Routers.ManageFile.addUser import addUserRoute


app = Flask(__name__)
CORS(app, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api

app.config.from_object(config)

dbManage.db.init_app(app)

app.register_blueprint(registerRoute)
app.register_blueprint(loginRoute)
app.register_blueprint(addUserRoute,url_prefix="/file/")

@app.before_first_request
def initdb():
    dbManage.db.create_all()
    if not Entity.Admin.query.filter(and_(Entity.Admin.name == "admin",
                                            Entity.Admin.admin_id == "0000000")).first():
        admin = Entity.Admin(admin_id="0000000", admin_pwd="admin", name="admin",
                               email="0000000@tongji.edu.cn")
        dbManage.db.session.add(admin)  # 添加数据
        dbManage.db.session.commit()



@app.route('/')  # 接口地址
def home():
    return "home"


###########3 web 服务器 ################
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)


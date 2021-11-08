from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model import Model
from sqlalchemy import and_, or_

# 蓝图名 蓝图路径
loginRoute = Blueprint('loginRoute', __name__)
CORS(loginRoute, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api

def AdminLogin(name, admin_pwd):

    admin = Model.Admin.query.filter(Model.Admin.name == name).first()
    if not admin:
        return "UserNotExist"
    admin = Model.Admin.query.filter(and_(Model.Admin.admin_pwd == admin_pwd,Model.Admin.name == name)).first()
    if not admin:
        return "PasswordWrong"
    else:
        return "Login"

def StudentLogin(s_id, s_pwd):
    student = Model.Student.query.filter(Model.Student.s_id == s_id).first()
    if not student:
        return "UserNotExist"
    student = Model.query.query.filter(and_(Model.query.s_pwd == s_pwd,Model.Student.s_id == s_id)).first()
    if not admin:
        return "PasswordWrong"
    else:
        return "Login"


@loginRoute.route('/adminLogin/',methods=['POST']) 
def adminLogin():
    # 接口本身
    data = request.form
    check = AdminLogin(data.get('username'),data.get('password'))
    return check


@loginRoute.route('/studentLogin/',methods=['POST'])  
def stuLogin():
    # 接口本身
    data = request.form
    check = StudentLogin(data.get('username'),data.get('password'))
    return check
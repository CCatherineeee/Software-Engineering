from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
import Model
# import Model
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

@loginRoute.route('/adminLogin/',methods=['POST']) 
def adminLogin():
    # 接口本身
    data = request.form
    check = AdminLogin(data.get('username'),data.get('password'))
    return check

# @loginRoute.route('/login/',methods=['POST']) 
# def adminLogin():
#     # 接口本身
#     data = request.form
#     name = data.get('username')
#     pwd = data.get('password')
#     adName  = admin = Model.Admin.query.filter(Model.Admin.name == name).first()
#     admin = Model.Admin.query.filter(and_(Model.Admin.admin_pwd == admin_pwd,Model.Admin.name == name)).first()
    



# @loginRoute.route('/studentLogin/',methods=['POST'])  
# def stuLogin():
#     # 接口本身
#     data = request.form
#     check = StudentLogin(data.get('username'),data.get('password'))
#     return check

@loginRoute.route('/login/',methods=['POST'])
def Login():
    data = request.form
    uid = data.get('id')
    pwd = data.get('password')
    teacher = Model.Teacher.query.filter(Model.Teacher.t_id == uid).first()
    if teacher:
        if teacher.check_password(pwd):
            return "TSuccess"
        else:
            return "PasswordWrong"
    student = Model.Student.query.filter(Model.Student.s_id == uid).first()
    if student:
        if student.check_password(pwd):
            return "SSuccess"
        else:
            return "SPasswordWrong"
    return pwd

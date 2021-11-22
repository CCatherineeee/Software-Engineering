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

@loginRoute.route('/studentLogin/',methods=['POST']) 
def StudentLogin(s_id, s_pwd):
    student = Model.Student.query.filter(Model.Student.s_id == s_id).first()
    if not student:
        data = {'id':"",'status':400,'message':'none'}  #错误返回
        return jsonify(data)
    # student = Model.Student.query.filter(and_(Model.Student.query.s_pwd == s_pwd,Model.Student.s_id == s_id)).first()
    student = Model.Student.query.filter(Model.Student.s_id == s_id).first()
    if student.check_password(s_pwd):
        data = {'id':s_id,'status':200,'message':'success'}

    else:
        data = {'id':"",'status':500,'message':'wrong'}
    return jsonify(data)


@loginRoute.route('/teacherLogin/',methods=['POST']) 
def TeacherLogin(t_id, t_pwd):
    teacher = Model.Teacher.query.filter(Model.Teacher.t_id == t_id).first()
    if not teacher:
        data = {'id':"",'status':400}  #错误返回
        return jsonify(data)
    teacher = Model.Teacher.query.filter(Model.Teacher.t_id == t_id).first()
    if teacher.check_password(t_pwd):  #检查密码
        data = {'id':t_id,'status':200,'message':'success'}

    else:
        data = {'id':t_id,'status':500,'message':'wrong'}
    return jsonify(data)



@loginRoute.route('/adminLogin/',methods=['POST']) 
def adminLogin():
    # 接口本身
    data = request.form
    check = AdminLogin(data.get('username'),data.get('password'))
    return check


# @loginRoute.route('/studentLogin/',methods=['POST'])  
# def stuLogin():
#     # 接口本身
#     data = request.form
#     check = StudentLogin(data.get('username'),data.get('password'))
#     return check

@loginRoute.route('/login/',methods=['POST']) 
def Login():
    # 接口本身
    data = request.form
    uid = data.get('id')
    pwd = data.get('password')
    teacher = Model.Teacher.query.filter(Model.Teacher.t_id == uid).first()
    if teacher:
        teacher = Model.Teacher.query.filter(and_(Model.Teacher.t_pwd == pwd, Model.Teacher.t_id == uid)).first()
        if teacher:
            return "TSuccess"
        else:
            return "TPasswordWrong"
    student = Model.Student.query.filter(Model.Student.s_id == uid).first()
    if student:
        student = Model.Student.query.filter(and_(Model.Student.s_pwd == pwd,Model.Student.s_id == uid)).first()
        if student:
            return "SSuccess"
        else:
            return "SPasswordWrong"
    return "UserNotExist"
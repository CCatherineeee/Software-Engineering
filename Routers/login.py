from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model import Entity
from sqlalchemy import and_, or_

# 蓝图名 蓝图路径
loginRoute = Blueprint('loginRoute', __name__)
CORS(loginRoute, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api

def AdminLogin(name, admin_pwd):
    """
    type: 1学生 2教师 3管理员
    """
    admin = Entity.Admin.query.filter(Entity.Admin.name == name).first()
    if not admin:
        return "UserNotExit"
    admin = Entity.Admin.query.filter(and_(Entity.Admin.admin_pwd == admin_pwd,Entity.Admin.name == name)).first()
    if not admin:
        return "PasswordWrong"
    else:
        return "Login"

@loginRoute.route('/adminLogin/',methods=['POST'])  # 接口地址
def login():
    # 接口本身
    data = request.form
    check = AdminLogin(data.get('username'),data.get('password'))
    return check
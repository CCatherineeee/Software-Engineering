from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Student,TeachingAssistant,Course,Class
from Model.Model import Teacher
from sqlalchemy import and_, or_
import time
import dbManage

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Routers import Role

deleteUserRoute = Blueprint('deleteUserRoute', __name__)
CORS(deleteUserRoute, resources=r'/*')	

def checkAdminToken(token,role):
    try:
        s = Serializer('WEBSITE_SECRET_KEY')
        token_id = s.loads(token)['id']
        token_role = s.loads(token)['role']
    except:
        return 301
    
    if token_role != role:
        return 404
    else:
        return 200

@deleteUserRoute.route('/delete/student/',methods=['POST'])  
def deleteStudent():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    s_id = data['s_id']
    token = data['token']
    res = checkAdminToken(token,Role.AdminRole)
    if res == 301:
        return jsonify({'code':res,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':res,'message':"无法访问页面",'data':None})
    else:
        student = Student.query.filter(Student.s_id == s_id).first()    
        if not student:
            return jsonify({'code':302,'message':"用户不存在",'data':None})
        dbManage.db.session.delete(student)
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"删除成功",'data':None})

@deleteUserRoute.route('/delete/Ta/',methods=['POST'])  
def deleteTA():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ta_id = data['ta_id']
    token = data['token']
    res = checkAdminToken(token,Role.AdminRole)
    if res == 301:
        return jsonify({'code':res,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':res,'message':"无法访问页面",'data':None})
    else:
        ta = TeachingAssistant.query.filter(TeachingAssistant.ta_id == ta_id).first()    
        if not ta:
            return jsonify({'code':302,'message':"用户不存在",'data':None})
        dbManage.db.session.delete(ta)
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"删除成功",'data':None})

@deleteUserRoute.route('/delete/teacher/',methods=['POST'])  
def deleteTeacher():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    t_id = data["t_id"]
    token = data['token']
    res = checkAdminToken(token,Role.AdminRole)
    if res == 301:
        return jsonify({'code':res,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':res,'message':"无法访问页面",'data':None})
    else:
        teacher = Teacher.query.filter(Teacher.t_id == t_id).first()
        courses = Course.query.filter(Course.duty_teacher == t_id).all()
        classes = Class.query.filter(Class.t_id == t_id).all()
        for c in classes:
            c.t_id = None
        for c in courses:
            c.duty_teacher = None
        dbManage.db.session.commit()

        if not teacher:
            return jsonify({'code':302,'message':"用户不存在",'data':None})
        dbManage.db.session.delete(teacher)
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"删除成功",'data':None})


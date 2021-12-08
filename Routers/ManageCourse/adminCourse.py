from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint,current_app,make_response
import json
from Model.Model import CourseType
from Model.Model import Course
from Model.Model import Teacher

from sqlalchemy import and_, or_
import time
import dbManage
import os
from sqlalchemy import and_, or_
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Routers import Role

adminCourseRoute = Blueprint('adminCourseRoute', __name__)
CORS(adminCourseRoute, resources=r'/*')	

def checkToken(token,role,role2 = None):
    try:
        s = Serializer('WEBSITE_SECRET_KEY')
        token_id = s.loads(token)['id']
        token_role = s.loads(token)['role']
    except:
        return 301
    if not role2:
        if token_role != role:
            return 404
        else:
            return 200
    else:
        if token_role != role2 and token_role != role:
            return 404
        else:
            return 200

@adminCourseRoute.route('/course/addType/',methods=['POST'])  
def addCourseType():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    name = data['name']
    prefix = data['prefix']
    token = data['token']
    res = checkToken(token,Role.AdminRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        ctype = CourseType.query.filter(CourseType.prefix == prefix).first()
        if ctype:
            return jsonify({'code':501,'message':"课程类型已存在",'data':None})
        ctype = CourseType.query.filter(CourseType.ct_name == name).first()
        if ctype:
            return jsonify({'code':502,'message':"课程名称已存在",'data':None})
        ctype = CourseType(prefix=prefix, ct_name=name)
        dbManage.db.session.add(ctype)
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"添加成功",'data':None})

@adminCourseRoute.route('/course/getType/',methods=['GET'])  
def getCourseType():
    token = request.args.get('token')
    res = checkToken(token,Role.AdminRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        typeS = dbManage.db.session.query(CourseType).all()
        content = []
        for type in typeS:
            temp = {'name':type.ct_name,'prefix':type.prefix}
            content.append(temp)
        return jsonify({'code':200,'message':"请求成功",'data':content})


@adminCourseRoute.route('/course/delType/',methods=['POST'])  
def delCourseType():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    prefix = data['prefix']
    token = data['token']
    res = checkToken(token,Role.AdminRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        ctype = CourseType.query.filter(CourseType.prefix == prefix).first()
        dbManage.db.session.delete(ctype)
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"删除成功",'data':content})

@adminCourseRoute.route('/course/addCourse/',methods=['POST'])  
def addCourse():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    semester = data['semester']
    year = data['year']
    prefix = data['prefix']
    t_id = data['t_id']
    token = data['token']
    res = checkToken(token,Role.AdminRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        if semester == '春季':
            semester_ = '00'
        elif semester == '秋季':
            semester_ = '01'

        c_id = prefix + year + semester_
        course = Course.query.filter(Course.c_id == c_id).first()
        if course:
            return jsonify({'code':500,'message':"课程已存在",'data':None})
        course = Course(c_id=c_id,prefix=prefix,course_semester=semester,course_year=year,duty_teacher=t_id)
        dbManage.db.session.add(course)
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"添加成功",'data':None})


@adminCourseRoute.route('/course/delCourse/',methods=['POST'])  
def delCourse():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    c_id = data['c_id']
    token = data['token']
    res = checkToken(token,Role.AdminRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        course = Course.query.filter(Course.c_id == c_id).first()
        if course:
            dbManage.db.session.delete(course)
            dbManage.db.session.commit()
            return jsonify({'code':200,'message':"删除成功",'data':None})
        return jsonify({'code':500,'message':"课程不存在",'data':None})

@adminCourseRoute.route('/course/setDuty/',methods=['POST'])  
def setDuty():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    courseID = data['courseID']
    t_id = data['t_id']
    token = data['token']
    res = checkToken(token,Role.AdminRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        course = Course.query.filter(Course.c_id == courseID).first()
        if not course:
            return jsonify({'code':500,'message':"课程不存在",'data':None})
        course.duty_teacher = t_id
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"设置成功",'data':None})

@adminCourseRoute.route('/course/getDuty/',methods=['GET'])  
def getDuty():
    token = request.args.get('token')
    res = checkToken(token,Role.AdminRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        courses = dbManage.db.session.query(Course).all()
        content = []
        for course in courses:
            t_name = None
            t_id = None
            if course.duty_teacher:
                teacher = Teacher.query.filter(Teacher.t_id == course.duty_teacher).first()
                t_id = course.duty_teacher
                t_name = teacher.name
            coursetype = CourseType.query.filter(CourseType.prefix == course.prefix).first()
            temp = {'name':coursetype.ct_name,'prefix':course.prefix,'semester':course.course_semester,"year":course.course_year,"t_id":t_id,"t_name":t_name,"c_id":course.c_id}
            content.append(temp)
        return jsonify({'code':200,'message':"请求成功",'data':content})


@adminCourseRoute.route('/course/getAllTeacher/',methods=['GET'])  
def getAllTeacher():
    token = request.args.get('token')
    res = checkToken(token,Role.AdminRole,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        res = checkToken(token,Role.TeacherRole)
        teachers = dbManage.db.session.query(Teacher).all()
        content = []
        for teacher in teachers:
            temp = {'name':teacher.name,'id':teacher.t_id}
            content.append(temp)
        return jsonify({'code':200,'message':"请求成功",'data':content})
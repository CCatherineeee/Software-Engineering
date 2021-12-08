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
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Routers import Role

teacherCourseRoute = Blueprint('teacherCourseRoute', __name__)
CORS(teacherCourseRoute, resources=r'/*')	

def checkToken(token,role):
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

@teacherCourseRoute.route('/course/myDuty/',methods=['POST'])  
def getMyDuty():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    t_id = data['t_id']
    token = data['token']
    try:
        s = Serializer('WEBSITE_SECRET_KEY')
        token_id = s.loads(token)['id']
        token_role = s.loads(token)['role']
    except:
        return jsonify({'code':301,'status':"验证过期",'data':None})
    
    if token_role != 2:
        return jsonify({'code':404,'status':"无法访问",'data':None})

    if t_id != token_id:
        return jsonify({'code':404,'status':"无法访问",'data':None})
    
    courses = Course.query.filter(Course.duty_teacher == t_id).all()
    content = []
    for course in courses:
        coursetype = CourseType.query.filter(CourseType.prefix == course.prefix).first()
        temp = {'name':coursetype.ct_name,'prefix':course.prefix,'semester':course.course_semester,"year":course.course_year, "course_id":course.c_id}
        content.append(temp)
    return jsonify({'code':200,'status':"请求成功",'data':content})
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

teacherCourseRoute = Blueprint('teacherCourseRoute', __name__)
CORS(teacherCourseRoute, resources=r'/*')	

@teacherCourseRoute.route('/course/myDuty/',methods=['GET'])  
def addCourseType():
    t_id = request.args.get('t_id')
    courses = Course.query.filter(Course.duty_teacher == t_id).all()
    content = []
    for course in courses:
        coursetype = CourseType.query.filter(CourseType.prefix == course.prefix).first()
        temp = {'name':coursetype.ct_name,'prefix':course.prefix,'semester':course.course_semester,"year":course.course_year}
        content.append(temp)
    return jsonify(content)
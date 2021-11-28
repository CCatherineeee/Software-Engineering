from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Course,Class
import dbManage



addCourseRoute = Blueprint('addCourseRoute', __name__)
CORS(addCourseRoute, resources=r'/*')	

@addCourseRoute.route('/addCourse',methods=['POST'])  
def addCourse():
    data = request.form
    # data = json.loads(data.decode("utf-8"))

    prefix = data['prefix']  #课程号前缀
    semester = data['semester']
    year = data['year']
    duty_teacher_id = data['t_id']

    if semester == '春季':
        semester_ = '00'
    elif semester == '秋季':
        semester_ = '01'

    course_list = Course.query.filter(Course.prefix == prefix).first()
    if course_list:
        result = {'status':400,'message':'该课程已存在'}
    else:

        course = Course(c_id = prefix + semester_ + year,prefix=prefix, 
        course_semester=semester, course_year=year, duty_teacher=duty_teacher_id)
        dbManage.db.session.add(course)
        dbManage.db.session.commit()
        result = {'status':200,'message':'添加课程成功'}

    return result
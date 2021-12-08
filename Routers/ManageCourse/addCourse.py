from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Course,Class
import dbManage
from Routers import Role
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


addCourseRoute = Blueprint('addCourseRoute', __name__)
CORS(addCourseRoute, resources=r'/*')	

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

@addCourseRoute.route('/addCourse',methods=['POST'])  
def addCourse():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    # data = json.loads(data.decode("utf-8"))

    prefix = data['prefix']  #课程号前缀
    semester = data['semester']
    year = data['year']
    duty_teacher_id = data['t_id']

    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        if semester == '春季':
            semester_ = '00'
        elif semester == '秋季':
            semester_ = '01'

        course_list = Course.query.filter(Course.prefix == prefix).first()
        if course_list:
            result = {'status':400,'message':'该课程已存在','data':None}
        else:

            course = Course(c_id = prefix + semester_ + year,prefix=prefix, 
            course_semester=semester, course_year=year, duty_teacher=duty_teacher_id)
            dbManage.db.session.add(course)
            dbManage.db.session.commit()
            result = {'status':200,'message':'添加课程成功','data':None}

        return result
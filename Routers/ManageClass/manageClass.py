from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Course,Class,TeacherClass
import dbManage
from sqlalchemy import and_, or_



manageClassRoute = Blueprint('manageClassRoute', __name__)
CORS(manageClassRoute, resources=r'/*')	


#责任教师开班，班号为课程号+总班数   需要选择开课的年份及季节
@manageClassRoute.route('/addClass',methods=['POST'])  
def addClass():
    data = request.form

    prefix = data['prefix']  #课程号前缀
    semester = data['semester']
    year = data['year']
    t_id = data['t_id']

    if semester == '春季':  #数据库课号：前缀+年份+开课时期
        semester = '00'
    elif semester == '秋季':
        semester = '01'

    course_id = prefix + year + semester

    course = Course.query.filter(Course.c_id == course_id).first()  #找出全部的这个课程
    if course:  #课程存在
        class_list = Class.query.filter(Class.course_id == course_id).all()  #找出课程名为这个的所有班级
        class_no = len(class_list)+1
        new_class = Class(class_id =course_id+str(class_no), course_id = course_id,class_number=class_no)
        teacher_class = TeacherClass(class_id = new_class.class_id , t_id=t_id)
        dbManage.db.session.add(new_class)
        dbManage.db.session.add(teacher_class)
        dbManage.db.session.commit()
        result = {'status':200,'message':'添加成功','class_id':new_class.class_id}
    else:
        result = {'status':400,'message':'该课程不存在','class_id':''}

    return jsonify(result)

#删除班级
@manageClassRoute.route('/deleteClass',methods=['POST'])  
def deleteClass():

    data = request.form

    class_id = data['class_id']  #课程号前缀


    old_class = Class.query.filter(Class.class_id == class_id).first()  #找出课程名为这个的所有班级

    if (old_class):
        dbManage.db.session.delete(old_class)
        dbManage.db.session.commit()
        result = {'status':200,'message':'删除成功'}

    else:
        result = {'status':400,'message':'该班级不存在，删除失败'}

    return jsonify(result)

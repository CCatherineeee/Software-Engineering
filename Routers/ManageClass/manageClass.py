from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Course,Class,TeacherClass,StudentClass,CourseType,Teacher,Student
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

#责任教师更改班级授课老师
@manageClassRoute.route('/changeTeacher',methods=['POST'])  
def changeTeacher():
    
    data = request.form

    class_id = data['class_id']  #课程号前缀
    t_id = data['t_id'] #老师工号

    this_class = Class.query.filter(Class.class_id == class_id).first()
    this_teacher = Teacher.query.filter(Teacher.t_id == t_id).first()

    if this_class and this_teacher:
        TeacherClass.query.filter_by(class_id = class_id).update({'t_id':t_id})
        # dbManage.db.session.(teacher_class)
        dbManage.db.session.commit()
        result = {'status':200,'message':'更改成功'}
    else:
        result = {'status':400,'message':'该课程或老师不存在'}

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

#根据学生学号获取所在的所有班级,班级信息
@manageClassRoute.route('/studentGetClass',methods=['POST'])  
def studentGetClass():

    data = request.form

    s_id = data['s_id']  #学生学号
    class_list = StudentClass.query.filter(StudentClass.s_id == s_id).all()
    all_class = []
    for class_item in class_list:
        this_class = Class.query.filter(Class.class_id == class_item.class_id).first()
        course_type = CourseType.query.filter(CourseType.prefix == this_class.prefix).first()
        if(this_class.course_semester=='00'):
            semester = '春季'
        else:
            semester = '秋季'
        
        data = {
            'class_id':class_item.class_id,
            'class_number':this_class.class_number,
            'prefix':this_class.prefix,
            'semester':semester,
            'year':this_class.year,
            'course_name':course_type.ct_name}
        all_class.append(data)

    return jsonify(all_class)

#根据老师工号获取所在的所有班级,班级信息
@manageClassRoute.route('/teacherGetClass',methods=['POST'])  
def teacherGetClass():

    data = request.form

    t_id = data['t_id']  #老师学号
    class_list = TeacherClass.query.filter(TeacherClass.t_id == t_id).all()
    all_class = []
    for class_item in class_list:
        this_class = Class.query.filter(Class.class_id == class_item.class_id).first()
        course_type = CourseType.query.filter(CourseType.prefix == this_class.prefix).first()
        if(this_class.course_semester=='00'):
            semester = '春季'
        else:
            semester = '秋季'
        
        data = {
            'class_id':class_item.class_id,
            'class_number':this_class.class_number,
            'prefix':this_class.prefix,
            'semester':semester,
            'year':this_class.year,
            'course_name':course_type.ct_name}
        all_class.append(data)

    return jsonify(all_class)

#通过班级号获取所有班级内信息
@manageClassRoute.route('/IDGetClass',methods=['POST'])  
def IDGetClass():
    data = request.form

    class_id = data['class_id']  #班级号
    this_class = Class.query.filter(Class.class_id == class_id).first()
    teacher_class = TeacherClass.query.filter(TeacherClass.class_id == class_id ).first()
    teacher = Teacher.query.filter(Teacher.t_id==teacher_class.t_id).first()
    if (this_class):
        result = {
            'status':200,
            'class_id':this_class.class_id,
            'course_id':this_class.course_id,
            'class_number':this_class.class_number,
            'teacher':teacher.name}
    else:  #不存在这个班级
        result = {
            'status':400,
            'class_id':'',
            'course_id':'',
            'class_number':'',
            'teacher':''
        }
    return jsonify(result)

#通过班级号获取所有班级内所有学生
@manageClassRoute.route('/IDGetClassStudent',methods=['POST'])  
def IDGetClassStudent():
    data = request.form
    class_id = data['class_id']  #班级号
    # this_class = Class.query.filter(Class.class_id == class_id).first()
    all_student = []
    student_list = StudentClass.query.filter(StudentClass.class_id == class_id).all()
    for student_item in student_list:
        stu = Student.query.filter(Student.s_id == student_item.s_id).first()
        stu_json = {'s_id':stu.s_id,'name':stu.name}
        all_student.append(stu_json)

    return jsonify(all_student)
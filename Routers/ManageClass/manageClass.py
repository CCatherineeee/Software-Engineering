from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Course,Class,StudentClass,CourseType,Teacher,Student
import dbManage
from sqlalchemy import and_, or_



manageClassRoute = Blueprint('manageClassRoute', __name__)
CORS(manageClassRoute, resources=r'/*')	


#责任教师开班，班号为课程号+总班数   需要选择开课的年份及季节
@manageClassRoute.route('/manageClass/addClass',methods=['POST'])  
def addClass():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    course_id = data['courseID']
    t_id = data['t_id']

    course = Course.query.filter(Course.c_id == course_id).first()  #找出全部的这个课程
    if course:  #课程存在
        class_list = Class.query.filter(Class.course_id == course_id).all()  #找出课程名为这个的所有班级
        class_no = len(class_list)+1
        new_class = Class(class_id =course_id+str(class_no), course_id = course_id,class_number=class_no, t_id = t_id)
        dbManage.db.session.add(new_class)
        dbManage.db.session.commit()
        result = {'status':200,'message':'添加成功','class_id':new_class.class_id}
    else:
        result = {'status':400,'message':'该课程不存在','class_id':''}

    return jsonify(result)

#责任教师更改班级授课老师
@manageClassRoute.route('/manageClass/changeTeacher',methods=['POST'])  
def changeTeacher():
    
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    class_id = data['class_id']  #课程号前缀
    t_id = data['t_id'] #老师工号

    this_class = Class.query.filter(Class.class_id == class_id).first()
    this_teacher = Teacher.query.filter(Teacher.t_id == t_id).first()

    if this_class and this_teacher:
        Class.query.filter_by(class_id = class_id).update({'t_id':t_id})
        # dbManage.db.session.(teacher_class)
        dbManage.db.session.commit()
        result = {'status':200,'message':'更改成功'}
    else:
        result = {'status':400,'message':'该课程或老师不存在'}

    return jsonify(result)
@manageClassRoute.route('/manageClass/showClass',methods=['GET'])  
def showClass():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    course_id = data['courseID']

    classes = Class.query.filter(Class.course_id == course_id).all()  #找出全部的这个课程
    content = []
    for class_ in classes:
        course = Course.query.filter(Course.c_id == course_id).first()
        teacher = Teacher.query.filter(Teacher.t_id == class_.t_id).first()
        coursetype = CourseType.query.filter(CourseType.prefix == course.prefix).first()
        temp = {'name':coursetype.ct_name,'prefix':course.prefix,'semester':course.course_semester,"year":course.course_year, "class_id":class_.class_id, "t_id":teacher.t_id,"t_name":teacher.name}
        content.append(temp)
    return jsonify(content)


#删除班级
@manageClassRoute.route('/manageClass/deleteClass',methods=['POST'])
def deleteClass():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    class_id = data['classID']  #课程号前缀

    old_class = Class.query.filter(Class.class_id == class_id).first()  #找出课程名为这个的所有班级

    if (old_class):
        dbManage.db.session.delete(old_class)
        dbManage.db.session.commit()
        result = {'status':200,'message':'删除成功'}

    else:
        result = {'status':400,'message':'该班级不存在，删除失败'}

    return jsonify(result)

#责任教师更改班级授课老师
@manageClassRoute.route('/changeTeacher/',methods=['POST'])  
def changeTeacher():
    
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    class_id = data['class_id']  #课程号前缀
    t_id = data['t_id'] #老师工号

    this_class = Class.query.filter(Class.class_id == class_id).first()

    if this_class:
        this_class.t_id = t_id
        # dbManage.db.session.(teacher_class)
        dbManage.db.session.commit()
        result = {'status':200,'message':'更改成功'}
    else:
        result = {'status':400,'message':'该课程或老师不存在'}

    return jsonify(result)

#根据学生学号获取所在的所有班级,班级信息
@manageClassRoute.route('/manageClass/studentGetClass',methods=['POST'])  
def studentGetClass():

    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    s_id = data['s_id']  #学生学号
    class_list = StudentClass.query.filter(StudentClass.s_id == s_id).all()
    if not class_list:
        return jsonify({'status':500,'message':'学生不存在'})
    all_class = []
    for class_item in class_list:
        this_class = Class.query.filter(Class.class_id == class_item.class_id).first()
        course_type = CourseType.query.filter(CourseType.prefix == this_class.course_id[:6]).first()
        teacher = Teacher.query.filter(Teacher.t_id==this_class.t_id).first()
        #看看这个课程是否存在
        if not course_type:
            return jsonify({'status':400,'message':'课程不存在'})
        if(this_class.course_id[10:12]=='00'):
            semester = '春季'
        else:
            semester = '秋季'
        
        data = {
            'class_id':class_item.class_id,
            'class_number':this_class.class_number,
            'prefix':course_type.prefix,
            'semester':semester,
            'year':this_class.course_id[6:10],
            'course_name':course_type.ct_name,
            'teacher':teacher.name}
        all_class.append(data)

    return jsonify(all_class)

#根据老师工号获取所在的所有班级,班级信息
@manageClassRoute.route('/manageClass/teacherGetClass',methods=['POST'])  
def teacherGetClass():

    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    t_id = data['t_id']  #老师学号
    class_list = Class.query.filter(Class.t_id == t_id).all()
    all_class = []
    for class_item in class_list:
        this_class = Class.query.filter(Class.class_id == class_item.class_id).first()
        course_type = CourseType.query.filter(CourseType.prefix == this_class.course_id[:6]).first()
        teacher = Teacher.query.filter(Teacher.t_id==this_class.t_id).first()
        
        data = {
            'class_id':class_item.class_id,
            'class_number':this_class.class_number,
            'prefix':course_type.prefix,
            'semester':this_class.semester,
            'year':this_class.course_id[6:10],
            'course_name':course_type.ct_name,
            'teacher':teacher.name}
        all_class.append(data)

    return jsonify(all_class)

#通过班级号获取所有班级内信息
@manageClassRoute.route('/manageClass/IDGetClass',methods=['POST'])  
def IDGetClass():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    class_id = data['class_id']  #班级号
    this_class = Class.query.filter(Class.class_id == class_id).first()
    # teacher_class = TeacherClass.query.filter(TeacherClass.class_id == class_id ).first()
    teacher = Teacher.query.filter(Teacher.t_id==this_class.t_id).first()
    course_type = CourseType.query.filter(CourseType.prefix == this_class.course_id[:6]).first()
    if(this_class.course_id[10:12]=='00'):
        semester = '春季'
    else:
        semester = '秋季'
    if (this_class):
        result = {
            'status':200,
            'class_id':this_class.class_id,
            'course_id':this_class.course_id,
            'class_number':this_class.class_number,
            'prefix':course_type.prefix,
            'semester':semester,
            'year':this_class.course_id[6:10],
            'course_name':course_type.ct_name,
            'teacher':teacher.name}
    else:  #不存在这个班级
        result = {
            'status':400,
            'class_id':'',
            'course_id':'',
            'class_number':'',
            'prefix':'',
            'semester':'',
            'year':'',
            'course_name':'',
            'teacher':''
        }
    return jsonify(result)

#通过班级号获取所有班级内所有学生
@manageClassRoute.route('/manageClass/IDGetClassStudent',methods=['POST'])  
def IDGetClassStudent():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    class_id = data['class_id']  #班级号
    # this_class = Class.query.filter(Class.class_id == class_id).first()
    all_student = {'data':[]}
    student_list = StudentClass.query.filter(StudentClass.class_id == class_id).all()
    for student_item in student_list:
        stu = Student.query.filter(Student.s_id == student_item.s_id).first()
        stu_json = {'s_id':stu.s_id,'name':stu.name}
        all_student['data'].append(stu_json)

    return jsonify(all_student)
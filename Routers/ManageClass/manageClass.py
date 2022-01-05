from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Course,Class, Experiment,StudentClass,CourseType, StudentExam, StudentExperiment,Teacher,Student,TeachingAssistant,TAClass
import dbManage
from sqlalchemy import and_, or_
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Routers import Role



manageClassRoute = Blueprint('manageClassRoute', __name__)
CORS(manageClassRoute, resources=r'/*')	

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

#责任教师开班，班号为课程号+总班数   需要选择开课的年份及季节
@manageClassRoute.route('/manageClass/addClass',methods=['POST'])  
def addClass():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    course_id = data['courseID']
    t_id = data['t_id']
    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        course = Course.query.filter(Course.c_id == course_id).first()  #找出全部的这个课程
        if course:  #课程存在
            class_list = Class.query.filter(Class.course_id == course_id).all()  #找出课程名为这个的所有班级
            class_no = len(class_list)+1
            new_class = Class(class_id =course_id+str(class_no), course_id = course_id,class_number=class_no, t_id = t_id)
            dbManage.db.session.add(new_class)
            dbManage.db.session.commit()
            result = {'code':200,'message':'添加成功','data':None}
        else:
            result = {'cdde':500,'message':'该课程不存在','data':None}

        return jsonify(result)

#责任教师更改班级授课老师
@manageClassRoute.route('/manageClass/changeTeacher',methods=['POST'])  
def changeTeacher():
    
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    class_id = data['class_id']  #课程号前缀
    t_id = data['t_id'] #老师工号
    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        this_class = Class.query.filter(Class.class_id == class_id).first()
        this_teacher = Teacher.query.filter(Teacher.t_id == t_id).first()

        if this_class and this_teacher:
            Class.query.filter_by(class_id = class_id).update({'t_id':t_id})
            # dbManage.db.session.(teacher_class)
            dbManage.db.session.commit()
            result = {'message':200,'message':'更改成功','data':None}
        else:
            result = {'message':500,'message':'该课程或老师不存在','data':None}

        return jsonify(result)

@manageClassRoute.route('/manageClass/showClass/',methods=['POST'])  
def showClass():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    course_id = data['courseID']
    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        classes = Class.query.filter(Class.course_id == course_id).all()  #找出全部的这个课程
        content = []
        for class_ in classes:
            course = Course.query.filter(Course.c_id == course_id).first()
            t_id = None
            t_name = None
            if class_.t_id:
                teacher = Teacher.query.filter(Teacher.t_id == class_.t_id).first()
                t_id = teacher.t_id
                t_name = teacher.name
            coursetype = CourseType.query.filter(CourseType.prefix == course.prefix).first()
            temp = {'name':coursetype.ct_name,'prefix':course.prefix,'semester':course.course_semester,"year":course.course_year, "class_id":class_.class_id, "t_id":t_id,"t_name":t_name}
            content.append(temp)
        return jsonify({'code':200,'message':"请求成功",'data':content})


#删除班级
@manageClassRoute.route('/manageClass/deleteClass',methods=['POST'])
def deleteClass():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    class_id = data['classID']  #课程号前缀
    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        old_class = Class.query.filter(Class.class_id == class_id).first()  #找出课程名为这个的所有班级

        if (old_class):
            dbManage.db.session.delete(old_class)
            dbManage.db.session.commit()
            result = {'code':200,'message':'删除成功','data':None}

        else:
            result = {'code':500,'500':'该班级不存在','data':None}

        return jsonify(result)

@manageClassRoute.route('/studentGetClass',methods=['POST'])  
def studentGetClass():

    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    s_id = data['s_id']
    token = data['token']
    try:
        s = Serializer('WEBSITE_SECRET_KEY')
        token_id = s.loads(token)['id']
        token_role = s.loads(token)['role']
    except:
        return jsonify({'code':301,'message':"验证过期",'data':None})

    if token_role != 1:
        return jsonify({'code':404,'message':"无法访问",'data':None})

    if s_id != token_id:
        return jsonify({'code':404,'message':"无法访问",'data':None})

    class_list = StudentClass.query.filter(StudentClass.s_id == s_id).all()
    all_class = []
    for class_item in class_list:
        this_class = Class.query.filter(Class.class_id == class_item.class_id).first()
        this_course = Course.query.filter(Course.c_id == this_class.course_id).first()
        course_type = CourseType.query.filter(CourseType.prefix == this_course.prefix).first()
        
        data = {
            'class_id':class_item.class_id,
            'class_number':this_class.class_number,
            'prefix':this_course.prefix,
            'semester':this_course.course_semester,
            'year':this_course.course_year,
            'course_name':course_type.ct_name}
        all_class.append(data)

    return jsonify({'code':200,'message':"请求成功",'data':all_class})

#根据老师工号获取所在的所有班级,班级信息
@manageClassRoute.route('/manageClass/teacherGetClass',methods=['POST'])  
def teacherGetClass():

    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    t_id = data['t_id']  #老师学号
    token = data['token']
    try:
        s = Serializer('WEBSITE_SECRET_KEY')
        token_id = s.loads(token)['id']
        token_role = s.loads(token)['role']
    except :
        return jsonify({'code':301,'message':"验证过期",'data':None})
    
    if token_role != 2:
        return jsonify({'code':404,'message':"无法访问",'data':None})

    if t_id != token_id:
        return jsonify({'code':404,'message':"无法访问",'data':None})

    class_list = Class.query.filter(Class.t_id == t_id).all()
    all_class = []
    for class_item in class_list:
        this_class = Class.query.filter(Class.class_id == class_item.class_id).first()
        this_course = Course.query.filter(Course.c_id == this_class.course_id).first()
        course_type = CourseType.query.filter(CourseType.prefix == this_course.prefix).first()
        teacher = Teacher.query.filter(Teacher.t_id==this_class.t_id).first()
        data = {
            'class_id':class_item.class_id,
            'class_number':this_class.class_number,
            'prefix':this_course.prefix,
            'semester':this_course.course_semester,
            'year':this_course.course_year,
            'course_name':course_type.ct_name}
        all_class.append(data)

    return jsonify({'code':200,'message':"请求成功",'data':all_class})
    
#通过班级号获取所有班级内信息
@manageClassRoute.route('/manageClass/IDGetClass',methods=['POST'])  
def IDGetClass():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    class_id = data['class_id']  #班级号
    this_class = Class.query.filter(Class.class_id == class_id).first()

    teacher = Teacher.query.filter(Teacher.t_id==this_class.t_id).first()
    course_type = CourseType.query.filter(CourseType.prefix == this_class.course_id[:6]).first()
    if(this_class.course_id[10:12]=='00'):
        semester = '春季'
    else:
        semester = '秋季'
    if (this_class):
        data = {
            'class_id':this_class.class_id,
            'course_id':this_class.course_id,
            'class_number':this_class.class_number,
            'prefix':course_type.prefix,
            'semester':semester,
            'year':this_class.course_id[6:10],
            'course_name':course_type.ct_name,
            'teacher':teacher.name}
        result = {'code':200,'message':"请求成功",'data':data}
    else:  #不存在这个班级
        result = {'code':500,'message':"班级不存在",'data':None}
    return jsonify(result)

#通过班级号获取所有班级内所有学生
@manageClassRoute.route('/manageClass/IDGetClassStudent',methods=['POST'])  
def IDGetClassStudent():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    class_id = data['class_id']  #班级号
    all_student = {'data':[]}
    student_list = StudentClass.query.filter(StudentClass.class_id == class_id).all()
    for student_item in student_list:
        stu = Student.query.filter(Student.s_id == student_item.s_id).first()
        stu_json = {'s_id':stu.s_id,'name':stu.name}
        all_student['data'].append(stu_json)
    ta_id = TAClass.query.filter(TAClass.class_id == class_id).first().ta_id
    ta_name = TeachingAssistant.query.filter(TeachingAssistant.ta_id == ta_id).first().name
    all_student.update({'ta_id':ta_id,"ta_name":ta_name})
    return {'code':200,'message':"获取成功",'data':all_student}

#通过班级号获取所有班级内所有学生的所有成绩
@manageClassRoute.route('/manageClass/GetClassStudentScore',methods=['POST'])  
def GetClassStudentScore():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    class_id = data['class_id']  #班级号
    all_student = {"experiment":[],"score":[],"type":[]}
    student_list = StudentClass.query.filter(StudentClass.class_id == class_id).all()
    for student_item in student_list:
        stu = Student.query.filter(Student.s_id == student_item.s_id).first()
        stu_json = {"name":stu.name,"id":student_item.s_id}
        stu_ex_list = StudentExperiment.query.filter(StudentExperiment.s_id == student_item.s_id).all()
        for ex_item in stu_ex_list:
            this_ex = Experiment.query.filter(Experiment.experiment_id==ex_item.experiment_id).first()
            if this_ex.course_id != class_id[:-1]:
                continue
            ex_name = "ex_" + str(ex_item.experiment_id)
            ex_name_json = {"label":this_ex.experiment_title,"key":ex_name}
            if ex_name_json not in all_student['experiment']:
                all_student['experiment'].append(ex_name_json)
                all_student['type'].append(this_ex.ex_type)
            if not ex_item.score:
                stu_json[ex_name] = 0
            else:
                stu_json[ex_name] = ex_item.score

        all_student['score'].append(stu_json)
        

    return {'code':200,'message':"成功获取",'data':all_student}


#通过课程号获取所有班级
@manageClassRoute.route('/manageClass/courseGetClass',methods=['POST'])  
def courseGetClass():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    course_id = data['course_id']  #课程号
    course = Course.query.filter(Course.c_id==course_id).first()
    if not course:
        return jsonify({'code':400,'message':"课程不存在",'data':None})
    class_list = Class.query.filter(Class.course_id==course_id).all()
    result = []
    for item in class_list:
        item_json = {"class_id":item.class_id}
        result.append(item_json)

    return jsonify({'code':200,'message':"获取成功",'data':result})
    

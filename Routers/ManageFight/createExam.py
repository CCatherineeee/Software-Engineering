from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Course,Class,Exam,Question,StudentClass,ExamGroup,StudentExam
import dbManage
from Routers import Role
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
import random
from Routers import Role

createFightRoute = Blueprint('createFightRoute', __name__)

@createFightRoute.route('/createExam',methods=['POST']) 
def createExam():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    course_id = data['course_id']
    title = data['title']
    start_time = data['start_time']
    end_time = data['end_time']

    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

    exam = Exam(course_id = course_id, title = title, start_time = start_time, end_time = end_time, status = 0)
    dbManage.db.session.add(exam)
    dbManage.db.session.commit()
    
    # 找到所有班级
    classes = Class.query.filter(Class.course_id == course_id).all()
    for class_ in classes:
        # 找到班级学生，生产测验小组
        students = StudentClass.query.filter(StudentClass.class_id == class_.class_id).all()
        while(len(students) > 4):
            sg = random.sample(students,3)
            students.remove(sg[0])
            students.remove(sg[1])
            students.remove(sg[2])
            ag = ExamGroup(exam_id = exam.exam_id,s_id_1 = sg[0].s_id,s_id_2 = sg[1].s_id,s_id_3 = sg[2].s_id)
            dbManage.db.session.add(ag)
        if len(students) == 4:
            ag1 = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[0].s_id,s_id_2 = students[1].s_id)
            ag2 = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[2].s_id,s_id_2 = students[3].s_id)
            dbManage.db.session.add(ag1)
            dbManage.db.session.add(ag2)
        if len(students) == 3:
            ag = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[0].s_id,s_id_2 = students[1].s_id,s_id_3 = students[2].s_id)
            dbManage.db.session.add(ag)
        if len(students) == 2:
            ag = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[0].s_id,s_id_2 = students[1].s_id)
            dbManage.db.session.add(ag)
        if len(students) == 1:
            ag = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[0].s_id)
            dbManage.db.session.add(ag)
    dbManage.db.session.commit()

    return jsonify({'code':200,'message':"添加成功",'data':exam.exam_id})

@createFightRoute.route('/getExam',methods=['POST']) 
def getExam():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    course_id = data['course_id']
    token = data['token']
    try:
        s = Serializer('WEBSITE_SECRET_KEY')
        token_id = s.loads(token)['id']
        token_role = s.loads(token)['role']
    except:
        return jsonify({'code':500,'message':"请求失败",'data':{'data':None,'role':None}})
    exams = Exam.query.filter(Exam.course_id == course_id).all()
    content = []
    for e in exams:
        now_time = datetime.datetime.now()
        if now_time > e.end_time:
            e.status = 3
            stopExam(e.exam_id)
            dbManage.db.session.commit()
        else:
            if now_time > e.start_time:
                e.status = 1
                pushExam(e.exam_id,course_id)
            else:
                e.status = 0
        is_submit = None
        score = None
        if token_role == Role.StudentRole:
            se = StudentExam.query.filter(StudentExam.exam_id == e.exam_id,StudentExam.s_id == token_id).first()
            if not se:
                is_submit = 0
            else:
                score = se.score
                is_submit = 1
        temp = {"exam_id":e.exam_id, "title": e.title, "start_time": str(e.start_time), "end_time": str(e.end_time), "status": e.status,'is_submit':is_submit,'score':score}
        content.append(temp)
    return jsonify({'code':200,'message':"请求成功",'data':{'data':content,'role':token_role}})


@createFightRoute.route('/getClassExam',methods=['POST']) 
def getClassExam():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    class_id = data['class_id']
    token = data['token']
    try:
        s = Serializer('WEBSITE_SECRET_KEY')
        token_id = s.loads(token)['id']
        token_role = s.loads(token)['role']
    except:
        return jsonify({'code':500,'message':"请求失败",'data':{'data':None,'role':None}})
    class_ = Class.query.filter(Class.class_id == class_id).first()
    exams = Exam.query.filter(Exam.course_id == class_.course_id).all()
    content = []
    for e in exams:
        now_time = datetime.datetime.now()
        if now_time > e.end_time:
            e.status = 3
            stopExam(e.exam_id)
            dbManage.db.session.commit()
        else:
            if now_time > e.start_time:
                e.status = 1
                pushExam(e.exam_id,class_id)
            else:
                e.status = 0
        is_submit = None
        score = None
        if token_role == Role.StudentRole:
            se = StudentExam.query.filter(StudentExam.exam_id == e.exam_id,StudentExam.s_id == token_id).first()
            if not se:
                is_submit = 0
            else:
                score = se.score
                is_submit = 1
        temp = {"exam_id":e.exam_id, "title": e.title, "start_time": str(e.start_time), "end_time": str(e.end_time), "status": e.status,'is_submit':is_submit,'score':score}
        content.append(temp)
    return jsonify({'code':200,'message':"请求成功",'data':{'data':content,'role':token_role}})

def pushExam(exam_id,class_id):

    exam = Exam.query.filter(Exam.exam_id == exam_id).first()
    exam.status = 1

    dbManage.db.session.commit()
    return jsonify({'code':200,'message':"请求成功",'data':None})

@createFightRoute.route('/pushExamForce',methods=['POST']) 
def pushExamForce():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    exam_id = data['exam_id']
    course_id = data['course_id']

    exam = Exam.query.filter(Exam.exam_id == exam_id).first()
    exam.status = 1
    exam.start_time = datetime.datetime.now()
    # 找到所有班级
    classes = Class.query.filter(Class.course_id == course_id).all()
    for class_ in classes:
        # 找到班级学生，生产测验小组
        students = StudentClass.query.filter(StudentClass.class_id == class_id).all()
        while(len(students) > 4):
            sg = random.sample(students,3)
            students.remove(sg[0])
            students.remove(sg[1])
            students.remove(sg[2])
            ag = ExamGroup(exam_id = exam.exam_id,s_id_1 = sg[0].s_id,s_id_2 = sg[1].s_id,s_id_3 = sg[2].s_id)
            dbManage.db.session.add(ag)
        if len(students) == 4:
            ag1 = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[0].s_id,s_id_2 = students[1].s_id)
            ag2 = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[2].s_id,s_id_2 = students[3].s_id)
            dbManage.db.session.add(ag1)
            dbManage.db.session.add(ag2)
        if len(students) == 3:
            ag = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[0].s_id,s_id_2 = students[1].s_id,s_id_3 = students[2].s_id)
            dbManage.db.session.add(ag)
        if len(students) == 2:
            ag = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[0].s_id,s_id_2 = students[1].s_id)
            dbManage.db.session.add(ag)
        if len(students) == 1:
            ag = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[0].s_id)
            dbManage.db.session.add(ag)
    dbManage.db.session.commit()

    return jsonify({'code':200,'message':"请求成功",'data':None})

def stopExam(exam_id):
    
    exam = Exam.query.filter(Exam.exam_id == exam_id).first()
    exam.status = 3
    dbManage.db.session.commit()
    egs = ExamGroup.query.filter(ExamGroup.exam_id == exam_id).all()
    for e in egs:
        dbManage.db.session.delete(e)
    dbManage.db.session.commit()
    return jsonify({'code':200,'message':"请求成功",'data':None})

@createFightRoute.route('/stopExam',methods=['POST']) 
def stopExamForce():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    exam_id = data['exam_id']
    exam = Exam.query.filter(Exam.exam_id == exam_id).first()
    exam.status = 3
    exam.end_time = datetime.datetime.now()
    dbManage.db.session.commit()
    egs = ExamGroup.query.filter(ExamGroup.exam_id == exam_id).all()
    for e in egs:
        dbManage.db.session.delete(e)
    dbManage.db.session.commit()
    return jsonify({'code':200,'message':"请求成功",'data':None})

@createFightRoute.route('/addQuestion',methods=['POST']) 
def addQuestion():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    exam_id = data['exam_id']
    questions = data['questions']
    all_score = 0
    this_exam = Exam.query.filter(Exam.exam_id == exam_id).first()
    for q in questions:
        title = q['title']
        option_a = q['option_a']
        option_b = q['option_b']
        option_c = q['option_c']
        option_d = q['option_d']
        q_type = q['q_type']
        q_score = q['q_score']
        checkList = q['checkList']
        answer = ""
        for c in checkList:
            answer = answer + c
        qs = Question(title = title, option_a = option_a, option_b = option_b, option_c = option_c, option_d = option_d, answer = answer, exam_id = exam_id, q_type = q_type,q_score = q_score)
        dbManage.db.session.add(qs)
        all_score += q_score
    dbManage.db.session.commit()
    this_exam.score = all_score
    return jsonify({'code':200,'message':"添加成功",'score':all_score})


@createFightRoute.route('/editExamTime',methods=['POST']) 
def editExamRime():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    exam_id = data['exam_id']
    start_time = data['start_time']
    end_time = data['end_time']
    class_id = data['class_id']

    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

    exam = Exam.query.filter(Exam.exam_id == exam_id).first()
    exam.start_time = start_time
    exam.end_time = end_time

    now_time = datetime.datetime.now()
    if now_time < end_time:
        # 找到所有班级
        classes = Class.query.filter(Class.course_id == course_id).all()
        for class_ in classes:
            # 找到班级学生，生产测验小组
            students = StudentClass.query.filter(StudentClass.class_id == class_id).all()
            while(len(students) > 4):
                sg = random.sample(students,3)
                students.remove(sg[0])
                students.remove(sg[1])
                students.remove(sg[2])
                ag = ExamGroup(exam_id = exam.exam_id,s_id_1 = sg[0].s_id,s_id_2 = sg[1].s_id,s_id_3 = sg[2].s_id)
                dbManage.db.session.add(ag)
            if len(students) == 4:
                ag1 = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[0].s_id,s_id_2 = students[1].s_id)
                ag2 = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[2].s_id,s_id_2 = students[3].s_id)
                dbManage.db.session.add(ag1)
                dbManage.db.session.add(ag2)
            if len(students) == 3:
                ag = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[0].s_id,s_id_2 = students[1].s_id,s_id_3 = students[2].s_id)
                dbManage.db.session.add(ag)
            if len(students) == 2:
                ag = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[0].s_id,s_id_2 = students[1].s_id)
                dbManage.db.session.add(ag)
            if len(students) == 1:
                ag = ExamGroup(exam_id = exam.exam_id,s_id_1 = students[0].s_id)
                dbManage.db.session.add(ag)

    dbManage.db.session.commit()
    return jsonify({'code':200,'message':"添加成功"})

@createFightRoute.route('/exam/examGetStudent',methods=['POST']) 
def examGetStudent():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    exam_id = data['exam_id']
    stu_list=[]
    this_exam = Exam.query.filter(Exam.exam_id==exam_id).first()
    if not this_exam:
        return jsonify({'code':400,'message':"考试不存在",'data':None})
    group_list = ExamGroup.query.filter(ExamGroup.exam_id==exam_id).all()
    for item in group_list:
        if(item.s_id_1):
            stu_list.append({"s_id":item.s_id_1})
        if(item.s_id_2):
            stu_list.append({"s_id":item.s_id_2})
        if(item.s_id_3):
            stu_list.append({"s_id":item.s_id_3})
    return jsonify({'code':200,'message':"获取成功",'data':stu_list})

@createFightRoute.route('/delExam',methods=['POST']) 
def delExam():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    exam_id = data['exam_id']
    token = data['token']
    try:
        s = Serializer('WEBSITE_SECRET_KEY')
        token_id = s.loads(token)['id']
        token_role = s.loads(token)['role']
    except:
        return jsonify({'code':500,'message':"请求失败",'data':{'data':None,'role':None}})
    exam = Exam.query.filter(Exam.exam_id == exam_id).first()
    dbManage.db.session.delete(exam)
    return jsonify({'code':200,'message':"删除成功"})
        
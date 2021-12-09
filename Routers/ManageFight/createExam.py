from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Course,Class,Exam,Question
import dbManage
from Routers import Role
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime

createFightRoute = Blueprint('createFightRoute', __name__)

@createFightRoute.route('/createExam',methods=['POST']) 
def createExam():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    class_id = data['class_id']
    title = data['title']
    start_time = data['start_time']
    end_time = data['end_time']

    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

    exam = Exam(class_id = class_id, title = title, start_time = start_time, end_time = end_time, status = 0)
    dbManage.db.session.add(exam)
    dbManage.db.session.commit()
    return jsonify({'code':200,'message':"添加成功",'data':exam.exam_id})

@createFightRoute.route('/getExam',methods=['POST']) 
def getExam():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    class_id = data['class_id']
    exams = Exam.query.filter(Exam.class_id == class_id).all()
    content = []
    for e in exams:
        now_time = datetime.datetime.now()
        if now_time > e.end_time:
            status = 3
        else:
            status = e.status
        temp = {"exam_id":e.exam_id, "title": e.title, "start_time": str(e.start_time), "end_time": str(e.end_time), "status": status}
        content.append(temp)
    return jsonify({'code':200,'message':"请求成功",'data':content})

@createFightRoute.route('/pushExam',methods=['POST']) 
def pushExam():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    exam_id = data['exam_id']
    exam = Exam.query.filter(Exam.exam_id == exam_id).first()
    exam.status = 1
    dbManage.db.session.commit()
    return jsonify({'code':200,'message':"请求成功",'data':None})

@createFightRoute.route('/stopExam',methods=['POST']) 
def stopExam():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    exam_id = data['exam_id']
    exam = Exam.query.filter(Exam.exam_id == exam_id).first()
    exam.status = 3
    dbManage.db.session.commit()
    return jsonify({'code':200,'message':"请求成功",'data':None})

@createFightRoute.route('/addQuestion',methods=['POST']) 
def addQuestion():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    exam_id = data['exam_id']
    questions = data['questions']
    for q in questions:
        title = q['title']
        option_a = q['option_a']
        option_b = q['option_b']
        option_c = q['option_c']
        option_d = q['option_d']
        answer = q['answer']
        q_type = q['q_type']
        q_score = q['q_score']
        qs = Question(title = title, option_a = option_a, option_b = option_b, option_c = option_c, option_d = option_d, answer = answer, exam_id = exam_id, q_type = q_type,q_score = q_score)
        dbManage.db.session.add(qs)
    dbManage.db.session.commit()
    return jsonify({'code':200,'message':"添加成功"})


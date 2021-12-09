from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Course,Class,Exam,Question
import dbManage
from Routers import Role
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime

getExamRoute = Blueprint('getExamRoute', __name__)

@getExamRoute.route('/getExamById',methods=['POST']) 
def getExamById():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    exam_id = data['exam_id']

    exam = Exam.query.filter(Exam.exam_id == exam_id).first()
    questions = Question.query.filter(Question.exam_id == exam_id).all()
    content=[]
    for q in questions:
        qs = {'title':q.title,'option_a':q.option_a,'option_b':q.option_b,'option_c':q.option_c,'option_d':q.option_d,
        'q_score':q.q_score,
        'q_type':q.q_type,'answer':q.answer,'q_id':q.question_id}
        content.append(qs)
    
    return jsonify({'code':200,'message':"添加成功",'data':{'ex_title':exam.title,'start_time':str(exam.start_time),'end_time':str(exam.end_time),'questions':content}})
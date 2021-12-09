from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Course,Class,Exam,Question,StudentExamQuestion,StudentExam,ExamGroup
import dbManage
from Routers import Role
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
from sqlalchemy import and_, or_


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
        answer = None
        checkList = None
        if q.q_type == 1 or q.q_type == 3:
            answer = int(q.answer)
        else:
            checkList = []
            for i in range(len(q.answer)):
                checkList.append(int(q.answer[i]))
        qs = {'title':q.title,'option_a':q.option_a,'option_b':q.option_b,'option_c':q.option_c,'option_d':q.option_d,
        'q_score':q.q_score,
        'q_type':q.q_type,'answer':answer,'q_id':q.question_id,'checkList':checkList}
        content.append(qs)
    
    return jsonify({'code':200,'message':"添加成功",'data':{'ex_title':exam.title,'start_time':str(exam.start_time),'end_time':str(exam.end_time),'questions':content}})

@getExamRoute.route('/submitExam',methods=['POST'])
def submitExam():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    answerList = data['answerList']
    s_id = data['s_id']
    exam_id = 0
    score = 0
    for a in answerList:
        answer = ""
        for c in a['checkList']:
            answer = answer + str(c)
        q = Question.query.filter(Question.question_id == a['q_id']).first()
        exam_id = q.exam_id
        if answer == q.answer and answer != None and answer != "":
            is_correct = True
            score  = score + q.q_score
        elif answer in q.answer and answer != None and answer != "":
            is_correct = False
            score  = score + q.q_score/2
        else:
            is_correct = False
        sq = StudentExamQuestion(s_id = s_id, choice = answer, q_id = a['q_id'],is_correct = is_correct)
        dbManage.db.session.add(sq)
    eg = ExamGroup.query.filter(ExamGroup.exam_id == exam_id).filter(or_(ExamGroup.s_id_1 == s_id,ExamGroup.s_id_2 == s_id,ExamGroup.s_id_3 == s_id)).first()
    se_1 = StudentExam.query.filter(and_(StudentExam.exam_id == exam_id,StudentExam.s_id == eg.s_id_1)).first()
    se_2 = StudentExam.query.filter(and_(StudentExam.exam_id == exam_id,StudentExam.s_id == eg.s_id_2)).first()
    se_3 = StudentExam.query.filter(and_(StudentExam.exam_id == exam_id,StudentExam.s_id == eg.s_id_3)).first()
    count = 0
    if se_1:
        count +=1
    if se_2:
        count +=1
    if se_3:
        count +=1
    if count == 0:
        score = score
    elif count == 1:
        score = score * 0.9
    else:
        score = score * 0.8
    se = StudentExam(exam_id = exam_id,s_id = s_id,score = score)
    dbManage.db.session.add(se)
    dbManage.db.session.commit()
    return jsonify({'code':200,'message':"提交成功",'data':{'rank':count + 1,'score':score}})
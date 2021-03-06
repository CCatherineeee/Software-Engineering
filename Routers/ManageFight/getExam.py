from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Course,Class,Exam,Question,StudentExamQuestion,StudentExam,ExamGroup,Student
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

@getExamRoute.route('/getCloseExam',methods=['POST'])
def getCloseExam():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    exam_id = int(data['exam_id'])
    s_id = str(data['s_id'])
    exam = Exam.query.filter(Exam.exam_id == exam_id).first()
    se = StudentExam.query.filter(and_(StudentExam.exam_id == exam_id, StudentExam.s_id == s_id)).first()
    questions = Question.query.filter(Question.exam_id == exam_id).all()
    content=[]
    answerList = []
    total_score = 0.0
    for q in questions:
        total_score = total_score + q.q_score
        answer = 0
        checkList = 0
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
        sq = StudentExamQuestion.query.filter(and_(StudentExamQuestion.q_id == q.question_id,StudentExamQuestion.s_id == s_id)).first()
        if not sq:
            return jsonify({'code':200,'message':"请求成功",'data':{'questionList':content,'answerList':None,'ex_title':exam.title,'start_time':str(exam.start_time),'end_time':str(exam.end_time),}})
        choice = sq.choice
        s_answer = 0
        s_checkList = []
        if choice == "":
            s_answer = 0
            s_checkList = []
        else:
            if q.q_type == 1 or q.q_type == 3:
                s_answer = str(sq.choice)
            else:
                for i in range(len(choice)):
                    s_checkList.append(int(choice[i]))
        answer = {'sq_id':q.question_id,'answer':s_answer,'checkList':s_checkList}
        answerList.append(answer)
    return jsonify({'code':200,'message':"请求成功",'data':{'questionList':content,'answerList':answerList,'ex_title':exam.title,'ex_score':total_score,'score':se.score,'start_time':str(exam.start_time),'end_time':str(exam.end_time),}})


@getExamRoute.route('/getExamGroupById',methods=['POST']) 
def getExamGroupById():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    exam_id = data['exam_id']
    s_id = data['s_id']

    ag = ExamGroup.query.filter(ExamGroup.exam_id == exam_id).filter(or_(ExamGroup.s_id_1 == s_id, ExamGroup.s_id_2 == s_id, ExamGroup.s_id_3 == s_id)).first()
    group = []
    s1 = Student.query.filter(Student.s_id == ag.s_id_1).first()
    se1 = StudentExam.query.filter(StudentExam.exam_id == exam_id, StudentExam.s_id == s1.s_id).first()
    if se1:
        score = se1.score
    else:
        score = None
    group.append({"id":ag.s_id_1,"name":s1.name,"score":score})
    s2 = Student.query.filter(Student.s_id == ag.s_id_2).first()
    se2 = StudentExam.query.filter(StudentExam.exam_id == exam_id, StudentExam.s_id==s2.s_id).first()
    if se2:
        score = se2.score
    else:
        score = None
    group.append({"id":ag.s_id_2,"name":s2.name,"score":score})
    if ag.s_id_3:
        s3 = Student.query.filter(Student.s_id == ag.s_id_3).first()
        se3 = StudentExam.query.filter(StudentExam.exam_id == exam_id, StudentExam.s_id==s3.s_id).first()
        if se3:
            score = se3.score
        else:
            score = None
        group.append({"id":ag.s_id_3,"name":s3.name,"score":score})
    return jsonify({'code':200,'message':"请求成功",'data':group})
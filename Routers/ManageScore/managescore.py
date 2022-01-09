from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import *
import dbManage
from Routers import Role
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
import random
from Routers import Role
from sqlalchemy import and_, or_

manageScoreRoute = Blueprint('manageScoreRoute', __name__)
CORS(manageScoreRoute, resources=r'/*')	

@manageScoreRoute.route('/tea/score',methods=['POST'])
def teaScore():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    class_id = data['class_id']
    class_ = Class.query.filter(Class.class_id == class_id).first()
    sc = StudentClass.query.filter(StudentClass.class_id == class_id).all()
    s_list = []
    for sc_item in sc:
        s_list.append(sc_item.s_id)
    exs = Experiment.query.filter(Experiment.course_id == class_.course_id).all()
    t = []
    name = []
    for e in exs:
        e_id = e.experiment_id
        name.append(e.experiment_title)
        se = StudentExperiment.query.filter(StudentExperiment.experiment_id == e_id).all()
        e = 0
        g = 0
        m = 0
        p = 0
        f = 0
        n = 0
        temp = []
        for s in se:
            if s.s_id not in s_list:
                pass
            if not s.score:
                n += 1
            else:
                if s.score >= 90:
                    e += 1
                elif s.score >= 80:
                    g += 1
                elif s.score >= 70:
                    m += 1
                elif s.score >=60:
                    p += 1
                else:
                    f += 1
        temp.append(e)
        temp.append(g)
        temp.append(m)
        temp.append(p)
        temp.append(f)
        temp.append(n)
        t.append(temp)
    return jsonify({'code':200,'message':"请求成功",'name':name, 'count':t})

@manageScoreRoute.route('/weight/set',methods=['POST'])
def setWeight():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    course_id = data['course_id']
    exam_weight = data['exam_weight']
    experiment_weight = data['experiment_weight']
    attendence_weight = data['attendence_weight']
    sw = ScoreWeight.query.filter(ScoreWeight.course_id == course_id).first()
    if sw:
        sw.exam_weight = exam_weight
        sw.experiment_weight = experiment_weight
        sw.attendence_weight = attendence_weight
    else:
        sw = ScoreWeight(course_id = course_id, exam_weight = exam_weight, experiment_weight = experiment_weight, attendence_weight = attendence_weight)
        db.session.add(sw)
    db.session.commit()
    return jsonify({'code':200,'message':"请求成功",'data' : None})

@manageScoreRoute.route('/weight/get',methods=['POST'])
def getWeight():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    course_id = data['course_id']
    sw = ScoreWeight.query.filter(ScoreWeight.course_id == course_id).first()
    if sw:
        return jsonify({'code':200,'message':"请求成功",'data' : {"exam_weight":sw.exam_weight, "experiment_weight":sw.experiment_weight, "attendence_weight":sw.attendence_weight}})
    else:
        return jsonify({'code':500,'message':"课程不存在",data : None})
    
#学生获得实验报告分
@manageScoreRoute.route('/student/getAllExScore',methods=['POST'])  
def getAllExScore():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    #class_id = data['class_id']   #课程号
    course_id = data["course_id"]
    s_id = data["s_id"]
    #course_id = class_id[:-1]
    this_course = Course.query.filter(Course.c_id==course_id).first()
    if not this_course:
        return jsonify({'status':400,'message':"该课程不存在"})

    ex_list = Experiment.query.filter(Experiment.course_id==course_id).all()
    result = []
    seq = 1
    for item in ex_list:
        if item.status != 0:
            stu_ex_item = StudentExperiment.query.filter(and_(StudentExperiment.experiment_id==item.experiment_id,StudentExperiment.s_id==s_id)).first()
            #学生有这个实验
            if stu_ex_item:
                if not stu_ex_item.score:
                    score = 0
                else:
                    score = stu_ex_item.score
                last_score = item.weight*score
                #result_item = {"name":item.experiment_title,"value":last_score}
                result_item = {"seq":seq,"title":item.experiment_title,"weight":item.weight,"score":score}
                result.append(result_item)
                seq += 1
    
    return jsonify({'status':200,'message':"获取成功",'data':result})


#学生获得出勤分
@manageScoreRoute.route('/student/getSubmitEx',methods=['POST'])  
def getSubmitEx():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    course_id = data["course_id"]
    s_id = data["s_id"]
    this_course = Course.query.filter(Course.c_id==course_id).first()
    this_student = Student.query.filter(Student.s_id==s_id).first()

    if not this_student:
        return jsonify({'status':400,'message':"该学生不存在"})
    if not this_course:
        return jsonify({'status':400,'message':"该课程不存在"})

    ex_list = Experiment.query.filter(Experiment.course_id==course_id).all()   #获得该课程的所有实验报告数量
    all_ex_num = len(ex_list)

    result = []
    seq = 1
    for item in ex_list:
        if item.status != 0:
            stu_ex_item = StudentExperiment.query.filter(and_(StudentExperiment.experiment_id==item.experiment_id,StudentExperiment.s_id==s_id)).first()
            #学生有这个实验,并提交了报告
            if stu_ex_item.submitTime:    #存在提交时间

                result_item = {"seq":seq,"title":item.experiment_title,"is_submit":1} #已提交
                result.append(result_item)
                seq += 1
            else:   #学生并没有提交这个报告
                result_item = {"seq":seq,"title":item.experiment_title,"is_submit":0} #未提交
                result.append(result_item)
                seq += 1

    return jsonify({'status':200,'message':"获取成功",'data':result})


#学生获得考试分
@manageScoreRoute.route('/student/getExamScore',methods=['POST'])  
def getExamScore():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    course_id = data["course_id"]
    s_id = data["s_id"]
    this_course = Course.query.filter(Course.c_id==course_id).first()
    this_student = Student.query.filter(Student.s_id==s_id).first()
    
    if not this_student:
        return jsonify({'status':400,'message':"该学生不存在"})
    if not this_course:
        return jsonify({'status':400,'message':"该课程不存在"})

    exam_list = Exam.query.filter(and_(Exam.course_id == course_id,Exam.status == 1)).all()   #寻找所有该课程可以参加的考试

    seq = 1
    result = []
    for exam_item in exam_list:
        stu_exam = StudentExam.query.filter(StudentExam.exam_id == exam_item.exam_id).first()
        if stu_exam:   #学生参与了该考试，得到分数

            result_item = {"seq":seq,"title":exam_item.title,"stu_score":stu_exam.score,"all_score":exam_item.score}
            result.append(result_item)
            seq += 1
        else:   #学生并未参与考试
            result_item = {"seq":seq,"title":exam_item.title,"stu_score":0,"all_score":exam_item.score}
            result.append(result_item)
            seq += 1

    return jsonify({'status':200,'message':"获取成功",'data':result})



#学生获得课程总评
@manageScoreRoute.route('/student/getCourseScore',methods=['POST'])  
def getCourseScore():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    course_id = data["course_id"]
    s_id = data["s_id"]
    this_course = Course.query.filter(Course.c_id==course_id).first()
    this_student = Student.query.filter(Student.s_id==s_id).first()
    this_weight = ScoreWeight.query.filter(ScoreWeight.course_id == course_id).first()
    if not this_student:
        return jsonify({'status':400,'message':"该学生不存在"})
    if not this_course:
        return jsonify({'status':400,'message':"该课程不存在"})

    ex_list = Experiment.query.filter(and_(Experiment.course_id==course_id,Experiment.status != 0)).all()   #获得该课程的所有实验报告数量
    ex_score = 0
    duty_score = 0
    stu_exam_score = 0
    all_ex_num = len(ex_list)
    take_ex_num = 0
    ex_all_score = 0
    

    for item in ex_list:
        if item.status != 0:
            stu_ex_item = StudentExperiment.query.filter(and_(StudentExperiment.experiment_id==item.experiment_id,StudentExperiment.s_id==s_id)).first()
            #学生有这个实验,并提交了报告
            if stu_ex_item.submitTime:    #存在提交时间
                take_ex_num += 1

    #计算出勤占比
    duty_score = (take_ex_num/all_ex_num) * (this_weight.attendence_weight * 100)

    for item in ex_list:
        stu_ex_item = StudentExperiment.query.filter(and_(StudentExperiment.experiment_id==item.experiment_id,StudentExperiment.s_id==s_id)).first()
        #学生有这个实验
        if stu_ex_item:
            if not stu_ex_item.score:
                score = 0
            else:
                score = stu_ex_item.score
            last_score = item.weight*score    #实验权重*实验得分=该实验最终总分 
            ex_score += last_score
    #计算实验分数
    ex_score = ex_score * this_weight.experiment_weight

    exam_list = Exam.query.filter(and_(Exam.course_id == course_id,Exam.status == 1)).all()   #寻找所有该课程可以参加的考试

    for exam_item in exam_list:
        stu_exam = StudentExam.query.filter(StudentExam.exam_id == exam_item.exam_id).first()
        if stu_exam:   #学生参与了该考试，得到分数
            stu_score = stu_exam.score
            stu_exam_score += stu_score
        else:   #学生并未参与考试
            stu_score = 0
            stu_exam_score += stu_score
        ex_all_score += exam_item.score  #每次考试的总分加起来

    exam_score = (stu_exam_score/ex_all_score) * 100 * this_weight.exam_weight
    result = {"attendence_score":duty_score,"ex_score":ex_score,"exam_score":exam_score}

    return jsonify({'status':200,'message':"获取成功",'data':result})



    

    

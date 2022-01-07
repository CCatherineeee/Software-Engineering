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

manageScoreRoute = Blueprint('manageScoreRoute', __name__)
CORS(manageScoreRoute, resources=r'/*')	

@manageScoreRoute.route('/tea/score',methods=['POST'])
def teaScore():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    class_id = data['class_id']
    class_ = Class.query.filter(Class.class_id == class_id).first()
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
    return jsonify({'code':200,'message':"请求成功",data : None})
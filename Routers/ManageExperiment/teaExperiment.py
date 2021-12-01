import re
from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
from flask import Blueprint
import json
from Model.Model import Class,StudentClass,Teacher,Student,TeachingAssistant,TAClass, Experiment,StudentExperiment
import dbManage
from sqlalchemy import and_, or_
import os
import xlrd
import uuid
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

teaExperimentRoute = Blueprint('teaExperimentRoute', __name__)
CORS(teaExperimentRoute, resources=r'/*')


basepath = os.path.dirname(__file__)

@teaExperimentRoute.route('/tea/Ex/getReport/',methods=['POST'])  
def getReport():
    data = request.form
    s_id = data['s_id']
    ex_id = data['ex_id']
    se = StudentExperiment.query.filter(StudentExperiment.experiment_id == ex_id,StudentExperiment.s_id == s_id).first()
    path = os.path.join(basepath,'StudentExFile',ex_id)
    filename = se.file_url.split(path+'/')[1]    
    return send_from_directory(path,filename,as_attachment=True)

@teaExperimentRoute.route('/tea/Ex/scoreReport/',methods=['POST'])  
def scoreReport():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    t_id = data['t_id']  #批改的老师的id
    s_id = data['s_id']
    ex_id = data['ex_id']
    score = data['score']
    se = StudentExperiment.query.filter(StudentExperiment.experiment_id == ex_id,StudentExperiment.s_id == s_id).first()
    se.score = score
    teacher = Teacher.query.filter(Teacher.t_id==t_id).first()
    se.grader = teacher.name
    dbManage.db.session.commit()
    return "success"


@teaExperimentRoute.route('/tea/Ex/taScoreReport/',methods=['POST'])  
def taScoreReport():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ta_id = data['ta_id']  #批改的老师的id
    s_id = data['s_id']
    ex_id = data['ex_id']
    score = data['score']
    se = StudentExperiment.query.filter(StudentExperiment.experiment_id == ex_id,StudentExperiment.s_id == s_id).first()
    se.score = score
    ta = TeachingAssistant.query.filter(TeachingAssistant.ta_id==ta_id).first()
    se.grader = ta.name
    dbManage.db.session.commit()
    return "success"
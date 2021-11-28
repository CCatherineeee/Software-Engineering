import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Blueprint
import json
from Model.Model import Class,StudentClass,Teacher,Student,TeachingAssistant,TAClass, Experiment
import dbManage
from sqlalchemy import and_, or_
import os
import xlrd
import uuid
import datetime

manageExperimentRoute = Blueprint('manageExperimentRoute', __name__)
CORS(manageExperimentRoute, resources=r'/*')	

@manageExperimentRoute.route('/course/addEx/',methods=['POST'])  
def addEx():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    course_id = data['course_id']
    title = data['title']
    brief = data['brief']
    end_time = data['end_time']
    weight = data['weight']
    end_time = datetime.datetime.strptime(end_time, "%m-%d-%Y %H:%M:%S")
    exs = Experiment.query.filter(Experiment.course_id == course_id).all()
    sw = 0
    for ex in exs:
        sw = sw + ex.weight
    if sw + weight > 1:
        return "WeightUnreasonable"
    experiment = Experiment(course_id = course_id, experiment_title = title, experiment_brief = brief, end_time = end_time, status = 0, weight = weight)
    dbManage.db.session.add(experiment) 
    dbManage.db.session.commit()
    return "success"

@manageExperimentRoute.route('/course/getEx/',methods=['GET'])  
def getEx():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    c_id = data['c_id']
    exs = Experiment.query.filter(Experiment.course_id == c_id).all()
    content = []
    for ex in exs:
        temp = {'ex_id':ex.experiment_id, 'title':ex.experiment_title,'brief':ex.experiment_brief,"create_time" : ex.create_time,"end_time" : ex.end_time, "weight":ex.weight, "status":ex.status}
        content.append(temp)
    return jsonify(content)


@manageExperimentRoute.route('/course/delEx/',methods=['POST'])  
def delEx():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    ex = Experiment.query.filter(Experiment.experiment_id == ex_id).first()
    dbManage.db.session.delete(ex) 
    dbManage.db.session.commit()
    return "success"

@manageExperimentRoute.route('/course/editEx/',methods=['POST'])  
def editEx():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    title = data['title']
    brief = data['brief']
    end_time = data['end_time']
    weight = data['weight']
    status = data['status']
    end_time = datetime.datetime.strptime(end_time, "%m-%d-%Y %H:%M:%S")
    new_ex = Experiment.query.filter(Experiment.experiment_id == ex_id).first()

    exs = Experiment.query.filter(Experiment.course_id == new_ex.course_id).all()
    sw = 0
    for ex in exs:
        sw = sw + ex.weight
    if sw - new_ex.weight + weight > 1:
        return "WeightUnreasonable"

    new_ex.experiment_title = title
    new_ex.experiment_brief = brief
    new_ex.weight = weight
    new_ex.status = status
    new_ex.end_time = end_time

    dbManage.db.session.commit()
    return "success"
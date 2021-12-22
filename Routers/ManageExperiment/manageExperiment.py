import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Blueprint
import json
from Model.Model import Class,StudentClass,Teacher,Student,TeachingAssistant,TAClass, Experiment,StudentExperiment
import dbManage
from sqlalchemy import and_, or_, func
import os
import xlrd
import uuid
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Routers import Role
from flask_cors import cross_origin


manageExperimentRoute = Blueprint('manageExperimentRoute', __name__)
CORS(manageExperimentRoute, resources=r'/*')	

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


@manageExperimentRoute.route('/course/addEx/',methods=['POST'])  
@cross_origin(supports_credentials=True)
def addEx():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        course_id = data['courseID']
        title = data['title']
        brief = data['brief']
        end_time = data['end_time']
        weight = float(data['weight'])
        ex_type = data['ex_type']
        is_online = eval(data['is_online'])
        
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        exs = Experiment.query.filter(Experiment.course_id == course_id).all()
        sw = 0
        for ex in exs:
            sw = sw + ex.weight
        if sw + weight > 1:
            return jsonify({'code':501,'message':"权重不合理",'data':None})
        experiment = Experiment(course_id = course_id, experiment_title = title, experiment_brief = brief, end_time = end_time, status = 0, weight = weight, ex_type = ex_type, is_online = is_online)
        dbManage.db.session.add(experiment) 
        dbManage.db.session.commit()

        exs = Experiment.query.filter(Experiment.course_id == course_id).all()
        new_ex_id = exs[len(exs)-1].experiment_id
        classes = Class.query.filter(Class.course_id == course_id).all()
        for c in classes:
            scs = StudentClass.query.filter(StudentClass.class_id == c.class_id).all()
            for sc in scs:
                se = StudentExperiment(experiment_id = new_ex_id,s_id = sc.s_id)
                dbManage.db.session.add(se) 
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"成功",'data':None})

@manageExperimentRoute.route('/course/getEx/',methods=['POST'])  
def getEx():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    c_id = data['c_id']
    exs = Experiment.query.filter(Experiment.course_id == c_id).all()
    content = []
    for ex in exs:
        now_time = datetime.datetime.now()
        if now_time > ex.end_time:
            status = 3
            ex.status = 3
            dbManage.db.session.commit()
        else:
            status = ex.status
        temp = {'ex_id':ex.experiment_id, 'title':ex.experiment_title,'brief':ex.experiment_brief,"create_time" : str(ex.create_time),"end_time" :str(ex.end_time), "weight":ex.weight, "status":status, 'ex_type' :ex.ex_type}
        content.append(temp)
    return jsonify({'code':200,'message':"成功",'data':content})


@manageExperimentRoute.route('/course/delEx/',methods=['POST'])  
def delEx():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        ex = Experiment.query.filter(Experiment.experiment_id == ex_id).first()
        dbManage.db.session.delete(ex) 
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"删除成功",'data':None})

@manageExperimentRoute.route('/course/editEx/',methods=['POST'])  
def editEx():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        ex_id = data['ex_id']
        title = data['title']
        brief = data['brief']
        end_time = data['end_time']
        weight = float(data['weight'])
        status = data['status']
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        new_ex = Experiment.query.filter(Experiment.experiment_id == ex_id).first()

        exs = Experiment.query.filter(Experiment.course_id == new_ex.course_id).all()
        sw = 0
        for ex in exs:
            sw = sw + ex.weight
        if sw - new_ex.weight + weight > 1:
           return jsonify({'code':501,'message':"权重不合理",'data':None})

        new_ex.experiment_title = title
        new_ex.experiment_brief = brief
        new_ex.weight = weight
        new_ex.status = status
        new_ex.end_time = end_time

        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"成功",'data':None})

@manageExperimentRoute.route('/course/pushEx/',methods=['POST'])  
def pushEx():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        ex = Experiment.query.filter(Experiment.experiment_id == ex_id).first()
        
        ex.status = 1
        
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"发布成功",'data':None})

@manageExperimentRoute.route('/course/stopEx/',methods=['POST'])  
def stopEx():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        ex = Experiment.query.filter(Experiment.experiment_id == ex_id).first()
        
        ex.status = 0
        
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"发布成功",'data':None})

@manageExperimentRoute.route('/course/getExById/',methods=['POST'])  
def getExById():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    ex = Experiment.query.filter(Experiment.experiment_id == ex_id).first()
    now_time = datetime.datetime.now()
    if now_time > ex.end_time:
        status = 3
        ex.status =3
        dbManage.db.session.commit()
    else:
        status = ex.status
    temp = {'ex_id':ex.experiment_id, 'title':ex.experiment_title,'brief':ex.experiment_brief,"create_time" : str(ex.create_time),"end_time" :str(ex.end_time), "weight":ex.weight, "status":status, 'ex_type' :ex.ex_type}
    return jsonify({'code':200,'message':"请求成功",'data':temp})
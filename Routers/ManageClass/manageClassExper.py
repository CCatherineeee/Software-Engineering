from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import *
import dbManage
from sqlalchemy import and_, or_
import os,datetime
from flask import current_app
import uuid
from Routers import Role

manageExperRoute = Blueprint('manageExperRoute', __name__)
CORS(manageExperRoute, resources=r'/*')	

@manageExperRoute.route('/exper/getClassExper',methods=['get'])  
def getClassExper():
    class_id = request.args.get('class_id')
    class_ = Class.query.filter(Class.class_id == class_id).first()
    exs = Experiment.query.filter(Experiment.course_id == class_.course_id).all()
    content = []
    for e in exs:
        e_id = e.experiment_id
        se = StudentExperiment.query.filter(StudentExperiment.experiment_id == e_id).all()
        t = []
        for s in se:
            temp = {"experiment_id":e.experiment_id, "experiment_title": e.experiment_title, "end_time": str(e.end_time), "status": e.status,'type':e.ex_type}
            if s.submitTime:
                temp.update({'isSubmit':"true"})
            else:
                temp.update({'isSubmit':"false"})
            temp.update({"upload_time":str(s.submitTime)})
            student = Student.query.filter(Student.s_id == s.s_id).first()
            temp.update({"s_id":s.s_id,"s_name":student.name})
            t.append(temp)
        content.append(t)
    return jsonify({'code':200,'message':"请求成功",'data':content})
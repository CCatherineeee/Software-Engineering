import re
from flask import Flask, request, jsonify,send_from_directory
from flask.globals import current_app
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

studentExperimentRoute = Blueprint('studentExperimentRoute', __name__)
CORS(studentExperimentRoute, resources=r'/*')


basepath = os.path.dirname(__file__)

def createFilePath(sID,exID,filename):
    ext = os.path.splitext(filename)[1]
    filename = os.path.splitext(filename)[0]
    path = os.path.join(basepath,'StudentExFile',exID)
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
    newFileName = sID + '_' + filename  + str(uuid.uuid1()) + ext
    path = os.path.join(path,newFileName)
    return path
    

@studentExperimentRoute.route('/Ex/stuUpload/',methods=['POST'])  
def uploadReport():
    report = request.files.get('report')
    data = request.form
    s_id = data['s_id']
    ex_id = data['ex_id']
    path = createFilePath(s_id,ex_id,report.filename)
    se = StudentExperiment.query.filter(StudentExperiment.experiment_id == ex_id,StudentExperiment.s_id == s_id).first()
    if se:
        if se.file_url:
            os.remove(se.file_url)
            se.file_url = path
        else :
            se.file_url = path
        report.save(path)
        dbManage.db.session.commit()
        return "success"
    else:
        return "NotExist"

@studentExperimentRoute.route('/Ex/getUpload/',methods=['POST'])  
def getReport():
    data = request.form
    s_id = data['s_id']
    ex_id = data['ex_id']
    s = Serializer('WEBSITE_SECRET_KEY', 60*30) # 60 secs by 30 mins
    token = s.dumps({'s_id': s_id,'ex_id':ex_id}).decode('utf-8') # encode user id 
    return token

@studentExperimentRoute.route('/Ex/showUpload/',methods=['POST'])  
def showReport():
    token = request.headers['Authorization']
    s = Serializer('WEBSITE_SECRET_KEY')
    try:
        s_id = s.loads(token)['s_id']
        ex_id = s.loads(token)['ex_id']
    except:
        return "Loss"
    se = StudentExperiment.query.filter(StudentExperiment.experiment_id == ex_id,StudentExperiment.s_id == s_id).first()
    path = os.path.join(basepath,'StudentExFile',ex_id)
    filename = se.file_url.split(path+'/')[1]    
    return send_from_directory(path,filename,as_attachment=True)


@studentExperimentRoute.route('/class/showEx/',methods=['POST'])  
def showEx():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    s_id = data['s_id']
    class_id = data['class_id']
    class_ = Class.query.filter(Class.class_id == class_id).first()
    course_id = class_.course_id
    Exs = Experiment.query.filter(Experiment.course_id == course_id).all()
    content = []
    for ex in Exs:
        now_time = datetime.datetime.now()
        if now_time > ex.end_time:
            status = 3
        else:
            status = ex.status
        se = StudentExperiment.query.filter(StudentExperiment.s_id == s_id, StudentExperiment.experiment_id == ex.experiment_id).first()
        temp = {"ex_id": ex.experiment_id, "experiment_title":ex.experiment_title, "experiment_brief":ex.experiment_brief, "end_time":str(ex.end_time), "weight":ex.weight, "score": se.score,"status": status}
        content.append(temp)
    return jsonify(content)
    
#学生下载实验模板

@studentExperimentRoute.route('/Ex/downloadExTemplate',methods=['POST'])  
def downloadExTemplate():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    experiment_id = data['experiment_id']

    ex = Experiment.query.filter(Experiment.experiment_id == experiment_id).first()
    if not ex:
        return jsonify({'status':400,'message':"该实验不存在"})
    experiment_path = current_app.config ["EXPERIMENT_UPLOAD_FOLDER"]
    template_name = ex.template_file
    return send_from_directory(experiment_path,template_name,as_attachment=True)
    #return jsonify({'tempUrl':template_url})

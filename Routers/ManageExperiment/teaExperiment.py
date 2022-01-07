import re
from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
from flask import Blueprint
import json
from Model.Model import Class,StudentClass,Teacher,Student,TeachingAssistant,TAClass, Experiment,StudentExperiment
import dbManage
from sqlalchemy import and_, or_
import os
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import datetime
from Routers import Role

teaExperimentRoute = Blueprint('teaExperimentRoute', __name__)
CORS(teaExperimentRoute, resources=r'/*')


basepath = os.path.dirname(__file__)

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

@teaExperimentRoute.route('/tea/Ex/getReport/',methods=['POST'])  
def getReport():
    data = request.form
    s_id = data['s_id']
    ex_id = data['ex_id']
    se = StudentExperiment.query.filter(StudentExperiment.experiment_id == ex_id,StudentExperiment.s_id == s_id).first()
    if not se.file_url:
        return jsonify({'code':500,'message':"未提交",'data':None})
    path = os.path.join(basepath,'StudentExFile',ex_id)
    filename = se.file_url.split(path+'/')[1]
    response = send_from_directory(path,filename,as_attachment=True)
    response.headers["Access-Control-Expose-Headers"] = "Content-disposition"  
    return response


@teaExperimentRoute.route('/tea/Ex/getReportList/',methods=['POST'])  
def getReportList():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    token = data['token']
    res1 = checkToken(token,Role.TeacherRole)
    res2 = checkToken(token,Role.TARole)
    if res1 == 301 or res2 == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res1 == 404 and res2 == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        path = os.path.join(basepath,'StudentExFile',str(ex_id))
        ses = StudentExperiment.query.filter(StudentExperiment.experiment_id == ex_id).all()
        content = []
        for se in ses:
            status = "否"
            if se.submitTime:
                status = "是"
            s = Student.query.filter(Student.s_id == se.s_id).first()
            temp = {"s_id" : se.s_id,"s_name":s.name,"score":se.score,"grader":se.grader,"submitTime":str(se.submitTime),"status":status}
            content.append(temp)
        return jsonify({'code':200,'message':"请求成功",'data':content})


@teaExperimentRoute.route('/tea/Ex/scoreReport/',methods=['POST'])  
def scoreReport():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    # t_id = data['t_id']  #批改的老师的id
    s_id = data['s_id']
    ex_id = data['ex_id']
    score = data['score']
    token = data['token']
    res1 = checkToken(token,Role.TeacherRole)
    res2 = checkToken(token,Role.TARole)
    if res1 == 301 or res2 == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res1 == 404 and res2 == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        se = StudentExperiment.query.filter(StudentExperiment.experiment_id == ex_id,StudentExperiment.s_id == s_id).first()
        se.score = score
        # teacher = Teacher.query.filter(Teacher.t_id==t_id).first()
        # se.grader = teacher.name
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"请求成功",'data':None})


@teaExperimentRoute.route('/tea/Ex/taScoreReport/',methods=['POST'])  
def taScoreReport():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ta_id = data['ta_id']  #批改的助教的id
    s_id = data['s_id']
    ex_id = data['ex_id']
    score = data['score']
    token = data['token']
    res = checkToken(token,Role.TARole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        se = StudentExperiment.query.filter(StudentExperiment.experiment_id == ex_id,StudentExperiment.s_id == s_id).first()
        se.score = score
        ta = TeachingAssistant.query.filter(TeachingAssistant.ta_id==ta_id).first()
        se.grader = ta.name
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"请求成功",'data':None})

#老师上传实验模板
@teaExperimentRoute.route('/tea/Ex/uploadTemplate',methods=['POST'])  
def uploadTemplate():
    template = request.files.get('template')
    data = request.form
    experiment_id = data['experiment_id']
    ex = Experiment.query.filter(Experiment.experiment_id == experiment_id).first()
    if not ex:
        return jsonify({'status':400,'message':"该实验不存在"})

    ext = os.path.splitext(template.filename)[1]
    filename = os.path.splitext(template.filename)[0]
    UPLOAD_FOLDER = current_app.config ["EXPERIMENT_UPLOAD_FOLDER"]

    nowtime = datetime.datetime.now().strftime("%Y-%m-%d")
    template.filename = filename+'_'+nowtime+ext
    #filepath = UPLOAD_FOLDER+template.filename
    template.save(UPLOAD_FOLDER+template.filename)
    ex.template_file = template.filename
    dbManage.db.session.commit()
    return jsonify({'status':200,'message':"上传模板成功"})
    
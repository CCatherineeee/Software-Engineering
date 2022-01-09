import re
from flask import Flask, request, jsonify,send_from_directory
from flask.globals import current_app
from flask_cors import CORS
from flask import Blueprint
import json
from Model.Model import Class,StudentClass,Teacher,Student,TeachingAssistant,TAClass, Experiment,StudentExperiment,Course,ExperimentReport
import dbManage
from sqlalchemy import and_, or_
import os
import xlrd
import uuid
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Routers import Role

studentExperimentRoute = Blueprint('studentExperimentRoute', __name__)
CORS(studentExperimentRoute, resources=r'/*')


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
    token = data['token']
    res = checkToken(token,Role.StudentRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        path = createFilePath(s_id,ex_id,report.filename)
        se = StudentExperiment.query.filter(StudentExperiment.experiment_id == ex_id,StudentExperiment.s_id == s_id).first()
        if se:
            if se.file_url:
                os.remove(se.file_url)
                se.file_url = path
            else :
                se.file_url = path
            se.submitTime = datetime.datetime.now()
            report.save(path)
            dbManage.db.session.commit()
            return jsonify({'code':200,'message':"提交成功",'data':None})
        else:
            return jsonify({'code':501,'message':"实验不存在",'data':None})

@studentExperimentRoute.route('/Ex/showUpload/',methods=['POST'])  
def showReport():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    s_id = data['s_id']
    ex_id = data['ex_id']

    se = StudentExperiment.query.filter(StudentExperiment.experiment_id == ex_id,StudentExperiment.s_id == s_id).first()
    if not se.file_url:
        return jsonify({'code':500,'message':"未提交",'data':None})
    path = os.path.join(basepath,'StudentExFile',str(ex_id))
    filename = se.file_url.split(path+'/')[1]    
    return send_from_directory(path,filename,as_attachment=True)


@studentExperimentRoute.route('/class/showEx/',methods=['POST'])  
def showEx():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    s_id = data['s_id']
    class_id = data['class_id']
    token = data['token']
    res = checkToken(token,Role.StudentRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
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
            if se.submitTime:
                is_submit = True
            else:
                is_submit = False
            temp = {"ex_id": ex.experiment_id, "experiment_title":ex.experiment_title, "experiment_brief":ex.experiment_brief, "end_time":str(ex.end_time), "weight":ex.weight, "score": se.score,"status": status,"type":ex.ex_type,"online":ex.is_online, 'is_submit':is_submit}
            content.append(temp)
        return jsonify({'code':200,'message':"无法访问页面",'data':content})
    
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

@studentExperimentRoute.route('/Ex/getClassAllScore',methods=['POST'])  
def getClassAllScore():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    class_id = data['class_id']
    s_id = data["s_id"]
    course_id = class_id[:-1]
    this_course = Course.query.filter(Course.c_id==course_id).first()
    if not this_course:
        return jsonify({'status':400,'message':"该课程不存在"})

    ex_list = Experiment.query.filter(Experiment.course_id==course_id).all()
    result = []
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
                result_item = {"name":item.experiment_title,"value":last_score}
                result.append(result_item)
    
    return jsonify({'status':200,'message':"获取成功",'data':result})

    
@studentExperimentRoute.route('/Ex/fillEx',methods=['POST'])  
def submitFilledReport():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    s_id = data["s_id"]
    goal = data['goal']
    device = data['device']
    step = data['step']
    process = data['process']
    result = data['result']
    er = ExperimentReport.query.filter(and_(ExperimentReport.s_id == s_id,ExperimentReport.ex_id == ex_id)).first()
    if not er:
        er = ExperimentReport(s_id = s_id, goal = goal, device = device, step = step, process = process, result = result,ex_id = ex_id)
        dbManage.db.session.add(er)  # 添加数据
    else:
        er.goal = goal
        er.device = device
        er.step = step
        er.process = process
        er.result = result
        er.ex_id = ex_id
        er.s_id = s_id
    dbManage.db.session.commit()
    se = StudentExperiment.query.filter(StudentExperiment.s_id == s_id, StudentExperiment.experiment_id == ex_id).first()
    se.report_id = er.report_id
    se.submitTime = datetime.datetime.now()
    dbManage.db.session.commit()
    
    return jsonify({'status':200,'message':"获取成功",'data':result})

@studentExperimentRoute.route('/Ex/cacheEx',methods=['POST'])  
def cacheFilledReport():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    s_id = data["s_id"]
    goal = data['goal']
    device = data['device']
    step = data['step']
    process = data['process']
    result = data['result']
    er = ExperimentReport.query.filter(and_(ExperimentReport.s_id == s_id,ExperimentReport.ex_id == ex_id)).first()
    if not er:
        er = ExperimentReport(s_id = s_id, goal = goal, device = device, step = step, process = process, result = result,ex_id = ex_id)
        dbManage.db.session.add(er)  # 添加数据
    else:
        er.goal = goal
        er.device = device
        er.step = step
        er.process = process
        er.result = result
        er.ex_id = ex_id
        er.s_id = s_id
    dbManage.db.session.commit()
    
    return jsonify({'status':200,'message':"获取成功",'data':result})



@studentExperimentRoute.route('/Ex/getFilledRort',methods=['POST'])  
def getFilledRort():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    s_id = data["s_id"]
    er = ExperimentReport.query.filter(and_(ExperimentReport.s_id == s_id,ExperimentReport.ex_id == ex_id)).first()
    if er:
        data = {"goal":er.goal, "device":er.device, "step":er.step, "process":er.process, "result":er.result}
    else:
        data = {"goal":"", "device":"", "step":"", "process":"", "result":""}
    
    return jsonify({'status':200,'message':"获取成功",'data':data})

@studentExperimentRoute.route('/Ex/checkFilled',methods=['POST'])  
def checkFilled():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    s_id = data["s_id"]
    er = ExperimentReport.query.filter(and_(ExperimentReport.s_id == s_id,ExperimentReport.ex_id == ex_id)).first()
    title = Experiment.query.filter(Experiment.experiment_id == ex_id).first().experiment_title
    data = {"goal":er.goal, "device":er.device, "step":er.step, "process":er.process, "result":er.result, "title":title}
    return jsonify({'status':200,'message':"获取成功",'data':data})

@studentExperimentRoute.route('/Ex/checkFileReport',methods=['POST'])  
def checkFileReport():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ex_id = data['ex_id']
    s_id = data["s_id"]
    se = StudentExperiment.query.filter(and_(StudentExperiment.s_id == s_id,StudentExperiment.ex_id == ex_id)).first()
    path = os.path.join(basepath,'StudentExFile',ex_id)
    filename = se.file_url.split(path+'/')[1]
    response = send_from_directory(path,filename,as_attachment=True)
    return response
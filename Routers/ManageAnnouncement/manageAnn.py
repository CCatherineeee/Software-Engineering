from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Student
from Model.Model import Teacher
from Model.Model import SystemAnnouncement,CourseAnnouncement
from sqlalchemy import and_, or_
import time
import dbManage
import datetime
from Routers import Role
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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

manageAnnRoute = Blueprint('manageAnnRoute', __name__)
CORS(manageAnnRoute, resources=r'/*')	


@manageAnnRoute.route('/sys/addAnn/',methods=['POST'])  
def addSysAnn():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    content = data['content']
    title = data['title']
    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期"})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面"})
    else:
        ann = SystemAnnouncement(title=title, content=content)
        dbManage.db.session.add(ann)  # 添加数据
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"添加成功"})

@manageAnnRoute.route('/sys/getAnn/',methods=['GET'])
def getSysAnn():
    annS = dbManage.db.session.query(SystemAnnouncement).all()
    content = []
    for ann in annS:
        temp = {'title':ann.title,'content':ann.content,'date':str(ann.create_time),'annoucement_id':ann.annoucement_id}
        content.append(temp)
    return jsonify(content)

@manageAnnRoute.route('/sys/delAnn/',methods=['POST'])
def delSysAnn():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    an_id = data['annoucement_id']
    token = data['token']
    res = checkToken(token,Role.AdminRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期"})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面"})
    else:
        ann = SystemAnnouncement.query.filter(SystemAnnouncement.annoucement_id == an_id).first()
        dbManage.db.session.delete(ann) 
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"删除成功"})

@manageAnnRoute.route('/course/addAnn/',methods=['POST'])  
def addCourseAnn():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    content = data['content']
    title = data['title']
    class_id = data['class_id']
    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期"})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面"})
    else:
        ann = CourseAnnouncement(title=title, content=content,class_id=class_id)
        dbManage.db.session.add(ann)  # 添加数据
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"添加成功"})

@manageAnnRoute.route('/course/getAnn/',methods=['POST'])
def getCourseAnn():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    class_id = data['class_id']
    annS = CourseAnnouncement.query.filter(CourseAnnouncement.class_id == class_id).all()
    content = []
    for ann in annS:
        temp = {'title':ann.title,'content':ann.content,'date':str(ann.create_time),'ann_id' : ann.annoucement_id}
        content.append(temp)
    return jsonify({'code':200,'message':"请求成功",'data':content})

@manageAnnRoute.route('/course/delAnn/',methods=['POST'])
def delCourseAnn():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    ann_id = data['ann_id']
    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期"})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面"})
    else:
        ann = CourseAnnouncement.query.filter(CourseAnnouncement.annoucement_id == ann_id).first()
        dbManage.db.session.delete(ann) 
        dbManage.db.session.commit()
        return jsonify({'code':200,'message':"删除成功"})
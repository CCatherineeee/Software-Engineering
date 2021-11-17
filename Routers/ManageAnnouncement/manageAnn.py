from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Student
from Model.Model import Teacher
from Model.Model import SystemAnnouncement
from sqlalchemy import and_, or_
import time
import dbManage
import datetime


manageAnnRoute = Blueprint('manageAnnRoute', __name__)
CORS(manageAnnRoute, resources=r'/*')	

@manageAnnRoute.route('/sys/addAnn/',methods=['POST'])  
def addSysAnn():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    content = data['content']
    title = data['title']
    ann = SystemAnnouncement(title=title, content=content)
    dbManage.db.session.add(ann)  # 添加数据
    dbManage.db.session.commit()
    return "success"

@manageAnnRoute.route('/sys/getAnn/',methods=['GET'])
def getSysAnn():
    annS = dbManage.db.session.query(SystemAnnouncement).all()
    content = []
    for ann in annS:
        temp = {'title':ann.title,'content':ann.content,'date':ann.create_time}
        content.append(temp)
    return jsonify(content)
from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint,current_app,make_response
import json
from Model.Model import Student,TeachingAssistant
from Model.Model import Teacher
from sqlalchemy import and_, or_
import time
import dbManage
import os

getUserInfoRoute = Blueprint('getUserInfoRoute', __name__)
CORS(getUserInfoRoute, resources=r'/*')	

@getUserInfoRoute.route('/getUserInfo/allUser/',methods=['GET'])  
def getUserInfo():
    students = dbManage.db.session.query(Student).all()
    teachers = dbManage.db.session.query(Teacher).all()
    tas = dbManage.db.session.query(TeachingAssistant).all()
    content = []
    for student in students:
        temp = {'id':student.s_id,'name':student.name,
            'phone_number':student.phone_number,'is_active':student.is_active,'email':student.email,'department':student.department,'role':1}
        content.append(temp)
    for teacher in teachers:
        temp = {'id':teacher.t_id,'name':teacher.name,
            'phone_number':teacher.phone_number,'is_active':teacher.is_active,'email':teacher.email,'department':teacher.department,'role':2}
        content.append(temp)
    for ta in tas:
        temp = {'id':ta.ta_id,'name':ta.name,'is_active':ta.is_active,'email':ta.email,'role':3}
        content.append(temp)
    return jsonify(content)

@getUserInfoRoute.route('/getUserInfo/Student/',methods=['GET'])  
def getStuentInfo():
    s_id = request.args.get('s_id')
    student = Student.query.filter(Student.s_id==s_id).first()
    temp = {}
    if student:
        temp = {'s_id':student.s_id,'name':student.name,
            'phone_number':student.phone_number,'is_active':student.is_active,'email':student.email,'department':student.department,'gender':student.gender}
    content = []
    content.append(temp)
    return jsonify(content)

@getUserInfoRoute.route('/getUserInfo/Teacher/',methods=['GET'])  
def getTeacherInfo():
    t_id = request.args.get('t_id')
    teacher = Teacher.query.filter(Teacher.t_id==t_id).first()
    temp = {}
    if teacher:
        temp = {'t_id':teacher.t_id,'name':teacher.name,
            'phone_number':teacher.phone_number,'is_active':teacher.is_active,'email':teacher.email,'department':teacher.department,'gender':teacher.gender}
    content = [] 
    content.append(temp)
    return jsonify(content)

@getUserInfoRoute.route('/getUserInfo/TA/',methods=['GET'])  
def getTAnfo():
    ta_id = request.args.get('ta_id')
    ta = TeachingAssistant.query.filter(TeachingAssistant.ta_id==ta_id).first()
    temp = {}
    if ta:
        temp = {'ta_id':ta.ta_id,'name':ta.name,
            'is_active':ta.is_active,'email':ta.email}
    content = [] 
    content.append(temp)
    return jsonify(content)

# show photo
@getUserInfoRoute.route('/getUserInfo/Student/showAvatar', methods=['POST'])
def showAvartar():
    if request.method == 'POST':
        data = request.form
        s_id = data['s_id']
        student = Student.query.filter(Student.s_id==s_id).first()
        if student is None:
            pic_url = {'url':"",'status':500,'message':"no student"}
        else:
            filename = student.avatar
            current_app.logger.debug('filename is %s' % filename)
            if filename:
                # image_data = open((current_app.config['AVATAR_UPLOAD_FOLDER']+filename), "rb").read()
                # response = make_response(image_data)
                # response.headers['Content-Type'] = 'image/png'
                # return response
                pic_url = {'url':'/static/avatar/'+filename,'status':200,'message':"Success"}
                return jsonify(pic_url)
            else:
                pic_url = {'url':"",'status':400,'message':"no avatar"}
            
        return jsonify(pic_url)
    else:
        pass
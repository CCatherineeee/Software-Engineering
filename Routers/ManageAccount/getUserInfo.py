from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Student
from Model.Model import Teacher
from sqlalchemy import and_, or_
import time
import dbManage

getUserInfoRoute = Blueprint('getUserInfoRoute', __name__)
CORS(getUserInfoRoute, resources=r'/*')	

@getUserInfoRoute.route('/getUserInfo/allUser/',methods=['GET'])  
def getUserInfo():
    students = dbManage.db.session.query(Student).all()
    teachers = dbManage.db.session.query(Teacher).all()
    content = []
    for student in students:
        temp = {'id':student.s_id,'name':student.name,
            'phone_number':student.phone_number,'is_active':student.is_active,'email':student.email,'department':student.department,'role':1}
        content.append(temp)
    for teacher in teachers:
        temp = {'id':teacher.t_id,'name':teacher.name,
            'phone_number':teacher.phone_number,'is_active':teacher.is_active,'email':teacher.email,'department':teacher.department,'role':2}
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
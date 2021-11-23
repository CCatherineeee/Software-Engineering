from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Student
from Model.Model import Teacher
from sqlalchemy import and_, or_
import time
import dbManage

deleteUserRoute = Blueprint('deleteUserRoute', __name__)
CORS(deleteUserRoute, resources=r'/*')	

@deleteUserRoute.route('/delete/student/',methods=['POST'])  
def deleteStudent():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    data = data['s_id']
    student = Student.query.filter(Student.s_id == data).first()    
    if not student:
        return "NotExist"
    dbManage.db.session.delete(student)
    dbManage.db.session.commit()
    return "Success"

@deleteUserRoute.route('/delete/teacher/',methods=['POST'])  
def deleteTeacher():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    data = data["t_id"]
    teacher = Teacher.query.filter(Teacher.t_id == data).first()    
    if not teacher:
        return "NotExist"
    dbManage.db.session.delete(teacher)
    dbManage.db.session.commit()
    return "Success"
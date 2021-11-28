import sys
sys.path.append('../')
from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
import Model.Model as Model
# import Model
from sqlalchemy import and_, or_
import os
import time
import uuid
import xlrd
from .myemail.sendEmail import send_email
import dbManage

addUserRoute = Blueprint('addUserRoute', __name__)
CORS(addUserRoute, resources=r'/*')	

def manageFile(uploadPath):
    workbook = xlrd.open_workbook(uploadPath)
    get_sheet_name = workbook.sheet_names()[0]
    sheet = workbook.sheet_by_name(get_sheet_name)
    ncols = sheet.ncols
    nrows = sheet.nrows
    for i in range(1, nrows):
        rowData = sheet.row_values(i)
        s_id = str(int(rowData[0]))
        if not Model.Student.query.filter(Model.Student.s_id == s_id).first():
            student = Model.Student(s_id=s_id, s_pwd=s_id, name=rowData[1], email=rowData[2])
            dbManage.db.session.add(student)
            dbManage.db.session.commit()
            send_email(rowData[2],0,student,0)
    


@addUserRoute.route('/Register/addStudent/',methods=['POST'])  
def addUser():
    fileList = request.files.getlist('file')

    for file in fileList:

        basepath = os.path.dirname(__file__)
        ext = os.path.splitext(file.filename)[1]
        filename = os.path.splitext(file.filename)[0]

        newFileName = filename + "_" + str(uuid.uuid1())  + ext

        uploadPath = os.path.join(basepath, 'userFile', newFileName)

        file.save(uploadPath)
        manageFile(uploadPath)
        os.remove(uploadPath)
    return "ok"

@addUserRoute.route('/Register/addSM/',methods=['POST'])  
def addStudentManually():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    name = data['name']
    s_id = data['id']
    email = data['email']

    user = Model.Student.query.filter(Model.Student.s_id == s_id).first()
    if user:
        return "UserIDExist"
    user = Model.Student.query.filter(Model.Student.email == email).first()
    if user:
        return "UserMailExist"
    else:
        student = Model.Student(s_id=s_id, s_pwd=s_id, name=name, email=email)
        dbManage.db.session.add(student)
        dbManage.db.session.commit()
        send_email(email,0,student,0)
        return "Success"



@addUserRoute.route('/Register/addTeacherManually/',methods=['POST'])  
def addTeacherManually():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    name = data['name']
    t_id = data['id']
    email = data['email']
    user = Model.Teacher.query.filter(Model.Teacher.t_id == t_id).first()
    if user:
        return "UserIDExist"
    user = Model.Teacher.query.filter(Model.Teacher.email == email).first()
    if user:
        return "UserMailExist"
    else:
        teacher = Model.Teacher(t_id=t_id,t_pwd=t_id,name=name,email=email)
        dbManage.db.session.add(teacher)
        dbManage.db.session.commit()
        send_email(email,0,teacher,1)
        return "Success"

#手动添加助教
@addUserRoute.route('/Register/addTAManually',methods=['POST'])  
def addTAManually():
    data = request.form
    name = data['name']
    ta_id = data['ta_id']
    email = data['email']

    user = Model.TeachingAssistant.query.filter(Model.TeachingAssistant.ta_id == ta_id).first()
    if user:
        return "UserIDExist"
    user = Model.TeachingAssistant.query.filter(Model.TeachingAssistant.email == email).first()
    if user:
        return "UserMailExist"
    else:
        ta = Model.TeachingAssistant(ta_id=ta_id, ta_pwd=ta_id, name=name, email=email)
        dbManage.db.session.add(ta)
        dbManage.db.session.commit()
        #send_email(email,0,ta)
        return "Success"
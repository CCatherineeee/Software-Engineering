from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model import Model
from sqlalchemy import and_, or_
import os
import time
import uuid

import xlrd
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
        if not Model.Student.query.filter(Model.Student.s_id == rowData[0]).first():
            student = Model.Student(s_id=rowData[0], s_pwd=rowData[0], name=rowData[1], email=rowData[2],is_active=0)
            dbManage.db.session.add(student)
            dbManage.db.session.commit()
    


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

@addUserRoute.route('/Register/addStudentManually/',methods=['POST'])  
def addStudentManually():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    name = data['name']
    s_id = data['id']
    email = data['email']
    user = Model.Student.query.filter(Model.Student.s_id == s_id).first()
    if user:
        return "UserExist"
    else:
        student = Model.Student(s_id=s_id, s_pwd=s_id, name=name, email=email,is_active=0)
        dbManage.db.session.add(student)
        dbManage.db.session.commit()
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
        return "UserExist"
    else:
        teacher = Model.Teacher(t_id=t_id, t_pwd=t_id, name=name, email=email,is_active=0)
        dbManage.db.session.add(teacher)
        dbManage.db.session.commit()
        return "Success"
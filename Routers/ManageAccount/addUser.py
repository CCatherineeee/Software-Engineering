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
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Routers import Role

addUserRoute = Blueprint('addUserRoute', __name__)
CORS(addUserRoute, resources=r'/*')	

def checkAdminToken(token,role):
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

def manageTeacher(uploadPath):
    workbook = xlrd.open_workbook(uploadPath)
    get_sheet_name = workbook.sheet_names()[0]
    sheet = workbook.sheet_by_name(get_sheet_name)
    ncols = sheet.ncols
    nrows = sheet.nrows
    for i in range(1, nrows):
        rowData = sheet.row_values(i)
        t_id = str(int(rowData[0]))
        if not Model.Teacher.query.filter(Model.Teacher.t_id == t_id).first():
            teacher = Model.Teacher(t_id=t_id, t_pwd=t_id, name=rowData[1], email=rowData[2])
            dbManage.db.session.add(teacher)
            send_email(rowData[2],0,teacher,1)
    dbManage.db.session.commit()


def manageTA(uploadPath):
    workbook = xlrd.open_workbook(uploadPath)
    get_sheet_name = workbook.sheet_names()[0]
    sheet = workbook.sheet_by_name(get_sheet_name)
    ncols = sheet.ncols
    nrows = sheet.nrows
    for i in range(1, nrows):
        rowData = sheet.row_values(i)
        s_id = str(int(rowData[0]))
        if not Model.TeachingAssistant.query.filter(Model.TeachingAssistant.ta_id == s_id).first():
            student = Model.TeachingAssistant(ta_id=s_id, ta_pwd=s_id, name=rowData[1], email=rowData[2])
            dbManage.db.session.add(student)
            dbManage.db.session.commit()
            send_email(rowData[2],0,student,2)
    


@addUserRoute.route('/Register/addStudent/',methods=['POST'])  
def addStudent():
    fileList = request.files.getlist('file')
    basepath = os.path.dirname(__file__)

    for file in fileList:

        ext = os.path.splitext(file.filename)[1]
        filename = os.path.splitext(file.filename)[0]

        newFileName = filename + "_" + str(uuid.uuid1())  + ext

        uploadPath = os.path.join(basepath, newFileName)

        file.save(uploadPath)
        manageFile(uploadPath)
        # os.remove(uploadPath)
    return jsonify({'code':200,'message':"添加成功",'data':None})

@addUserRoute.route('/Register/addTeacher/',methods=['POST'])  
def addTeacher():
    fileList = request.files.getlist('file')
    basepath = os.path.dirname(__file__)

    for file in fileList:
        ext = os.path.splitext(file.filename)[1]
        filename = os.path.splitext(file.filename)[0]

        newFileName = filename + "_" + str(uuid.uuid1())  + ext

        uploadPath = os.path.join(basepath, newFileName)

        file.save(uploadPath)
        manageTeacher(uploadPath)
        os.remove(uploadPath)
    return jsonify({'code':200,'message':"添加成功",'data':None})

@addUserRoute.route('/Register/addTA/',methods=['POST'])  
def addTA():
    fileList = request.files.getlist('file')
    basepath = os.path.dirname(__file__)

    for file in fileList:

        ext = os.path.splitext(file.filename)[1]
        filename = os.path.splitext(file.filename)[0]

        newFileName = filename + "_" + str(uuid.uuid1())  + ext

        uploadPath = os.path.join(basepath, newFileName)

        file.save(uploadPath)
        manageTA(uploadPath)
        os.remove(uploadPath)
    return jsonify({'code':200,'message':"添加成功",'data':None})

@addUserRoute.route('/Register/addSM/',methods=['POST'])  
def addStudentManually():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    name = data['name']
    s_id = data['id']
    email = data['email']
    token = data['token']
    res = checkAdminToken(token,Role.AdminRole)
    if res == 301:
        return jsonify({'code':res,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        user = Model.Student.query.filter(Model.Student.s_id == s_id).first()
        if user:
            return jsonify({'code':302,'message':"用户ID已存在",'data':None})
        user = Model.Student.query.filter(Model.Student.email == email).first()
        if user:
            return jsonify({'code':302,'message':"用户邮箱已被注册",'data':None})
        else:
            student = Model.Student(s_id=s_id, s_pwd=s_id, name=name, email=email)
            dbManage.db.session.add(student)
            dbManage.db.session.commit()
            send_email(email,0,student,0)
            return jsonify({'code':200,'message':"添加成功",'data':None})



@addUserRoute.route('/Register/addTeacherManually/',methods=['POST'])  
def addTeacherManually():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    name = data['name']
    t_id = data['id']
    email = data['email']
    token = data['token']
    res = checkAdminToken(token,Role.AdminRole)
    if res == 301:
        return jsonify({'code':res,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        user = Model.Teacher.query.filter(Model.Teacher.t_id == t_id).first()
        if user:
            return jsonify({'code':302,'message':"用户ID已存在",'data':None})
        user = Model.Teacher.query.filter(Model.Teacher.email == email).first()
        if user:
            return jsonify({'code':302,'message':"用户邮箱已被注册",'data':None})
        else:
            teacher = Model.Teacher(t_id=t_id,t_pwd=t_id,name=name,email=email)
            dbManage.db.session.add(teacher)
            dbManage.db.session.commit()
            send_email(email,0,teacher,1)
            return jsonify({'code':200,'message':"添加成功",'data':None})

#手动添加助教
@addUserRoute.route('/Register/addTAManually',methods=['POST'])  
def addTAManually():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    name = data['name']
    ta_id = data['ta_id']
    email = data['email']
    token = data['token']
    res = checkAdminToken(token,Role.AdminRole)
    if res == 301:
        return jsonify({'code':res,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        user = Model.TeachingAssistant.query.filter(Model.TeachingAssistant.ta_id == ta_id).first()
        if user:
            return jsonify({'code':302,'message':"用户ID已存在",'data':None})
        user = Model.TeachingAssistant.query.filter(Model.TeachingAssistant.email == email).first()
        if user:
            return jsonify({'code':302,'message':"用户邮箱已被注册",'data':None})
        else:
            ta = Model.TeachingAssistant(ta_id=ta_id, ta_pwd=ta_id, name=name, email=email)
            dbManage.db.session.add(ta)
            dbManage.db.session.commit()
            #send_email(email,0,ta)
            return jsonify({'code':200,'message':"添加成功",'data':None})
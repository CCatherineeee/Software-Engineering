import re
from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Class,StudentClass,Teacher,Student,TeachingAssistant,TAClass
import dbManage
from sqlalchemy import and_, or_
import os
import xlrd
import uuid



classAddStudentRoute = Blueprint('classAddStudentRoute', __name__)
CORS(classAddStudentRoute, resources=r'/*')	


#教师设置助教
@classAddStudentRoute.route('/classAddTA',methods=['POST'])  
def classAddTA():
    data = request.form

    ta_id = data['ta_id']  #课程号前缀
    class_id = data['class_id']

    this_ta = TeachingAssistant.query.filter(TeachingAssistant.ta_id == ta_id).first()
    this_class = Class.query.filter(Class.class_id == class_id).first()

    if this_ta and this_class:  #两个都存在
        ta_class = TAClass(class_id = this_class.class_id , ta_id=this_ta.ta_id)
        dbManage.db.session.add(ta_class)
        dbManage.db.session.commit()
        result = {'status':200,'message':'添加成功'}
    else:
        result = {'status':400,'message':'该班级或助教不存在'}
    return jsonify(result)


#教师手动导入学生
@classAddStudentRoute.route('/classAddStudentManually',methods=['POST'])  
def classAddStudentManually():
    data = request.form

    s_id = data['s_id']  #课程号前缀
    class_id = data['class_id']

    this_stu = Student.query.filter(Student.s_id == s_id).first()
    this_class = Class.query.filter(Class.class_id == class_id).first()

    if this_stu and this_class:  #两个都存在
        student_class = StudentClass(class_id = this_class.class_id , s_id=this_stu.s_id)
        dbManage.db.session.add(student_class)
        dbManage.db.session.commit()
        result = {'status':200,'message':'添加成功'}
    else:
        result = {'status':400,'message':'该班级或学生不存在'}
    return jsonify(result)

#教师表格添加学生
@classAddStudentRoute.route('/classAddStudentFile',methods=['POST'])  
def classAddStudentManually():
    fileList = request.files.getlist('file')
    class_id = request.form['class_id']

    for file in fileList:

        basepath = os.path.dirname(__file__)
        ext = os.path.splitext(file.filename)[1]
        filename = os.path.splitext(file.filename)[0]

        newFileName = filename + "_" + str(uuid.uuid1())  + ext

        uploadPath = os.path.join(basepath, 'userFile', newFileName)

        file.save(uploadPath)
        manageStudentFile(uploadPath)
        os.remove(uploadPath)
    return "ok"

def manageStudentFile(path):
    workbook = xlrd.open_workbook(path)
    get_sheet_name = workbook.sheet_names()[0]
    sheet = workbook.sheet_by_name(get_sheet_name)
    ncols = sheet.ncols
    nrows = sheet.nrows
    for i in range(1, nrows):
        rowData = sheet.row_values(i)
        if Student.query.filter(Student.s_id == rowData[0]).first():  #学生存在
            student_class_item = StudentClass(class_id ='class_id', s_id=rowData[0])
            dbManage.db.session.add(student_class_item)
        if i==nrows-1:
            dbManage.db.session.commit()
            result = {'status':200,'message':'添加完毕'}

        else:
            result = {'status':400,'message':rowData[0]+'不存在'}
            break
    return jsonify(result)
    
        


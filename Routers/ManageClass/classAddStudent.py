import re
from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Class,StudentClass,Teacher,Student,TeachingAssistant,TAClass,Experiment,StudentExperiment
import dbManage
from sqlalchemy import and_, or_
import os
import xlrd
import uuid
from Routers import Role
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


classAddStudentRoute = Blueprint('classAddStudentRoute', __name__)
CORS(classAddStudentRoute, resources=r'/*')	

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

#教师设置助教
@classAddStudentRoute.route('/classAddTA',methods=['POST'])  
def classAddTA():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    ta_id = data['ta_id']  #课程号前缀
    class_id = data['class_id']
    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        this_ta = TeachingAssistant.query.filter(TeachingAssistant.ta_id == ta_id).first()
        this_class = Class.query.filter(Class.class_id == class_id).first()
        if this_ta and this_class:  #两个都存在
            tc = TAClass.query.filter(and_(TAClass.ta_id == ta_id,TAClass.class_id == class_id)).first()
            if tc:
                return jsonify({'code':500,'message':"该助教已存在于课程",'data':None})
            ta_class = TAClass(class_id = this_class.class_id , ta_id=this_ta.ta_id)
            dbManage.db.session.add(ta_class)
            dbManage.db.session.commit()
            result = {'code':200,'message':'添加成功','data':None}
        else:
            result = {'code':400,'message':'该班级或助教不存在','data':None}
        return jsonify(result)


#教师手动导入学生
@classAddStudentRoute.route('/classAddStudentManually',methods=['POST'])  
def classAddStudentManually():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    s_id = data['s_id']  #课程号前缀
    class_id = data['class_id']
    token = data['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        sc = StudentClass.query.filter(StudentClass.class_id == class_id ,StudentClass.s_id == s_id).first()
        if sc:
            return jsonify({'code':401,'message':'学生已存在','data':None})

        this_stu = Student.query.filter(Student.s_id == s_id).first()
        this_class = Class.query.filter(Class.class_id == class_id).first()

        if this_stu and this_class:  #两个都存在
            student_class = StudentClass(class_id = this_class.class_id , s_id=this_stu.s_id)
            dbManage.db.session.add(student_class)
            dbManage.db.session.commit()
            course_id = this_class.course_id
            Exs = Experiment.query.filter(Experiment.course_id == course_id).all()
            selist = []
            for ex in Exs:
                se = StudentExperiment(experiment_id = ex.experiment_id,s_id = s_id)
                selist.append(se)
            dbManage.db.session.add_all(selist)
            dbManage.db.session.commit()
            result = {'code':200,'message':'添加成功','data':None}
        else:
            result = {'code':402,'message':'该班级或学生不存在','data':None}
        return jsonify(result)

#教师表格添加学生
@classAddStudentRoute.route('/classAddStudentFile',methods=['POST'])  
def classAddStudentFile():
    fileList = request.files.getlist('file')
    class_id = request.form['class_id']
    token = request.form['token']
    res = checkToken(token,Role.TeacherRole)
    if res == 301:
        return jsonify({'code':301,'message':"验证过期",'data':None})
    elif res == 404:
        return jsonify({'code':404,'message':"无法访问页面",'data':None})
    else:
        for file in fileList:

            basepath = os.path.dirname(__file__)
            ext = os.path.splitext(file.filename)[1]
            filename = os.path.splitext(file.filename)[0]

            newFileName = filename + "_" + str(uuid.uuid1())  + ext

            uploadPath = os.path.join(basepath, 'userFile', newFileName)

            file.save(uploadPath)
            result = manageStudentFile(uploadPath,class_id)
            os.remove(uploadPath)
        return jsonify(result)

def manageStudentFile(path,class_id):
    workbook = xlrd.open_workbook(path)
    get_sheet_name = workbook.sheet_names()[0]
    sheet = workbook.sheet_by_name(get_sheet_name)
    ncols = sheet.ncols
    nrows = sheet.nrows
    for i in range(1, nrows):
        rowData = sheet.row_values(i)
        s_id = str(int(rowData[0]))
        if Student.query.filter(Student.s_id == s_id).first():  #学生存在
            student_class_item = StudentClass(class_id =class_id, s_id=s_id)
            dbManage.db.session.add(student_class_item)
            if (i==nrows-1):
                dbManage.db.session.commit()
                result = {'code':200,'message':'添加完毕','data':None}
        else:
            result = {'code':400,'message':s_id+'不存在','data':None}
            break
    return jsonify(result)
    
        


from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Student
from Model.Model import Teacher
from sqlalchemy import and_, or_
import time
import dbManage

editUserInfoRoute = Blueprint('editUserInfoRoute', __name__)
CORS(editUserInfoRoute, resources=r'/*')	

@editUserInfoRoute.route('/editInfo/Student/',methods=['POST'])  
def editStudentInfo():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    name = data['name']
    s_id = data['s_id']
    email = data['email']
    gender = data['gender']
    phone_number = data['phone_number']

    # student = dbManage.db.session.query(Student).filter(Student.s_id == s_id)
    student = Student.query.filter(Student.s_id==s_id).first()
    if not student:
        return "NotExist"
    student.s_id = s_id
    student.name = name
    student.email = email
    student.gender = gender
    student.phone_number = phone_number

    dbManage.db.session.commit()
    return "Success"

@editUserInfoRoute.route('/editInfo/Teacher/',methods=['POST'])  
def editTeacherInfo():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    name = data['name']
    t_id = data['t_id']
    email = data['email']
    gender = data['gender']
    phone_number = data['phone_number']

    # student = dbManage.db.session.query(Student).filter(Student.s_id == s_id)
    teacher = Teacher.query.filter(Teacher.t_id==t_id).first()
    if not teacher:
        return "NotExist"
    teacher.t_id = t_id
    teacher.name = name
    teacher.email = email
    teacher.gender = gender
    teacher.phone_number = phone_number

    dbManage.db.session.commit()
<<<<<<< HEAD
    return "Success"

@editUserInfoRoute.route('/editInfo/Student/changePwd',methods=['POST'])  
def change_student_pwd():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    s_id = data['s_id']
    old_pwd = data['old_password']
    new_pwd = data['new_password']

    student = Student.query.filter(Student.s_id==s_id).first()
    if not student:
        return "NotExist"
    if(student.check_password(old_pwd)):
        student.password(new_pwd)
        dbManage.db.session.add(student)
        dbManage.db.session.commit()
        data = {'result':200,'message':'修改成功'}
    else:
        data = {'result':400,'message':'密码错误'}

    return jsonify(data)

@editUserInfoRoute.route('/editInfo/Teacher/changePwd',methods=['POST'])  
def change_teacher_pwd():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    t_id = data['t_id']
    old_pwd = data['old_password']
    new_pwd = data['new_password']
    
    teacher = Teacher.query.filter(Teacher.t_id==t_id).first()
    if not teacher:
        return "NotExist"
    if(teacher.check_password(old_pwd)):
        teacher.password(new_pwd)
        dbManage.db.session.add(teacher)
        dbManage.db.session.commit()
        data = {'result':200,'message':'修改成功'}
    else:
        data = {'result':400,'message':'密码错误'}

    return jsonify(data)

@editUserInfoRoute.route('/editInfo/Student/resetPwd',methods=['POST'])  
def reset_student_pwd():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    s_id = data['s_id']
    new_pwd = data['new_password']

    student = Student.query.filter(Student.s_id==s_id).first()
    if not student:
        data = {'result':400,'message':'重置失败'}
        return jsonify(data)
    
    student.password(new_pwd)
    dbManage.db.session.add(student)
    dbManage.db.session.commit()


    return jsonify(data)

@editUserInfoRoute.route('/editInfo/Teacher/resetPwd',methods=['POST'])  
def reset_teacher_pwd():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    t_id = data['t_id']
    new_pwd = data['new_password']

    teacher = Teacher.query.filter(Teacher.t_id==t_id).first()
    if not teacher:
        data = {'result':400,'message':'重置失败'}
        return jsonify(data)
    
    teacher.password(new_pwd)
    dbManage.db.session.add(teacher)
    dbManage.db.session.commit()
    data = {'result':200,'message':'重置成功'}

    return jsonify(data)
=======
    return "Success"
>>>>>>> remotes/origin/myserver

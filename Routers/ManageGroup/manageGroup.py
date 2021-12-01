import re
from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json

from sqlalchemy.sql.elements import Null
from Model.Model import Class,ClassGroup,StudentGroup,Student,StudentClass
import dbManage
from sqlalchemy import and_, or_
import os
import xlrd
import uuid



manageGroup = Blueprint('manageGroup', __name__)
CORS(manageGroup, resources=r'/*')	

#教师添加小组(先添加小组再添加学生)
@manageGroup.route('/group/addGroup',methods=['POST'])  
def addGroup():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    class_id = data['class_id']
    if not Class.query.filter(Class.class_id == class_id).first():  #班级不存在
        return jsonify({'status':400,'message':'班级不存在'})
    group_list = ClassGroup.query.filter(ClassGroup.class_id == class_id).all()
    seq_number = len(group_list)+1
    group = ClassGroup(class_id = class_id,seq_number = seq_number)
    dbManage.db.session.add(group)
    dbManage.db.session.commit()
    result = {'status':200,'message':'创建小组成功'}
    return jsonify(result)

#教师为小组添加学生(前端默认老师只能添加这个班级内的学生进入小组)
@manageGroup.route('/group/groupAddStudent',methods=['POST'])  
def groupAddStudent():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    group_id = data['group_id']
    s_id = data['s_id']
    group = ClassGroup.query.filter(ClassGroup.group_id == group_id).first()
    student = Student.query.filter(Student.s_id == s_id).first()

    if not (group and student):
        result = {'status':400,'message':'小组或学生不存在'}
        return result


    if StudentGroup.query.filter(and_(StudentGroup.group_id == group_id,StudentGroup.s_id==s_id)):
        result = {'status':500,'message':'小组已存在该学生'}
    studentGroup = StudentGroup(group_id = group_id,s_id=s_id)
    dbManage.db.session.add(studentGroup)
    dbManage.db.session.commit()
    result = {'status':200,'message':'小组添加学生成功'}
    return result
    
#教师指定组长
@manageGroup.route('/group/addLeader',methods=['POST'])  
def addLeader():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    group_id = data['group_id']
    s_id = data['s_id']

    group = ClassGroup.query.filter(ClassGroup.group_id == group_id).first()
    student = Student.query.filter(Student.s_id == s_id).first()
    if not (group and student):
        result = {'status':400,'message':'小组或学生不存在'}
        return result
    studentGroup = StudentGroup.query.filter(and_(StudentGroup.group_id == group_id,StudentGroup.s_id==s_id)).first()
    if not studentGroup:
        result = {'status':500,'message':'小组不存在该学生'}
        return result
    studentGroup.is_leader = 1
    dbManage.db.session.commit()
    result = {'status':200,'message':'设置组长成功'}
    return result
    
#教师删除小组
@manageGroup.route('/group/deleteGroup',methods=['POST'])  
def deleteGroup():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    group_id = data['group_id']
    group = ClassGroup.query.filter(ClassGroup.group_id == group_id).first()
    if not (group):
        result = {'status':400,'message':'小组不存在'}
    dbManage.db.session.delete(group) 
    dbManage.db.session.commit()
    result = {'status':200,'message':'删除成功'}
    return result
    

#教师删除小组成员（有改动的应该是小组-学生表）
@manageGroup.route('/group/changeGroup',methods=['POST'])  
def changeGroup():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    group_id = data['group_id']
    s_id = data['s_id']
    group = ClassGroup.query.filter(ClassGroup.group_id == group_id).first()
    student = Student.query.filter(Student.s_id == s_id).first()
    if not (group and student):
        result = {'status':400,'message':'小组或学生不存在'}
        return result
    studentGroup = StudentGroup.query.filter(and_(StudentGroup.group_id == group_id,StudentGroup.s_id ==s_id)).first()
    if not studentGroup:
        result = {'status':500,'message':'小组内没有成员'}
        return result
    dbManage.db.session.delete(studentGroup) 
    dbManage.db.session.commit()
    result = {'status':200,'message':'小组删除成员成功'}
    return result

#获取一个班级内的所有小组
@manageGroup.route('/group/getClassGroup',methods=['POST'])  
def getClassGroup():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    class_id = data['class_id']
    if not Class.query.filter(Class.class_id == class_id).first():  #班级不存在
        return jsonify({'status':400,'message':'班级不存在'})
    group_list = ClassGroup.query.filter(ClassGroup.class_id == class_id).all()
    result = []

    for item in group_list:
        leader_name = ''
        leader_id = ''
        studentgroup_list = StudentGroup.query.filter(StudentGroup.group_id==item.group_id).all()
        for stu_item in studentgroup_list:
            if stu_item.is_leader == 1:
               leader = Student.query.filter(Student.s_id==stu_item.s_id).first()
               leader_name = leader.name
               leader_id = leader.s_id
               break

        group_data = {'seq_number':item.seq_number,'leader_id':leader_id,'leader_name':leader_name} #获得小组序号和组长姓名
        result.append(group_data)

    return jsonify(result)

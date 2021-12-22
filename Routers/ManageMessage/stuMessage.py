import re
from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json

from sqlalchemy.sql.elements import Null
from Model.Model import Student,StudentMessage
import dbManage
from sqlalchemy import and_, or_,desc
import datetime




stuMessage = Blueprint('stuMessage', __name__)
CORS(stuMessage, resources=r'/*')	

#添加学生个人消息
@stuMessage.route('/message/addStuMessage',methods=['POST'])  
def addStuMessage():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    s_id = data['s_id']
    title = data['title']
    content = data['content']
    deadline = data['deadline']
    deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")


    student = Student.query.filter(Student.s_id==s_id).first()
    if not student:
        return jsonify({'status':400,'message':'找不到学生'})

    stuMessage = StudentMessage(s_id = s_id,title = title ,content = content, deadline = deadline)
    dbManage.db.session.add(stuMessage)
    dbManage.db.session.commit()
    result = {'status':200,'message':'成功添加'}
    return result

#更改学生个人消息状态（未读修改为已读）
@stuMessage.route('/message/changeStuMessage',methods=['POST'])  
def changeStuMessage():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    s_id = data['s_id']
    stu_message_id = data['stu_message_id']
    student = Student.query.filter(Student.s_id==s_id).first()
    if not student:
        return jsonify({'status':400,'message':'找不到学生'})

    stuMessage = StudentMessage.query.filter(StudentMessage.stu_message_id==stu_message_id).first()
    if not stuMessage:
        return jsonify({'status':500,'message':'该条消息不存在或被删除'})
    stuMessage.is_read = 1
    dbManage.db.session.commit()
    result = {'status':200,'message':'成功修改成已读'}
    return result

#获取学生所有个人信息（包括已读和未读，后端自动把已读的放在后面）
@stuMessage.route('/message/getStuMessage',methods=['POST'])  
def getStuMessage():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    s_id = data['s_id']
    student = Student.query.filter(Student.s_id==s_id).first()
    if not student:
        return jsonify({'status':400,'message':'找不到学生'})
    result = {}
    stuMessage_list = StudentMessage.query.filter(StudentMessage.s_id==s_id).order_by(desc('create_time')).all()
    read = []
    not_read = []  #优先未读，然后已读
    i = 0
    for item in stuMessage_list:

        data = {'stu_message_id':item.stu_message_id,'title':item.title,
        'content':item.content,'create_time':item.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        'is_read':item.is_read,'deadline':item.deadline.strftime("%Y-%m-%d %H:%M:%S"),'seq':str(i)}

        if item.is_read == 0:
            not_read.append(data)

        else:
            read.append(data)
        i+=1
        
    result["not_read"] = not_read
    result["read"] = read
    return jsonify(result)

#删除学生个人信息

@stuMessage.route('/message/deleteStuMessage',methods=['POST'])  
def deleteStuMessage():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    s_id = data['s_id']
    stu_message_id = data['stu_message_id']
    student = Student.query.filter(Student.s_id==s_id).first()
    if not student:
        return jsonify({'status':400,'message':'找不到学生'})

    stuMessage = StudentMessage.query.filter(StudentMessage.stu_message_id==stu_message_id).first()
    if not stuMessage:
        return jsonify({'status':500,'message':'该条消息不存在或被删除'})
    dbManage.db.session.delete(stuMessage)
    dbManage.db.session.commit()
    result = {'status':200,'message':'成功删除'}
    return result
    
    
    
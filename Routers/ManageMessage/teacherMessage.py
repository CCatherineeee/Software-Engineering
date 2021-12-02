import re
from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json

from sqlalchemy.sql.elements import Null
from Model.Model import Teacher,TeacherMessage
import dbManage
from sqlalchemy import and_, or_,desc




teacherMessage = Blueprint('teacherMessage', __name__)
CORS(teacherMessage, resources=r'/*')	

#添加教师个人消息
@teacherMessage.route('/message/addTeacherMessage',methods=['POST'])  
def addTeacherMessage():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    t_id = data['t_id']
    title = data['title']
    content = data['content']

    teacher = Teacher.query.filter(Teacher.t_id==t_id).first()
    if not teacher:
        return jsonify({'status':400,'message':'找不到教师'})

    teacherMessage = TeacherMessage(t_id = t_id,title = title ,content = content)
    dbManage.db.session.add(teacherMessage)
    dbManage.db.session.commit()
    result = {'status':200,'message':'成功添加'}
    return result

#更改教师个人消息状态（未读修改为已读）
@teacherMessage.route('/message/changeTeacherMessage',methods=['POST'])  
def changeTeacherMessage():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    t_id = data['t_id']
    tea_message_id = data['tea_message_id']
    teacher = Teacher.query.filter(Teacher.t_id==t_id).first()
    if not teacher:
        return jsonify({'status':400,'message':'找不到教师'})

    teacherMessage = TeacherMessage.query.filter(TeacherMessage.tea_message_id==tea_message_id).first()
    if not teacherMessage:
        return jsonify({'status':500,'message':'该条消息不存在或被删除'})
    teacherMessage.is_read = 1
    dbManage.db.session.commit()
    result = {'status':200,'message':'成功修改成已读'}
    return result

#获取教师所有个人信息（包括已读和未读，后端自动把已读的放在后面）
@teacherMessage.route('/message/getTeacherMessage',methods=['POST'])  
def getTeacherMessage():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    t_id = data['t_id']
    teacher = Teacher.query.filter(Teacher.t_id==t_id).first()
    if not teacher:
        return jsonify({'status':400,'message':'找不到教师'})
    result = {}
    teacherMessage_list = TeacherMessage.query.filter(TeacherMessage.t_id==t_id).order_by(desc('create_time')).all()
    read = []
    not_read = []  #优先未读，然后已读
    for item in teacherMessage_list:

        data = {'tea_message_id':item.tea_message_id,'title':item.title,
        'content':item.content,'create_time':item.create_time.strftime("%Y-%m-%d %H:%M:%S"),'is_read':item.is_read}

        if item.is_read == 0:
            not_read.append(data)

        else:
            read.append(data)

    result["not_read"] = not_read
    result["read"] = read
    return jsonify(result)

#删除老师个人信息

@teacherMessage.route('/message/deleteTeacherMessage',methods=['POST'])  
def deleteTeacherMessage():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    t_id = data['t_id']
    tea_message_id = data['tea_message_id']
    teacher = Teacher.query.filter(Teacher.t_id==t_id).first()
    if not teacher:
        return jsonify({'status':400,'message':'找不到教师'})

    teaMessage = TeacherMessage.query.filter(TeacherMessage.tea_message_id==tea_message_id).first()
    if not teaMessage:
        return jsonify({'status':500,'message':'该条消息不存在或被删除'})
    dbManage.db.session.delete(teaMessage)
    dbManage.db.session.commit()
    result = {'status':200,'message':'成功删除'}
    return result
    
    
    
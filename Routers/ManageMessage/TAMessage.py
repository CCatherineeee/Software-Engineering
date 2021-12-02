import re
from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json

from sqlalchemy.sql.elements import Null
from Model.Model import TAMessage,TeachingAssistant
import dbManage
from sqlalchemy import and_, or_,desc




TAMessageManage = Blueprint('TAMessageManage', __name__)
CORS(TAMessageManage, resources=r'/*')	

#添加助教个人消息
@TAMessageManage.route('/message/addTAMessage',methods=['POST'])  
def addTAMessage():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    ta_id = data['ta_id']
    title = data['title']
    content = data['content']

    ta = TeachingAssistant.query.filter(TeachingAssistant.ta_id==ta_id).first()
    if not ta:
        return jsonify({'status':400,'message':'找不到助教'})

    tAMessage = TAMessage(ta_id = ta_id,title = title ,content = content)
    dbManage.db.session.add(tAMessage)
    dbManage.db.session.commit()
    result = {'status':200,'message':'成功添加'}
    return result

#更改助教个人消息状态（未读修改为已读）
@TAMessageManage.route('/message/changeTAMessage',methods=['POST'])  
def changeTAMessage():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    ta_id = data['ta_id']
    ta_message_id = data['ta_message_id']
    ta = TeachingAssistant.query.filter(TeachingAssistant.ta_id==ta_id).first()
    if not ta:
        return jsonify({'status':400,'message':'找不到学生'})

    tAMessage = TAMessage.query.filter(TAMessage.ta_message_id==ta_message_id).first()
    if not TAMessage:
        return jsonify({'status':500,'message':'该条消息不存在或被删除'})
    tAMessage.is_read = 1
    dbManage.db.session.commit()
    result = {'status':200,'message':'成功修改成已读'}
    return result

#获取助教所有个人信息（包括已读和未读，后端自动把已读的放在后面）
@TAMessageManage.route('/message/getTAMessage',methods=['POST'])  
def getTAMessage():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    ta_id = data['ta_id']
    ta = TeachingAssistant.query.filter(TeachingAssistant.ta_id==ta_id).first()
    if not ta:
        return jsonify({'status':400,'message':'找不到助教'})
    result = {}
    tAMessage_list = TAMessage.query.filter(TAMessage.ta_id==ta_id).order_by(desc('create_time')).all()
    read = []
    not_read = []  #优先未读，然后已读
    for item in tAMessage_list:

        data = {'ta_message_id':item.ta_message_id,'title':item.title,
        'content':item.content,'create_time':item.create_time.strftime("%Y-%m-%d %H:%M:%S"),'is_read':item.is_read}

        if item.is_read == 0:
            not_read.append(data)

        else:
            read.append(data)

    result["not_read"] = not_read
    result["read"] = read
    return jsonify(result)

#删除助教个人信息

@TAMessageManage.route('/message/deleteTAMessage',methods=['POST'])  
def deleteTAMessage():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    ta_id = data['ta_id']
    ta_message_id = data['ta_message_id']
    ta = TeachingAssistant.query.filter(TeachingAssistant.ta_id==ta_id).first()
    if not ta:
        return jsonify({'status':400,'message':'找不到学生'})

    tAMessage = TAMessage.query.filter(TAMessage.ta_message_id==ta_message_id).first()
    if not TAMessage:
        return jsonify({'status':500,'message':'该条消息不存在或被删除'})
    dbManage.db.session.delete(tAMessage)
    dbManage.db.session.commit()
    result = {'status':200,'message':'成功删除'}
    return result
    
    
    
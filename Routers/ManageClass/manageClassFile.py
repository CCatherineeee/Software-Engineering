from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import ClassFile,Class
import dbManage
from sqlalchemy import and_, or_
import os,datetime
from flask import current_app



manageClassFileRoute = Blueprint('manageClassFileRoute', __name__)
CORS(manageClassFileRoute, resources=r'/*')	


#新增班级文件(只能传一个)
@manageClassFileRoute.route('/manageClassFileRoute/addClassFile',methods=['POST'])  
def addClassFile():
    file = request.files.getlist('file')[0]
    # class_id = request.args.get('class_id')
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    class_id =data['class_id']
    this_class = Class.query.filter(Class.class_id == class_id).first()
    if not this_class:  #班级不存在
        return jsonify({'status':500,'message':'班级不存在'})
    UPLOAD_FOLDER = current_app.config ["CLASSFILE_UPLOAD_FOLDER"]

    # ext = os.path.splitext(file.filename)[1]
    # filename = os.path.splitext(file.filename)[0]
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # newFileName = filename + ext
    filepath = '{}{}'.format(UPLOAD_FOLDER,file.filename)
    file.save(filepath)
    class_id = request.form['class_id']
    if not ClassFile.query.filter(ClassFile.file_url == filepath).first():
        classfile = ClassFile(class_id = class_id,file_url = filepath,file_name = file.filename,upload_time = nowtime)
        dbManage.db.session.add(classfile)
        dbManage.db.session.commit()
        result = {'status':200,'message':'上传成功'}
    else:
        result = {'status':400,'message':'文件已存在'}
    return jsonify(result)

#获取班级所有文件
@manageClassFileRoute.route('/manageClassFileRoute/getClassFile',methods=['POST'])  
def getClassFile():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    class_id =data['class_id']
    this_class = Class.query.filter(Class.class_id == class_id).first()
    if not this_class:  #班级不存在
        return jsonify({'file_url':'','filename':''})
    
    file_result = []
    class_file_list = ClassFile.query.filter(ClassFile.class_id == class_id).all()

    for item in class_file_list:
        file_item = {'file_url':"/static/classFile/"+item.file_name,'filename':item.file_name}
        file_result.append(file_item)

    return jsonify(file_result)

#根据文件名删除班级文件
@manageClassFileRoute.route('/manageClassFileRoute/deleteClassFile',methods=['POST'])  
def deleteClassFile():

    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    class_id =data['class_id']
    file_url = data['file_url']
    file_url = os.getcwd()+file_url
    class_file = ClassFile.query.filter(and_(ClassFile.class_id == class_id,ClassFile.file_url == file_url)).first()
    if class_file:
        dbManage.db.session.delete(class_file)
        os.remove(file_url)
        dbManage.db.session.commit()
        result = {'status':200,'message':'删除成功'}
    else:
        result = {'status':400,'message':'删除失败,班级或文件名不存在'}

    return jsonify(result)

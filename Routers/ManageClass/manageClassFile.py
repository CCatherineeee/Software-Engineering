from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import ClassFile,Class
import dbManage
from sqlalchemy import and_, or_
import os,datetime
from flask import current_app



manageClassRoute = Blueprint('manageClassRoute', __name__)
CORS(manageClassRoute, resources=r'/*')	


#新增班级文件
@manageClassRoute.route('/addClassFile',methods=['POST'])  
def addClassFile():
    file = request.files.getlist('file')
    class_id = request.form['class_id']
    this_class = Class.query.filter(Class.class_id == class_id).first()
    if not this_class:  #班级不存在
        return jsonify({'status':500,'message':'班级不存在'})
    UPLOAD_FOLDER = current_app.config ["CLASSFILE_UPLOAD_FOLDER"]

    ext = os.path.splitext(file.filename)[1]
    filename = os.path.splitext(file.filename)[0]
    newFileName = filename + "_" + datetime.datetime.now()  + ext
    filepath = '{}{}'.format(UPLOAD_FOLDER,newFileName)
    file.save(filepath)
    class_id = request.form['class_id']
    if not ClassFile.query.filter(ClassFile.file_url == filepath).first():
        classfile = ClassFile(class_id = class_id,file_url = filepath,file_name = newFileName)
        dbManage.db.session.add(classfile)
        dbManage.db.session.commit()
        result = {'status':200,'message':'上传成功'}
    else:
        result = {'status':400,'message':'文件已存在'}
    return jsonify(result)

#获取班级所有文件
@manageClassRoute.route('/getClassFile',methods=['POST'])  
def getClassFile():

    class_id = request.form['class_id']
    this_class = Class.query.filter(Class.class_id == class_id).first()
    if not this_class:  #班级不存在
        return jsonify({'status':500,'message':'班级不存在'})
    
    file_result = []
    class_file_list = ClassFile.query.filter(ClassFile.class_id == class_id).all()

    for item in class_file_list:
        file_item = {'fileurl':item.file_url,'filename':item.file_name}
        file_result.append(file_item)

    return jsonify(file_result)

#根据文件名删除班级文件
@manageClassRoute.route('/getClassFile',methods=['POST'])  
def getClassFile():

    class_id = request.form['class_id']
    file_name = request.form['file_name']

    class_file = ClassFile.query.filter(and_(ClassFile.class_id == class_id,ClassFile.file_name == file_name)).first()
    if class_file:
        dbManage.db.session.delete(class_file)
        dbManage.db.session.commit()
        result = {'status':200,'message':'删除成功'}
    else:
        result = {'status':400,'message':'删除失败,班级或文件名不存在'}

    return jsonify(result)

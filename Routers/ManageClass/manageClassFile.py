from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import ClassFile,Class
import dbManage
from sqlalchemy import and_, or_
import os,datetime
from flask import current_app
import uuid




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
        file_item = {'file_url':"/static/classFile/"+item.file_name,'filename':item.file_name,'date':str(item.upload_time),'id':item.file_id}
        file_result.append(file_item)

    return jsonify(file_result)

@manageClassFileRoute.route('/manageClassFileRoute/deleteClassFile',methods=['POST'])  
def deleteClassFile():

    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    class_id =data['class_id']
    file_id = data['id']
    class_file = ClassFile.query.filter(ClassFile.file_id == file_id).first()
    if class_file:
        dbManage.db.session.delete(class_file)
        os.remove(class_file.file_url)
        dbManage.db.session.commit()
        result = {'status':200,'message':'删除成功'}
    else:
        result = {'status':400,'message':'删除失败,班级或文件名不存在'}

    return jsonify(result)

basepath = "ClassFile"

def createFilePath(class_id,filename):
    ext = os.path.splitext(filename)[1]
    filename = os.path.splitext(filename)[0]
    path = os.path.join(basepath,class_id)
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
    newFileName = filename  + str(uuid.uuid1()) + ext
    path = os.path.join(path,newFileName)
    return path


@manageClassFileRoute.route('/manageClassFileRoute/addFile',methods=['POST'])  
def addClassFileList():
    filelist = request.files.getlist('files')
    data = request.form
    class_id =data.get('class_id')
    this_class = Class.query.filter(Class.class_id == class_id).first()
    if not this_class:  #班级不存在
        return jsonify({'status':500,'message':'班级不存在'})
    for f in filelist : 
        path = createFilePath(class_id,f.filename)
        f.save(path)
        classfile = ClassFile(class_id = class_id, file_url = path,file_name = f.filename)
        dbManage.db.session.add(classfile)
    dbManage.db.session.commit()
    result = {'status':200,'message':'上传成功'}
    return jsonify(result)

@manageClassFileRoute.route('/manageClassFileRoute/download/',methods=['POST'])  
def download():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    file_id = data['id']
    class_id = data['class_id']
    cf = ClassFile.query.filter(ClassFile.file_id == file_id).first()
    
    path = os.path.join(basepath,class_id)
    filename = cf.file_url.split(path+'/')[1]
    # filename = secure_filename(filename)

    response = send_from_directory(path,filename,as_attachment=True)
    response.headers["Access-Control-Expose-Headers"] = "Content-disposition"  
    return response

@manageClassFileRoute.route('/manageClassFileRoute/preview/',methods=['POST'])  
def preview():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    file_id = data['id']
    class_id = data['class_id']
    cf = ClassFile.query.filter(ClassFile.file_id == file_id).first()
    
    path = os.path.join(basepath,class_id)
    filename = cf.file_url.split(path+'/')[1]
    # filename = secure_filename(filename)

    response = send_from_directory(path,filename,as_attachment=False)
    response.headers["Access-Control-Expose-Headers"] = "Content-disposition"  
    return response
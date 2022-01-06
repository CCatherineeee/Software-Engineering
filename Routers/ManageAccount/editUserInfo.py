from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json

from skimage.util import dtype
from Model.Model import Admin, Student,TeachingAssistant
from Model.Model import Teacher
from sqlalchemy import and_, or_
from Routers import Role
import time
import dbManage
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_cors import cross_origin
import os
from skimage import io
from skimage import transform
import numpy as np

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
    return "Success"

@editUserInfoRoute.route('/editInfo/TA/',methods=['POST'])  
def editTAInfo():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    name = data['name']
    ta_id = data['ta_id']
    email = data['email']

    # student = dbManage.db.session.query(Student).filter(Student.s_id == s_id)
    ta = TeachingAssistant.query.filter(TeachingAssistant.ta_id==ta_id).first()
    if not ta:
        return "NotExist"
    ta.s_id = ta_id
    ta.name = name
    ta.email = email

    dbManage.db.session.commit()
    return "Success"

    
@editUserInfoRoute.route('/editInfo/Admin/',methods=['POST'])  
@cross_origin(supports_credentials=True)
def editAdminInfo():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    name = data['name']
    admin_id = data['admin_id']
    email = data['email']
    phone_number = data['phone_number']

    # student = dbManage.db.session.query(Student).filter(Student.s_id == s_id)
    admin = Admin.query.filter(Admin.admin_id==admin_id).first()
    if not admin:
        return "NotExist"
    admin.admin_id = admin_id
    admin.name = name
    admin.email = email
    admin.phone_number = phone_number

    dbManage.db.session.commit()
    return "Success"

@editUserInfoRoute.route('/editInfo/Student/changePwd',methods=['POST'])  
@cross_origin(supports_credentials=True)
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
        student.set_password(new_pwd)
        dbManage.db.session.add(student)
        dbManage.db.session.commit()
        data = {'code':200,'message':'修改成功','data':None}
    else:
        data = {'code':500,'message':'密码错误','data':None}

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
        teacher.set_password(new_pwd)
        dbManage.db.session.add(teacher)
        dbManage.db.session.commit()
        data = {'code':200,'message':'修改成功','data':None}
    else:
        data = {'code':500,'message':'密码错误','data':None}

    return jsonify(data)

@editUserInfoRoute.route('/editInfo/TA/changePwd',methods=['POST'])  

def change_ta_pwd():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    ta_id = data['ta_id']
    old_pwd = data['old_password']
    new_pwd = data['new_password']
    
    ta = TeachingAssistant.query.filter(TeachingAssistant.ta_id==ta_id).first()
    if not ta:
        return "NotExist"
    if(ta.check_password(old_pwd)):
        ta.set_password(new_pwd)
        dbManage.db.session.add(ta)
        dbManage.db.session.commit()
        data = {'code':200,'message':'修改成功'}
    else:
        data = {'code':500,'message':'密码错误','data':None}

    return jsonify(data)

@editUserInfoRoute.route('/editInfo/admin/changePwd',methods=['POST'])  

def change_admin_pwd():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    admin_id = data['admin_id']
    old_pwd = data['old_password']
    new_pwd = data['new_password']
    
    admin = Admin.query.filter(Admin.admin_id==admin_id).first()
    if not admin:
        return "NotExist"
    if(admin.admin_pwd==old_pwd):
        admin.admin_pwd = new_pwd
        dbManage.db.session.add(admin)
        dbManage.db.session.commit()
        data = {'code':200,'message':'修改成功'}
    else:
        data = {'code':500,'message':'密码错误','data':None}

    return jsonify(data)

@editUserInfoRoute.route('/editInfo/Student/resetPwd',methods=['POST'])  
def reset_student_pwd():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    s_id = data['s_id']
    new_pwd = data['new_password']

    student = Student.query.filter(Student.s_id==s_id).first()
    if not student:
        data = {'code':400,'message':'重置失败','data':None}
        return jsonify(data)
    
    student.set_password(new_pwd)
    dbManage.db.session.add(student)
    dbManage.db.session.commit()
    data = {'code':200,'message':'重置成功','data':None}


    return jsonify(data)

@editUserInfoRoute.route('/editInfo/Teacher/resetPwd',methods=['POST'])  
def reset_teacher_pwd():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    t_id = data['t_id']
    new_pwd = data['new_password']

    teacher = Teacher.query.filter(Teacher.t_id==t_id).first()
    if not teacher:
        data = {'code':400,'message':'重置失败','data':None}
        return jsonify(data)
    
    teacher.set_password(new_pwd)
    dbManage.db.session.add(teacher)
    dbManage.db.session.commit()
    data = {'code':200,'message':'重置成功','data':None}

    return jsonify(data)

@editUserInfoRoute.route('/editInfo/TA/resetPwd',methods=['POST'])  

def reset_ta_pwd():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    ta_id = data['ta_id']
    new_pwd = data['new_password']
    
    ta = TeachingAssistant.query.filter(TeachingAssistant.ta_id==ta_id).first()
    if not ta:
        return "NotExist"

    ta.set_password(new_pwd)
    dbManage.db.session.add(ta)
    dbManage.db.session.commit()
    data = {'code':200,'message':'修改成功'}

    return jsonify(data)



@editUserInfoRoute.route('/editInfo/uploadAvatar',methods=['POST'])  
@cross_origin(supports_credentials=True)
def upload_avatar():

    avatar = request.files['avatar']
    userID = request.form['id']
    token = request.form['token']
    try:
        s = Serializer('WEBSITE_SECRET_KEY')
        token_role = s.loads(token)['role']
    except:
        return False

    if avatar is None:
        result = {'code':400,'message':'未成功上传'}
    else:
        ext = os.path.splitext(avatar.filename)[1]
        fname = os.path.splitext(avatar.filename)[0]
        UPLOAD_FOLDER = current_app.config ["AVATAR_UPLOAD_FOLDER"]
        ALLOWED_EXTENSIONS = [ '.png', '.jpg' , '.jpeg' , '.gif']
        if ext not in ALLOWED_EXTENSIONS:
            result = {'code':500,'message':'文件类型错误','data':None}

        else:

            if token_role==Role.TeacherRole:  #是老师
                teacher = Teacher.query.filter(Teacher.t_id==userID).first()
                if teacher:
                    teacher.avatar = '{}_{}'.format(userID,fname+ext)
                    dbManage.db.session.commit()
                    avatar.save( '{}{}_{}'.format(UPLOAD_FOLDER,userID,fname+ext))
                    #修改大小
                    img = io.imread(UPLOAD_FOLDER+userID+'_'+fname+ext)
                    width = 210
                    height = 210
                    dim = (width, height)
                    resized = transform.resize(img, dim)
                    _resz = np.zeros((resized.shape[0],resized.shape[1],resized.shape[2]),dtype=np.uint8)
                    for i in range(resized.shape[0]):
                        for j in range(resized.shape[1]):
                            for k in range(resized.shape[2]):
                                _resz[i][j][k] = resized[i][j][k] * 255  
                    _resz.dtype=np.uint8
                    io.imsave(UPLOAD_FOLDER+userID+'_'+fname+ext, _resz)
                    result = {'code':200,'message':'上传头像成功','data':None}
                else:
                    result = {'code':501,'message':'未找到用户','data':None}
            elif token_role==Role.StudentRole:  #是学生
                    student = Student.query.filter(Student.s_id==userID).first()
                    if student:
                        student.avatar = '{}_{}'.format(userID,fname+ext)
                        dbManage.db.session.commit()
                        avatar.save( '{}{}_{}'.format(UPLOAD_FOLDER,userID,fname+ext))
                        #修改大小
                        img = io.imread(UPLOAD_FOLDER+userID+'_'+fname+ext)
                        width = 210
                        height = 210
                        dim = (width, height)
                        resized = transform.resize(img, dim)
                        _resz = np.zeros((resized.shape[0],resized.shape[1],resized.shape[2]),dtype=np.uint8)
                        for i in range(resized.shape[0]):
                            for j in range(resized.shape[1]):
                                for k in range(resized.shape[2]):
                                    _resz[i][j][k] = resized[i][j][k] * 255  
                        _resz.dtype=np.uint8
                        io.imsave(UPLOAD_FOLDER+userID+'_'+fname+ext, _resz)
                        result = {'code':200,'message':'上传头像成功','data':None}
                    else:
                        result = {'code':501,'message':'未找到用户','data':None}
            else:
                result = {'code':400,'message':'ID错误','data':None}
            
    
    return jsonify(result)
                

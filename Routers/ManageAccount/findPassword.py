from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Student
from Model.Model import Teacher
from sqlalchemy import and_, or_
from dbManage import db
from Model import Student,Teacher

findPassword = Blueprint('findPassword', __name__)
CORS(findPassword, resources=r'/*')	

@findPassword.route('/findPassword/<userId>',methods=['POST'])  
def findPassword(userId):
    if len(userId)==7:  #是学生
        student = Student.query.filter(Student.s_id == userId).first() 
        token = student.generate_confirmation_token()  #生成token
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    name = data['name']
    s_id = data['s_id']
    email = data['email']
    gender = data['gender']
    phone_number = data['phone_number']
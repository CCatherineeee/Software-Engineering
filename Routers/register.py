from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
from Model import Entity as En
import json
import Model.dbManage as dbManage

# 蓝图名 蓝图路径
registerRoute = Blueprint('registerRoute', __name__)
CORS(registerRoute, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api


RegistedEmail = 3
RegistedUser = 2
def valid_regist(user_id, email):
    user = User.query.filter(User.email == email).first()
    if user:
        return RegistedEmail
    else:
        user_ = User.query.filter(User.user_id == user_id).first()
        if user_:
            return RegistedUser
    return True

@registerRoute.route('/student_register', methods=['POST'])
def StudentRegister():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    # if (valid_regist(data.get('id'), data.get('email')) == RegistedUser):   
    #     return "RegistedUser"
    # if (valid_regist(data.get('id'), data.get('email')) == RegistedEmail):
    #     return "RegistedEmail"
    if En.load_student(data.get('id'))!= None:
        print("该用户已经被注册了！")
        return "False"
    else:
        student = En.Student(id =data.get('id') , password =data.get('password'),  name = data.get('name'), email = data.get('email'))
        token = student.generate_confirmation_token()
        dbManage.db.session.add(student)
        dbManage.db.session.commit()
        # send_email(user.email, 'Confirm Your Account',
        # '您的账号已创建，请点击下面的链接确认账号。', user=user, token=token)
        #flash('A confirmation email has been sent to you by email.')
        print("账号已创建")
        return "Created"

from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint

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

@registerRoute.route('/register/', methods=['POST'])
def register():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    if (valid_regist(data.get('sid'), data.get('email')) == RegistedUser):   
        return "RegistedUser"
    if (valid_regist(data.get('sid'), data.get('email')) == RegistedEmail):
        return "RegistedEmail"
    else:
        user = User(user_id =data.get('sid') , user_pwd =data.get('password'),  name = data.get('name'), email = data.get('email'),
                       is_active=0,role=0)
        dbManage.db.session.add(user)
        dbManage.db.session.commit()
    return "Created"

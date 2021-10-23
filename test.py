from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint

# 蓝图名 蓝图路径
get = Blueprint('test', __name__)
CORS(get, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api

# 由蓝图定义的视图
@get.route('/get/',methods=['GET'])
def test():
    # print(123)
    data = request.args
    # data = data.to_dict()
    # print(data.post)

    return data
from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Course,Class
import dbManage



addClassRoute = Blueprint('addClassRoute', __name__)
CORS(addClassRoute, resources=r'/*')	

@addClassRoute.route('/addClass',methods=['POST'])  
def addClass():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))

    course_id = data['course_id']  #课程号前缀
    # prefix = course_id[:-6]
    course_list = Course.query.filter(Course.course_id == course_id).all()

    if(course_list):

        if len(course_list)!=0:
            class_num = len(course_list) + 1

        else:
            class_num = 1

            new_class = Class(course_id =course_id,class_number= class_num)

            dbManage.db.session.add(new_class)
            dbManage.db.session.commit()

            result = {'status':200,'message':'添加班级成功'}
    else:
        result = {'status':200,'message':'添加班级失败，课程不存在'}

    return jsonify(result)

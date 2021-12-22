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
from Routers import Role

manageExperRoute = Blueprint('manageExperRoute', __name__)
CORS(manageExperRoute, resources=r'/*')	

@manageExperRoute.route('/exper/getClassExper',methods=['POST'])  
def getClassExper():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    class_id = data['class_id']
    
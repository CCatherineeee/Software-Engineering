from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model import Entity
from sqlalchemy import and_, or_
import os
import time
import uuid

addUserRoute = Blueprint('addUserRoute', __name__)
CORS(addUserRoute, resources=r'/*')	

@addUserRoute.route('/addUser/',methods=['POST'])  
def addUser():
    fileList = request.files.getlist('file')

    for file in fileList:

        basepath = os.path.dirname(__file__)
        ext = os.path.splitext(file.filename)[1]
        filename = os.path.splitext(file.filename)[0]

        newFileName = filename + "_" + str(uuid.uuid1())  + ext

        uploadPath = os.path.join(basepath, 'userFile', newFileName)

        file.save(uploadPath)
    return "ok"
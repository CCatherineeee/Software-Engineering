from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model.Model import Student
from Model.Model import Teacher
from sqlalchemy import and_, or_
import time
import dbManage


editUserInfoRoute = Blueprint('editUserInfoRoute', __name__)
CORS(editUserInfoRoute, resources=r'/*')	
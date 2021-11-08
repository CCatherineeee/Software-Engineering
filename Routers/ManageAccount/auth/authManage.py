from flask import render_template,  request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint
from dbManage import db
from ..myemail.sendEmail import send_email
from flask import current_app
from flask_restful import Api
from flask import jsonify
from Model.Model import Student,Teacher
   

auth = Blueprint('auth', __name__)


api = Api()

def init_api(current_app):
    api.init_app(current_app)


@auth.route('/confirm/<user_ID>/<token>')  #生成的route没有区别！
# @login_required
def confirm(user_ID,token):

    if len(user_ID)==7:   #是学生
        stud = Student.query.filter(Student.s_id==user_ID).first()
        if stud is not None:
            if stud.is_active:  #已经激活了
                status = {'status':100,'message':'already confirmed'}
            if stud.confirm(token):
                db.session.commit()
                status = {'status':200,'message':'now have confirmed'}
        else:
            status = {'status':400,'message':'confirmed failed'}
    else:   #是老师
        teacher = Teacher.query.filter(Teacher.t_id==user_ID).first()
        if teacher is not None:
            if teacher.is_active:  #已经激活了
                status = {'status':100,'message':'already confirmed'}
            if teacher.confirm(token):
                db.session.commit()
                status = {'status':200,'message':'now have confirmed'}
        else:
            status = {'status':400,'message':'confirmed failed'}
    return jsonify(status)


# @auth.route('/confirm')
# # @login_required
# def resend_confirmation():
#     ha = Student('1951095','1233','小雯砸','1284915396@qq.com')
#     token = ha.generate_confirmation_token()
#     if(send_email(ha.email,0,ha)):
#         status = {'status':200,'message':'Success'}
#     else:
#         status = {'status':400,'message':'Failed'}
#     return jsonify(status)
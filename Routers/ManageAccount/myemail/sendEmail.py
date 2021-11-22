import smtplib
from email.mime.text import MIMEText
from email.header import Header              # Header 用来构建邮件头
from . import redis_captcha 
import random
from .redis_captcha import redis_get                                       # 导入验证码模块
from flask_mail import Message
from flask import render_template
from flask import Blueprint
from flask_login import current_user
from dbManage import db
from flask import jsonify

email = Blueprint('email', __name__)
'''
获取num位验证码
'''

def get_random_captcha(num):
    code_list = []
    # 每一位验证码都有三种可能（大写字母，小写字母，数字）
    for i in range(num):
        statu = random.randint(1, 3)
        if statu == 1:
            a = random.randint(65, 90)
            random_uppercase = chr(a)
            code_list.append(random_uppercase)
        
        elif statu == 2:
            b = random.randint(97, 122)
            random_lowercase = chr(b)
            code_list.append(random_lowercase)
        
        elif statu == 3:
            random_num = random.randint(0, 9)
            code_list.append(str(random_num))
    
    verification_code = "".join(code_list)               # 生成随机验证码
    return verification_code

'''
发送邮件,code表示发送内容 ，code=0表示用户激活提示，code=1表示发送验证码
输入：发送人邮箱
输入：Success/Failed(console)
'''
def send_email(receiver,code,user):    #这里增加一个标志位！
    _user = "1284915396@qq.com"
    _pwd  = "otxvdgxwvvqbiadg"
    _to   = receiver          

    if code==0:
        content = "您的账户已被创建，请登录平台激活"
        subject = "实验管理系统激活提示"
    elif code==1:
        captcha = get_random_captcha(4)           # 生成4位验证码
        content = "您的邮箱验证码为:"+captcha
        subject = "实验管理系统验证！"

    msg = MIMEText(content)   #邮件内容
    
    msg['From'] = Header(_user)
    msg['TO'] = Header(",".join(_to))
    # msg["Subject"] = Header(subject).encode()
    token = user.generate_confirmation_token()  
    if len(user.s_id)==7:
        new_content = render_template("confirm.html",user = user,s_id=user.s_id,token = token)
    else:
        new_content = render_template("confirm_t.html",user = user,t_id=user.t_id,token = token)
    msg = MIMEText(new_content,_subtype='html',_charset='gb2312')    #创建一个实例，这里设置为html格式邮件
    msg["Subject"] = Header(subject).encode()

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
        print ("Success!")
        if code == 1:
            if len(_to)>1:
                for item in _to:
                    redis_captcha.redis_set(key=item, value=captcha)        # redis中都是键值对类型，存储验证码
            else:
                redis_captcha.redis_set(key=_to[0], value=captcha)        # redis中都是键值对类型，存储验证码
        return True
    except (smtplib.SMTPException):
        print ("Falied")
        return False

'''
验证邮箱验证码
输入：发送人邮箱，验证码
输出：0(false)/1(true)
'''
@email.route('/users/validateCaptcha',methods=['POST'])  
def validate_captcha(email,captcha):           # 方法命名规则是：validate_字段名()
        # 取redis中保存的验证码         s    第一个redis_captcha是新对象，第二个redis_captcha是redis_captcha.py文件
        redis_captcha = redis_get(email)
        if not redis_captcha or captcha.lower() != redis_captcha.lower():    # 不区分大小写
            data = {'status':400,'message':'wrong'}
        else:
            data = {'status':200,'message':'true'}
        return jsonify(data)


'''
发送邮箱验证码
输入：发送人邮箱
输出：json
'''
@email.route('/users/sendCaptcha',methods=['POST'])  
def send_captcha(receiver):
    _user = "1284915396@qq.com"
    _pwd  = "otxvdgxwvvqbiadg"
    _to   = receiver
    captcha = get_random_captcha(4)           # 生成4位验证码
    content = "您的邮箱验证码为:"+captcha
    subject = "实验管理系统验证！"
    msg = MIMEText(content)   #邮件内容
    
    msg['From'] = Header(_user)
    msg['TO'] = Header(",".join(_to))
    msg["Subject"] = Header(subject).encode()

    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    s.login(_user, _pwd)
    s.sendmail(_user, _to, msg.as_string())
    s.quit()
    try:
        if len(_to)>1:
            for item in _to:
                redis_captcha.redis_set(key=item, value=captcha)        # redis中都是键值对类型，存储验证码
        else:
            redis_captcha.redis_set(key=_to[0], value=captcha)        # redis中都是键值对类型，存储验证码
        status = {'status':200,'message':'Success'}
        return jsonify(status)
    except (smtplib.SMTPException):
        status = {'status':400,'message':'Failed'}
        return jsonify(status)
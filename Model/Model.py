from re import template
from dbManage import db
from sqlalchemy import ForeignKey
import datetime
from werkzeug.security import generate_password_hash, check_password_hash  
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import LoginManager
from flask_login import UserMixin

login_manager = LoginManager()
login_manager.session_protection = 'strong' #安全等级
"""
 
 Tables
 
 @ lxy
 21.10.2021
 
"""

# TODO Major表
# TODO 联系表


class Student(UserMixin,db.Model):
    """
    类描述：学生，学生ID位7位
    """
    __tablename__ = 'student'
    s_id = db.Column(db.String(64), primary_key=True, autoincrement=False)  # 表明是主键  学生学号是7位，老师是5位
    s_pwd = db.Column(db.String(1024))
    name = db.Column(db.String(64))   # 名字
    email = db.Column(db.String(64),unique=True)
    gender = db.Column(db.String(10))  # 0女，1男
    phone_number = db.Column(db.String(11))   # 11位电话号码（选填）
    is_active = db.Column(db.Integer,default = 0)  # 是否激活，0未激活，1已激活
    department = db.Column(db.String(64))  # 学院
    avatar = db.Column(db.String(200),default=None)
    # major = db.Column(db.String(64))  # 专业

    def __repr__(self):
        return '<User %r>' % self.__tablename__

    # 修改密码加密操作中的字段，在manage.py映射数据库时候，使用字段还是保持相同
    def __init__(self,s_id,s_pwd,name,email):  #只需要这几个参数
        self.s_id = s_id
        self.set_password(s_pwd)       # 调用该方法 返回下面的self._password数值，
        self.name = name
        self.email = email

    #创建一个学生的时候，只需要提供它初始的ID、密码、姓名和邮箱即可，其他的信息等学生登陆后再更改
    
    # 密码加密操作
    @property
    def password(self):                   # 密码取值
        raise AttributeError('password 是不可读属性')

    # @password.setter                      # 密码加密
    def set_password(self, password):
        self.s_pwd = generate_password_hash(password)

    # 用于验证后台登录密码是否和数据库一致，raw_password是后台登录输入的密码
    def check_password(self, raw_password):
        result = check_password_hash(self.s_pwd, raw_password)   # 相当于用相同的hash加密算法加密raw_password，检测与数据库中是否一致
        return result

    #生成确认令牌，过期时间为1h
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.s_id})
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.s_id:
            return False
        self.is_active = 1
        db.session.add(self)
        return True



class Teacher(UserMixin,db.Model):
    """
    类描述：教师，教师ID为5位
    """
    __tablename__ = 'teacher'
    t_id = db.Column(db.String(64), primary_key=True, autoincrement=False) 
    t_pwd = db.Column(db.String(1024))
    name = db.Column(db.String(64))   # 名字
    email = db.Column(db.String(64),unique=True)
    gender = db.Column(db.String(64))
    phone_number = db.Column(db.String(11))   # 11位电话号码（选填）
    is_active = db.Column(db.Integer,default=0)  # 是否激活，0未激活，1已激活
    department = db.Column(db.String(64))   # 专业

    def __repr__(self):
        return '<User %r>' % self.__tablename__

        # 修改密码加密操作中的字段，在manage.py映射数据库时候，使用字段还是保持相同
    def __init__(self,t_id,t_pwd,name,email):  #只需要这几个参数
        self.t_id = t_id
        self.set_password(t_pwd)         # 调用该方法 返回下面的self._password数值，
        self.name = name
        self.email = email

    #创建一个学生的时候，只需要提供它初始的ID、密码、姓名和邮箱即可，其他的信息等学生登陆后再更改
    
    # 密码加密操作
    @property
    def password(self):                   # 密码取值
        return self.t_pwd

    # @password.setter                      # 密码加密
    def set_password(self, raw_password):
        self.t_pwd = generate_password_hash(raw_password)

    # 用于验证后台登录密码是否和数据库一致，raw_password是后台登录输入的密码
    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)   # 相当于用相同的hash加密算法加密raw_password，检测与数据库中是否一致
        return result

    #生成确认令牌，过期时间为1h
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.t_id})
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.t_id:
            return False
        self.is_active = 1
        db.session.add(self)
        return True


class Admin(db.Model): 
    """
    类描述：管理员，管理员的ID为4位

    类属性：
    admin_id, admin_pwd, name, email, phone_number, state
    """
    __tablename__ = 'admin'
    admin_id = db.Column(db.String(64), primary_key=True, default="0000") 
    admin_pwd = db.Column(db.String(64))
    name = db.Column(db.String(64))   # 名字
    email = db.Column(db.String(64))
    phone_number = db.Column(db.String(11))   # 11位电话号码（选填）
    state = db.Column(db.Integer)  # 是否在线

    def __repr__(self):
        return '<User %r>' % self.__tablename__


class TeachingAssistant(db.Model):
    """
    类描述：助教表，主码为学号
    """
    __tablename__ = 'teaching_assistant'
    ta_id = db.Column(db.String(64), primary_key=True, autoincrement=False)  # 表明是主键  学生学号是7位，老师是5位
    ta_pwd = db.Column(db.String(150))
    name = db.Column(db.String(64))   # 名字
    email = db.Column(db.String(64),unique=True)
    is_active = db.Column(db.Integer,default = 0)  # 是否激活，0未激活，1已激活

    # 修改密码加密操作中的字段，在manage.py映射数据库时候，使用字段还是保持相同
    def __init__(self,ta_id,ta_pwd,name,email):  #只需要这几个参数
        self.ta_id = ta_id
        self.set_password(ta_pwd)         # 调用该方法 返回下面的self._password数值，
        self.name = name
        self.email = email

    #创建一个学生的时候，只需要提供它初始的ID、密码、姓名和邮箱即可，其他的信息等学生登陆后再更改
    
    # 密码加密操作
    @property
    def password(self):                   # 密码取值
        return self.ta_pwd

    # @password.setter                      # 密码加密
    def set_password(self, raw_password):
        self.ta_pwd = generate_password_hash(raw_password)

    # 用于验证后台登录密码是否和数据库一致，raw_password是后台登录输入的密码
    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)   # 相当于用相同的hash加密算法加密raw_password，检测与数据库中是否一致
        return result

    #生成确认令牌，过期时间为1h
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.ta_id})
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.ta_id:
            return False
        self.is_active = 1
        db.session.add(self)
        return True


class CourseType(db.Model):
    """
    类描述：课程类型表，用于存储曾经开过的课程类型，便于管理
    """
    __tablename__ = 'course_type'
    ct_name = db.Column(db.String(64)) # 存放课程中文名称
    prefix = db.Column(db.String(64),primary_key = True) # 存放课号前缀

class Course(db.Model):
    """
    类描述：课程表，由课号前缀、开课学期、学年组成主码，并记录责任教师ID
    """
    __tablename__ = 'course'
    c_id = db.Column(db.String(256),primary_key=True)
    prefix = db.Column(db.String(64), ForeignKey("course_type.prefix",ondelete='CASCADE')) 
    course_semester = db.Column(db.String(64))  #春季为00  秋季为01
    course_year = db.Column(db.String(64))  #如2019
    duty_teacher = db.Column(db.String(64),ForeignKey("teacher.t_id",ondelete='CASCADE'))

class Class(db.Model):
    """
    类描述：班级

    主码应为course_id + class_number
    """
    __tablename__ = 'class'

    class_id = db.Column(db.String(256),primary_key=True) 
    course_id = db.Column(db.String(256),ForeignKey("course.c_id",ondelete='CASCADE'))
    class_number = db.Column(db.Integer)
    t_id = db.Column(db.String(64), ForeignKey('teacher.t_id',ondelete='CASCADE')) 

    #一对多关联
    # experiments = db.relationship('Experiment', backref='class', lazy='dynamic', cascade='all, delete-orphan', passive_deletes = True)
    exams = db.relationship('Exam', backref='class', lazy='dynamic', cascade='all, delete-orphan', passive_deletes = True)
    course_announcement = db.relationship('CourseAnnouncement', backref='class', lazy='dynamic', cascade='all, delete-orphan', passive_deletes = True)

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class Experiment(db.Model):
    """
    类描述：实验表，实验-课程关系为一对多，故无需建立联系表，主码为自增的ID
    实验-教师关系为 一对多 
    """
    __tablename__ = 'experiment'
    experiment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    course_id = db.Column(db.String(256),ForeignKey("course.c_id",ondelete='CASCADE'))
    t_id = db.Column(db.String(5), ForeignKey('teacher.t_id',ondelete='CASCADE')) 
    experiment_title = db.Column(db.String(64))
    experiment_brief = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    end_time = db.Column(db.DateTime)
    weight = db.Column(db.Float)
    ex_type = db.Column(db.String(10))
    status = db.Column(db.Integer) # 1发布 0 未发布 3 在线提交 4 在线提交+模拟实验 （5 提交文件+模拟实验）
    template_file = db.Column(db.String(100),default = '实验模板.docx')
    is_online = db.Column(db.Integer,default = 0)  #0 不是线上实验  1 是线上实验

    def __repr__(self):
        return '<User %r>' % self.__tablename__



class SystemAnnouncement(db.Model):
    """
    类描述：系统公告
    """
    __tablename__ = 'sys_announcement'
    annoucement_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    admin_id = db.Column(db.String(64),ForeignKey("admin.admin_id",ondelete='CASCADE'))
    title = db.Column(db.String(128))
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class CourseAnnouncement(db.Model):
    """
    类描述：课程公告，主码为自增的id，外码约束course_id
    """
    __tablename__ = 'course_announcement'
    annoucement_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    title = db.Column(db.String(128))
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    class_id = db.Column(db.String(256),ForeignKey("class.class_id",ondelete='CASCADE'))

    def __repr__(self):
        return '<User %r>' % self.__tablename__


class ClassGroup(db.Model):
    """
    类描述：小组表，主码为小组ID，自增
    """
    __tablename__ = 'class_group'
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表明是主键  学生学号是7位，老师是5位
    class_id = db.Column(db.String(256),ForeignKey("class.class_id",ondelete='CASCADE'),nullable=True) 
    seq_number = db.Column(db.Integer,nullable=True) #班级中的小组序号

class StudentMessage(db.Model):
    """
    类描述：学生信息表，主码自增
    """
    __tablename__ = 'student_message'
    stu_message_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    s_id = db.Column(db.String(64), ForeignKey('student.s_id',ondelete='CASCADE'))
    title = db.Column(db.String(100)) 
    content = db.Column(db.String(300)) 
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    is_read = db.Column(db.Integer,default = 0) #标志是否已读，默认为0：不是

class TeacherMessage(db.Model):
    """
    类描述：教师信息，主码自增
    """
    __tablename__ = 'teacher_message'
    tea_message_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    t_id = db.Column(db.String(64), ForeignKey('teacher.t_id',ondelete='CASCADE'))
    title = db.Column(db.String(100)) 
    content = db.Column(db.String(300)) 
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    is_read = db.Column(db.Integer,default = 0) #标志是否已读，默认为0：不是


class TAMessage(db.Model):
    """
    类描述：助教信息表，主码自增
    """
    __tablename__ = 'ta_message'
    ta_message_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    ta_id = db.Column(db.String(64), ForeignKey('teaching_assistant.ta_id',ondelete='CASCADE'))
    title = db.Column(db.String(100)) 
    content = db.Column(db.String(300)) 
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    is_read = db.Column(db.Integer,default = 0) #标志是否已读，默认为0：不是



class StudentExperiment(db.Model):
    """
    类描述：学生-实验联系表  多-多
    """
    __tablename__ = 'student_experiment'
    experiment_id = db.Column(db.Integer, ForeignKey('experiment.experiment_id',ondelete='CASCADE'), primary_key=True)  
    s_id = db.Column(db.String(64), ForeignKey('student.s_id',ondelete='CASCADE'),primary_key=True)
    file_url = db.Column(db.String(1024))
    score = db.Column(db.Integer)
    grader = db.Column(db.String(64))  #批改人姓名，不是ID
    submitTime = db.Column(db.DateTime,onupdate=datetime.datetime.now())
    def __repr__(self):
        return '<User %r>' % self.__tablename__


class StudentClass(db.Model):
    """
    类说明：学生-课程表，联系表，多对多
    """
    __tablename__ = 'student_class'
    class_id = db.Column(db.String(256),ForeignKey("class.class_id",ondelete='CASCADE'),primary_key=True) 
    s_id = db.Column(db.String(64),ForeignKey("student.s_id",ondelete='CASCADE'),primary_key=True)


class ClassFile(db.Model):  #ClassFile
    """
    类描述：课程文件，联系表，一对多
    
    指课程中由老师上传的文件资料，主码由 file_id  组成，
    """
    __tablename__ = 'class_file'

    file_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    class_id = db.Column(db.String(256), ForeignKey("class.class_id"))
    file_url = db.Column(db.String(128)) # 服务器文件存放地址
    file_name = db.Column(db.String(128)) #文件名
    upload_time = db.Column(db.String(50),default=datetime.datetime.now()) #上传时间

    def __repr__(self):
        return '<course_file %r>' % self.__tablename__



class TAClass(db.Model):
    """
    类描述：联系表，班级助教，是多对多关系
    """
    __tablename__ = 'ta_class'
    ta_id = db.Column(db.String(64),ForeignKey("teaching_assistant.ta_id",ondelete='CASCADE') ,primary_key=True)
    class_id = db.Column(db.String(256), ForeignKey("class.class_id",ondelete='CASCADE'),primary_key=True)
    def __repr__(self):
        return '<course_file %r>' % self.__tablename__

class StudentGroup(db.Model):
    """
    类描述：学生-小组表，联系表
    """
    __tablename__ = 'student_group'
    group_id = db.Column(db.Integer,ForeignKey("class_group.group_id",ondelete='CASCADE') ,primary_key=True)
    s_id = db.Column(db.String(64),ForeignKey("student.s_id",ondelete='CASCADE'),primary_key=True)
    is_leader = db.Column(db.Integer,default = 0) #标志是否是组长，默认为0：不是
    def __repr__(self):
        return '<User %r>' % self.__tablename__


class Auction(db.Model):
    """
    类描述：学生-小组表，联系表
    """
    __tablename__ = 'auction'
    auction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_id = db.Column(db.String(64),ForeignKey("student.s_id",ondelete='CASCADE'))
    experiment_id = db.Column(db.Integer, ForeignKey('experiment.experiment_id',ondelete='CASCADE')) #实验id
    good = db.Column(db.Integer,nullable=False) #商品，0代表茶壶，1是背包，2是抱枕
    price = db.Column(db.Integer,nullable=False) #所出价格
    role = db.Column(db.Integer,nullable=False) #角色，0是需求者，1是供给者


#######################  考试  ####################3333

class Exam(db.Model):
    """
    类描述：考试，考试-课程关系为，一个考试对应一个课程，一个课程对应多个考试，故一对多，不建立联系表
    """
    __tablename__ = 'exam'
    exam_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.Integer)     # 0为未开始 1为进行中 3为截至
    class_id = db.Column(db.String(256),ForeignKey("class.class_id",ondelete='CASCADE'))
    def __repr__(self):
        return '<User %r>' % self.__tablename__

class Question(db.Model):
    """
    类描述：考试的问题，问题-测验关系为，一个问题对应一个测验，一个测验对应多个问题，故一对多，部建立联系表
    """
    __tablename__ = 'question'
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    option_a = db.Column(db.Text)
    option_b = db.Column(db.Text)
    option_c = db.Column(db.Text)
    option_d = db.Column(db.Text)
    answer = db.Column(db.String(64))
    q_score = db.Column(db.Float)
    exam_id = db.Column(db.Integer, ForeignKey('exam.exam_id',ondelete='CASCADE'))
    q_type = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class StudentExam(db.Model):
    """
    类描述：学生-测验表，联系表，考试-学生关系为，一个学生对应多个考试，一个考试对应多个学生，故多对多，建立联系表
    """
    __tablename__ = 'student_exam'
    exam_id = db.Column(db.Integer,ForeignKey("exam.exam_id",ondelete='CASCADE') ,primary_key=True)
    s_id = db.Column(db.String(64),ForeignKey("student.s_id",ondelete='CASCADE'),primary_key=True)
    score = db.Column(db.Float)
    spare_time = db.Column(db.Integer)
    def __repr__(self):
        return '<User %r>' % self.__tablename__

class StudentExamQuestion(db.Model):
    """
    类描述：学生-考试问题联系表 多-多
    """
    __tablename__ = 'student_examquestion'
    sq_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    q_id =  db.Column(db.Integer,ForeignKey('question.question_id',ondelete='CASCADE'))
    s_id = db.Column(db.String(64), ForeignKey('student.s_id',ondelete='CASCADE')) 
    choice = db.Column(db.String(10))  #选项
    is_correct = db.Column(db.Integer)   #0错误，1正确
    
    def __repr__(self):
        return '<User %r>' % self.__tablename__

class ExamGroup(db.Model):
    __tablename__ = 'exam_group'
    group_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    exam_id = db.Column(db.Integer,ForeignKey("exam.exam_id",ondelete='CASCADE'))
    s_id_1 = db.Column(db.String(64))
    s_id_2 = db.Column(db.String(64))
    s_id_3 = db.Column(db.String(64))

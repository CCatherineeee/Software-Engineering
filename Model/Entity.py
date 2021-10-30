import sys
sys.path.append("D:\\1课程资料\\大三上\\软件工程\\flask操作数据库\\SE")

from enum import unique
from .dbManage import db
from sqlalchemy import ForeignKey
import datetime
from werkzeug.security import generate_password_hash, check_password_hash  
from flask_login import UserMixin
from flask import current_app
# from app import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask_login import LoginManager

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
    类描述：学生
    """
    __tablename__ = 'student'
    s_id = db.Column(db.String(7), primary_key=True)  # 表明是主键  学生学号是7位，老师是5位
    s_pwd = db.Column(db.String(150))  #加密的密码
    name = db.Column(db.String(64))   # 名字
    email = db.Column(db.String(64),unique=True)
    gender = db.Column(db.String(10))  # 0女，1男
    phone_number = db.Column(db.String(11))   # 11位电话号码（选填）
    is_active = db.Column(db.Integer,default=0)  # 是否激活，0未激活，1已激活
    department = db.Column(db.String(64))  # 专业

    def __repr__(self):
        return '<User %r>' % self.__tablename__

    # 修改密码加密操作中的字段，在manage.py映射数据库时候，使用字段还是保持相同
    def __init__(self,id,password,name,email):  #只需要这几个参数
        self.s_id = id
        self.password = password         # 调用该方法 返回下面的self._password数值，
        self.name = name
        self.email = email

    #创建一个学生的时候，只需要提供它初始的ID、密码、姓名和邮箱即可，其他的信息等学生登陆后再更改
    
    # 密码加密操作
    @property
    def password(self):                   # 密码取值
        return self.s_pwd

    @password.setter                      # 密码加密
    def password(self, raw_password):
        self.s_pwd = generate_password_hash(raw_password)

    # 用于验证后台登录密码是否和数据库一致，raw_password是后台登录输入的密码
    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)   # 相当于用相同的hash加密算法加密raw_password，检测与数据库中是否一致
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
    类描述：教师
    """
    __tablename__ = 'teacher'
    t_id = db.Column(db.String(5), primary_key=True)  # 表明是主键  学生学号是7位，老师是5位
    t_pwd = db.Column(db.String(64))
    name = db.Column(db.String(64))   # 名字
    email = db.Column(db.String(64),unique=True)
    phone_number = db.Column(db.String(11))   # 11位电话号码（选填）
    is_active = db.Column(db.Integer)  # 是否激活，0未激活，1已激活
    department = db.Column(db.String(64))   # 专业

    def __repr__(self):
        return '<User %r>' % self.__tablename__

    # 修改密码加密操作中的字段，在manage.py映射数据库时候，使用字段还是保持相同
    def __init__(self,id,password,name,email):  #只需要这几个参数
        self.t_id = id
        self.password = password         # 调用该方法 返回下面的self._password数值，
        self.name = name
        self.email = email

    # 创建一个教师的时候，只需要提供它初始的ID、密码、姓名和邮箱即可，其他的信息等学生登陆后再更改
    
    # 密码加密操作
    @property
    def password(self):                   # 密码取值
        return self.t_pwd

    @password.setter                      # 密码加密
    def password(self, raw_password):
        self.t_pwd = generate_password_hash(raw_password)

    # 用于验证后台登录密码是否和数据库一致，raw_password是后台登录输入的密码
    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)   # 相当于用相同的hash加密算法加密raw_password，检测与数据库中是否一致
        return result


class Admin(UserMixin,db.Model):
    """
    类描述：管理员

    类属性：
    admin_id, admin_pwd, name, email, phone_number, state
    """
    __tablename__ = 'admin'
    admin_id = db.Column(db.String(5), primary_key=True)  # 表明是主键  学生学号是7位，老师是5位
    admin_pwd = db.Column(db.String(64))
    name = db.Column(db.String(64))   # 名字
    email = db.Column(db.String(64))
    phone_number = db.Column(db.String(11))   # 11位电话号码（选填）
    state = db.Column(db.Integer)  # 是否在线

    def __repr__(self):
        return '<User %r>' % self.__tablename__


class Class(db.Model):
    """
    类描述：班级
    """
    __tablename__ = 'class'
    class_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表明是主键  学生学号是7位，老师是5位
    class_name = db.Column(db.String(64))
    s_number = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.__tablename__


class Experiment(db.Model):
    """
    类描述：实验
    """
    __tablename__ = 'experiment'
    experiment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表明是主键  学生学号是7位，老师是5位
    experiment_title = db.Column(db.String(64))
    experiment_brief = db.Column(db.String(8192))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    end_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<User %r>' % self.__tablename__


class ExperimentFile(db.Model):
    """
    类描述：实验文件
    """
    __tablename__ = 'experiment_file'
    experiment_file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表明是主键  学生学号是7位，老师是5位
    experiment_id = db.Column(db.Integer, ForeignKey('experiment.experiment_id'))
    file_name = db.Column(db.String(50))
    size = db.Column(db.Float)

    def __repr__(self):
        return '<User %r>' % self.__tablename__


class Course(db.Model):
    """
    类描述：课程

    课号应为course_id+course_type
    """
    __tablename__ = 'course'
    course_id = db.Column(db.String(10), primary_key=True)  # 表明是主键  学生学号是7位，老师是5位
    course_name = db.Column(db.String(64))
    course_type = db.Column(db.Integer)  # 课号的后几位
    cover = db.Column(db.String(128))  # 封面
    course_state = db.Column(db.Integer)  # 是否开课 0/1
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    change_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<User %r>' % self.__tablename__


class CourseFile(db.Model):
    """
    类描述：课程文件
    """
    __tablename__ = 'course_file'
    course_file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表明是主键  学生学号是7位，老师是5位
    course_id = db.Column(db.String(10), ForeignKey('course.course_id'))
    file_name = db.Column(db.String(128))
    size = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.__tablename__


class Assignment(db.Model):
    """
    类描述：作业
    """
    __tablename__ = 'assignment'
    assignment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表明是主键  学生学号是7位，老师是5位
    course_id = db.Column(db.String(10), ForeignKey('course.course_id'))
    assignment_title = db.Column(db.String(128))
    assignment_content = db.Column(db.String(4096))
    change_time = db.Column(db.DateTime, default=datetime.datetime.now())
    end_time = db.Column(db.DateTime)
    weight = db.Column(db.Float)

    def __repr__(self):
        return '<User %r>' % self.__tablename__


class Exam(db.Model):
    """
    类描述：考试
    """
    __tablename__ = 'exam'
    exam_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表明是主键  学生学号是7位，老师是5位
    title = db.Column(db.String(64))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.Integer)     # 0为未开始 1为进行中 2为戒指

    def __repr__(self):
        return '<User %r>' % self.__tablename__


class Question(db.Model):
    """
    类描述：考试的问题
    """
    __tablename__ = 'question'
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表明是主键  学生学号是7位，老师是5位
    title = db.Column(db.String(128))
    option_a = db.Column(db.String(128))
    option_b = db.Column(db.String(128))
    option_c = db.Column(db.String(128))
    option_d = db.Column(db.String(128))
    answer = db.Column(db.Integer)
    experiment_id = db.Column(db.Integer, ForeignKey('experiment.experiment_id'))
    comment = db.Column(db.String(2048))

    def __repr__(self):
        return '<User %r>' % self.__tablename__


# # 权限定义，不是模型，没有继承db.Model
# class Permission(object):
#     # 255 二进制表示所有的权限
#     ALL_PERMISSION = 0b1111111111111111          # 每一位数代表一个权限，共7个权限，8位1个字节
    
#     # 创建账户
#     CREATE_ACCOUNT        = 0b0000000000000001
    
#     # 分配权限
#     ALLOCATE_AUTHORITY    = 0b0000000000000010
    
#     # 编辑账户信息
#     EDIT_INFORMATION      = 0b0000000000000100
    
#     # 注销账户
#     LOGOUT                = 0b0000000000001000
    
#     # 设立课程
#     COURSE                = 0b0000000000010000

#     # 发布课程实验项目
#     RELEASE               = 0b0000000000100000

#     # 参与教学实验项目
#     PARTICIPATE           = 0b0000000001000000

#     # 上传
#     UPLOAD                = 0b0000000010000000

#     # 下载
#     DOWNLOAD              = 0b0000000100000000

#     # 批改
#     CORRECT               = 0b0000001000000000

#     # 管理成绩
#     MANAGE_GRADE          = 0b0000010000000000

#     # 关闭课程
#     CLOSE_COURSE          = 0b0000100000000000

#     # 访问权限（只能访问网站，没有其他操作）
#     VISITER               = 0b0001000000000000

# # 权限与角色是多对多的关系，创建他们的中间表
# role_teacher = db.Table(
#     "role_teacher",
#     db.Column("role_id", db.Integer, db.ForeignKey('role.id'), primary_key=True),
#     db.Column("teacher_id", db.String(5), db.ForeignKey('teacher.t_id'), primary_key=True),
# )

# role_student = db.Table(
#     "role_student",
#     db.Column("role_id", db.Integer, db.ForeignKey('role.id'), primary_key=True),
#     db.Column("student_id", db.String(7), db.ForeignKey('student.s_id'), primary_key=True),
# )

# role_admin = db.Table(
#     "role_admin",
#     db.Column("role_id", db.Integer, db.ForeignKey('role.id'), primary_key=True),
#     db.Column("admin_id", db.String(5), db.ForeignKey('admin.admin_id'), primary_key=True),
# )


# # 角色模型定义   继承了db.Model
# class Role(db.Model):
#     """
#     类描述：角色表
#     """
#     __tablename__ = 'role'
    
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)      # 主键  自增
#     name = db.Column(db.String(50), nullable=False)                       # 非空，角色名称
#     #desc = db.Column(db.String(250), nullable=False)                      # 非空
#     permission = db.Column(db.Integer, default=Permission.VISITOR)    # 默认先给仅访问权限

#     # 反向查询属性,关联中间表secondary=cms_role_user,对应了CMS_User模型,建立模型联系,不映射到数据库中
#     #users = db.relationship('CMS_User', secondary=cms_role_user, backref="roles")
#     teachers = db.relationship('Teacher', secondary=role_teacher, backref="roles")
#     students = db.relationship('Student', secondary=role_student, backref="roles")
#     admins = db.relationship('Admin', secondary=role_admin, backref="roles")
#-------------------------------------------联系表------------------------------------


class TeacherClass(db.Model):
    """
    类描述：教师-班级联系表
    """
    __tablename__ = 'teacher_class'
    class_id = db.Column(db.Integer, ForeignKey('class.class_id'), primary_key=True)  
    t_id = db.Column(db.String(5), ForeignKey('teacher.t_id'))  # 表明是主键  学生学号是7位，老师是5位

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class StudentClass(db.Model):
    """
    类描述：学生-班级联系表
    """
    __tablename__ = 'student_class'
    class_id = db.Column(db.Integer, ForeignKey('class.class_id'), primary_key=True)  
    s_id = db.Column(db.String(7), ForeignKey('student.s_id'))  # 表明是主键  学生学号是7位，老师是5位

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class TeacherExperiment(db.Model):
    """
    类描述：教师-实验联系表
    """
    __tablename__ = 'teacher_experiment'
    experiment_id = db.Column(db.Integer, ForeignKey('experiment.experiment_id'), primary_key=True)  
    t_id = db.Column(db.String(5), ForeignKey('teacher.t_id'))  # 表明是主键  学生学号是7位，老师是5位

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class StudentExperiment(db.Model):
    """
    类描述：学生-实验联系表
    """
    __tablename__ = 'student_experiment'
    experiment_id = db.Column(db.Integer, ForeignKey('experiment.experiment_id'), primary_key=True)  
    t_id = db.Column(db.String(5), ForeignKey('teacher.t_id'))  # 表明是主键  学生学号是7位，老师是5位

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class TeacherCourse(db.Model):
    """
    类描述：老师-课程联系表
    """
    __tablename__ = 'teacher_course'
    course_id = db.Column(db.String(10), ForeignKey('course.course_id'), primary_key=True)  
    t_id = db.Column(db.String(5), ForeignKey('teacher.t_id')) 

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class StudentCourse(db.Model):
    """
    类描述：学生-课程联系表
    """
    __tablename__ = 'student_course'
    course_id = db.Column(db.String(10), ForeignKey('course.course_id'), primary_key=True)  
    s_id = db.Column(db.String(7), ForeignKey('student.s_id'))  

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class StudentAssginment(db.Model):
    """
    类描述：学生-作业联系表
    """
    __tablename__ = 'student_assginment'
    s_id = db.Column(db.String(7), ForeignKey('student.s_id'), primary_key=True)  
    assignment_id = db.Column(db.Integer, ForeignKey('assignment.assignment_id'), primary_key=True)  
    score =  db.Column(db.Integer)  #作业成绩

    def __repr__(self):
        return '<User %r>' % self.__tablename__

        
class TeacherExam(db.Model):
    """
    类描述：教师-考试联系表
    """
    __tablename__ = 'teacher_exam'
    exam_id = db.Column(db.Integer, ForeignKey('exam.exam_id'),primary_key=True) 
    t_id = db.Column(db.String(5), ForeignKey('teacher.t_id')) 
    assignment_id = db.Column(db.Integer, ForeignKey('assignment.assignment_id'), primary_key=True)  
    score =  db.Column(db.Integer)  #作业成绩

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class ExamQuestion(db.Model):
    """
    类描述：考试-问题联系表
    """
    __tablename__ = 'exam_question'
    eq_id =  db.Column(db.Integer,primary_key=True)
    exam_id = db.Column(db.Integer, ForeignKey('exam.exam_id')) 
    question_id = db.Column(db.Integer, ForeignKey('question.question_id')) 

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class StudentExamQuestion(db.Model):
    """
    类描述：学生-考试问题联系表
    """
    __tablename__ = 'student_examquestion'
    eq_id =  db.Column(db.Integer,ForeignKey('exam_question.eq_id'),primary_key=True)
    s_id = db.Column(db.String(7), ForeignKey('student.s_id')) 
    spare_time = db.Column(db.DateTime)  #花费时长
    is_correct = db.Column(db.Integer)   #0错误，1正确
    
    def __repr__(self):
        return '<User %r>' % self.__tablename__
#---------------------------------------返回对象函数-------------------------------------
'''
如果能找到用户，这个函数必须返回用户对象；否则应该返回 None。
'''
@login_manager.user_loader
def load_student(s_id):
    return Student.query.get(s_id)

@login_manager.user_loader
def load_teacher(t_id):
    return Teacher.query.get(t_id)

@login_manager.user_loader
def load_admin(admin_id):
    return Admin.query.get(admin_id)
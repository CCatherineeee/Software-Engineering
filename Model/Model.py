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
    s_pwd = db.Column(db.String(150))
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
        self.password = s_pwd         # 调用该方法 返回下面的self._password数值，
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
    类描述：教师，教师ID为5位
    """
    __tablename__ = 'teacher'
    t_id = db.Column(db.String(64), primary_key=True, autoincrement=False) 
    t_pwd = db.Column(db.String(150))
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
        self.password = t_pwd         # 调用该方法 返回下面的self._password数值，
        self.name = name
        self.email = email

    #创建一个学生的时候，只需要提供它初始的ID、密码、姓名和邮箱即可，其他的信息等学生登陆后再更改
    
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

"""
class Class():
    class_id  设置级联删除
    course_id 
    class_no 

    责任教师：开课

class ClassTeacher():
    classid pk
    t_id pk

class ClassStudent():
    class_id pk
    s_id pk

"""

class CourseType(db.Model):
    """
    类描述：课程类型表，用于存储曾经开过的课程类型，便于管理
    """
    __tablename__ = 'course_type'
    ct_name = db.Column(db.String(64)) # 存放课程中文名称
    ct_prefix = db.Column(db.String(64),primary_key = True) # 存放课号前缀

class Course(db.Model):
    """
    类描述：课程表，由课号前缀、开课学期、学年组成主码，并记录责任教师ID
    """
    __tablename__ = 'course'
    c_id = db.Column(db.String(256),primary_key=True)
    prefix = db.Column(db.String(64), ForeignKey("course_type.ct_prefix")) 
    course_semester = db.Column(db.String(64))  #春季为00  秋季为01
    course_year = db.Column(db.String(64))  #如2019
    duty_teacher = db.Column(db.String(64),ForeignKey("teacher.t_id"))

class Class(db.Model):
    """
    类描述：班级

    主码应为course_id + class_number
    """
    __tablename__ = 'class'

    class_id = db.Column(db.Integer,primary_key=True) 
    course_id = db.Column(db.String(256),ForeignKey("course.c_id"))
    class_number = db.Column(db.Integer)

    #一对多关联
    experiments = db.relationship('Experiment', backref='class', lazy='dynamic', cascade='all, delete-orphan', passive_deletes = True)
    exams = db.relationship('Exam', backref='class', lazy='dynamic', cascade='all, delete-orphan', passive_deletes = True)
    course_announcement = db.relationship('CourseAnnouncement', backref='class', lazy='dynamic', cascade='all, delete-orphan', passive_deletes = True)

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class Experiment(db.Model):
    """
    类描述：实验表，实验-课程关系为一对多，故无需建立联系表，主码为自增的ID
    """
    __tablename__ = 'experiment'
    experiment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    class_id = db.Column(db.Integer,ForeignKey("class.class_id",ondelete='CASCADE'))
    experiment_title = db.Column(db.String(64))
    experiment_brief = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    end_time = db.Column(db.DateTime)
    weight = db.Column(db.Float)

    def __repr__(self):
        return '<User %r>' % self.__tablename__

"""
实验与实验文件的关系，对于一个实验，有多个学生提交的实验文件，一个实验文件只能是一个实验里的，因此是一对多关系
实验文件与学生的关系，对于一个实验文件，只能是一个学生提交的，对于一个学生， 需要提交多个实验文件，因此是一对多关系
"""

"""
class StudentExperiment(db.Model):
    """
    # 类描述：指学生上传的实验报告作业，实体表，主码为自增的ID
"""
    __tablename__ = 'student_experiment'
    experiment_id = db.Column(db.Integer, ForeignKey('experiment.experiment_id'))

    def __repr__(self):
        return '<User %r>' % self.__tablename__
"""

class Exam(db.Model):
    """
    类描述：考试，考试-课程关系为，一个考试对应一个课程，一个课程对应多个考试，故一对多，不建立联系表
    """
    __tablename__ = 'exam'
    exam_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.Integer)     # 0为未开始 1为进行中 2为戒指
    class_id = db.Column(db.Integer,ForeignKey("class.class_id",ondelete='CASCADE'))
    def __repr__(self):
        return '<User %r>' % self.__tablename__

class Question(db.Model):
    """
    类描述：考试的问题，问题-测验关系为，一个问题对应一个测验，一个测验对应多个问题，故一对多，部建立联系表
    """
    __tablename__ = 'question'
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表明是主键  学生学号是7位，老师是5位
    title = db.Column(db.String(128))
    option_a = db.Column(db.String(128))
    option_b = db.Column(db.String(128))
    option_c = db.Column(db.String(128))
    option_d = db.Column(db.String(128))
    answer = db.Column(db.Integer)
    experiment_id = db.Column(db.Integer, ForeignKey('exam.exam_id'))
    comment = db.Column(db.String(2048))

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class SystemAnnouncement(db.Model):
    """
    类描述：系统公告
    """
    __tablename__ = 'sys_announcement'
    annoucement_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    admin_id = db.Column(db.String(64),ForeignKey("admin.admin_id"))
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
    class_id = db.Column(db.Integer,ForeignKey("class.class_id",ondelete='CASCADE'))

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


"""

class AnnouncementCourse(db.Model):
"""
    # 类描述：公告课程表
"""
    __tablename__ = 'announcement_course'
    annoucement_id = db.Column(db.Integer, primary_key=True)  


    
    course_type = db.Column(db.Integer,primary_key=True)  
    course_semester = db.Column(db.String(64),primary_key=True)
    course_year = db.Column(db.String(64),primary_key=True)
    class_id = db.Column(db.Integer,primary_key=True)

    t_id = db.Column(db.Integer)

    __table_args__ = (db.ForeignKeyConstraint(
      ['course_type', 'course_semester','course_year','class_id','annoucement_id'], 
      ['course.course_type', 'course.course_semester','course.course_year','course.class_id','announcement.annoucement_id']),)

"""
##############################################################

"""
class TeacherClass(db.Model):
    __tablename__ = 'teacher_class'
    class_id = db.Column(db.Integer, ForeignKey('class.class_id'), primary_key=True)  
    t_id = db.Column(db.String(5), ForeignKey('teacher.t_id'))  

    def __repr__(self):
        return '<User %r>' % self.__tablename__
"""

"""
class StudentClass(db.Model):
    __tablename__ = 'student_class'
    class_id = db.Column(db.Integer, ForeignKey('class.class_id'), primary_key=True)  
    s_id = db.Column(db.String(7), ForeignKey('student.s_id'))  # 表明是主键  学生学号是7位，老师是5位

    def __repr__(self):
        return '<User %r>' % self.__tablename__
"""

"""

class Assignment(db.Model):
"""
    # 类描述：作业，似乎并没有这个需求
"""
    __tablename__ = 'assignment'
    assignment_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    course_id = db.Column(db.String(256),ForeignKey("course.course_id"), primary_key=True)
    assignment_title = db.Column(db.String(128))
    assignment_content = db.Column(db.Text)
    change_time = db.Column(db.DateTime, default=datetime.datetime.now())
    end_time = db.Column(db.DateTime)
    weight = db.Column(db.Float)

    __table_args__ = (db.ForeignKeyConstraint(
      ['course_type', 'course_semester','course_year','class_id'], 
      ['course.course_type', 'course.course_semester','course.course_year','course.class_id']),)

    def __repr__(self):
        return '<User %r>' % self.__tablename__
"""


############################联系表#################################

class TeacherExperiment(db.Model):
    """
    类描述：教师-实验联系表  1-多
    """
    __tablename__ = 'teacher_experiment'
    experiment_id = db.Column(db.Integer, ForeignKey('experiment.experiment_id'), primary_key=True)  
    t_id = db.Column(db.String(5), ForeignKey('teacher.t_id')) 
    def __repr__(self):
        return '<User %r>' % self.__tablename__

class StudentExperiment(db.Model):
    """
    类描述：学生-实验联系表  多-多
    """
    __tablename__ = 'student_experiment'
    experiment_id = db.Column(db.Integer, ForeignKey('experiment.experiment_id'), primary_key=True)  
    s_id = db.Column(db.String(5), ForeignKey('student.s_id'))  # 表明是主键  学生学号是7位，老师是5位

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class TeacherCourse(db.Model):
    """
    类描述：老师-课程联系表  多-多
    """
    __tablename__ = 'teacher_course'
    course_id = db.Column(db.String(10), ForeignKey('course.c_id'), primary_key=True)  
    t_id = db.Column(db.String(5), ForeignKey('teacher.t_id')) 

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class StudentCourse(db.Model):
    """
    类描述：学生-课程联系表  多-多
    """
    __tablename__ = 'student_course'
    course_id = db.Column(db.String(10), ForeignKey('course.c_id'), primary_key=True)  
    s_id = db.Column(db.String(7), ForeignKey('student.s_id'))  

    def __repr__(self):
        return '<User %r>' % self.__tablename__

# class StudentAssginment(db.Model):
#     """
#     类描述：学生-作业联系表 多-多
#     """
#     __tablename__ = 'student_assginment'
#     s_id = db.Column(db.String(7), ForeignKey('student.student_id'), primary_key=True)  
#     assignment_id = db.Column(db.Integer, ForeignKey('assignment.assignment_id'), primary_key=True)  
#     score =  db.Column(db.Integer)  #作业成绩

#     def __repr__(self):
#         return '<User %r>' % self.__tablename__

        
# class TeacherExam(db.Model):
#     """
#     类描述：教师-考试联系表 1-多
#     """
#     __tablename__ = 'teacher_exam'
#     exam_id = db.Column(db.Integer, ForeignKey('exam.exam_id'),primary_key=True) 
#     t_id = db.Column(db.String(5), ForeignKey('teacher.t_id')) 
#     assignment_id = db.Column(db.Integer, ForeignKey('assignment.assignment_id'), primary_key=True)  
#     score =  db.Column(db.Integer)  #作业成绩

#     def __repr__(self):
#         return '<User %r>' % self.__tablename__

class ExamQuestion(db.Model):
    """
    类描述：考试-问题联系表 1-多
    """
    __tablename__ = 'exam_question'
    eq_id =  db.Column(db.Integer,primary_key=True)
    exam_id = db.Column(db.Integer, ForeignKey('exam.exam_id')) 
    question_id = db.Column(db.Integer, ForeignKey('question.question_id')) 

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class StudentExamQuestion(db.Model):
    """
    类描述：学生-考试问题联系表 多-多
    """
    __tablename__ = 'student_examquestion'
    eq_id =  db.Column(db.Integer,ForeignKey('exam_question.eq_id'),primary_key=True)
    s_id = db.Column(db.String(7), ForeignKey('student.s_id')) 
    spare_time = db.Column(db.DateTime)  #花费时长
    is_correct = db.Column(db.Integer)   #0错误，1正确
    
    def __repr__(self):
        return '<User %r>' % self.__tablename__

class StudentClass(db.Model):
    """
    类说明：学生-课程表，联系表，多对多
    """
    __tablename__ = 'student_class'
    class_id = db.Column(db.Integer,ForeignKey("class.class_id"),primary_key=True) 
    s_id = db.Column(db.String(64),ForeignKey("student.s_id"),primary_key=True)

class TeacherClass(db.Model):
    """
    类说明：教师-课程表，联系表，多对多

    注意：该表内的教师指的是任课教师，责任教师应在course表下

    """
    __tablename__ = 'teacher_class'
    class_id = db.Column(db.Integer,ForeignKey("class.class_id"),primary_key=True) 
    t_id = db.Column(db.String(64),ForeignKey("teacher.t_id"),primary_key=True)

class ClassFile(db.Model):  #ClassFile
    """
    类描述：课程文件，联系表，一对多
    
    指课程中由老师上传的文件资料，主码由 file_id  组成，
    """
    __tablename__ = 'class_file'

    file_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    class_id = db.Column(db.String(256), ForeignKey("class.class_id"))
    file_url = db.Column(db.String(128),default='../static/classFile') # 服务器文件存放地址
    file_name = db.Column(db.String(128)) #文件名

    def __repr__(self):
        return '<course_file %r>' % self.__tablename__

class StudentExperimentFile(db.Model):
    __tablename__ = 'student_experiment_file'
    file_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    experiment_id = db.Column(db.Integer,ForeignKey("experiment.experiment_id"))  
    s_id = db.Column(db.String(64),ForeignKey("student.s_id"))
    score = db.Column(db.Integer)

class StudentExam(db.Model):
    """
    类描述：学生-测验表，联系表，考试-学生关系为，一个学生对应多个考试，一个考试对应多个学生，故多对多，建立联系表
    """
    __tablename__ = 'student_exam'
    exam_id = db.Column(db.Integer,ForeignKey("exam.exam_id") ,primary_key=True)
    s_id = db.Column(db.String(64),ForeignKey("student.s_id"),primary_key=True)
    score = db.Column(db.Integer)
    def __repr__(self):
        return '<User %r>' % self.__tablename__

class TAClass(db.Model):
    """
    类描述：联系表，班级助教，是多对多关系
    """
    __tablename__ = 'ta_class'
    ta_id = db.Column(db.String(64),ForeignKey("teaching_assistant.ta_id") ,primary_key=True)
    class_id = db.Column(db.String(256), ForeignKey("class.class_id"),primary_key=True)
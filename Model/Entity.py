from dbManage import db
from sqlalchemy import ForeignKey
import datetime

"""
 
 Tables
 
 @ lxy
 21.10.2021
 
"""

# TODO Major表
# TODO 联系表


class Student(db.Model):
    """
    类描述：学生
    """
    __tablename__ = 'user'
    s_id = db.Column(db.Integer, primary_key=True, autoincrement=False)  # 表明是主键  学生学号是7位，老师是5位
    s_pwd = db.Column(db.String(64))
    name = db.Column(db.String(64))   # 名字
    email = db.Column(db.String(64))
    gender = db.Column(db.String(10))  # 0女，1男
    phone_number = db.Column(db.String(11))   # 11位电话号码（选填）
    is_active = db.Column(db.Integer)  # 是否激活，0未激活，1已激活
    department = db.Column(db.String(64))  # 专业

    def __repr__(self):
        return '<User %r>' % self.__tablename__


class Teacher(db.Model):
    """
    类描述：教师
    """
    __tablename__ = 'teacher'
    t_id = db.Column(db.Integer, primary_key=True, autoincrement=False)  # 表明是主键  学生学号是7位，老师是5位
    t_pwd = db.Column(db.String(64))
    name = db.Column(db.String(64))   # 名字
    email = db.Column(db.String(64))
    phone_number = db.Column(db.String(11))   # 11位电话号码（选填）
    is_active = db.Column(db.Integer)  # 是否激活，0未激活，1已激活
    department = db.Column(db.String(64))   # 专业

    def __repr__(self):
        return '<User %r>' % self.__tablename__


class Admin(db.Model):
    """
    类描述：管理员

    类属性：
    admin_id, admin_pwd, name, email, phone_number, state
    """
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表明是主键  学生学号是7位，老师是5位
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
    file_name = db.Column(db.String(8192))
    size = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.__tablename__


class Course(db.Model):
    """
    类描述：课程

    课号应为course_id+course_type
    """
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表明是主键  学生学号是7位，老师是5位
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
    course_id = db.Column(db.Integer, ForeignKey('course.course_id'))
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
    course_id = db.Column(db.Integer, ForeignKey('course.course_id'))
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
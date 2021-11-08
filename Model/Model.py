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
    类描述：学生，学生ID位7位
    """
    __tablename__ = 'student'
    s_id = db.Column(db.String(64), primary_key=True, autoincrement=False)  # 表明是主键  学生学号是7位，老师是5位
    s_pwd = db.Column(db.String(64))
    name = db.Column(db.String(64))   # 名字
    email = db.Column(db.String(64))
    gender = db.Column(db.String(10))  # 0女，1男
    phone_number = db.Column(db.String(11))   # 11位电话号码（选填）
    is_active = db.Column(db.Integer)  # 是否激活，0未激活，1已激活
    department = db.Column(db.String(64))  # 学院
    # major = db.Column(db.String(64))  # 专业

    def __repr__(self):
        return '<User %r>' % self.__tablename__


class Teacher(db.Model):
    """
    类描述：教师，教师ID为5位
    """
    __tablename__ = 'teacher'
    t_id = db.Column(db.String(64), primary_key=True, autoincrement=False) 
    t_pwd = db.Column(db.String(64))
    name = db.Column(db.String(64))   # 名字
    email = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    phone_number = db.Column(db.String(11))   # 11位电话号码（选填）
    is_active = db.Column(db.Integer)  # 是否激活，0未激活，1已激活
    department = db.Column(db.String(64))   # 专业

    def __repr__(self):
        return '<User %r>' % self.__tablename__

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
    course_id = db.Column(db.String(256),primary_key=True)
    ct_prefix = db.Column(db.String(64), ForeignKey("course_type.ct_prefix")) 
    course_semester = db.Column(db.String(64))
    course_year = db.Column(db.String(64))
    duty_teacher = db.Column(db.String(64),ForeignKey("teacher.t_id"))

class Class(db.Model):
    """
    类描述：课程

    主码应为course_id + class_number
    """
    __tablename__ = 'class'

    class_id = db.Column(db.String(256),primary_key=True) 
    course_id = db.Column(db.String(256),ForeignKey("course.course_id"))
    class_number = db.Column(db.Integer)
    def __repr__(self):
        return '<User %r>' % self.__tablename__

class StudentClass(db.Model):
    """
    类说明：学生-课程表，联系表，多对多
    """
    __tablename__ = 'student_class'
    class_id = db.Column(db.String(256),ForeignKey("class.class_id"),primary_key=True) 
    s_id = db.Column(db.String(64),ForeignKey("student.s_id"),primary_key=True)

class TeacherClass(db.Model):
    """
    类说明：教师-课程表，联系表，多对多

    注意：该表内的教师指的是任课教师，责任教师应在course表下

    """
    __tablename__ = 'teacher_class'
    class_id = db.Column(db.String(256),ForeignKey("class.class_id"),primary_key=True) 
    t_id = db.Column(db.String(64),ForeignKey("teacher.t_id"),primary_key=True)

class ClassFile(db.Model):  #ClassFile
    """
    类描述：课程文件，联系表，一对多
    
    指课程中由老师上传的文件资料，主码由 file_id  组成，
    """
    __tablename__ = 'class_file'

    file_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    class_id = db.Column(db.String(256), ForeignKey("class.class_id"))
    file_url = db.Column(db.String(128)) # 服务器文件存放地址
    file_name = db.Column(db.String(128))

    def __repr__(self):
        return '<course_file %r>' % self.__tablename__

class Experiment(db.Model):
    """
    类描述：实验表，实验-课程关系为一对多，故无需建立联系表，主码为自增的ID
    """
    __tablename__ = 'experiment'
    experiment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    class_id = db.Column(db.String(256),ForeignKey("class.class_id"))
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

class StudentExperimentFile(db.Model):
    __tablename__ = 'student_experiment_file'
    file_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    experiment_id = db.Column(db.Integer,ForeignKey("experiment.experiment_id"))  
    s_id = db.Column(db.String(64),ForeignKey("student.s_id"))
    score = db.Column(db.Integer)

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
    class_id = db.Column(db.String(256),ForeignKey("class.class_id"))
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
    class_id = db.Column(db.String(256),ForeignKey("class.class_id"))

    def __repr__(self):
        return '<User %r>' % self.__tablename__


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


# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Admin(Base):
    __tablename__ = 'admin'

    admin_id = Column(String(64), primary_key=True)
    admin_pwd = Column(String(64))
    name = Column(String(64))
    email = Column(String(64))
    phone_number = Column(String(11))
    state = Column(Integer)


class CourseType(Base):
    __tablename__ = 'course_type'

    ct_name = Column(String(64))
    prefix = Column(String(64), primary_key=True)


class Student(Base):
    __tablename__ = 'student'

    s_id = Column(String(64), primary_key=True)
    s_pwd = Column(String(150))
    name = Column(String(64))
    email = Column(String(64), unique=True)
    gender = Column(String(10))
    phone_number = Column(String(11))
    is_active = Column(Integer)
    department = Column(String(64))
    avatar = Column(String(200))


class Teacher(Base):
    __tablename__ = 'teacher'

    t_id = Column(String(64), primary_key=True)
    t_pwd = Column(String(150))
    name = Column(String(64))
    email = Column(String(64), unique=True)
    gender = Column(String(64))
    phone_number = Column(String(11))
    is_active = Column(Integer)
    department = Column(String(64))


class TeachingAssistant(Base):
    __tablename__ = 'teaching_assistant'

    ta_id = Column(String(64), primary_key=True)
    ta_pwd = Column(String(150))
    name = Column(String(64))
    email = Column(String(64), unique=True)
    is_active = Column(Integer)


class Course(Base):
    __tablename__ = 'course'

    c_id = Column(String(256), primary_key=True)
    prefix = Column(ForeignKey('course_type.prefix', ondelete='CASCADE'), index=True)
    course_semester = Column(String(64))
    course_year = Column(String(64))
    duty_teacher = Column(ForeignKey('teacher.t_id', ondelete='CASCADE'), index=True)

    teacher = relationship('Teacher')
    course_type = relationship('CourseType')


class StudentMessage(Base):
    __tablename__ = 'student_message'

    stu_message_id = Column(Integer, primary_key=True)
    s_id = Column(ForeignKey('student.s_id', ondelete='CASCADE'), index=True)
    title = Column(String(100))
    content = Column(String(300))
    create_time = Column(DateTime)
    is_read = Column(Integer)
    deadline = Column(DateTime)

    s = relationship('Student')


class SysAnnouncement(Base):
    __tablename__ = 'sys_announcement'

    annoucement_id = Column(Integer, primary_key=True)
    admin_id = Column(ForeignKey('admin.admin_id', ondelete='CASCADE'), index=True)
    title = Column(String(128))
    content = Column(Text)
    create_time = Column(DateTime)

    admin = relationship('Admin')


class TaMessage(Base):
    __tablename__ = 'ta_message'

    ta_message_id = Column(Integer, primary_key=True)
    ta_id = Column(ForeignKey('teaching_assistant.ta_id', ondelete='CASCADE'), index=True)
    title = Column(String(100))
    content = Column(String(300))
    create_time = Column(DateTime)
    is_read = Column(Integer)

    ta = relationship('TeachingAssistant')


class TeacherMessage(Base):
    __tablename__ = 'teacher_message'

    tea_message_id = Column(Integer, primary_key=True)
    t_id = Column(ForeignKey('teacher.t_id', ondelete='CASCADE'), index=True)
    title = Column(String(100))
    content = Column(String(300))
    create_time = Column(DateTime)
    is_read = Column(Integer)
    deadline = Column(DateTime)

    t = relationship('Teacher')


class Class(Base):
    __tablename__ = 'class'

    class_id = Column(String(256), primary_key=True)
    course_id = Column(ForeignKey('course.c_id', ondelete='CASCADE'), index=True)
    class_number = Column(Integer)
    t_id = Column(ForeignKey('teacher.t_id', ondelete='CASCADE'), index=True)

    course = relationship('Course')
    t = relationship('Teacher')
    ss = relationship('Student', secondary='student_class')
    tas = relationship('TeachingAssistant', secondary='ta_class')


class Experiment(Base):
    __tablename__ = 'experiment'

    experiment_id = Column(Integer, primary_key=True)
    course_id = Column(ForeignKey('course.c_id', ondelete='CASCADE'), index=True)
    t_id = Column(ForeignKey('teacher.t_id', ondelete='CASCADE'), index=True)
    experiment_title = Column(String(64))
    experiment_brief = Column(Text)
    create_time = Column(DateTime)
    end_time = Column(DateTime)
    weight = Column(Float)
    status = Column(Integer)
    template_file = Column(String(100))
    ex_type = Column(String(10))
    is_online = Column(Integer)

    course = relationship('Course')
    t = relationship('Teacher')


class Auction(Base):
    __tablename__ = 'auction'

    auction_id = Column(Integer, primary_key=True)
    s_id = Column(ForeignKey('student.s_id', ondelete='CASCADE'), index=True)
    experiment_id = Column(ForeignKey('experiment.experiment_id', ondelete='CASCADE'), index=True)
    good = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    role = Column(Integer, nullable=False)

    experiment = relationship('Experiment')
    s = relationship('Student')


class ClassFile(Base):
    __tablename__ = 'class_file'

    file_id = Column(Integer, primary_key=True)
    class_id = Column(ForeignKey('class.class_id', ondelete='CASCADE'), index=True)
    file_url = Column(String(128))
    file_name = Column(String(128))
    upload_time = Column(String(50))

    _class = relationship('Clas')


class ClassGroup(Base):
    __tablename__ = 'class_group'

    group_id = Column(Integer, primary_key=True)
    class_id = Column(ForeignKey('class.class_id', ondelete='CASCADE'), index=True)
    seq_number = Column(Integer)

    _class = relationship('Clas')


class CourseAnnouncement(Base):
    __tablename__ = 'course_announcement'

    annoucement_id = Column(Integer, primary_key=True)
    title = Column(String(128))
    content = Column(Text)
    create_time = Column(DateTime)
    class_id = Column(ForeignKey('class.class_id', ondelete='CASCADE'), index=True)

    _class = relationship('Clas')


class Exam(Base):
    __tablename__ = 'exam'

    exam_id = Column(Integer, primary_key=True)
    title = Column(String(64))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(Integer)
    class_id = Column(ForeignKey('class.class_id', ondelete='CASCADE'), index=True)

    _class = relationship('Clas')


t_student_class = Table(
    'student_class', metadata,
    Column('class_id', ForeignKey('class.class_id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('s_id', ForeignKey('student.s_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


class StudentExperiment(Base):
    __tablename__ = 'student_experiment'

    experiment_id = Column(ForeignKey('experiment.experiment_id', ondelete='CASCADE'), primary_key=True, nullable=False)
    s_id = Column(ForeignKey('student.s_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
    file_url = Column(String(1024))
    score = Column(Float)
    grader = Column(String(64))
    submitTime = Column(DateTime)

    experiment = relationship('Experiment')
    s = relationship('Student')


t_ta_class = Table(
    'ta_class', metadata,
    Column('ta_id', ForeignKey('teaching_assistant.ta_id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('class_id', ForeignKey('class.class_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


class ExamGroup(Base):
    __tablename__ = 'exam_group'

    group_id = Column(Integer, primary_key=True)
    exam_id = Column(ForeignKey('exam.exam_id', ondelete='CASCADE'), index=True)
    s_id_1 = Column(String(64))
    s_id_2 = Column(String(64))
    s_id_3 = Column(String(64))

    exam = relationship('Exam')


class Question(Base):
    __tablename__ = 'question'

    question_id = Column(Integer, primary_key=True)
    title = Column(Text)
    option_a = Column(Text)
    option_b = Column(Text)
    option_c = Column(Text)
    option_d = Column(Text)
    answer = Column(String(64))
    q_score = Column(Float)
    exam_id = Column(ForeignKey('exam.exam_id', ondelete='CASCADE'), index=True)
    q_type = Column(Integer)

    exam = relationship('Exam')


class StudentExam(Base):
    __tablename__ = 'student_exam'

    exam_id = Column(ForeignKey('exam.exam_id', ondelete='CASCADE'), primary_key=True, nullable=False)
    s_id = Column(ForeignKey('student.s_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
    score = Column(Float)
    spare_time = Column(Integer)

    exam = relationship('Exam')
    s = relationship('Student')


class StudentGroup(Base):
    __tablename__ = 'student_group'

    group_id = Column(ForeignKey('class_group.group_id', ondelete='CASCADE'), primary_key=True, nullable=False)
    s_id = Column(ForeignKey('student.s_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
    is_leader = Column(Integer)

    group = relationship('ClassGroup')
    s = relationship('Student')


class StudentExamQuestion(Base):
    __tablename__ = 'student_examquestion'

    sq_id = Column(Integer, primary_key=True)
    q_id = Column(ForeignKey('question.question_id', ondelete='CASCADE'), index=True)
    s_id = Column(ForeignKey('student.s_id', ondelete='CASCADE'), index=True)
    choice = Column(String(10))
    is_correct = Column(Integer)

    q = relationship('Question')
    s = relationship('Student')

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
    course_id = db.Column(db.String(10), ForeignKey('course.course_id'), primary_key=True)  
    t_id = db.Column(db.String(5), ForeignKey('teacher.t_id')) 

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class StudentCourse(db.Model):
    """
    类描述：学生-课程联系表  多-多
    """
    __tablename__ = 'student_course'
    course_id = db.Column(db.String(10), ForeignKey('course.course_id'), primary_key=True)  
    s_id = db.Column(db.String(7), ForeignKey('student.s_id'))  

    def __repr__(self):
        return '<User %r>' % self.__tablename__

class StudentAssginment(db.Model):
    """
    类描述：学生-作业联系表 多-多
    """
    __tablename__ = 'student_assginment'
    s_id = db.Column(db.String(7), ForeignKey('student.student_id'), primary_key=True)  
    assignment_id = db.Column(db.Integer, ForeignKey('assignment.assignment_id'), primary_key=True)  
    score =  db.Column(db.Integer)  #作业成绩

    def __repr__(self):
        return '<User %r>' % self.__tablename__

        
class TeacherExam(db.Model):
    """
    类描述：教师-考试联系表 1-多
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
    s_id = db.Column(db.String(7), ForeignKey('student.student_id')) 
    spare_time = db.Column(db.datetime)  #花费时长
    is_correct = db.Column(db.Integer)   #0错误，1正确
    
    def __repr__(self):
        return '<User %r>' % self.__tablename__
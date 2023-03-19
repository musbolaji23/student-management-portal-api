from ..utils import db

class StudentCourse(db.Model):
    __tablename__='student_course'
    student_course_id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('students.student_id'))
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.course_id'))
    earned_credit = db.Column(db.Float())
    grade = db.Column(db.String())
    #course = db.relationship('Course', backref='student_course')
    

    def __repr__(self):
        return f"<StudentCourse {self.student_id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
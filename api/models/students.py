from ..utils import db

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password_hash = db.Column(db.Text(), nullable=False) 
    gpa = db.Column(db.Float())
    courses = db.relationship('Course', secondary='student_course' )
    #student_courses = db.relationship('StudentCourse', backref='students')


    def __repr__(self):
        return f"<Student {self.email}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    # @classmethod
    # def get_by_id(cls, id):
    #     return cls.query.get_or_404(id)

from ..utils import db
from datetime import datetime

class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer(), primary_key=True)
    course_code = db.Column (db.String(100), nullable=False, unique=True)
    course_title = db.Column (db.String(100), nullable=False)
    credit_unit = db.Column (db.Integer(), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    teacher_id = db.Column (db.String(60), db.ForeignKey('teachers.teacher_id'))
    
    
    def __repr__(self):
        return f"<Course {self.id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)



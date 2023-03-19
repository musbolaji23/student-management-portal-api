from ..utils import db

class Teacher(db.Model):
    __tablename__ = 'teachers'

    teacher_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    courses = db.relationship('Course', backref='teachers')

    def __repr__(self):
        return f"<Teacher {self.name}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()


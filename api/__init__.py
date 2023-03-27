from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate 
from flask_jwt_extended import JWTManager
from .StudentCourse.views import studentcourse_namespace
from .teacher.views import teacher_namespace
from .student.views import std_namespace
from .course.views import course_namespace
from .config.config import config_dict
from .models.courses import Course
from .models.StudentCourse import StudentCourse
from .models.teacher import Teacher
from .models.students import Student
from .utils import db
from werkzeug.exceptions import NotFound, MethodNotAllowed


def create_app(config=config_dict['dev']):
    
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    api = Api(app)

    api.add_namespace(course_namespace)
    api.add_namespace(studentcourse_namespace)
    api.add_namespace(teacher_namespace)
    api.add_namespace(std_namespace, '/std')

    @app.errorhandler(NotFound)
    def not_found(error):
        return {"error":"not found"}, 404
    
    @app.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error":"not found"}, 404


    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'Course': Course,
            'Studentcourse': StudentCourse,
            'Teacher': Teacher,
            'Student': Student }
            
    return app

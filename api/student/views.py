from flask_restx import  Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from ..models.students import Student
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus

std_namespace = Namespace('student', description='name space for student authentication')

signup_model = std_namespace.model(
    'Signup', {
    'student_id': fields.Integer(),
    'name': fields.String(required=True, description="A firstname"),
    'email': fields.String(required=True, description="An email"),
    'password': fields.String(required=False, description="A password")
    }
)

student_model = std_namespace.model(
    'Student', {
    'student_id': fields.Integer(),
    'name': fields.String(required=True, description="A firstname"),
    'email': fields.String(required=True, description="An email"),
    }
)    

login_model = std_namespace.model(
    'login', {
    'email': fields.String(required=True, description="An email"),
    'password': fields.String(required=True, description="A password")
    }
)

@std_namespace.route('/signup')
class Signup(Resource):

    @std_namespace.expect(signup_model)
    @std_namespace.marshal_with(student_model)
    def post(self):
        """
            Sign up a student
        """
        data = request.get_json()

        new_student = Student(
            name = data.get('name'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password'))
        )
        print(new_student)
        new_student.save()

        return new_student, HTTPStatus.CREATED
    
    @std_namespace.marshal_with(student_model)
    def get(self):
        """
        Get all students
        """
        students = Student.query.all()

        return students, HTTPStatus.OK


@std_namespace.route('/login')
class Login(Resource):

    def post(self):
        """
            Generate JWT Token
        """

        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        student = Student.query.filter_by(email=email).first()

        if (student is not None) and check_password_hash(student.password_hash, password):

            access_token = create_access_token(identity=student.student_id)
            refresh_token = create_refresh_token(identity=student.student_id)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.CREATED

@std_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        
        student_id = get_jwt_identity()
        access_token = create_access_token(identity=student_id)
        return {"access_token": access_token}, HTTPStatus.OK
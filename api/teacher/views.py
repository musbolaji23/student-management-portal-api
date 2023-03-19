from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from http import HTTPStatus
from ..models.teacher import Teacher

teacher_namespace = Namespace('teacher', description='name space for teacher')

teacher_model = teacher_namespace.model(
    'Teacher', {
        'name': fields.String(description='name'),
        'email': fields.String(description='email')
    }
)

@teacher_namespace.route('/signup')
class Signup(Resource):

    @teacher_namespace.expect(teacher_model)
    @teacher_namespace.marshal_with(teacher_model)
    def post(self):
        """
            Sign up a student
        """
        data = request.get_json()

        new_teacher = Teacher(
            name = data.get('name'),
            email = data.get('email')
        )

        print(new_teacher)
        
        new_teacher.save()

        return new_teacher, HTTPStatus.CREATED
    
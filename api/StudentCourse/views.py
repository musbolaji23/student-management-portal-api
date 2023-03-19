from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from ..models.StudentCourse import StudentCourse


studentcourse_namespace = Namespace('studentcourse', description='name space for course')

studentcourse_model = studentcourse_namespace.model(
    'StudentCourse', {
        'student_id': fields.Integer(description='An ID'),
        'course_id': fields.Integer(description='firstname'),
        'grade': fields.String(description='grade'),
        'earned_credit': fields.Float(description='earned_credit'),
    }
)


@studentcourse_namespace.route('/assign')
class AssignScores(Resource):

    @studentcourse_namespace.expect(studentcourse_namespace.model)
    @studentcourse_namespace.marshal_with(studentcourse_namespace.model)
    @jwt_required()
    def post(self):
        """
            post earned units
        """
        data = request.get_json()
        print(data.get('student_id'))
        new_studentcourse = StudentCourse(
            student_id = data.get('student_id'),
            course_id = data.get('course_id'),
            grade = data.get('grade'),
            earned_credit = data.get('earned_credit'),
         )

        new_studentcourse.save()

        return new_studentcourse, HTTPStatus.CREATED
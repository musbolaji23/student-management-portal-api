from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from ..models.courses import Course
from ..models.students import Student

course_namespace = Namespace('course', description='name space for course')

course_model = course_namespace.model(
    'Course', {
        'course_id': fields.Integer(description='An ID'),
        'course_code': fields.String(description='course_code'),
        'course_title': fields.String(description='course title'),
        'credit_unit': fields.Integer(description='course unit')        
        }
)
 
@course_namespace.route('/courses')
class CourseGetCreate(Resource):

    @course_namespace.marshal_with(course_model)
    @jwt_required()
    def get(self):
        """
            Get all courses
        """
        courses = Course.query.all()

        return courses, HTTPStatus.OK
    
    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @jwt_required()
    def post(self):
        """
            register a course
        """

        name = get_jwt_identity()

        current_student = Student.query.filter_by(name=name).first()

        data = course_namespace.payload

        new_course = Course (
            course_code = data['course_code'],
            course_title = data['course_title'],
            credit_unit = data['credit_unit'],
            teacher_id = data['teacher_id']
        )

        new_course.student = current_student

        new_course.save()

        return new_course, HTTPStatus.CREATED

@course_namespace.route('/course/<int:course_id>')
class GetUpdateDelete(Resource):

    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @jwt_required()
    def get(self, course_id):
        """
            Retrieve a course by id
        """
        course = Course.get_by_id(course_id)

        return course, HTTPStatus.OK
    
@course_namespace.route('/course/<int:student_id>/courses')
class StudentCourses(Resource):
    
    @course_namespace.marshal_list_with(course_model)
    def get(self, student_id):
        """
        Get all Student courses
        """
        student = Student.get_by_id(student_id)

        courses = student.courses

        return courses, HTTPStatus.OK
    
@course_namespace.route('/student/<int:student_id>/course/<int:course_id>')
class getSpecificCourseByStudent(Resource):

    @course_namespace.marshal_with(course_model)
    def get (self, student_id, course_id):
        """
        Get a student specific course
        """
        student = Student.get_by_id(student_id)

        course = Course.query.filter_by(id=course_id).filter_by(student=student).first()

        return course, HTTPStatus.OK
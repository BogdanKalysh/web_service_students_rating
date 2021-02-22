from marshmallow import Schema, fields, post_load, validates

class NewUser(Schema):
    name = fields.String(required = True)
    email = fields.Email(required = True)
    password = fields.String(required = True)
    type_of_user = fields.String(required = True)
    group_id = fields.Integer()

    @validates('type_of_user')
    def validate_type_of_user(self, type_of_user):
        if type_of_user != 'teacher' and type_of_user != 'student' and type_of_user != 'admin':
            raise ValidationError('invalid type of user')

class UserInfo(Schema):
    id = fields.Integer()
    name = fields.String(required = True)
    email = fields.Email(required = True)
    type_of_user = fields.String(required = True)
    group_id = fields.Integer()

class GroupInfo(Schema):
    id = fields.Integer()
    name = fields.String(required = True)

class SubjectInfo(Schema):
    id = fields.Integer()
    name = fields.String(required = True)

class MarkInfo(Schema):
    id = fields.Integer()
    date = fields.Date(required = True)
    mark = fields.Float(required = True)
    subject_id = fields.Integer(required = True)
    student_id = fields.Integer(required = True)


class RatingInfo(Schema):
    id = fields.Integer()
    student_id = fields.Integer(required = True)
    student_name = fields.String(required = True)
    group_name = fields.String(required = True)
    mark = fields.Float(required = True)

    # def __init__(self, student_id, student_name, group_name, mark):
    #     self.student_id = student_id
    #     self.student_name = student_name
    #     self.group_name = group_name
    #     self.mark = mark
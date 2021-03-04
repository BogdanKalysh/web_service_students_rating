from flask import Blueprint, jsonify, request
from sqlalchemy.sql.functions import current_user

from schemas import *
from models import *
from werkzeug.security import check_password_hash
from flask_httpauth import HTTPBasicAuth

blueprint = Blueprint("Rating",__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email, password):
    session = Session()
    user = session.query(users).filter_by(email=email).one()
    if check_password_hash(user.password, password):
        return user




@blueprint.route("/user", methods = ["POST"])
@auth.login_required
def add_user():

    try:
        my_user = auth.current_user()
        if my_user.type_of_user == 'admin':
            session = Session()
            user_data = NewUser().load(request.json)
            user_obj = users(**user_data)

            db_user = session.query(users).filter(users.email == user_obj.email).first()
            if(db_user != None):
                return(jsonify({"error": "User whith such email already exists"})), 403

            if(user_obj.type_of_user != 'student'):
                user_obj.group_id = None
            if(user_obj.type_of_user == 'student' and user_obj.group_id == None):
                return(jsonify({"error": "Students must be added to some group"})), 403

            session.add(user_obj)
            session.commit()

            if(user_obj.type_of_user == 'student'):
                group_obj = session.query(groups).filter(groups.id == user_obj.group_id).first()
                rating_obj = rating(user_obj.id, user_obj.name, group_obj.name, 0)

                session.add(rating_obj)
                session.commit()

        else:
            return(jsonify({"error": "no access to creating users"})), 403
    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401
    
    return jsonify(UserInfo().dump(user_obj)), 200

@blueprint.route("/user/<int:id>", methods = ["PUT"])
@auth.login_required
def update_user(id):
    try:
        my_user = auth.current_user()
        if my_user.type_of_user == 'admin':
            session = Session()
            user_data = NewUser().load(request.json)
            user_obj = users(**user_data)

            user_data['password'] = user_obj.password

            db_user = session.query(users).filter(users.email == user_obj.email, users.id != id).first()
            if(db_user != None):
                return(jsonify({"error": "User whith such email already exists"})), 403

            orig_user = session.query(users).filter(users.id == id).first()
            if(orig_user == None):
                return(jsonify({"error": "User with this id does not exist"})), 403

            for key, value in user_data.items():
                setattr(orig_user, key, value)

            if(orig_user.type_of_user != 'student'):
                orig_user.group_id = None

            if(orig_user.type_of_user == 'student'):
                group_obj = session.query(groups).filter(groups.id == user_obj.group_id).first()

                rating_obj = session.query(rating).filter(rating.student_id == orig_user.id).first()

                new_rating_obj = rating(orig_user.id, orig_user.name, group_obj.name, rating_obj.mark)

                session.query(rating).filter(rating.student_id == orig_user.id).delete()
                session.add(new_rating_obj)

                session.commit()


            session.commit()
        else:
            return(jsonify({"error": "no access to updating users"})), 403
    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401
    
    return jsonify(UserInfo().dump(orig_user)), 200

@blueprint.route("/user/<int:id>", methods = ["DELETE"])
@auth.login_required
def delete_user(id):
    try:
        my_user = auth.current_user()
        if my_user.type_of_user == 'admin':
            session = Session()

            orig_user = session.query(users).filter(users.id == id).first()
            if(orig_user == None):
                return(jsonify({"error": "User with this id does not exist"})), 403

            if(orig_user.type_of_user == 'student'):

                session.query(rating).filter(rating.student_id == id).delete()
                session.commit()

            for group in orig_user.groups:
                orig_user.groups.remove(group)
                session.commit()

            for subject in orig_user.subjects:
                orig_user.subjects.remove(subject)
                session.commit()


            session.query(marks).filter(marks.student_id == id).delete()
            session.commit()
            session.query(users).filter(users.id == id).delete()
            session.commit()

        else:
            return(jsonify({"error": "no access to deleting users"})), 403
    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401
    
    return jsonify({"Successfully deleted user" : "OK", "id" : id}), 200




@blueprint.route("/group", methods = ["POST"])
@auth.login_required
def add_group():
    try:
        my_user = auth.current_user()
        if my_user.type_of_user == 'admin':
            session = Session()
            group_data = GroupInfo().load(request.json)
            group_obj = groups(**group_data)

            db_group = session.query(groups).filter(groups.name == group_obj.name).first()
            if(db_group != None):
                return(jsonify({"error": "Group whith such name already exists"})), 403

            session.add(group_obj)
            session.commit()
        else:
            return(jsonify({"error": "no access to creating groups"})), 403
    except Exception:
        return(jsonify({"error":"wrong data"})), 401
    
    return jsonify(GroupInfo().dump(group_obj)), 200

@blueprint.route("/group/<int:id>", methods = ["PUT"])
@auth.login_required
def update_group(id):
    try:
        my_user = auth.current_user()
        if my_user.type_of_user == 'admin':
            session = Session()
            group_data = GroupInfo().load(request.json)
            group_obj = groups(**group_data)


            db_group = session.query(groups).filter(groups.name == group_obj.name, groups.id != id).first()
            if(db_group != None):
                return(jsonify({"error": "Group whith such name already exists"})), 403

            orig_group = session.query(groups).filter(groups.id == id).first()
            if(orig_group == None):
                return(jsonify({"error": "Group with this id does not exist"})), 403

            for key, value in group_data.items():
                setattr(orig_group, key, value)

            session.commit()
        else:
            return(jsonify({"error": "no access to updating groups"})), 403
    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401
    
    return jsonify(GroupInfo().dump(orig_group)), 200


@blueprint.route("/group/<int:id>", methods = ["DELETE"])
@auth.login_required
def delete_group(id):
    try:
        my_user = auth.current_user()
        if my_user.type_of_user == 'admin':
            session = Session()

            orig_group = session.query(groups).filter(groups.id == id).first()
            if(orig_group == None):
                return(jsonify({"error": "Group with this id does not exist"})), 403

            group_student = session.query(users).filter(users.group_id == id).first()
            if(group_student != None):
                return(jsonify({"error": "Group contains students, can't be deleted"})), 403

            for teacher in orig_group.teachers:
                orig_group.teachers.remove(teacher)
            session.commit()

            session.query(groups).filter(groups.id == id).delete()

            session.commit()
        else:
            return(jsonify({"error": "no access to deleting groups"})), 403
    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401
    
    return jsonify({"Successfully deleted group, id " : id}), 200




@blueprint.route("/subject", methods = ["POST"])
@auth.login_required
def add_subject():
    try:
        my_user = auth.current_user()
        if my_user.type_of_user == 'admin':
            session = Session()
            subject_data = SubjectInfo().load(request.json)
            subject_obj = subjects(**subject_data)

            db_subject = session.query(subjects).filter(subjects.name == subject_obj.name).first()
            if(db_subject != None):
                return(jsonify({"error": "Subject whith such name already exists"})), 403

            session.add(subject_obj)
            session.commit()
        else:
            return(jsonify({"error": "no access to creating subjects"})), 403
    except Exception:
        return(jsonify({"error":"wrong data"})), 401
    
    return jsonify(SubjectInfo().dump(subject_obj)), 200


@blueprint.route("/subject/<int:id>", methods = ["DELETE"])
@auth.login_required
def delete_subject(id):
    try:
        my_user = auth.current_user()
        if my_user.type_of_user == 'admin':
            session = Session()

            orig_subject = session.query(subjects).filter(subjects.id == id).first()
            if(orig_subject == None):
                return(jsonify({"error": "Subject with this id does not exist"})), 403

            subject_mark = session.query(marks).filter(marks.subject_id == id).first()
            if(subject_mark != None):
                return(jsonify({"error": "There are marks from this subject, can't be deleted"})), 403

            for user in orig_subject.users:
                orig_subject.users.remove(user)
            session.commit()
            
            session.query(subjects).filter(subjects.id == id).delete()
            session.commit()
        else:
            return(jsonify({"error": "no access to deleting subjects"})), 403
    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401
    
    return jsonify({"Successfully deleted subject, id " : id}), 200




@blueprint.route("/user/<int:user_id>/subject/<int:subject_id>", methods = ["POST"])
@auth.login_required
def add_subject_to_user(user_id, subject_id):
    try:
        my_user = auth.current_user()
        if my_user.type_of_user == 'admin':
            session = Session()

            db_subject = session.query(subjects).filter(subjects.id == subject_id).first()
            db_user = session.query(users).filter(users.id == user_id).first()

            if(db_user == None):
                return(jsonify({"error": "user with this id does not exist"})), 403
            if(db_user.type_of_user != 'student' and db_user.type_of_user != 'teacher'):
                return(jsonify({"error": "you can add subjects only to teachers or students"})), 403
            if(db_subject == None):
                return(jsonify({"error": "subject with this id does not exist"})), 403
            
            for user in db_subject.users:
                if(user.id == int(user_id)):
                    return(jsonify({"error": "such relation already exists"})), 403


            db_subject.users.append(db_user)
            session.commit()
        else:
            return(jsonify({"error": "no access to managing subjects"})), 403
    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401
    
    return jsonify({"Successfully added subject" : "OK"}), 200


@blueprint.route("/user/<int:user_id>/subject/<int:subject_id>", methods = ["DELETE"])
@auth.login_required
def delete_subject_to_user(user_id, subject_id):
    try:
        my_user = auth.current_user()
        if my_user.type_of_user == 'admin':
            session = Session()

            db_subject = session.query(subjects).filter(subjects.id == subject_id).first()
            db_user = session.query(users).filter(users.id == user_id).first()

            if(db_user == None):
                return(jsonify({"error": "user with this id does not exist"})), 403
            if(db_subject == None):
                return(jsonify({"error": "subject with this id does not exist"})), 403
            
            for user in db_subject.users:
                if(user.id == user_id):
                    db_subject.users.remove(user)
                    session.commit()
                    return jsonify({"Successfully deleted relation" : "OK"}), 200
            return(jsonify({"error": "such relation does not exist"})), 403

        else:
            return(jsonify({"error": "no access to managing subjects"})), 403
    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401




@blueprint.route("/teacher/<int:teacher_id>/group/<int:group_id>", methods = ["POST"])
@auth.login_required
def add_group_to_teacher(teacher_id, group_id):
    try:
        my_user = auth.current_user()
        if my_user.type_of_user == 'admin':
            session = Session()

            db_group = session.query(groups).filter(groups.id == group_id).first()
            db_user = session.query(users).filter(users.id == teacher_id).first()

            if(db_user == None):
                return(jsonify({"error": "user with this id does not exist"})), 403
            if(db_user.type_of_user != 'teacher'):
                return(jsonify({"error": "you can add groups only to teachers"})), 403
            if(db_group == None):
                return(jsonify({"error": "group with this id does not exist"})), 403
            
            for user in db_group.teachers:
                if(user.id == int(teacher_id)):
                    return(jsonify({"error": "such relation already exists"})), 403

            db_group.teachers.append(db_user)
            session.commit()
        else:
            return(jsonify({"error": "no access to managing grups"})), 403
    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401
    
    return jsonify({"Successfully added group to a techer" : "OK"}), 200


@blueprint.route("/teacher/<int:teacher_id>/group/<int:group_id>", methods = ["DELETE"])
@auth.login_required
def delete_group_to_teacher(teacher_id, group_id):
    try:
        my_user = auth.current_user()
        if my_user.type_of_user == 'admin':
            session = Session()

            db_group = session.query(groups).filter(groups.id == group_id).first()
            db_user = session.query(users).filter(users.id == teacher_id).first()

            if(db_user == None):
                return(jsonify({"error": "user with this id does not exist"})), 403
            if(db_group == None):
                return(jsonify({"error": "group with this id does not exist"})), 403
            
            for user in db_group.teachers:
                if(user.id == teacher_id):
                    db_group.teachers.remove(user)
                    session.commit()
                    return jsonify({"Successfully deleted relation" : "OK"}), 200
            return(jsonify({"error": "such relation does not exist"})), 403

        else:
            return(jsonify({"error": "no access to managing subjects"})), 403
    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401




@blueprint.route("/mark", methods = ["POST"])
@auth.login_required
def add_mark_to_student():
    try:
        my_user = auth.current_user()
        if my_user.type_of_user == 'teacher':
            session = Session()

            mark_data = MarkInfo().load(request.json)
            mark_obj = marks(**mark_data)


            subject_obj = session.query(subjects).filter(subjects.id == mark_obj.subject_id).first()
            if(subject_obj == None):
                return(jsonify({"error": "subject with this id does not exist"})), 403

            student_obj = session.query(users).filter(users.id == mark_obj.student_id).first()
            if(student_obj == None):
                return(jsonify({"error": "student with this id does not exist"})), 403

            group_obj = session.query(groups).filter(groups.id == student_obj.group_id).first()

            if(student_obj.type_of_user != 'student'):
                return(jsonify({"error": "you can give marks to students only"})), 403

            for user in subject_obj.users:
                if(user.id == my_user.id):
                    break
            else:
                return(jsonify({"error": "you can not give marks from this subject"})), 403

            for user in group_obj.teachers:
                if(user.id == my_user.id):
                    break
            else:
                return(jsonify({"error": "you can not give marks to this group students"})), 403

            session.add(mark_obj)
            session.commit()

            rating_obj = session.query(rating).filter(rating.student_id == mark_obj.student_id).first()

            summ = 0

            all_marks = session.query(marks).filter(marks.student_id == mark_obj.student_id).all()

            for mark_obj in all_marks:
                summ += mark_obj.mark
            summ /= len(all_marks)

            new_rating_obj = rating(rating_obj.student_id, rating_obj.student_name, rating_obj.group_name, summ)
            session.query(rating).filter(rating.student_id == mark_obj.student_id).delete()
            session.add(new_rating_obj)

            session.commit()

        else:
            return(jsonify({"error": "no access to giving marks"})), 403
    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401
    
    return jsonify(MarkInfo().dump(mark_obj)), 200


@blueprint.route("/mark/<int:id>", methods = ["DELETE"])
@auth.login_required
def update_mark_to_student(id):
    try:
        my_user = auth.current_user()
        if my_user.type_of_user == 'teacher':
            session = Session()

            mark_obj = session.query(marks).filter(marks.id == id).first()

            if(mark_obj == None):
                 return(jsonify({"error": "mark with this id does not exist"})), 403

            subject_obj = session.query(subjects).filter(subjects.id == mark_obj.subject_id).first()
            if(subject_obj == None):
                return(jsonify({"error": "subject with this id does not exist"})), 403

            student_obj = session.query(users).filter(users.id == mark_obj.student_id).first()
            if(student_obj == None):
                return(jsonify({"error": "student with this id does not exist"})), 403

            group_obj = session.query(groups).filter(groups.id == student_obj.group_id).first()
            if(group_obj == None):
                return(jsonify({"error": "this student does not have group"})), 403

            for user in subject_obj.users:
                if(user.id == my_user.id):
                    break
            else:
                return(jsonify({"error": "you can not delete marks from this subject"})), 403

            for user in group_obj.teachers:
                if(user.id == my_user.id):
                    break
            else:
                return(jsonify({"error": "you can not delete marks of this group students"})), 403

            session.query(marks).filter(marks.id == id).delete()
            session.commit()

            rating_obj = session.query(rating).filter(rating.student_id == mark_obj.student_id).first()

            summ = 0

            all_marks = session.query(marks).filter(marks.student_id == mark_obj.student_id).all()
            if(all_marks != []):
                for mark_obj in all_marks:
                    summ += mark_obj.mark
                summ /= len(all_marks)

                new_rating_obj = rating(rating_obj.student_id, rating_obj.student_name, rating_obj.group_name, summ)
                session.query(rating).filter(rating.student_id == mark_obj.student_id).delete()
                session.add(new_rating_obj)

                session.commit()

        else:
            return(jsonify({"error": "no access to deleting marks"})), 403
    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401
    
    return jsonify({"Mark deleted sucessfully" : "OK"}), 200


@blueprint.route("/student/<int:student_id>/marks", methods = ["GET"])
@auth.login_required
def get_student_marks(student_id):
    try:
        session = Session()

        all_marks = session.query(marks).filter(marks.student_id == student_id).all()

    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401
    
    return jsonify(MarkInfo(many = True).dump(all_marks)), 200




@blueprint.route("/students", methods = ["GET"])
@auth.login_required
def get_students_rating():
    try:
        session = Session()

        all_students = session.query(rating).all()

    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401
    
    return jsonify(RatingInfo(many = True).dump(all_students)), 200


@blueprint.route("/students/<int:id>", methods = ["GET"])
@auth.login_required
def get_student_rating(id):
    try:
        session = Session()

        student = session.query(rating).filter(rating.student_id == id).first()

        if(student == None):
            return(jsonify({"error":"student with this id does not exist"})), 401

    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401
    
    return jsonify(RatingInfo().dump(student)), 200


@blueprint.route("/students/top/<int:quant>", methods = ["GET"])
@auth.login_required
def get_top_students_rating(quant):
    try:
        session = Session()
        all_students = session.query(rating).all()

    except Exception:
        return(jsonify({"code":401,"error":"wrong data"})), 401

    lil = RatingInfo(many = True).dump(all_students)
    lil2 = sorted(lil, key = lambda i: i['mark'], reverse = True)
    
    return jsonify(lil2[0:int(quant)]), 200
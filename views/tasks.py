from flask import request
from flask_restful import Resource

from models import User, DashBoard, Task, serialize_multiple
from settings import db


class Tasks(Resource):
    def get(self):
        return serialize_multiple(Task.query.all())

    def post(self):
        data = request.get_json()

        task = Task(**data)
        db.session.add(task)
        db.session.flush()

        task_id = task.id
        db.session.commit()

        return {"id": task_id}, 201


class SingleTask(Resource):
    def get(self, task_id):
        return Task.query.get(task_id).serialize()


class TaskUsers(Resource):
    def get(self, task_id):
        return serialize_multiple(Task.query.get(task_id).users_id)

    def post(self, task_id):
        user_id = request.get_json()['user_id']
        task = Task.query.get(task_id)
        task.users_id.append(User.query.get(user_id))
        db.session.commit()

        return {}, 201


class TaskMasterUser(Resource):
    def get(self, task_id):
        user_id = Task.query.get(task_id).master_user_id
        print(user_id)
        return User.query.get(user_id).serialize()

    def patch(self, task_id):
        data = request.get_json()
        db.session.query(Task).filter_by(id=task_id).update(data)
        db.session.commit()
        return 204


class TaskComment(Resource):    # Vopros
    def get(self, task_id):
        return Task.query.get(task_id).task_comment

    def post(self, task_id):
        data = request.get_json()['task_comment']
        user = request.get_json()['users_id']
        task = Task.query.get(task_id)
        if user in task.users_id:
            db.session.query(Task).filter_by(id=task_id).update(data)
            db.session.commit()
            return {}, 201
        else:
            return f"You cant comment this Task"


class TaskStatus(Resource):
    def get(self, task_id):
        print(task_id)
        return Task.query.get(task_id).status

    def post(self, task_id):
        data = request.get_json()['status']
        st = ['to do', 'in progress', 'done']
        if data.lower() in st:
            db.session.query(Task).filter_by(id=task_id).update(data)
        else:
            return f"Inappropriate operation", 406

    def patch(self, task_id):
        data = request.get_json()
        db.session.query(Task).filter_by(id=task_id).update(data)
        db.session.commit()
        return 204


class TaskWithStatus(Resource):
    def get(self, status):
        print(status)
        status_ = status.replace("-", " ")
        return serialize_multiple(Task.query.filter_by(status=status_).all())

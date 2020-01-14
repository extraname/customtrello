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
        return serialize_multiple(Task.query.get(task_id).users)

    def post(self, task_id):
        user_id = request.get_json()['user_id']
        task = Task.query.get(task_id)
        task.users.append(User.query.get(user_id))
        db.session.commit()

        return {}, 201


class TaskMasterUser(Resource):     # VOPROS
    def get(self, tasks_id):
        user_id = Task.query.get(tasks_id).master_user_id
        return serialize_multiple(User.query.get(user_id))

    def patch(self, task_id):
        data = request.get_json()
        db.session.query(Task).filter_by(id=task_id).update(data)
        db.session.commit()
        return 204


class TaskComment(Resource):    # Vopros
    def get(self, task_id):
        return serialize_multiple(Task.query.get(task_id).task_comment)

    def post(self, task_id):
        data = request.get_json()['task_comment']
        user = request.get_json()['users_id']
        task = Task.query.get(task_id)
        if user in task.users:
            db.session.query(Task).filter_by(id=task_id).update(data)
            db.session.commit()
            return {}, 201
        else:
            return f"You cant comment this Task"


class TaskStatus(Resource):     # VOPROS
    def get(self, task_id):
        return serialize_multiple(Task.query.get(task_id).status)

    def post(self, task_id):
        data = request.get_json()['status']
        st = ['to do', 'in progress', 'done']
        if data.lower() in st:
            db.session.query(Task).filter_by(id=task_id).update(data)
        else:
            return f"Inappropriate operation", 406

    def patch(self, task_id):
        data = request.get_json()['status']
        db.session.query(Task).filter_by(id=task_id).update(data)
        db.session.commit()
        return 204


class TaskWithStatus(Resource):
    def get(self, status):
        return Task.query.filter_by(status=status).get.all()

from flask import request
from flask_restful import Resource

from models import User, DashBoard, Task, serialize_multiple
from settings import db


class DashBoards(Resource):
    def get(self):
        return serialize_multiple(DashBoard.query.all())

    def post(self):
        data = request.get_json()

        dashboard = DashBoard(**data)
        db.session.add(dashboard)
        db.session.flush()

        dashboard_id = dashboard.id
        db.session.commit()

        return {"id": dashboard_id}, 201


class DashBoardUsers(Resource):
    def get(self, dashboard_id):
        return serialize_multiple(DashBoard.query.get(dashboard_id).users)

    def post(self, dashboard_id):
        user_id = request.get_json()['user_id']
        dashboard = DashBoard.query.get(dashboard_id)
        dashboard.users.append(User.query.get(user_id))
        db.session.commit()

        return {}, 201


class DashBoardTasks(Resource):
    def get(self, dashboard_id):
        return serialize_multiple(
            Task.query.filter(Task.dashboard_id == dashboard_id).all()
        )

    def post(self, dashboard_id):   # Задать вопросы
        task_id = request.get_json()['task_id']
        dashboard = DashBoard.query.get(dashboard_id)
        dashboard.tasks.append(Task.query.get(task_id))
        db.session.commit()

        return {}, 201

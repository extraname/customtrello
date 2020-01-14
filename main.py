from settings import app, api

from views.dashboards import DashBoard, DashBoards, DashBoardUsers,\
    DashBoardTasks
from views.tasks import Task, SingleTask, Tasks, TaskMasterUser, TaskUsers,\
    TaskComment, TaskStatus, TaskWithStatus
from views.users import User, Users, SingleUser

api.add_resource(Users, '/users')
api.add_resource(SingleUser, '/users/<int:user_id>')

api.add_resource(DashBoards, '/dashboards')
api.add_resource(DashBoardUsers, '/dashboards/<int:dashboard_id>/users')
api.add_resource(DashBoardTasks, '/dashboards/<int:dashboard_id>/tasks')

api.add_resource(Tasks, '/tasks')
api.add_resource(SingleTask, '/tasks/<int:task_id>')
api.add_resource(TaskMasterUser, '/tasks/<int:tasks_id>/master')
api.add_resource(TaskUsers, '/tasks/<int:task_id>/users')
api.add_resource(TaskComment, '/tasks/<int:task_id>/comment')
api.add_resource(TaskStatus, '/tasks/<int:task_id>/status')
api.add_resource(TaskWithStatus, '/tasks/<string:status>')

if __name__ == "__main__":
    app.run()

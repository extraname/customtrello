from settings import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }


dashboard_users_table = db.Table(
    "dashboard_users", db.Model.metadata,
    db.Column('dashboard_id', db.Integer, db.ForeignKey("dashboards.id")),
    db.Column('user_id', db.Integer, db.ForeignKey("users.id"))
)


class DashBoard(db.Model):
    __tablename__ = 'dashboards'

    id = db.Column(db.Integer, primary_key=True)
    dashboard_name = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship(
        "User",
        secondary=dashboard_users_table,
        backref="dashboard"
    )

    tasks = db.relationship("Task", backref="dashboard")

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.dashboard_name,
            "users": self.users,
            "tasks": self.tasks
        }


task_users_table = db.Table(
    "task_users", db.Model.metadata,
    db.Column('task_id', db.Integer, db.ForeignKey("tasks.id")),
    db.Column('user_id', db.Integer, db.ForeignKey("users.id"))
)


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    dashboard_id = db.Column(db.Integer, db.ForeignKey("dashboards.id"))
    master_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    users_id = db.relationship(
        "User",
        secondary=task_users_table,
        backref="tasks"
    )
    text = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(15), nullable=False)
    task_comment = db.Column(db.String(25), unique=True, nullable=True)

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "dashboard_id": self.dashboard_id,
            "name": self.name,
            "text": self.text,
            "status": self.status,
            "comment": self.task_comment,
            "master_id": self.master_user_id
        }


def serialize_multiple(objects: list) -> list:
    return [obj.serialize() for obj in objects]


if __name__ == '__main__':
    db.create_all()

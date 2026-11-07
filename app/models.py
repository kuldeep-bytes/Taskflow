from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    start_at = db.Column(db.DateTime)

    due_at = db.Column(db.DateTime)

    completed_at = db.Column(db.DateTime)

    @property
    def status(self):

        if self.completed:
            return "Completed"

        if self.due_at and self.due_at < datetime.now():
            return "Overdue"

        return "Pending"
from django.db.models import (
    Model,
    ForeignKey,
    TextField
)
from django.contrib.auth import get_user_model
from app.tasks.models import Solution

UserModel = get_user_model()


class Save(Model):

    content = TextField(default="", blank=True)
    task = ForeignKey(Solution)
    user = ForeignKey(UserModel)


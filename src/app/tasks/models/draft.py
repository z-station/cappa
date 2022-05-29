from django.contrib.auth import get_user_model
from django.db.models import (
    Model,
    ForeignKey,
    TextField,
    CharField
)
from app.tasks.models import Task
from app.translators.enums import TranslatorType

UserModel = get_user_model()


class Draft(Model):

    task = ForeignKey(Task)
    user = ForeignKey(UserModel)
    translator = CharField(
        max_length=100,
        choices=TranslatorType.CHOICES
    )
    content = TextField()

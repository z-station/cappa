from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CustomModelBackend(ModelBackend):

    """ Расширенный бекенд.
        аутентификация по логину или email """

    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            if username is not None:
                user = UserModel.objects.get(username=username)
            elif email is not None:
                user = UserModel.objects.get(email=email)
            else:
                raise UserModel.DoesNotExist
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

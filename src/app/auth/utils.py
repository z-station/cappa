from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.utils import timezone

from app.accounts.enums import UserRole
from app.service.enums import SiteAccessType

UserModel = get_user_model()


def logout_users_by_access_type(access_type: SiteAccessType):

    users_ids = None
    if access_type == SiteAccessType.TEACHER:
        users_ids = set(
            UserModel.objects
            .filter(role=UserRole.LEARNER)
            .values_list('pk', flat=True)
        )
    if access_type == SiteAccessType.SUPERUSER:
        users_ids = set(
            UserModel.objects
            .filter(is_superuser=False)
            .values_list('pk', flat=True)
        )

    if not users_ids:
        return
    deleted_sessions_count = 0
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in sessions:
        auth_user_id = session.get_decoded().get('_auth_user_id')
        if int(auth_user_id) in users_ids:
            session.delete()
            deleted_sessions_count +=1
    print(deleted_sessions_count)

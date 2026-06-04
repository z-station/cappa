from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.test import Client, RequestFactory, TestCase

from app.accounts.enums import UserRole
from app.service.admin.site import SiteSettingsAdmin
from app.service.enums import SiteAccessType
from app.service.models.site import SiteSettings

User = get_user_model()


class SigninLogoutOnSiteSettingsChangeTests(TestCase):

    password = 'testpass123'

    def setUp(self):
        self.client = Client()
        self.learner = User.objects.create_user(
            username='learner',
            email='learner@example.com',
            password=self.password,
        )
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password=self.password,
            role=UserRole.TEACHER,
        )
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password=self.password,
        )
        self.site_settings, _ = SiteSettings.objects.get_or_create(
            id=settings.SITE_ID,
            defaults={
                'domain': 'example.com',
                'name': 'Test Site',
            },
        )
        self.site_settings.signin = SiteAccessType.ALL
        self.site_settings.save(update_fields=['signin'])
        self.site_settings_admin = SiteSettingsAdmin(SiteSettings, AdminSite())
        self.admin_request = RequestFactory().get('/')

    def _login(self, user):
        self.assertTrue(self.client.login(username=user.username, password=self.password))

    def _change_signin(self, access_type):
        self.site_settings.signin = access_type
        self.site_settings_admin.save_model(
            self.admin_request,
            self.site_settings,
            form=None,
            change=True,
        )

    def _session_has_user(self, user):
        session_key = self.client.session.session_key
        if not session_key:
            return False
        try:
            session = Session.objects.get(session_key=session_key)
        except Session.DoesNotExist:
            return False
        return session.get_decoded().get('_auth_user_id') == str(user.pk)

    def test_logout_learner_when_signin_changes_to_teacher_only(self):
        self._login(self.learner)
        self.assertTrue(self._session_has_user(self.learner))

        self._change_signin(SiteAccessType.TEACHER)

        self.assertFalse(self._session_has_user(self.learner))

    def test_keeps_teacher_session_when_signin_changes_to_teacher_only(self):
        self._login(self.teacher)
        self.assertTrue(self._session_has_user(self.teacher))

        self._change_signin(SiteAccessType.TEACHER)

        self.assertTrue(self._session_has_user(self.teacher))

    def test_logout_non_superuser_when_signin_changes_to_superuser_only(self):
        self._login(self.teacher)
        self.assertTrue(self._session_has_user(self.teacher))

        self._change_signin(SiteAccessType.SUPERUSER)

        self.assertFalse(self._session_has_user(self.teacher))

    def test_keeps_superuser_session_when_signin_changes_to_superuser_only(self):
        self._login(self.superuser)
        self.assertTrue(self._session_has_user(self.superuser))

        self._change_signin(SiteAccessType.SUPERUSER)

        self.assertTrue(self._session_has_user(self.superuser))

    def test_does_not_logout_when_signin_changes_to_all(self):
        self.site_settings.signin = SiteAccessType.TEACHER
        self.site_settings.save(update_fields=['signin'])
        self._login(self.learner)
        self.assertTrue(self._session_has_user(self.learner))

        self._change_signin(SiteAccessType.ALL)

        self.assertTrue(self._session_has_user(self.learner))

    def test_does_not_logout_when_signin_is_unchanged(self):
        self._login(self.learner)
        self.assertTrue(self._session_has_user(self.learner))

        self.site_settings.logo_title = 'updated'
        self.site_settings.save(update_fields=['logo_title'])

        self.assertTrue(self._session_has_user(self.learner))

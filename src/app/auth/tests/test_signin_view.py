from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from rest_framework.authtoken.models import Token

from app.accounts.enums import UserRole
from app.auth.permissions import SignInPermission
from app.service.enums import SiteAccessType
from app.service.models.site import SiteSettings

User = get_user_model()


class SignInViewTests(TestCase):

    signin_url = '/auth/signin/'
    password = 'testpass123'

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password=self.password,
            first_name='Test',
            last_name='User',
        )

    def _set_signin_access(self, access_type):
        site_settings, _ = SiteSettings.objects.get_or_create(
            id=settings.SITE_ID,
            defaults={
                'domain': 'example.com',
                'name': 'Test Site',
            },
        )
        site_settings.signin = access_type
        site_settings.save(update_fields=['signin'])
        return site_settings

    def _post_signin(self, login=None, password=None, next_path='/', **extra):
        data = {
            'login': login if login is not None else self.user.username,
            'password': password if password is not None else self.password,
            'next': next_path,
        }
        data.update(extra)
        return self.client.post(self.signin_url, data)

    def test_get_renders_signin_page_for_anonymous_user(self):
        # Act
        response = self.client.get(self.signin_url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/signin.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['signup_path'], '/auth/signup/')

    def test_get_redirects_active_authenticated_user(self):
        # Arrange
        self.client.login(username=self.user.username, password=self.password)

        # Act
        response = self.client.get(self.signin_url)

        # Assert
        self.assertRedirects(response, '/')

    def test_get_uses_next_query_param_in_form(self):
        # Act
        response = self.client.get(self.signin_url, {'next': '/groups/'})

        # Assert
        self.assertEqual(response.context['form'].initial['next'], '/groups/')
        self.assertEqual(
            response.context['signup_path'],
            '/auth/signup/?next=/groups/',
        )

    def test_get_uses_referer_path_when_next_is_missing(self):
        # Act
        response = self.client.get(
            self.signin_url,
            HTTP_REFERER='http://example.com/courses/list/',
        )

        # Assert
        self.assertEqual(response.context['form'].initial['next'], '/courses/list/')

    def test_post_success_with_username_logs_in_and_creates_token(self):
        # Act
        response = self._post_signin()

        # Assert
        self.assertRedirects(response, '/')
        self.assertIn('_auth_user_id', self.client.session)
        self.assertTrue(Token.objects.filter(user=self.user).exists())

    def test_post_success_with_email(self):
        # Act
        response = self._post_signin(login=self.user.email)

        # Assert
        self.assertRedirects(response, '/')
        self.assertIn('_auth_user_id', self.client.session)

    def test_post_success_redirects_to_next_path(self):
        # Act
        response = self._post_signin(next_path='/courses/')

        # Assert
        self.assertRedirects(response, '/courses/')

    def test_post_invalid_credentials_shows_error(self):
        # Act
        response = self._post_signin(password='wrong-password')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/signin.html')
        self.assertFormError(
            response,
            'form',
            None,
            'Проверьте правильность написания логина и пароля',
        )

    def test_post_empty_fields_shows_error(self):
        # Act
        response = self._post_signin(login='', password='')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            'form',
            None,
            'Заполните обязательные поля',
        )

    def test_post_inactive_user_shows_error(self):
        # Arrange
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])

        # Act
        response = self._post_signin()

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            'form',
            None,
            'Учетная запись не активна',
        )

    def test_post_denies_learner_when_signin_for_teachers_only(self):
        # Arrange
        self._set_signin_access(SiteAccessType.TEACHER)

        # Act
        response = self._post_signin()

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            'form',
            None,
            SignInPermission.message,
        )
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_post_allows_teacher_when_signin_for_teachers_only(self):
        # Arrange
        self._set_signin_access(SiteAccessType.TEACHER)
        self.user.role = UserRole.TEACHER
        self.user.save(update_fields=['role'])

        # Act
        response = self._post_signin()

        # Assert
        self.assertRedirects(response, '/')
        self.assertIn('_auth_user_id', self.client.session)

    def test_post_denies_regular_user_when_signin_for_superusers_only(self):
        # Arrange
        self._set_signin_access(SiteAccessType.SUPERUSER)

        # Act
        response = self._post_signin()

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            'form',
            None,
            SignInPermission.message,
        )

    def test_post_allows_superuser_when_signin_for_superusers_only(self):
        # Arrange
        self._set_signin_access(SiteAccessType.SUPERUSER)
        self.user.is_superuser = True
        self.user.save(update_fields=['is_superuser'])

        # Act
        response = self._post_signin()

        # Assert
        self.assertRedirects(response, '/')

    def test_post_allows_user_when_signin_is_open_for_all(self):
        # Arrange
        self._set_signin_access(SiteAccessType.ALL)

        # Act
        response = self._post_signin()

        # Assert
        self.assertRedirects(response, '/')

    def test_post_reuses_existing_token(self):
        # Arrange
        Token.objects.create(user=self.user)

        # Act
        response = self._post_signin()

        # Assert
        self.assertRedirects(response, '/')
        self.assertEqual(Token.objects.filter(user=self.user).count(), 1)

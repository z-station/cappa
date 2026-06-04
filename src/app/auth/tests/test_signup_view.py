from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from rest_framework.authtoken.models import Token

from app.auth.permissions import SignInPermission, SignUpPermission
from app.service.enums import SiteAccessType
from app.service.models.site import SiteSettings

User = get_user_model()


class SignUpViewTests(TestCase):

    signup_url = '/auth/signup/'
    password = 'testpass123'

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password=self.password,
            first_name='Existing',
            last_name='User',
        )

    def _get_site_settings(self):
        site_settings, _ = SiteSettings.objects.get_or_create(
            id=settings.SITE_ID,
            defaults={
                'domain': 'example.com',
                'name': 'Test Site',
            },
        )
        return site_settings

    def _valid_signup_data(self, **overrides):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': self.password,
            'password2': self.password,
            'next': '/',
        }
        data.update(overrides)
        return data

    def _post_signup(self, **overrides):
        return self.client.post(self.signup_url, self._valid_signup_data(**overrides))

    def test_get_renders_signup_page_for_anonymous_user(self):
        # Act
        response = self.client.get(self.signup_url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/signup.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['signin_path'], '/auth/signin/')
        self.assertFalse(response.context['confirm_signup'])

    def test_get_redirects_active_authenticated_user(self):
        # Arrange
        self.client.login(username=self.user.username, password=self.password)

        # Act
        response = self.client.get(self.signup_url)

        # Assert
        self.assertRedirects(response, '/')

    def test_get_uses_next_query_param_in_form(self):
        # Act
        response = self.client.get(self.signup_url, {'next': '/groups/'})

        # Assert
        self.assertEqual(response.context['form'].initial['next'], '/groups/')
        self.assertEqual(
            response.context['signin_path'],
            '/auth/signin/?next=/groups/',
        )

    def test_get_uses_referer_path_when_next_is_missing(self):
        # Act
        response = self.client.get(
            self.signup_url,
            HTTP_REFERER='http://example.com/courses/list/',
        )

        # Assert
        self.assertEqual(response.context['form'].initial['next'], '/courses/list/')

    def test_get_reflects_confirm_signup_setting(self):
        # Arrange
        site_settings = self._get_site_settings()
        site_settings.confirm_signup = True
        site_settings.save(update_fields=['confirm_signup'])

        # Act
        response = self.client.get(self.signup_url)

        # Assert
        self.assertTrue(response.context['confirm_signup'])

    def test_post_success_creates_user_logs_in_and_creates_token(self):
        # Act
        response = self._post_signup()

        # Assert
        new_user = User.objects.get(username='newuser')
        self.assertRedirects(response, '/')
        self.assertTrue(new_user.is_active)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), new_user.pk)
        self.assertTrue(Token.objects.filter(user=new_user).exists())

    def test_post_success_redirects_to_next_path(self):
        # Act
        response = self._post_signup(next='/courses/')

        # Assert
        self.assertRedirects(response, '/courses/')
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_post_with_confirm_signup_creates_inactive_user_without_login(self):
        # Arrange
        site_settings = self._get_site_settings()
        site_settings.confirm_signup = True
        site_settings.save(update_fields=['confirm_signup'])

        # Act
        response = self._post_signup()

        # Assert
        new_user = User.objects.get(username='newuser')
        self.assertRedirects(response, '/')
        self.assertFalse(new_user.is_active)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertFalse(Token.objects.filter(user=new_user).exists())

    def test_post_denied_when_signup_disabled(self):
        # Arrange
        site_settings = self._get_site_settings()
        site_settings.signup = False
        site_settings.save(update_fields=['signup'])

        # Act
        response = self._post_signup()

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/signup.html')
        self.assertFormError(
            response,
            'form',
            None,
            SignUpPermission.message,
        )
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_post_renders_error_without_login_when_signin_restricted(self):
        # Arrange
        site_settings = self._get_site_settings()
        site_settings.signin = SiteAccessType.TEACHER
        site_settings.save(update_fields=['signin'])

        # Act
        response = self._post_signup()

        # Assert
        new_user = User.objects.get(username='newuser')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/signup.html')
        self.assertFormError(
            response,
            'form',
            None,
            SignInPermission.message,
        )
        self.assertTrue(new_user.is_active)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertFalse(Token.objects.filter(user=new_user).exists())

    def test_post_duplicate_username_shows_error(self):
        # Act
        response = self._post_signup(username=self.user.username)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            'form',
            'username',
            'Пользователь с таким логином уже существует',
        )

    def test_post_password_mismatch_shows_error(self):
        # Act
        response = self._post_signup(password2='another-password')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            'form',
            None,
            'Пароли не совпадают',
        )
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_post_duplicate_email_shows_error(self):
        # Act
        response = self._post_signup(email=self.user.email)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            'form',
            None,
            'Пользователь с такой почтой уже существует',
        )
        self.assertFalse(User.objects.filter(username='newuser').exists())

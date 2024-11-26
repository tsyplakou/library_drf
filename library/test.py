from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class TestCase(APITestCase):
    user = None

    def set_user(self, user):
        if user is None:
            self.client.logout()
            self.user = None
            return

        self.user = user
        token = Token.objects.create(user=user)
        self.client.force_login(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

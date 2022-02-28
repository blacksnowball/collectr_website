from django.test import TestCase
from rest_framework.test import APITestCase
from .models import CustomUser
from rest_framework import status
from django.urls import reverse
from django.core import mail
from django.conf import settings
import jwt

class TestRegister(APITestCase):
    """
    A class for testing registration. Checks correct email is sent out without actually sending emails.
    Checks email token correctly encodes user ID.
    """

    def setUp(self):
        self.url=reverse("register")

    def test_register_email_is_sent(self):
        ### Before running unit tests, change the email domain.
        ### as per user_views.py comments, lines 33 & 127
        data = {"email" : "test@email.com", "username": "Jemima", "password": "mango2389", "password2": "mango2389"}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual("registration", mail.outbox[0].subject)
        self.assertEqual("collectr2021@outlook.com", mail.outbox[0].from_email)
        self.assertEqual("test@email.com", mail.outbox[0].to[0])


    def test_register_token(self):
        # integration testing was done in postman with real email sending / actually following email link.
        data = {"email" : "test@email.com", "username": "Jemima", "password": "mango2389", "password2": "mango2389"}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reg_token = mail.outbox[0].body.partition("?token=")[2].strip()

        payload = jwt.decode(reg_token, settings.SECRET_KEY, algorithms='HS256')
        user = CustomUser.objects.get(id=payload['user_id'])
        self.assertEqual(user.username, "Jemima")


class TestLogin(APITestCase):
    """
    A class for testing successfull and unsuccessfull logon attempts..
    """

    def setUp(self):
        self.url=reverse("login")
        self.active_jim = CustomUser.objects.create_user(email="jim@gmail.com", username="jim", password="mango2389", is_active=True)
        self.inactive_bob = CustomUser.objects.create_user(email="bob@gmail.com", username="bob", password="croissant843", is_active=False)

    def test_good_logon(self):
        data = {"username": "jim", "password": "mango2389"}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_view_accessible_with_token(self):
        data = {"username": "jim", "password": "mango2389"}
        response_login = self.client.post(self.url, data, format='multipart')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + TokensFromResponse(response_login).access)
        data = {"refresh": TokensFromResponse(response_login).refresh}
        response_logout = self.client.post(reverse("logout"), data)
        self.assertEqual(response_logout.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_view_inaccessible_without_token(self):
        data = {"refresh": "how you doin?"}
        response_logout = self.client.post(reverse("logout"), data)
        self.assertEqual(response_logout.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bad_username(self):
        data = {"username": "jimbo", "password": "mango2389"}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual("no access token", TokensFromResponse(response).access)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_username(self):
        data = {"username": "", "password": "mango2389"}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual("no access token", TokensFromResponse(response).access)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_password(self):
        data = {"username": "jim", "password": "#MangoesAreEvil"}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual("no access token", TokensFromResponse(response).access)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_password(self):
        data = {"username": "jim", "password": ""}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual("no access token", TokensFromResponse(response).access)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inactive_user(self):
        data = {"username": "bob", "password": "croissant843"}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual("no access token", TokensFromResponse(response).access)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestResetPassword(APITestCase):
    """
    A class for testing password reset. Checks correct email is sent out without actually sending emails.
    Checks email token correctly encodes user ID.
    """

    def setUp(self):
        self.url=reverse("reset")
        self.forgetful_user = CustomUser.objects.create_user(email="resetter@email.com", username="Jeoffrey", password="mango2389",
                                                         is_active=True)

    def test_reset_email_is_sent(self):
        ### Before running unit tests, change the email domain.
        ### as per user_views.py comments, lines 33 & 127
        data = {"email" : "resetter@email.com"}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual("reset", mail.outbox[0].subject)
        self.assertEqual("collectr2021@outlook.com", mail.outbox[0].from_email)
        self.assertEqual("resetter@email.com", mail.outbox[0].to[0])


    def test_reset_token(self):
        # integration testing was done in postman with real email sending / actually following email link.
        data = {"email" : "resetter@email.com"}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reset_token = mail.outbox[0].body.partition("?token=")[2].strip()

        payload = jwt.decode(reset_token, settings.SECRET_KEY, algorithms='HS256')
        user = CustomUser.objects.get(id=payload['user_id'])
        self.assertEqual(user.username, "Jeoffrey")


class TokensFromResponse():

    def __init__(self, response):
        self.access="no access token"
        self.refresh="no refresh token"
        try:
            self.access = response.json()['tokens']['access']
            self.refresh = response.json()['tokens']['refresh']
        except KeyError:
            pass


def printSpecial(nickname, value):
    print("\n"+"  value:----------------------"+nickname)
    print(value)
    print("\n"+"type:-----------------------")
    print(type(value))
    # print("\n"+"repr:------")
    # print(repr(value))
    print("\n"+"---------------------------")

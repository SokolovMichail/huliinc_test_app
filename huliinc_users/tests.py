# Create your tests here.
import json
import unittest.mock
from unittest.mock import patch, Mock, MagicMock

from django.test import TestCase
from huliinc_users.models import CustomUser


def confirm_send_email(var):
    var.append('OK')

class ViewTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(email="a@b.com", password="123",user_information="IamUser")
        CustomUser.objects.create_user(email="b@c.com", password="123", user_information="IamUser2",is_verified=True)

    def test_user_get_case(self):
        """Animals that can speak are correctly identified"""
        response = self.client.get("/api/users")
        data = json.loads(response.content.decode())
        assert len(data['users']) == 2

    def test_user_create_case(self):
        email_sent_flag = []
        mock = Mock(side_effect=confirm_send_email(email_sent_flag))
        with unittest.mock.patch('huliinc_users.send_email.EmailSender.send_registration_email',mock):
            response = self.client.post(
                "/api/users",
                data = {
                    "email": "d@q.com",
                    "password": "1234",
                    "user_information": "Test User in Fixture"
                }
            )
            assert email_sent_flag[0]=='OK'
            assert response.status_code == 200
            user = CustomUser.objects.get(email='d@q.com')
            assert not user.is_verified

    def test_user_verification(self):
        response = self.client.get(
            "/api/users/verify?email=a@b.com",
        )
        assert response.status_code == 200
        user = CustomUser.objects.get(email='a@b.com')
        assert user.is_verified

    def test_user_patch_case(self):
        response = self.client.patch(
            "/api/users",
            data = {
                "email": "b@c.com",
                "password": "1234",
                "user_information": "Test User in Fixture"
            },
            content_type="application/json"
        )
        assert response.status_code == 200
        user = CustomUser.objects.get(email='b@c.com')
        assert user.user_information == "Test User in Fixture"
        assert user.check_password("1234")

    def test_user_token(self):
        response = self.client.post(
            "/api/users/token",
            data={
                "email": "b@c.com",
                "password": "12",
            },
            content_type="application/json"
        )
        assert response.status_code == 401
        response = self.client.post(
            "/api/users/token",
            data={
                "email": "b@c.com",
                "password": "123",
            },
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        token = data['access']
        response = self.client.get(
            "/me",
            data={
                "email": "b@c.com",
            },
            headers={
                "Authorization":f"Bearer {token}"
            },
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        assert data['user_information'] == "IamUser2"




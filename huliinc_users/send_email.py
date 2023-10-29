import copy
import os

from django.contrib.auth import get_user_model
from mailjet_rest import Client


class EmailSender:
    EMAIL = "djangoexamplebot@tutanota.com"

    data = {
        "From": {
            "Email": "djangoexamplebot@tutanota.com",
            "Name": "Registration"
        },
        "To": [
            {
                "Email": "",
            }
        ],
        "Subject": "",
        "TextPart": ""
    }

    @classmethod
    def generate_registration_email_data(cls, formed_link):
        data = copy.deepcopy(cls.data)
        data['Subject'] = "Registration to site"
        data['TextPart'] = f"""
        Welcome! In order to complete your registration, please go to {formed_link} 
        """
        return data

    @classmethod
    def generate_daily_report(cls):
        User = get_user_model()

        data = copy.deepcopy(cls.data)
        data['Subject'] = "Daily Report"
        data['TextPart'] = f"""
                Currently, there are {len(User.objects.all(is_verified=True))} verified users in the database.
                """
        return data

    @staticmethod
    def get_api_keys():
        api_pub = os.getenv("MAILJET_APIKEY_PUBLIC")
        api_sec = os.getenv("MAILJET_APIKEY_SECRET")
        return api_pub, api_sec


    @classmethod
    def send_registration_email(cls, email: str, request):
        host_ip = os.getenv("HOST_IP")
        host_port = os.getenv("HOST_PORT")
        api_pub, api_sec = EmailSender.get_api_keys()
        registration_link = f"http://{host_ip}:{host_port}/api/users/register?email={email}"
        mailjet = Client(auth=(api_pub, api_sec), version='v3.1')
        message = cls.generate_registration_email_data(registration_link)
        message['To'][0]['Email'] = email
        data = {
            'Messages': [
                message
            ]
        }
        result = mailjet.send.create(data=data)

    @classmethod
    def send_report_email(cls):
        api_pub, api_sec = EmailSender.get_api_keys()
        mailjet = Client(auth=(api_pub, api_sec), version='v3.1')
        message = cls.generate_daily_report()
        message['To'][0]['Email'] = os.getenv("ADMIN_EMAIL")
        data = {
            'Messages': [
                message
            ]
        }
        result = mailjet.send.create(data=data)

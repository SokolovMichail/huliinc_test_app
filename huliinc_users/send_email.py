import copy
import os

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
        pass

    @classmethod
    def send_email(cls, email: str, request):
        host_ip = os.getenv("HOST_IP")
        host_port = os.getenv("HOST_PORT")
        api_pub = os.getenv("MAILJET_APIKEY_PUBLIC")
        api_sec = os.getenv("MAILJET_APIKEY_SECRET")
        registration_link = f"http://{host_ip}:{host_port}/api/users/register?email={email}"
        mailjet = Client(auth=(api_pub, api_sec), version='v3.1')
        message =  cls.generate_registration_email_data(registration_link)
        message['To'][0]['Email'] = email
        data = {
            'Messages': [
                message
            ]
        }
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())

from django.contrib.auth import get_user_model

from huliinc_users.send_email import EmailSender


class ReportGenerator():

    @staticmethod
    def send_report():
        EmailSender.send_report_email()
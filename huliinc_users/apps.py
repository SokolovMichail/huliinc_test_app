from django.apps import AppConfig


class HuliincUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'huliinc_users'

    def ready(self):
        from . import report_cron_sender
        report_cron_sender.start()

# class ReportConfig(AppConfig):
#     name = 'huliinc_users'
#
#     def ready(self):
#         from . import report_cron_sender
#         report_cron_sender.start()
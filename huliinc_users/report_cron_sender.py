from apscheduler.schedulers.background import BackgroundScheduler

from huliinc_users.generate_report import ReportGenerator


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(ReportGenerator.generate_report,'interval',hours=24)
    scheduler.start()
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig


class NewstrainingConfig(AppConfig):
    name = "newstraining"

    def ready(self):
        print(f'lookign for jobs')
        scheduler = BackgroundScheduler()
        scheduler.get_job(job_id='daily_training_scheduler',jobstore='mysql+mysqldb://mysql4321:mysql4321@database:3306/mysql4321')
        scheduler.start()
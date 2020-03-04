from datetime import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler
from .views import threadRun


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(threadRun, 'interval', minutes=2)
    scheduler.start()
from newstraining.fndDriver import FNDDriver
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import  SQLAlchemyJobStore
import datetime
from django.conf import settings
log = settings.LOG

from newstraining.trainingEnums import TrainingEnums


class Jobs:
    fndDriver = FNDDriver()

    def run(self,
            selectedJobType=None,
            selectedAlgorithmType=None,
            selectedInputTypes=None,
            selectedOutputType=None,
            selectedMin=None,
            selectedHour=None,
            selectedDailyHourField=None,
            selectedDailyMinField=None):
        pass


class ManualTrainingJobs(Jobs):
    def run(self,
            selectedJobType=None,
            selectedAlgorithmType=None,
            selectedInputTypes=None,
            selectedOutputType=None,
            selectedMin=None,
            selectedHour=None,
            selectedDailyHourField=None,
            selectedDailyMinField=None):
        self.fndDriver.run(selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType)


class DailyTrainingJobs(Jobs):
    def start(self, selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType):
        self.fndDriver.run(selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType)

    def run(self,
            selectedJobType=None,
            selectedAlgorithmType=None,
            selectedInputTypes=None,
            selectedOutputType=None,
            selectedMin=None,
            selectedHour=None,
            selectedDailyHourField=None,
            selectedDailyMinField=None):
        jobstores = {
            'default': SQLAlchemyJobStore(url='mysql+mysqldb://mysql4321:mysql4321@database:3306/mysql4321')
        }
        scheduler = BackgroundScheduler()
        scheduler.configure(jobstores=jobstores)
        configurationName = str("daily_training_scheduler" + "_" + datetime.datetime.now().strftime(TrainingEnums.TIMESTAMP_FORMAT.value))
        log.debug(f'configuration name: {configurationName}')
        if selectedMin is not None:
            log.debug(f'Adding job for {selectedMin} minutes')
            scheduler.add_job(self.start,
                              args=[selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType],
                              trigger='interval', minutes=int(selectedMin),id=configurationName)
            log.debug(f'Job added successfully for {selectedMin} minutes')
        elif selectedHour is not None:
            log.debug(f'Adding job for {selectedHour} hours')
            scheduler.add_job(self.start,
                              args=[selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType],
                              trigger='cron', id=configurationName, hour=int(selectedHour))
            log.debug(f'Job added successfully for {selectedHour} hours')
        elif selectedDailyHourField is not None:
            log.debug(f'Adding job for {selectedDailyHourField}:{selectedDailyMinField} daily')
            scheduler.add_job(self.start,
                              args=[selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType],
                              trigger='cron', id=configurationName, day_of_week='mon-sun', hour=int(selectedDailyHourField), minute=int(selectedDailyMinField))
            log.debug(f'Job added successfully for {selectedDailyHourField}:{selectedDailyMinField} hours')
        scheduler.start()

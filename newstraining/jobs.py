from newstraining.fndDriver import FNDDriver
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import  SQLAlchemyJobStore


class Jobs:
    fndDriver = FNDDriver()

    def run(self, selectedJobType=None, selectedAlgorithmType=None, selectedInputTypes=None, selectedOutputType=None):
        pass


class ManualTrainingJobs(Jobs):
    def run(self, selectedJobType=None, selectedAlgorithmType=None, selectedInputTypes=None, selectedOutputType=None):
        self.fndDriver.run(selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType)


class DailyTrainingJobs(Jobs):
    def start(self, selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType):
        self.fndDriver.run(selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType)

    def run(self, selectedJobType=None, selectedAlgorithmType=None, selectedInputTypes=None, selectedOutputType=None):
        jobstores = {
            'default': SQLAlchemyJobStore(url='mysql+mysqldb://mysql4321:mysql4321@database:3306/mysql4321')
        }
        scheduler = BackgroundScheduler()
        scheduler.configure(jobstores=jobstores)
        scheduler.add_job(self.start,
                          args=[selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType],
                          trigger='interval', minutes=2,id='daily_training_scheduler')
        scheduler.start()

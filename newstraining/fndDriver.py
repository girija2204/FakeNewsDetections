from django.conf import settings
from newstraining.dao.fndetectordao import FNDetectorDao
from newstraining.executor.fndExecutor import FNDExecutor
from newstraining.fndContext import FNDContext
from newstraining.trainingUtil import TrainingUtil
from newstraining.trainingEnums import TrainingEnums
import pdb

log = settings.LOG


class FNDDriver:
    def __init__(self):
        pass

    def saveConfiguration(self,jobType=None,algorithmType=None,inputTypes=None,outputType=None):
        dao = FNDetectorDao(trainingJobType=jobType, trainingAlgoName=algorithmType, inputTypes=inputTypes,
                            outputType=outputType)
        configuration = dao.saveConfiguration()
        return configuration

    def run(self,jobType=None,algorithmType=None,inputTypes=None,outputType=None):
        log.debug(f"Inside ntDriver run")
        dao = FNDetectorDao(trainingJobType=jobType,trainingAlgoName=algorithmType,inputTypes=inputTypes,outputType=outputType)
        # configuration = dao.getConfiguration()
        configuration = dao.saveConfiguration()
        if not configuration:
            log.debug(f"Training incomplete due to invalid configuration")
            return
        fndContext = self.getFNDContext(configuration)
        self.process(fndContext)

    def process(self, fndContext):
        fndExecutor = FNDExecutor()
        fndExecutor.execute(fndContext)

    def getFNDContext(self, configuration):
        startDate = TrainingUtil.getConfigAttribute(
            configSection=TrainingEnums.TRAINING_CONTEXT.value,
            configKey=TrainingEnums.TRAINING_STARTDATE.value,
        )
        endDate = TrainingUtil.getConfigAttribute(
            configSection=TrainingEnums.TRAINING_CONTEXT.value,
            configKey=TrainingEnums.TRAINING_ENDDATE.value,
        )
        fndContext = FNDContext(processName="training")
        fndContext.fndConfig = configuration
        if (
                startDate is not None
                and startDate is not ""
                and endDate is not None
                and endDate is not ""
        ):
            fndContext.trainStartDate = startDate
            fndContext.trainEndDate = endDate
            log.debug(f"Training Start Date: {startDate}, Training End Date: {endDate}")
        else:
            log.debug(f"No start date or end date")
        return fndContext

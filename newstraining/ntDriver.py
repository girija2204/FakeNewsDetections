from django.conf import settings
from newstraining.dao.fndetectordao import FNDetectorDao
from newstraining.executor.fndExecutor import FNDExecutor
from newstraining.fndContext import FNDContext
from newstraining.trainingUtil import TrainingUtil
from newstraining.trainingEnums import TrainingEnums

log = settings.LOG


class FNDDriver:
    def __init__(self):
        pass

    def run(self):
        log.debug(f"Inside ntDriver run")
        dao = FNDetectorDao()
        if not dao.getTrainingAlgo():
            log.debug(f"Training incomplete due to invalid configuration")
            return
        configuration = dao.getConfiguration()
        if not configuration:
            log.debug(f"Training incomplete due to invalid configuration")
            return
        log.debug(f"Configuration Loaded: {configuration}")
        fndContext = self.getFNDContext(configuration)
        self.process(fndContext)

    def process(self, fndContext):
        fndExecutor = FNDExecutor()
        fndExecutor.execute(fndContext)

    def getFNDContext(self, configuration):
        startDate, endDate = None, None
        startDate = TrainingUtil.getConfigAttribute(
            configSection=TrainingEnums.TRAINING_CONTEXT.value,
            configKey=TrainingEnums.TRAINING_STARTDATE.value,
        )
        endDate = TrainingUtil.getConfigAttribute(
            configSection=TrainingEnums.TRAINING_CONTEXT.value,
            configKey=TrainingEnums.TRAINING_ENDDATE.value,
        )
        if startDate is None or startDate is "" or endDate is None or endDate is "":
            log.debug(f"No start date or end date")
            fndContext = FNDContext(
                fndConfig=configuration, trainStartDate=None, trainEndDate=None
            )
        else:
            log.debug(f"startDate: {startDate}, endDate: {endDate}")
            fndContext = FNDContext(
                trainStartDate=startDate, trainEndDate=endDate, fndConfig=configuration
            )
        return fndContext

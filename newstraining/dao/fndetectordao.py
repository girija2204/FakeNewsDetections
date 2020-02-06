from django.conf import settings
from newstraining.models.fndConfig import FNDConfig
from newstraining.trainingUtil import TrainingUtil
from newstraining.trainingEnums import TrainingEnums

log = settings.LOG


class FNDetectorDao:
    def __init__(self):
        self.trainingAlgo = ""
        self.trainingName = ""
        self.validate()

    def validate(self):
        self.trainingAlgo = TrainingUtil.getConfigAttribute(
            configSection=TrainingEnums.TRAINING_CONFIGURATIONS.value,
            configKey=TrainingEnums.TRAINING_ALGO.value,
        )
        if self.trainingAlgo:
            log.debug(
                f"Configuration loaded - section: {TrainingEnums.TRAINING_CONFIGURATIONS.value}"
                f" and key: {TrainingEnums.TRAINING_ALGO.value} - trainingAlgo: {self.trainingAlgo}"
            )
        else:
            log.debug(
                f"Invalid configuration provided - section: {TrainingEnums.TRAINING_CONFIGURATIONS.value}"
                f" and key: {TrainingEnums.TRAINING_ALGO.value}"
            )
            return None

    def getModelConfig(self):
        if not self.trainingAlgo:
            log.debug(f"No training name")
            return None

        return FNDConfig.objects.filter(name=self.trainingAlgo).first()

    def getConfiguration(self):
        modelConfig = self.getModelConfig()
        if not modelConfig:
            log.debug(f"Invalid configurations provided")
            return None

        return modelConfig

    def getTrainingAlgo(self):
        return self.trainingAlgo

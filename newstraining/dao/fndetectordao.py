from django.conf import settings
from newstraining.models.fndConfig import FNDConfig
from newstraining.trainingUtil import TrainingUtil
from newstraining.trainingEnums import TrainingEnums
from newstraining.configurationValidator import ConfigurationValidator
from newstraining.exceptions.configurationException import ConfigurationException
import pdb

log = settings.LOG


class FNDetectorDao:
    trainingAlgo = None
    trainingName = None

    def __init__(self):
        self.trainingAlgo = TrainingUtil.getConfigAttribute(
            configSection=TrainingEnums.TRAINING_CONFIGURATIONS.value,
            configKey=TrainingEnums.TRAINING_ALGO.value,
        )
        self.trainingName = TrainingUtil.getConfigAttribute(
            configSection=TrainingEnums.TRAINING_CONFIGURATIONS.value,
            configKey=TrainingEnums.TRAINING_NAME.value,
        )
        # pdb.set_trace()
        self.validate()
        log.debug(
            f"Configuration file loaded: {self.trainingName}, {self.trainingAlgo}"
        )

    def validate(self):
        ConfigurationValidator.isNotNull("trainingAlgo", self.trainingAlgo)
        ConfigurationValidator.isNotNull("trainingName", self.trainingName)

    def getModelConfig(self):
        if not self.trainingAlgo or not self.trainingName:
            error = f"No training name or training algo provided"
            log.debug(error)
            raise ConfigurationException(error)

        return (
            FNDConfig.objects.filter(fndType=self.trainingAlgo)
            .filter(name=self.trainingName)
            .first()
        )

    def getConfiguration(self):
        modelConfig = self.getModelConfig()
        # pdb.set_trace()
        if modelConfig is None:
            error = f"No valid configurations found"
            log.debug(error)
            raise ConfigurationException(error)
        return modelConfig

    def getTrainingAlgo(self):
        return self.trainingAlgo

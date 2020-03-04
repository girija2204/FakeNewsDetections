from django.conf import settings

from newstraining.models.fndOutput import FNDOutput
from newstraining.models.fndModel import FNDModel
from newstraining.models.fndInput import FNDInput
from newstraining.models.fndConfig import FNDConfig
from newstraining.trainingUtil import TrainingUtil
from newstraining.trainingEnums import TrainingEnums
from newstraining.configurationValidator import ConfigurationValidator
from newstraining.exceptions.configurationException import ConfigurationException
import pdb

log = settings.LOG


class FNDetectorDao:
    trainingJobType = None
    trainingAlgoName = None
    inputTypes = None
    outputType = None

    def __init__(self,trainingJobType,trainingAlgoName,inputTypes,outputType):
        if trainingJobType and trainingAlgoName and inputTypes:
            log.debug(f'training job type: {trainingJobType} and training algo name: {trainingAlgoName}')
            self.trainingJobType = trainingJobType
            self.trainingAlgoName = trainingAlgoName
            self.inputTypes = inputTypes
            self.outputType = outputType
        else:
            self.trainingJobType = TrainingUtil.getConfigAttribute(
                configSection=TrainingEnums.TRAINING_CONFIGURATIONS.value,
                configKey=TrainingEnums.TRAINING_JOB_TYPE.value,
            )
            self.trainingAlgoName = TrainingUtil.getConfigAttribute(
                configSection=TrainingEnums.TRAINING_CONFIGURATIONS.value,
                configKey=TrainingEnums.TRAINING_ALGO_NAME.value,
            )
            inputTypes = TrainingUtil.getConfigAttribute(
                configSection=TrainingEnums.TRAINING_CONFIGURATIONS.value,
                configKey=TrainingEnums.INPUT_TYPES.value
            )
            self.inputTypes = [type.strip() for type in inputTypes.split(',')]
            self.outputType = TrainingUtil.getConfigAttribute(
                configSection=TrainingEnums.TRAINING_CONFIGURATIONS.value,
                configKey=TrainingEnums.OUTPUT_TYPE.value
            )
        self.validate()
        log.debug(
            f"Configuration file loaded: {self.trainingAlgoName}, {self.trainingJobType}, {self.inputTypes}, {self.outputType}"
        )
        for type in self.inputTypes:
            log.debug(f'type: {type}')

    def validate(self):
        ConfigurationValidator.isNotNull("trainingAlgoName", self.trainingAlgoName)
        ConfigurationValidator.isNotNull("trainingJobType", self.trainingJobType)
        ConfigurationValidator.isNotNull("inputTypes",self.inputTypes)
        ConfigurationValidator.isNotNull("outputType", self.outputType)

    def getModelConfig(self):
        if not self.trainingAlgoName or not self.trainingJobType:
            error = f"No training name or training algo provided"
            log.debug(error)
            raise ConfigurationException(error)

        return (
            FNDConfig.objects.filter(fndType=self.trainingJobType)
            .filter(name=self.trainingAlgoName)
            .first()
        )

    def saveConfiguration(self):
        log.debug(f'Saving configuration')
        model = FNDModel.objects.filter(name=self.trainingAlgoName).first()
        inputs = []
        for type in self.inputTypes:
            input = FNDInput.objects.filter(variableName=type.lower()).first()
            if input is not None:
                inputs.append(input.id)
        output = FNDOutput.objects.filter(variableName=self.outputType.lower()).first().id
        newConfig = FNDConfig(name=self.trainingAlgoName,fndType=self.trainingJobType,fndModel=model,fndInputs=inputs,fndOutput=output)
        newConfig.save()
        return newConfig

    def getConfiguration(self):
        modelConfig = self.getModelConfig()
        if modelConfig is None:
            error = f"No valid configurations found"
            log.debug(error)
            raise ConfigurationException(error)
        return modelConfig

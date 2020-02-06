from django.conf import settings
from newstraining.trainingUtil import TrainingUtil
from newstraining.configurationValidator import ConfigurationValidator
import time
import os
from newstraining.trainingEnums import TrainingEnums
import pdb

log = settings.LOG
basedir = settings.BASE_DIR


class AbstractAlgorithm:
    def __init__(self):
        self.modelFilePath = ""
        self.modelFileBaseName = ""
        self.trainTestSplitRatio = ""
        self.validate()

    def validate(self):
        ConfigurationValidator.isNotNull(self.modelFilePath)
        ConfigurationValidator.isNotNull(self.trainTestSplitRatio)
        ConfigurationValidator.isNotNull(self.modelFileBaseName)
        ConfigurationValidator.isDirectory(self.modelFilePath)

    def train(self, trainingInput, fndContext, embeddingMatrix=None):
        trainTestSplitRatio = self.getTrainingProperties(
            TrainingEnums.TRAIN_TEST_SPLIT_RATIO.value, fndContext
        )
        if not trainTestSplitRatio:
            log.debug(f"Unable to train, as trainTestSplitRatio is not provided")
            return
        X_train, X_test, Y_train, Y_test = TrainingUtil.splitTrainTest(
            trainingInput[0], trainingInput[1], trainTestSplitRatio
        )

    def predict(self, predictionInput, fndContext):
        pass

    def getTrainTestSplitRatio(self):
        self.getTrainTestSplitRatio()

    def getTrainingProperties(self, propertyName, fndContext):
        fndModelAttribute = fndContext.fndConfig.fndModel.fndmodelattribute_set.filter(
            name=propertyName
        ).first()
        return fndModelAttribute.value

    def evaluateModel(self):
        pass

    def createModelFileName(self, fndContext):
        modelFileBasename = self.getTrainingProperties(
            TrainingEnums.MODEL_FILE_BASENAME.value, fndContext
        )
        if modelFileBasename is None or not modelFileBasename:
            log.debug(f"Configuration Error")
            return
        timestr = time.strftime(TrainingEnums.TIMESTAMP_FORMAT.value)
        modelFileName = str(modelFileBasename + "_" + timestr)
        return modelFileName

    def getModelFilePath(self, fndContext):
        modelFilePath = self.getTrainingProperties(
            TrainingEnums.MODEL_FILE_PATH.value, fndContext=fndContext
        )
        if modelFilePath is None or not modelFilePath:
            log.debug(f"Configuration Error")
            return
        modelFullPath = os.path.join(basedir, modelFilePath)
        if not os.path.isdir(modelFullPath):
            log.debug(f"Invalid path provided")
            return
        return modelFullPath

    def getModelFileExtension(self, fndContext):
        modelSaveType = self.getTrainingProperties(
            TrainingEnums.MODEL_SAVE_TYPE.value, fndContext=fndContext
        )
        if modelSaveType is None or not modelSaveType:
            log.debug(f"Configuration Error")
            return
        if modelSaveType is TrainingEnums.H5_SAVE_TYPE.value:
            return TrainingEnums.H5_EXTENSION.value
        else:
            return TrainingEnums.H5_EXTENSION.value

    def saveModel(self, model, fndContext):
        modelFileName = self.createModelFileName(fndContext=fndContext)
        modelFilePath = self.getModelFilePath(fndContext=fndContext)
        modelFileExtension = self.getModelFileExtension(fndContext=fndContext)
        savepath = f'{modelFilePath}+""+{modelFileName}+"."+{modelFileExtension}'
        try:
            model.save(savepath)
            log.debug(f"Model saved at: {savepath}")
        except RuntimeError:
            log.debug(
                f"Runtime error occured while saving the model file at: {savepath}"
            )

    def loadModel(self, fndContext):
        modelFileName = self.getModelFileName(fndContext=fndContext)
        modelFilePath = self.getModelFilePath(fndContext=fndContext)
        modelFileExtension = self.getModelFileExtension(fndContext=fndContext)
        savepath = f'{modelFilePath}+""+{modelFileName}+"."+{modelFileExtension}'
        try:
            # model.save(savepath)
            log.debug(f"Model saved at: {savepath}")
        except RuntimeError:
            log.debug(
                f"Runtime error occured while saving the model file at: {savepath}"
            )

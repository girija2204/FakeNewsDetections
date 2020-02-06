from django.conf import settings
from newstraining.trainingUtil import TrainingUtil
from newstraining.configurationValidator import ConfigurationValidator
import time
import datetime
import os
from keras.models import load_model
from newstraining.trainingEnums import TrainingEnums
from newstraining.models.fndRunDetail import FNDRunDetail
import pdb

log = settings.LOG
basedir = settings.BASE_DIR


class AbstractAlgorithm:
    def __init__(self, fndContext):
        self.validate(fndContext)

    def validate(self, fndContext):
        ConfigurationValidator.isNotNull("modelFilePath", fndContext.modelFilePath)
        ConfigurationValidator.isNotNull(
            "trainTestSplitRatio", fndContext.trainTestSplitRatio
        )
        ConfigurationValidator.isNotNull(
            "modelFileBaseName", fndContext.modelFileBasename
        )
        ConfigurationValidator.isDirectory("modelFilePath", fndContext.modelFilePath)
        ConfigurationValidator.isNotNull("modelSaveType", fndContext.modelSaveType)

    def train(self, trainingInput, fndContext, embeddingMatrix=None):
        X_train, X_test, Y_train, Y_test = TrainingUtil.splitTrainTest(
            trainingInput[0], trainingInput[1], fndContext.trainTestSplitRatio
        )

    def predict(self, predictionInput, fndContext):
        pass

    def getTrainTestSplitRatio(self):
        self.getTrainTestSplitRatio()

    def evaluateModel(self):
        pass

    def createModelFileName(self, fndContext):
        modelFileName = str(
            fndContext.modelFileBasename
            + "_"
            + fndContext.runStartTime.strftime(TrainingEnums.TIMESTAMP_FORMAT.value)
        )
        return modelFileName

    def getModelFilePath(self, fndContext):
        modelFullPath = os.path.join(basedir, fndContext.modelFilePath)
        if not os.path.isdir(modelFullPath):
            log.debug(f"Invalid path provided")
            return
        return modelFullPath

    def saveModel(self, model, fndContext):
        modelFileName = self.createModelFileName(fndContext=fndContext)
        modelFilePath = self.getModelFilePath(fndContext=fndContext)
        savepath = f"{modelFilePath}{modelFileName}.{fndContext.modelFileExtension}"
        try:
            model.save(savepath)
            fndContext.modelFileName = modelFileName
            log.debug(f"Model saved at: {savepath}")
        except RuntimeError:
            log.debug(
                f"Runtime error occured while saving the model file at: {savepath}"
            )

    def getRecentRunDetail(self):
        currentDate = datetime.datetime.now().date()
        nextDate = currentDate + datetime.timedelta(days=1)
        return (
            FNDRunDetail.objects.filter(runStartTime__range=[currentDate, nextDate])
            .order_by("-runStartTime")
            .first()
        )

    def loadModel(self, fndContext):
        recentRunDetail = self.getRecentRunDetail()
        model = None
        if recentRunDetail is not None:
            modelFileName = recentRunDetail.modelFileName
            modelFilePath = self.getModelFilePath(fndContext=fndContext)
            loadpath = f"{modelFilePath}{modelFileName}.{fndContext.modelFileExtension}"
            try:
                model = load_model(loadpath)
                log.debug(f"Model loaded from: {loadpath}")
            except RuntimeError:
                log.debug(
                    f"Runtime error occured while loading the model file from: {loadpath}"
                )
        return model

from newstraining.preprocessor.contentPreprocessor import ContentPreprocessor
from django.conf import settings

from newstraining.trainingEnums import TrainingEnums
from newstraining.trainingUtil import TrainingUtil
from newstraining.algorithm.impl.neuralNetwork import NeuralNetwork
from newstraining.algorithm.impl.convolutionalNeuralNetwork import ConvolutionalNN
from newstraining.algorithm.impl.lstm import LSTM
from newstraining.algorithm.abstractAlgorithm import AbstractAlgorithm
from keras.models import load_model
from newstraining.exceptions.invalidPathException import InvalidPathException
import pdb
import os

log = settings.LOG
basedir = settings.BASE_DIR


class AlgorithmAdapter:
    class __AlgorithmAdapter:
        def __init__(self):
            pass

    instance = None

    def __init__(self):
        if not AlgorithmAdapter.instance:
            AlgorithmAdapter.instance = AlgorithmAdapter.__AlgorithmAdapter()
            log.debug("Algorithm adapter created")
        else:
            log.debug("Algorithm adapter loaded")

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def initiateTraining(self, trainingInput, fndContext):
        # pdb.set_trace()
        if trainingInput.empty or not fndContext:
            log.debug(f"Initiation failed")
            return
        log.debug(f"Training Initiation")
        fndInputs = fndContext.fndConfig.fndModel.fndinput_set.filter(
            trainingIndicator="Y"
        ).all()
        preprocessor = None
        for fndInput in fndInputs:
            if fndInput.variableName == "content":
                preprocessor = ContentPreprocessor()
        preprocessedTrainingInput = preprocessor.preprocess(trainingInput, fndContext)
        fndAlgoName = self.getFNDAlgoName()
        if not fndAlgoName:
            log.debug("training algo not configured. Cannot train further")
            return
        klass = globals()[fndAlgoName]
        fndContext.trainTestSplitRatio = float(
            self.getTrainingProperties(
                TrainingEnums.TRAIN_TEST_SPLIT_RATIO.value, fndContext
            )
        )
        fndContext.modelFileBasename = self.getTrainingProperties(
            TrainingEnums.MODEL_FILE_BASENAME.value, fndContext
        )
        fndContext.modelFilePath = self.getTrainingProperties(
            TrainingEnums.MODEL_FILE_PATH.value, fndContext=fndContext
        )
        fndContext.modelSaveType = self.getTrainingProperties(
            TrainingEnums.MODEL_SAVE_TYPE.value, fndContext=fndContext
        )
        fndContext.modelFileExtension = self.getModelFileExtension(
            fndContext=fndContext
        )
        fndContext.tokenizerFileBasename = self.getTrainingProperties(
            TrainingEnums.TOKENIZER_FILE_BASENAME.value, fndContext
        )
        fndContext.tokenizerFilePath = self.getTrainingProperties(
            TrainingEnums.TOKENIZER_FILE_PATH.value, fndContext
        )
        fndContext.tokenizerFileType = self.getTrainingProperties(
            TrainingEnums.TOKENIZER_FILE_TYPE.value, fndContext
        )
        fndContext.tokenizerFileExtension = self.getTokenizerFileExtension(fndContext)

        algo = klass(fndContext)
        algo.train(preprocessedTrainingInput, fndContext)

    def getFNDAlgoName(self):
        return TrainingUtil.getAlgoName()

    def getTrainingProperties(self, propertyName, fndContext):
        fndModelAttribute = fndContext.fndConfig.fndModel.fndmodelattribute_set.filter(
            name=propertyName
        ).first()
        return fndModelAttribute.value

    def getModelFileExtension(self, fndContext):
        if fndContext.modelSaveType == TrainingEnums.H5_SAVE_TYPE.value:
            return TrainingEnums.H5_EXTENSION.value
        else:
            return TrainingEnums.H5_EXTENSION.value

    def getTokenizerFileExtension(self, fndContext):
        if fndContext.tokenizerFileType == TrainingEnums.PICKLE_FILE_TYPE.value:
            return TrainingEnums.PICKLE_EXTENSION.value

    def initiatePrediction(self, predictionInput, fndContext):
        if predictionInput.empty or not fndContext:
            log.debug(f"Initiation failed")
            return
        if fndContext.processName == "prediction":
            log.debug(f"Prediction Initiation")
            recentRunDetail = TrainingUtil.loadRecentRunDetail()
            fndInputs = recentRunDetail.fndConfig.fndModel.fndinput_set.filter(
                trainingIndicator="Y"
            ).all()
            preprocessor = None
            for fndInput in fndInputs:
                if fndInput.variableName == "content":
                    preprocessor = ContentPreprocessor()
            preprocessedTrainingInput = preprocessor.preprocess(
                predictionInput, fndContext
            )
            paddedInput = preprocessor.getPaddedSequences(preprocessedTrainingInput)

            modelFileName = recentRunDetail.modelFileName
            # pdb.set_trace()
            modelFilePath = (
                recentRunDetail.fndConfig.fndModel.fndmodelattribute_set.filter(
                    name=TrainingEnums.MODEL_FILE_PATH.value
                )
                .first()
                .value
            )
            modelFullPath = os.path.join(basedir, modelFilePath)
            modelSaveType = (
                recentRunDetail.fndConfig.fndModel.fndmodelattribute_set.filter(
                    name=TrainingEnums.MODEL_SAVE_TYPE.value
                )
                .first()
                .value
            )
            fndContext.modelSaveType = modelSaveType
            loadpath = f"{modelFullPath}{modelFileName}.{self.getModelFileExtension(fndContext=fndContext)}"
            try:
                log.debug(f"loading the recent model for prediction from: {loadpath}")
                model = load_model(loadpath)
                log.debug(f"Model loaded from: {loadpath}")
                classPredicted = model.predict_classes(paddedInput)
                log.debug(f"predicted class: {classPredicted}")
                return classPredicted
            except InvalidPathException:
                raise InvalidPathException(
                    f"Runtime error occured while loading the model file from: {loadpath}"
                )

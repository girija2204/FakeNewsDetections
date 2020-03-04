from tensorflow.keras.models import load_model

from newstraining.models.fndInput import FNDInput
from newstraining.preprocessor.contentPreprocessor import ContentPreprocessor
from django.conf import settings
import os
import numpy as np
from newstraining.trainingEnums import TrainingEnums
from newstraining.trainingUtil import TrainingUtil
from newstraining.algorithm.impl.neuralNetwork import NeuralNetwork
from newstraining.algorithm.impl.convolutionalNeuralNetwork import ConvolutionalNN
from newstraining.algorithm.impl.lstmAlgo import LSTMAlgo
from newstraining.algorithm.abstractAlgorithm import AbstractAlgorithm
from newstraining.exceptions.invalidPathException import InvalidPathException
from newstraining.exceptions.detectionFailureException import DetectionFailureException
import pdb

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
        fndInputs = []
        inputs = fndContext.fndConfig.fndInputs
        for input in inputs:
            fndInput = FNDInput.objects.get(pk=input)
            preprocessor = None
            if fndInput.variableName.lower() == "content":
                preprocessor = ContentPreprocessor()
            preprocessedTrainingInput = preprocessor.preprocess(trainingInput, fndContext)
            log.debug(f"Preprocessing done")
            fndAlgoName = self.getFNDAlgoName()
            if not fndAlgoName:
                log.debug("training algo not configured. Cannot train further")
                return
            # pdb.set_trace()
            klass = globals()[fndAlgoName]
            fndContext.trainTestSplitRatio = float(
                self.getTrainingProperties(
                    TrainingEnums.TRAIN_TEST_SPLIT_RATIO.value, fndContext
                )
            )

            log.debug(
                f"Splitting the dataset: {fndContext.trainTestSplitRatio} for test and {1 - float(fndContext.trainTestSplitRatio)} for train"
            )
            X_train, X_test, Y_train, Y_test = TrainingUtil.splitTrainTest(
                preprocessedTrainingInput["content"],
                preprocessedTrainingInput["label"],
                float(fndContext.trainTestSplitRatio),
            )
            embedding_matrix = preprocessor.getEmbeddingMatrix(data=X_train)
            # paddedX_train = preprocessor.getPaddedSequences(X_train)
            # paddedX_test = preprocessor.getPaddedSequences(X_test)

            embedding_layer = preprocessor.getEmbeddingLayer()

            fndContext = self.populateFndContext(fndContext=fndContext)

            algo = klass(fndContext)
            log.debug("Adding content preprocessor to algo")
            # pdb.set_trace()
            algo.preprocessors.append(preprocessor)
            # pdb.set_trace()
            model = algo.train(X_train, X_test, Y_train, Y_test,
                fndContext=fndContext,
                embeddingLayer=embedding_layer,
            )

            log.debug("Saving the tokenizer")
            algo.saveTokenizer(tokenizer=preprocessor.tokenizer, fndContext=fndContext)
            log.debug("Saving the model")
            algo.saveModel(model=model, fndContext=fndContext)

            # log.debug("Evaluating the model on test data set")
            # algo.evaluateModel(model, X_test, Y_test, fndContext)
            # log.debug("Training over")

    def getFNDAlgoName(self):
        return TrainingUtil.getAlgoName()

    def getTrainingProperties(self, propertyName, fndContext):
        log.debug(propertyName)
        fndModelAttribute = fndContext.fndConfig.fndModel.fndmodelattribute_set.filter(
            name=propertyName
        ).first()
        log.debug(fndModelAttribute)
        return fndModelAttribute.value

    def getModelFileExtension(self, fndContext):
        if fndContext.modelSaveType == TrainingEnums.H5_SAVE_TYPE.value:
            return TrainingEnums.H5_EXTENSION.value
        else:
            return TrainingEnums.H5_EXTENSION.value

    def getTokenizerFileExtension(self, fndContext):
        if fndContext.tokenizerFileType == TrainingEnums.PICKLE_FILE_TYPE.value:
            return TrainingEnums.PICKLE_EXTENSION.value

    def populateFndContext(self, fndContext):
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
        return fndContext

    def initiatePrediction(self, predictionInput, fndContext):
        if predictionInput.empty or not fndContext:
            log.debug(f"Initiation failed")
            return
        if fndContext.processName == "prediction":
            log.debug(f"Prediction Initiation")
            # pdb.set_trace()
            try:
                recentRunDetail = TrainingUtil.loadRecentRunDetail()
                if not recentRunDetail:
                    error = f'Unable to detect. Please report to admin.'
                    log.debug(error)
                    raise DetectionFailureException(error)
                else:
                    log.debug(f'Loading model trained at runtime: {recentRunDetail.runStartTime}')
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
                log.debug(f"loading the recent model for prediction from: {loadpath}")
                model = load_model(loadpath)
                log.debug(f"Model loaded from: {loadpath}")
                # pdb.set_trace()
                classPredicted = model.predict_classes(np.array(paddedInput ))
                log.debug(f"predicted class: {classPredicted}")
                return classPredicted
            except InvalidPathException as ipe:
                log.debug(ipe)
            except DetectionFailureException as dfe:
                log.debug(dfe)

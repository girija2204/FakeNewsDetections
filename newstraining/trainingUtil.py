from django.conf import settings
from sklearn.model_selection import train_test_split

from newstraining.models.fndRunDetail import FNDRunDetail
from newstraining.trainingEnums import TrainingEnums
import pdb
import os
import datetime
import pickle
import pandas as pd

configParser = settings.CONFIG_PARSER
basedir = settings.BASE_DIR
log = settings.LOG


class TrainingUtil:
    @staticmethod
    def getConfigAttribute(configSection, configKey):
        if configParser.has_section(configSection) and configParser.has_option(
            configSection, configKey
        ):
            return configParser.get(configSection, configKey)
        return None

    @staticmethod
    def splitTrainTest(dataset, labels, splitRatio):
        X_train, X_test, Y_train, Y_test = train_test_split(
            dataset, labels, test_size=splitRatio, random_state=42
        )
        return X_train, X_test, Y_train, Y_test

    @staticmethod
    def getAlgoName():
        algo = TrainingUtil.getConfigAttribute(
            TrainingEnums.TRAINING_CONFIGURATIONS.value,
            TrainingEnums.TRAINING_NAME.value,
        )
        return algo

    @staticmethod
    def getWordEmbeddingsFileName():
        embeddingLocation = TrainingUtil.getConfigAttribute(
            TrainingEnums.WORD_EMBEDDING_CONFIGURATIONS.value,
            TrainingEnums.EMBEDDING_DIRECTORY.value,
        )
        embeddingFileName = TrainingUtil.getConfigAttribute(
            TrainingEnums.WORD_EMBEDDING_CONFIGURATIONS.value,
            TrainingEnums.EMBEDDING_FILENAME.value,
        )
        embeddingFilePath = os.path.join(embeddingLocation, embeddingFileName)
        return str(embeddingFilePath).replace('"', "")

    @staticmethod
    def getMaxLength():
        return TrainingUtil.getConfigAttribute(
            TrainingEnums.WORD_EMBEDDING_CONFIGURATIONS.value,
            TrainingEnums.MAX_LENGTH_PADDING.value,
        )

    @staticmethod
    def loadRecentRunDetail():
        return FNDRunDetail.objects.order_by("-runStartTime").first()


    @staticmethod
    def loadTokenizer():
        recentRunDetail = TrainingUtil.loadRecentRunDetail()
        tokenizer = None
        if recentRunDetail is not None:
            tokenizerFileName = recentRunDetail.tokenizerFileName
            tokenizerFilePath = (
                recentRunDetail.fndConfig.fndModel.fndmodelattribute_set.filter(
                    name=TrainingEnums.TOKENIZER_FILE_PATH.value
                )
                .first()
                .value
            )
            tokenizerFileType = (
                recentRunDetail.fndConfig.fndModel.fndmodelattribute_set.filter(
                    name=TrainingEnums.TOKENIZER_FILE_TYPE.value
                )
                .first()
                .value
            )
            tokenizerFileExtension = None
            # pdb.set_trace()
            if tokenizerFileType == TrainingEnums.PICKLE_FILE_TYPE.value:
                tokenizerFileExtension = TrainingEnums.PICKLE_EXTENSION.value
            tokenizerFullPath = os.path.join(basedir, tokenizerFilePath)
            loadPath = (
                f"{tokenizerFullPath}{tokenizerFileName}.{tokenizerFileExtension}"
            )
            with open(loadPath, "rb") as handle:
                tokenizer = pickle.load(handle)
        return tokenizer

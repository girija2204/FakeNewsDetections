from django.conf import settings
from sklearn.model_selection import train_test_split
from newstraining.trainingEnums import TrainingEnums
import pdb
import os

configParser = settings.CONFIG_PARSER


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
    def getAlgo():
        algo = TrainingUtil.getConfigAttribute(
            TrainingEnums.TRAINING_CONFIGURATIONS.value,
            TrainingEnums.TRAINING_ALGO.value,
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

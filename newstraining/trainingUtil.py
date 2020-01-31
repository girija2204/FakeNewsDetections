from django.conf import settings
from sklearn.model_selection import train_test_split
from newstraining.trainingEnums import TrainingEnums

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
        return TrainingUtil.getConfigAttribute(
            TrainingEnums.TRAINING_CONFIGURATIONS, TrainingEnums.TRAINING_ALGO
        )

    @staticmethod
    def getWordEmbeddingsFileName():
        embeddingLocation = TrainingUtil.getConfigAttribute(
            TrainingEnums.WORD_EMBEDDING_CONFIGURATIONS,
            TrainingEnums.EMBEDDING_DIRECTORY,
        )
        embeddingFileName = TrainingUtil.getConfigAttribute(
            TrainingEnums.WORD_EMBEDDING_CONFIGURATIONS,
            TrainingEnums.EMBEDDING_FILENAME,
        )
        return embeddingLocation + embeddingFileName

    @staticmethod
    def getMaxLength():
        return TrainingUtil.getConfigAttribute(
            TrainingEnums.WORD_EMBEDDING_CONFIGURATIONS,
            TrainingEnums.MAX_LENGTH_PADDING,
        )

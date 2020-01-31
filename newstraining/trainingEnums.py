from enum import Enum


class TrainingEnums(Enum):
    TRAINING_CONFIGURATIONS = "trainingConfigurations"
    TRAINING_NAME = "trainingName"
    TRAINING_ALGO = "trainingAlgo"
    TRAINING_CONTEXT = "trainingContext"
    TRAINING_STARTDATE = "trainingStartDate"
    TRAINING_ENDDATE = "trainingEndDate"
    DATASET_CONFIGURATIONS = "datasetConfigurations"
    DATA_FILEPATH = "dataFilepath"
    DATA_FILENAME = "dataFilename"
    WORD_EMBEDDING_CONFIGURATIONS = "wordembeddingConfigurations"
    EMBEDDING_DIRECTORY = "embeddingDirectory"
    EMBEDDING_FILENAME = "embeddingFileName"
    MAX_LENGTH_PADDING = "maxLengthForPadding"

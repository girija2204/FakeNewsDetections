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
    TRAIN_TEST_SPLIT_RATIO = "TRAIN_TEST_SPLIT_RATIO"
    MODEL_FILE_BASENAME = "MODEL_FILE_BASENAME"
    MODEL_FILE_PATH = "MODEL_FILE_PATH"
    MODEL_SAVE_TYPE = "MODEL_SAVE_TYPE"
    TIMESTAMP_FORMAT = "%Y%m%d-%H%M%S"
    H5_SAVE_TYPE = "h5py"
    H5_EXTENSION = "h5"

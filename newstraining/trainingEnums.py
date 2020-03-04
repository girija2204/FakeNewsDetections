from enum import Enum


class TrainingEnums(Enum):
    # configuration file
    TRAINING_CONFIGURATIONS = "trainingConfigurations"
    TRAINING_ALGO_NAME = "trainingAlgoName"
    TRAINING_JOB_TYPE = "trainingJobType"
    INPUT_TYPES = "inputTypes"
    OUTPUT_TYPE = "outputType"
    TRAINING_CONTEXT = "trainingContext"
    TRAINING_STARTDATE = "trainingStartDate"
    TRAINING_ENDDATE = "trainingEndDate"
    DATASET_CONFIGURATIONS = "datasetConfigurations"
    DATA_FILEPATH = "dataFilepath"
    DATA_FILENAME = "dataFilename"

    # word embedding
    WORD_EMBEDDING_CONFIGURATIONS = "wordembeddingConfigurations"
    EMBEDDING_DIRECTORY = "embeddingDirectory"
    EMBEDDING_FILENAME = "embeddingFileName"
    MAX_LENGTH_PADDING = "maxLengthForPadding"

    # model attributes
    TRAIN_TEST_SPLIT_RATIO = "TRAIN_TEST_SPLIT_RATIO"
    MODEL_FILE_BASENAME = "MODEL_FILE_BASENAME"
    MODEL_FILE_PATH = "MODEL_FILE_PATH"
    MODEL_SAVE_TYPE = "MODEL_SAVE_TYPE"
    H5_SAVE_TYPE = "h5py"
    H5_EXTENSION = "h5"

    # tokenizer
    TOKENIZER_FILE_PATH = "TOKENIZER_FILE_PATH"
    TOKENIZER_FILE_BASENAME = "TOKENIZER_FILE_BASENAME"
    TOKENIZER_FILE_TYPE = "TOKENIZER_FILE_TYPE"
    PICKLE_FILE_TYPE = "pickle"
    PICKLE_EXTENSION = "pickle"

    # date time
    TIMESTAMP_FORMAT = "%Y%m%d-%H%M%S"

    # training types
    DAILY_TRAINING = "DAILY_TRAINING"
    MANUAL_TRAINING = "MANUAL_TRAINING"
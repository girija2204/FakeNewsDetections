class FNDContext:
    trainStartDate = None
    trainEndDate = None
    runStartTime = None
    runEndTime = None
    modelFileBasename = None
    trainTestSplitRatio = None
    modelFilePath = None
    modelSaveType = None
    modelFileExtension = None
    fndConfig = None
    modelFileName = None

    def __init__(self, fndConfig):
        self.fndConfig = fndConfig

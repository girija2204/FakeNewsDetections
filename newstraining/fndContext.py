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
    processName = None
    tokenizerFileBasename = None
    tokenizerFilePath = None
    tokenizerFileType = None
    tokenizerFileExtension = None
    tokenizerFileName = None

    def __init__(self, processName):
        self.processName = processName

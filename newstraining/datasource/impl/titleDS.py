from newstraining.datasource.abstractDS import AbstractDS

# yet not figured out how title is going to behave while FND
class TitleDS(AbstractDS):
    def __init__(self):
        super().__init__()

    def getLabelledData(self, dataset, columnNames):
        pass

    def getDataset(self, fndInput, fndOutput, startDate=None, endDate=None):
        pass

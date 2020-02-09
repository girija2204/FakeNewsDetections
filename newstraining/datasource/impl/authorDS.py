from newstraining.datasource.abstractDS import AbstractDS

# need to get details of author, his profile and other information
class AuthorDS(AbstractDS):
    def __init__(self):
        super().__init__()

    def getLabelledData(self, dataset, columnNames):
        pass

    def getDataset(self, fndContext, fndInput, fndOutput, startDate=None, endDate=None):
        pass

import numpy as np
from newsextractor.models import NewsArticle
from django.conf import settings
from newstraining.datasource.abstractDS import AbstractDS
import pandas as pd
import pdb

from newstraining.models.fndOutput import FNDOutput
from newstraining.models.fndInput import FNDInput

log = settings.LOG


class ContentDS(AbstractDS):
    def __init__(self):
        super().__init__()

    def getLabelledData(self, dataset, columnNames):
        return dataset[columnNames]

    def getDataFromDB(self, startDate=None, endDate=None):
        if startDate == None or endDate == None:
            log.debug(f"startDate or endDate is None, so getting all the records")
            newsArticles = NewsArticle.objects.all()
        else:
            if startDate > endDate:
                log.debug(
                    f"Unable to fetch news articles as start date is after end date"
                )
                return
            log.debug(
                f"getting records between startDate: {startDate} and endDate: {endDate}"
            )
            newsArticles = NewsArticle.objects.filter(
                date_posted__range=[startDate, endDate]
            )
        return newsArticles

    def getDataset(self, fndContext, input, output, startDate=None, endDate=None):
        log.debug(f"Inside contentDS")
        fndInput = FNDInput.objects.get(pk=input)
        fndOutput = FNDOutput.objects.get(pk=output)
        news_articles = self.getDataFromDB(startDate, endDate)
        dataset = pd.DataFrame.from_records(news_articles.values())
        # pdb.set_trace()
        if fndContext.processName == "training":
            colNames = [fndInput.variableName.lower(), fndOutput.variableName.lower()]
        else:
            colNames = [fndInput.variableName.lower()]
        labelledData = self.getLabelledData(dataset, colNames)
        return labelledData

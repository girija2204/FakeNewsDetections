from newstraining.datasource.inputDataGenerator import InputDataGenerator
from newstraining.algorithm.algorithmAdapter import AlgorithmAdapter
from django.conf import settings
import pandas as pd
import numpy as np
from keras.models import Sequential
from newsextractor.models import NewsArticle
import datetime
from newstraining.models.fndRunDetail import FNDRunDetail
import pdb

log = settings.LOG


class FNDExecutor:
    # news_articles = None
    def __init__(self):
        pass
        # news_articles = pd.read_csv("D:\\ml and dl\\keras\\dataset\\csv files\\dataset_2.csv")
        # for index in range(0,news_articles.shape[0]):
        #     newsArticle = NewsArticle(title=news_articles.iloc[index][2],content=news_articles.iloc[index][1],fake_status=news_articles.iloc[index][0],author=news_articles.iloc[index][3])
        #     newsArticle.save()

    def execute(self, fndContext):
        runStartTime = datetime.datetime.now()
        inputDataGenerator = InputDataGenerator(fndContext)
        trainingInput = inputDataGenerator.generateInput("training")
        # pdb.set_trace()
        algorithmAdapter = AlgorithmAdapter()
        algorithmAdapter.initiateDetection(
            trainingInput=trainingInput, fndContext=fndContext
        )
        runEndTime = datetime.datetime.now()
        self.saveFndRunDetail(fndContext=fndContext,runStartTime=runStartTime,runEndTime=runEndTime)

    def saveFndRunDetail(
        self,
        fndContext,
        runStartTime,
        runEndTime,
        historyStartTime=None,
        historyEndTime=None,
    ):
        fndRunDetail = FNDRunDetail(
            runStartTime=runStartTime,
            runEndTime=runEndTime,
            historyStartTime=historyStartTime,
            historyEndTime=historyEndTime,
            fndConfig=fndContext.fndConfig,
        )
        fndRunDetail.save()

    def getData(self, dataset, columnNames):
        textData = []
        for columnName in columnNames:
            textData.append(dataset[columnName])
        return textData

    def getLabels(self, dataset, columnName):
        labels = self.news_articles.loc[columnName]
        labels = np.array(list(map(lambda x: 0 if x == False else 1, labels)))
        return labels

from django.core.management.base import BaseCommand, CommandError

from newstraining.models import FNDConfig
from newstraining.models.fndInput import FNDInput
from newstraining.models.fndModel import FNDModel
from newstraining.models.fndOutput import FNDOutput
from newstraining.models.fndModelAttribute import FNDModelAttribute
from newstraining.models.jobTypes import JobTypes
from newsextractor.models import NewsArticle
from django.conf import settings

log = settings.LOG


def populateFndInput():
    log.debug(f'inserting records into FNDInput table')
    fndInputs = [{'variableName': 'Content', 'variableSymbol': 'CNT', 'trainingIndicator': 'Y'},
                 {'variableName': 'Title', 'variableSymbol': 'TIT', 'trainingIndicator': 'Y'},
                 {'variableName': 'Date Posted', 'variableSymbol': 'DTP', 'trainingIndicator': 'Y'}]
    for fndInput in fndInputs:
        input = FNDInput(variableName=fndInput['variableName'], variableSymbol=fndInput['variableSymbol'],
                         trainingIndicator=fndInput['trainingIndicator'])
        input.save()


def populateFndOutput():
    log.debug(f'inserting records into FNDOutput table')
    fndOutputs = [{'variableName': 'fake_status', 'variableSymbol': 'FS'}]
    for fndOutput in fndOutputs:
        output = FNDOutput(variableName=fndOutput['variableName'], variableSymbol=fndOutput['variableSymbol'])
        output.save()


def populateFndModel():
    log.debug(f'inserting records into FNDModel table')
    fndModels = [{'name': 'NeuralNetwork', 'algorithm': 'NeuralNetwork'},
                 {'name': 'ConvolutionalNN', 'algorithm': 'ConvolutionalNN'},
                 {'name': 'LSTMAlgo', 'algorithm': 'LSTMAlgo'}]
    for fndModel in fndModels:
        model = FNDModel(name=fndModel['name'], algorithm=fndModel['algorithm'])
        model.save()


def populateModelAttribute():
    log.debug(f'inserting records into FNDModelAttribute table')
    model = FNDModel.objects.filter(name='LSTMAlgo').first()
    fndModelAttributes = [{'name': 'MODEL_FILE_BASENAME', 'value': 'fnd_model'},
                          {'name': 'MODEL_FILE_PATH', 'value': 'models\\NeuralNetwork\\'},
                          {'name': 'MODEL_SAVE_TYPE', 'value': 'h5py'},
                          {'name': 'TRAIN_TEST_SPLIT_RATIO', 'value': '0.20'},
                          {'name': 'TOKENIZER_FILE_PATH', 'value': 'resources\\tokenizer\\'},
                          {'name': 'WORD_EMBEDDING_FILE_PATH', 'value': 'resources\\word-embedding\\'},
                          {'name': 'WORD_EMBEDDING_FILE_NAME', 'value': 'embedding'},
                          {'name': 'TOKENIZER_FILE_TYPE', 'value': 'pickle'},
                          {'name': 'TOKENIZER_FILE_BASENAME', 'value': 'tokenizer'}]
    for fndModelAttribute in fndModelAttributes:
        attribute = FNDModelAttribute(name=fndModelAttribute['name'], value=fndModelAttribute['value'], fndModel=model)
        attribute.save()


def populateFndConfig():
    log.debug(f'inserting records into FNDConfig table')
    model = FNDModel.objects.filter(name='LSTMAlgo').first()
    fndConfigs = [{'name': 'LSTMAlgo', 'fndType': 'DAILY_TRAINING'},
                  {'name': 'LSTMAlgo', 'fndType': 'FULL_TRAINING'}]
    for fndConfig in fndConfigs:
        config = FNDConfig(name=fndConfig['name'], fndType=fndConfig['fndType'], fndModel=model)
        config.save()

def populateJobTypes():
    log.debug(f'inserting records into JobTypes table')
    jobTypes = [{'typeName':'MANUAL_TRAINING','code':'MT1.1','expression':None},
                {'typeName':'DAILY_TRAINING','code':'DT1.1','expression':None},
                {'typeName':'DAILY_TRAINING','code':'DT1.2','expression':None}]
    for jobType in jobTypes:
        jt = JobTypes(typeName=jobType['typeName'],code=jobType['code'],expression=jobType['expression'])
        jt.save()

def populateNewsArticles():
    log.debug(f'inserting records into NewsArticles table')
    newsArticles = [{
            'title': 'The Purge: Election Year Promo Wants You To Purge For America',
            'content': 'The Purge: Election Year Promo Wants You To Purge For America By Corey Chichizola Random Article Blend',
            'author': None,
            'fake_status': 1,
            'date_posted': None
        },
        {
            'title': 'Marceau beloved for artistry, helping WWII orphans  J.',
            'content': 'paris | In 1944, the French Jewish Resistance decided to evacuate the Jewish children hidden in an orphanage west of Paris and transport them by train to Switzerland. Resistance commander George Loinger called on his young cousin, Marcel Mangel, to help him organize the dangerous train',
            'author': None,
            'fake_status': 1,
            'date_posted': None
        },
        {
            'title': 'Top Design Magazine - Web Design and Digital Content',
            'content': 'in Design Ugly fonts, unreadable fonts, bad fonts they have terrorized us for far too long, infiltrating our homes via e-mail or IM. Some font typefaces are so offensive that the only solution is to remove them from your computer and hope that everyone will do it until every copy of them are completely destroyed. In this article I have collected 10 of the most hated fonts. From the start please understand that Im not saying that these fonts are the worst possible fonts. I know t',
            'author': None,
            'fake_status': 0,
            'date_posted': None
        },
        {
            'title': 'Here are the federal agencies and programs Trump wants to eliminate',
            'content': 'President Trump just released his budget plan for the next fiscal year, which proposes some big changes in government spending. Here\'s a look at what agencies are helped and hurt by the proposal. (Jenny Starrs/The Washington Post) President Trump\'s budget blueprint proposes to counterbalance a $54 billion increase in defense spending with a slew of steep cuts to discretionary spending programs, including by scrapping federal funding Those cuts include the complete elimination of a number of agencies and programs across the federal government. They include some familiar names, like the Energy Star program and the Low Income Home Energy Assistance Program (LIHEAP), as well as more obscure programs that do things like fund airports in rural areas, help low-income families, fight climate change a',
            'author': None,
            'fake_status': 1,
            'date_posted': None
        },
        {
            'title': 'I Know Why the Caged Bird Sings: Maya Angelou, Oprah Winfrey: 9780345514400: Amazon.com: Books',
            'content': 'Here\'s my review on one of the three books that I\'ve read by Maya Angelou: I Know Why The Caged Bird Sings: Smiling Through Sadness Maya Angelous first memoir, I Know Why The Caged Bird Sings, captures the sweetest, purest, and the most honest inner voice of a black child who grew up to be a heroine. Dr. Angelou does not censor anything; She wants us to know it all. It is so true, straightforward, and uncensored that many white parents have attempted to ban this book from schools. This memorable and mysterious auto',
            'author': None,
            'fake_status': 0,
            'date_posted': None
        }
    ]
    for article in newsArticles:
        newsArticle = NewsArticle(title=article['title'],content=article['content'],author=article['author'],fake_status=article['fake_status'],date_posted=article['date_posted'])
        newsArticle.save()

def deleteExistingTableData():
    log.debug(f'deleting existing records from FNDConfig table')
    FNDConfig.objects.all().delete()
    log.debug(f'deleting existing records from FNDInput table')
    FNDInput.objects.all().delete()
    log.debug(f'deleting existing records from FNDOutput table')
    FNDOutput.objects.all().delete()
    log.debug(f'deleting existing records from FNDModelAttribute table')
    FNDModelAttribute.objects.all().delete()
    log.debug(f'deleting existing records from FNDModel table')
    FNDModel.objects.all().delete()
    log.debug(f'deleting existing records from JobTypes table')
    JobTypes.objects.all().delete()
    log.debug(f'deleting existing news articles from NewsArticles table')
    NewsArticle.objects.all().delete()


class Command(BaseCommand):
    help = 'DB Initial Setup'

    def handle(self, *args, **options):
        deleteExistingTableData()
        populateFndModel()
        # populateFndConfig()
        populateFndInput()
        populateFndOutput()
        populateModelAttribute()
        populateJobTypes()
        populateNewsArticles()
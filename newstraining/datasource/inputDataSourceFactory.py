from newstraining.datasource.impl.contentDS import ContentDS
from newstraining.datasource.impl.authorDS import AuthorDS
from newstraining.datasource.impl.titleDS import TitleDS
from django.conf import settings

log = settings.LOG


class InputDataSourceFactory:
    class __InputDataSourceFactory:
        def __init__(self):
            pass

    instance = None

    def __init__(self):
        if not InputDataSourceFactory.instance:
            InputDataSourceFactory.instance = (
                InputDataSourceFactory.__InputDataSourceFactory()
            )
            log.debug(f"InputDataSourceFactory created")
        else:
            log.debug(f"InputDataSourceFactory loaded")

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def getInputDataSource(self, fndInput):
        dataSource = None
        log.debug(f"fndInput: {fndInput}")
        if (
            fndInput.variableName.lower() == "content"
            and fndInput.trainingIndicator == "Y"
        ):
            dataSource = ContentDS()
        elif (
            fndInput.variableName.lower() == "author"
            and fndInput.trainingIndicator == "Y"
        ):
            dataSource = AuthorDS()
        if (
            fndInput.variableName.lower() == "title"
            and fndInput.trainingIndicator == "Y"
        ):
            dataSource = TitleDS()

        log.debug(f"datasource: {dataSource}")
        return dataSource

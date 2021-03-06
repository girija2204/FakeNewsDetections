from newstraining.datasource.inputDataSourceFactory import InputDataSourceFactory
from django.conf import settings
import pdb

log = settings.LOG


class InputDataGenerator:
    class __InputDataGenerator:
        def __init__(self, fndContext):
            self.context = fndContext

    instance = None

    def __init__(self, fndContext):
        if not InputDataGenerator.instance:
            InputDataGenerator.instance = InputDataGenerator.__InputDataGenerator(
                fndContext
            )
            log.debug(f"InputDataGenerator created")
        else:
            InputDataGenerator.instance.context = fndContext
            log.debug(f"InputDataGenerator loaded")

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def generateInput(self, generateType):
        log.debug(f"Generating input for tranining: {generateType}")
        if generateType == "training":
            dataset = None
            context = InputDataGenerator.instance.context
            trainStartDate = context.trainStartDate
            trainEndDate = context.trainEndDate
            fndConfig = context.fndConfig
            log.debug(f"trainStartDate: {trainStartDate}")
            log.debug(f"trainEndDate: {trainEndDate}")
            log.debug(f"fndConfig: {fndConfig}")
            # pdb.set_trace()
            fndInputs = fndConfig.fndInputs
            fndOutput = fndConfig.fndOutput
            # will be a loop as multiple inputs will participate in training
            # for fndInput in fndInputs:
            #     inputDataSourceFactory = InputDataSourceFactory()
            #     dataSource = inputDataSourceFactory.getInputDataSource(fndInput)
            #     if dataSource is not None:
            #         dataset = dataSource.getDataset(
            #             fndInput=fndInput,
            #             fndOutput=fndOutput,
            #             startDate=trainStartDate,
            #             endDate=trainEndDate,
            #         )
            log.debug(f'fndInputs: {fndInputs}')
            log.debug(f'fndOutputs: {fndOutput}')
            dataset = None
            for fndInput in fndInputs:
                inputDataSourceFactory = InputDataSourceFactory()
                dataSource = inputDataSourceFactory.getInputDataSource(fndInput)
                if dataSource is not None:
                    dataset = dataSource.getDataset(
                        fndContext=context,
                        input=fndInput,
                        output=fndOutput,
                        startDate=trainStartDate,
                        endDate=trainEndDate,
                    )
                log.debug(f"dataset: {dataset}")
            return dataset

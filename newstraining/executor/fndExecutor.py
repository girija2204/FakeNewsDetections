from newstraining.datasource.inputDataGenerator import InputDataGenerator
from newstraining.algorithm.algorithmAdapter import AlgorithmAdapter
from django.conf import settings

log = settings.LOG


class FNDExecutor:
    def __init__(self):
        pass

    def execute(self, fndContext):
        inputDataGenerator = InputDataGenerator(fndContext)
        trainingInput = inputDataGenerator.generateInput("training")

        algorithmAdapter = AlgorithmAdapter()
        algorithmAdapter.initiateDetection(
            trainingInput=trainingInput, fndContext=fndContext
        )

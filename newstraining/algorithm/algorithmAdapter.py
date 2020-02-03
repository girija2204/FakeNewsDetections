from newstraining.preprocessor.contentPreprocessor import ContentPreprocessor
from django.conf import settings
from newstraining.trainingUtil import TrainingUtil
from newstraining.algorithm.impl.neuralNetwork import NeuralNetwork
from newstraining.algorithm.impl.convolutionalNeuralNetwork import ConvolutionalNN
from newstraining.algorithm.impl.lstm import LSTM
import pdb

log = settings.LOG


class AlgorithmAdapter:
    class __AlgorithmAdapter:
        def __init__(self):
            pass

    instance = None

    def __init__(self):
        if not AlgorithmAdapter.instance:
            AlgorithmAdapter.instance = AlgorithmAdapter.__AlgorithmAdapter()
            log.debug("Algorithm adapter created")
        else:
            log.debug("Algorithm adapter loaded")

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def initiateDetection(self, trainingInput, fndContext):
        if trainingInput.empty or not fndContext:
            log.debug(f"Initiation failed")
            return
        log.debug(f"Algorithm Initiation")
        fndInputs = fndContext.fndConfig.fndModel.fndinput_set.filter(
            trainingIndicator="Y"
        ).all()
        preprocessor = None
        for fndInput in fndInputs:
            if fndInput.variableName == "content":
                preprocessor = ContentPreprocessor()
        preprocessedTrainingInput = preprocessor.preprocess(trainingInput, fndContext)
        fndAlgo = self.getFNDAlgo()
        if not fndAlgo:
            log.debug("training algo not configured. Cannot train further")
            return
        klass = globals()[fndAlgo]
        algo = klass()

        algo.train(preprocessedTrainingInput, fndContext)

    def getFNDAlgo(self):
        return TrainingUtil.getAlgo()

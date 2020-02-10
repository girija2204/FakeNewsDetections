import matplotlib.pyplot as plt
from keras.layers import Flatten
from keras.layers.core import Dense
from keras.layers.embeddings import Embedding
from keras.models import Sequential
from newstraining.algorithm.abstractAlgorithm import AbstractAlgorithm
from django.conf import settings
from newstraining.trainingUtil import TrainingUtil
from newstraining.trainingEnums import TrainingEnums
from newstraining.preprocessor.contentPreprocessor import ContentPreprocessor
import pdb

log = settings.LOG


class NeuralNetwork(AbstractAlgorithm):
    def __init__(self, fndContext):
        super().__init__(fndContext)

    def train(self, X_train, Y_train, fndContext, embeddingLayer=None):
        model = Sequential()
        model.add(embeddingLayer)
        model.add(Flatten())
        model.add(Dense(1, activation="sigmoid"))

        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["acc"])
        print(model.summary())
        # pdb.set_trace()
        history = model.fit(
            X_train, Y_train, batch_size=128, epochs=6, verbose=1, validation_split=0.2,
        )

        return model

    def predict(self, predictionInput, fndContext):
        loadedModel = self.loadModel(fndContext=fndContext)
        log.debug(f"model loaded")
        fndInputs = fndContext.fndConfig.fndModel.fndinput_set.filter(
            trainingIndicator="Y"
        ).all()
        preprocessor = None
        for fndInput in fndInputs:
            if fndInput.variableName == "content":
                preprocessor = ContentPreprocessor()
                log.debug("Using contentPreprocessor")
        paddedX_test = preprocessor.getPaddedSequences(data=predictionInput)
        classPredicted = loadedModel.predict_classes(paddedX_test)
        log.debug(f"predicted class: {classPredicted}")
        return classPredicted

    def evaluateModel(self, model, X_test, Y_test, fndContext):
        score = model.evaluate(X_test, Y_test, verbose=1)
        log.debug(f"Test score using baseline NN:{score[0] * 100}")
        log.debug(f"Test accuracy using baseline NN:{score[1] * 100}")

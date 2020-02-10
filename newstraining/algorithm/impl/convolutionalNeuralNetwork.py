from newstraining.algorithm.abstractAlgorithm import AbstractAlgorithm
from keras.layers import Flatten
from keras.layers.core import Dense
from keras.models import Sequential
from keras.layers import GlobalMaxPooling1D, Conv1D
from django.conf import settings

log = settings.LOG


class ConvolutionalNN(AbstractAlgorithm):
    def __init__(self, fndContext):
        super().__init__(fndContext)

    def train(self, X_train, Y_train, fndContext, embeddingLayer=None):
        model = Sequential()
        model.add(embeddingLayer)
        model.add(Conv1D(128, 5, activation="relu"))
        model.add(GlobalMaxPooling1D())
        model.add(Dense(1, activation="sigmoid"))
        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["acc"])

        print(model.summary())

        history = model.fit(
            X_train, Y_train, batch_size=128, epochs=6, verbose=1, validation_split=0.2
        )

        return model

    def predict(self, predictionInput, fndContext):
        pass

    def evaluateModel(self, model, X_test, Y_test, fndContext):
        score = model.evaluate(X_test, Y_test, verbose=1)
        log.debug(f"Test score using convolutional NN:{score[0] * 100}")
        log.debug(f"Test accuracy using convolutional NN:{score[1] * 100}")

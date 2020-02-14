from keras.layers import Flatten
from newstraining.algorithm.abstractAlgorithm import AbstractAlgorithm
from keras.layers import GlobalMaxPooling1D, LSTM, Dropout, Conv1D, MaxPooling1D, BatchNormalization
from keras.models import Sequential
from keras.layers.core import Dense
from django.conf import settings

log = settings.LOG


class LSTMAlgo(AbstractAlgorithm):
    def __init__(self, fndContext):
        super().__init__(fndContext)

    def train(self, X_train, Y_train, fndContext, embeddingLayer=None):
        model = Sequential()
        model.add(embeddingLayer)
        model.add(Dropout(0.2))
        model.add(Conv1D(filters=32, kernel_size=5, padding='same', activation='relu'))
        model.add(MaxPooling1D(pool_size=2))
        model.add(Conv1D(filters=64, kernel_size=3, padding='same', activation='relu'))
        model.add(MaxPooling1D(pool_size=2))
        model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
        model.add(BatchNormalization())
        model.add(Dense(256, activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(1, activation="sigmoid"))
        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["acc"])
        print(model.summary())

        history = model.fit(
            X_train, Y_train, batch_size=128, epochs=10, verbose=1, validation_split=0.15
        )

        return model

    def predict(self, predictionInput, fndContext):
        pass

    def evaluateModel(self, model, X_test, Y_test, fndContext):
        score = model.evaluate(X_test, Y_test, verbose=1)
        log.debug(f"Test score using LSTM:{score[0] * 100}")
        log.debug(f"Test accuracy using LSTM:{score[1] * 100}")

from math import ceil
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, LSTM, Dropout, Conv1D, MaxPooling1D, BatchNormalization
from tensorflow.keras.models import Sequential
from django.conf import settings
from newstraining.algorithm.abstractAlgorithm import AbstractAlgorithm
import pdb

log = settings.LOG


class LSTMAlgo(AbstractAlgorithm):
    def __init__(self, fndContext):
        super().__init__(fndContext)

    def createModel(self,embeddingLayer=None):
        pdb.set_trace()
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
        return model

    def compileModel(self,model,optimizer,loss,metrics):
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        return model

    def batch_generator(self,X, y, batch_size, mode):
        size = len(X)
        X_copy = X.copy()
        y_copy = y.copy()
        i = 0
        while True:
            left, right = i * batch_size, (i + 1) * batch_size
            right = min(size, right)
            log.debug("getting padded seqeunces")
            # pdb.set_trace()
            X_batch = self.preprocessors[0].getPaddedSequences(X_copy[left:right])
            y_batch = y_copy[left:right]
            yield X_batch, y_batch
            if right >= size:
                i = 0
                X_copy = X.copy()
                y_copy = y.copy()
            else:
                i = i + 1

    def train(self, X_train, X_test, Y_train, Y_test, fndContext, embeddingLayer=None):
        pdb.set_trace()
        model = self.createModel(embeddingLayer=embeddingLayer)
        model = self.compileModel(model,"adam","binary_crossentropy",["acc"])
        log.debug(model.summary())
        batch_size = 128
        filepath = "/content/drive/My Drive/Colab Notebooks/weights-improvement-{epoch:02d}-{val_accuracy:.2f}.hdf5"
        # checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
        es = EarlyStopping(monitor='val_loss', patience=5, verbose=2)
        callbacks_list = [es]
        history = model.fit_generator(generator=self.batch_generator(X_train,Y_train,batch_size,mode="training"),
                                      steps_per_epoch=ceil(len(X_train) / batch_size),
                                      epochs=20,
                                      verbose=1,
                                      callbacks = callbacks_list,
                                      validation_data=self.batch_generator(X_test, Y_test, batch_size,mode="testing"),
                                      validation_steps=ceil(len(X_test) / batch_size))

        return model

    def predict(self, predictionInput, fndContext):
        pass

    def evaluateModel(self, model, X_test, Y_test, fndContext):
        score = model.evaluate(X_test, Y_test, verbose=1)
        log.debug(f"Test score using LSTM:{score[0] * 100}")
        log.debug(f"Test accuracy using LSTM:{score[1] * 100}")

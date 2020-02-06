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

    def train(self, trainingInput, fndContext, embeddingMatrix=None):
        log.debug(
            f"Splitting the dataset: {fndContext.trainTestSplitRatio} for test and {1-float(fndContext.trainTestSplitRatio)} for train"
        )
        X_train, X_test, Y_train, Y_test = TrainingUtil.splitTrainTest(
            trainingInput["content"],
            trainingInput["label"],
            float(fndContext.trainTestSplitRatio),
        )
        fndInputs = fndContext.fndConfig.fndModel.fndinput_set.filter(
            trainingIndicator="Y"
        ).all()
        preprocessor = None
        for fndInput in fndInputs:
            if fndInput.variableName == "content":
                preprocessor = ContentPreprocessor()
        paddedX_train = preprocessor.getPaddedSequences(X_train)
        paddedX_test = preprocessor.getPaddedSequences(X_test)
        embedding_matrix = preprocessor.getEmbeddingMatrix(data=X_train)

        model = Sequential()
        embedding_layer = Embedding(
            preprocessor.getVocabularySize(),
            100,
            weights=[embedding_matrix],
            input_length=int(TrainingUtil.getMaxLength()),
            trainable=False,
        )
        model.add(embedding_layer)
        model.add(Flatten())
        model.add(Dense(1, activation="sigmoid"))

        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["acc"])
        print(model.summary())
        # pdb.set_trace()
        history = model.fit(
            paddedX_train,
            Y_train,
            batch_size=128,
            epochs=6,
            verbose=1,
            validation_split=0.2,
        )

        score = model.evaluate(paddedX_test, Y_test, verbose=1)
        log.debug(f"Test score using baseline NN:{score[0] * 100}")
        log.debug(f"Test accuracy using baseline NN:{score[1] * 100}")

        log.debug("Saving the model")
        self.saveModel(model=model, fndContext=fndContext)
        log.debug("Training over")

    def predict(self, predictionInput, fndContext):
        loadedModel = self.loadModel(fndContext=fndContext)
        log.debug(f'model loaded')
        fndInputs = fndContext.fndConfig.fndModel.fndinput_set.filter(
            trainingIndicator="Y"
        ).all()
        preprocessor = None
        for fndInput in fndInputs:
            if fndInput.variableName == "content":
                preprocessor = ContentPreprocessor()
                log.debug('Using contentPreprocessor')
        paddedX_test = preprocessor.getPaddedSequences(data=predictionInput)
        classPredicted = loadedModel.predict_classes(paddedX_test)
        log.debug(f'predicted class: {classPredicted}')
        return classPredicted

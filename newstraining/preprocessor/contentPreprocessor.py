import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from newstraining.preprocessor.preprocessor import Preprocessor
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from django.conf import settings
from newstraining.trainingUtil import TrainingUtil
import pandas as pd

import pdb


log = settings.LOG


class ContentPreprocessor(Preprocessor):
    class __ContentPreprocessor:
        tokenizer = None

        def __init__(self):
            pass

    instance = None

    def __init__(self):
        super().__init__()
        if not ContentPreprocessor.instance:
            ContentPreprocessor.instance = ContentPreprocessor.__ContentPreprocessor()
            log.debug(f"ContentPreprocessor created")
        else:
            log.debug(f"ContentPreprocessor loaded")

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def removeSymbols(self, contentData, columnName):
        log.debug(f"Removing unnecessary symbols")
        for index, content in enumerate(contentData):
            content = re.sub("[^a-zA-Z0-9]", " ", content)
            content = re.sub(r"\s+[a-zA-Z]\s+", " ", content)
            content = re.sub(r"\s+", " ", content)
            contentData.iloc[index] = content
        return contentData

    def stemText(self, contentData):
        log.debug(f"Stemming text")
        lemmatizer = WordNetLemmatizer()
        for index, content in enumerate(contentData):
            stemmedContent = [lemmatizer.lemmatize(word.lower()) for word in content]
            contentData.iloc[index] = " ".join(word for word in stemmedContent)
        return contentData

    def removeStopWords(self, contentData):
        log.debug(f"Removing stop words")
        stop_words = set(stopwords.words("english"))
        for index, content in enumerate(contentData):
            filteredContent = []
            for word in content:
                if not word in stop_words:
                    filteredContent.append(word)
            contentData.iloc[index] = filteredContent
        return contentData

    def tokenizeSentence(self, contentData):
        log.debug(f"Tokenizing sentences")
        for index, content in enumerate(contentData):
            contentData.iloc[index] = word_tokenize(content)
        return contentData

    def createTokenizer(self, X_train):
        tokenizer = Tokenizer(num_words=5000)
        tokenizer.fit_on_texts(X_train)
        x = tokenizer.word_index
        # pdb.set_trace()
        if self.tokenizer is not None:
            self.tokenizer = None
        self.tokenizer = tokenizer
        return tokenizer

    def createWordEmbeddingDictionary(self):
        log.debug("Creating Word Embedding Dictionary from Glove")
        embeddings_dictionary = dict()
        glove_file = open(TrainingUtil.getWordEmbeddingsFileName(), encoding="utf8")
        for line in glove_file:
            records = line.split()
            word = records[0]
            vector_dimensions = np.asarray(records[1:], dtype="float32")
            embeddings_dictionary[word] = vector_dimensions
        glove_file.close()
        return embeddings_dictionary

    def getVocabularySize(self):
        log.debug(f"Vocabulary size: {len(self.tokenizer.word_index) + 1}")
        return len(self.tokenizer.word_index) + 1

    def createEmbeddingMatrix(self, embeddings_dictionary, tokenizer):
        log.debug(f"Creating word embedding matrix")
        # pdb.set_trace()
        embedding_matrix = np.zeros((self.getVocabularySize(), 100))
        for word, index in tokenizer.word_index.items():
            embedding_vector = embeddings_dictionary.get(word)
            if embedding_vector is not None:
                embedding_matrix[index] = embedding_vector

        return embedding_matrix

    def getPaddedSequences(self, data):
        if self.tokenizer is not None:
            log.debug(f"Tokenizer is already set")
            tokenizer = self.tokenizer
        else:
            log.debug(f"No tokenizer is set, so loading it from last training run")
            tokenizer = TrainingUtil.loadTokenizer()

        log.debug(f"Converting data to sequences")
        sequenceData = tokenizer.texts_to_sequences(data)

        maxlen = int(TrainingUtil.getMaxLength())
        log.debug(f"Padding upto maxLegnth of Sequences: {maxlen}")

        paddedSequenceData = pad_sequences(sequenceData, padding="post", maxlen=maxlen)
        return paddedSequenceData

    def getEmbeddingMatrix(self, data):
        # pdb.set_trace()
        # tokenizer = self.tokenizer
        # if tokenizer is None:
        tokenizer = self.createTokenizer(data)

        embedding_dictionary = self.createWordEmbeddingDictionary()
        embedding_matrix = self.createEmbeddingMatrix(
            embeddings_dictionary=embedding_dictionary, tokenizer=tokenizer
        )
        return embedding_matrix

    def preprocess(self, data, fndContext):
        log.debug(f"preprocessing start with contentPreprocessor")
        # pdb.set_trace()
        contentData = self.removeSymbols(data["content"], "content")
        contentData = self.tokenizeSentence(contentData)
        contentData = self.removeStopWords(contentData)
        contentData = self.stemText(contentData)
        filteredContentData = pd.DataFrame(columns=["content"], data=contentData)
        if fndContext.processName == "training":
            label = pd.DataFrame(data["fake_status"])
            filteredContentData = filteredContentData.join(label)
            filteredContentData.columns = ["content", "label"]
        else:
            filteredContentData.columns = ["content"]
        return filteredContentData

#doc tung file, bo html.
import gensim, re, pickle, datetime, os, multiprocessing
import numpy as np
import pandas as pd
from os import listdir
from Normalization import chuanhoachuTV
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences

from keras.layers import Dense, Embedding, Input, Conv2D, MaxPooling2D, concatenate, Dropout
from keras.layers.core import Reshape, Flatten
from keras.models import Model
from keras.callbacks import ModelCheckpoint
from Normalization import chuanhoachuTV as c
from underthesea import text_normalize
from Normalization import stopword as s
sep = os.sep

data_folder = "C:/Users/LENOVO/PycharmProjects/abc/Learning/Data/Full_Data"
model_folder = "C:/Users/LENOVO/PycharmProjects/abc/Learning/Model/Full_Model"
result_folder = "C:/Users/LENOVO/PycharmProjects/abc/Learning/Result"
EMBEDDING_DIM = 300

def txtTokenizer(texts):
    tokenizer = Tokenizer(lower=True, filters=',.')
    tokenizer.fit_on_texts(texts)

    word_index = tokenizer.word_index
    return tokenizer, word_index

def loadData(data_folder):
    texts = []
    labels = []
    count = 0
    for f in listdir(data_folder):
        count += 1
        with open(data_folder + sep + f, 'r', encoding='UTF-8') as file:
            for line in file:
                l = line.rstrip()
                l = c.remove_html(l)
                l = c.remove_special_character(l)
                l = c.remove_consec_duplicates(l)

                l = text_normalize(l)
                l = s.deStopword(l)
                if (len(l) == 0):
                    continue
                texts = texts + [l]
                label = f[:len(f) - 4]  # binhthuong.txt > binhthuong
                labels = labels + [label]

    return texts, labels


if __name__ == '__main__':

    #load data and label it
    texts, labels = loadData(data_folder)
    print(texts)

    #create or load tokenizer model
    if not os.path.exists(model_folder + sep + "tokenizer.pkl"):
        print("Create tokenizer model")
        tokenizer, word_index = txtTokenizer(texts)
        # print("tokenizer", tokenizer)
        print("word_index", word_index)
        # save tokenizer
        file = open(model_folder + sep + "tokenizer.pkl", 'wb')
        pickle.dump([tokenizer, word_index], file)
        file.close()

    else:
        print("Tokenizer model found, load it!")
        file = open(model_folder + sep + "tokenizer.pkl", 'rb')
        tokenizer, word_index = pickle.load(file)
        file.close()
    print(word_index)
    # transform data to number
    X = tokenizer.texts_to_sequences(texts)
    X = pad_sequences(X)
    print(X)
    print(X.shape)

    y = pd.get_dummies(labels)

    # split to train data and validation data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=True)
    #
    # # create or load word2vec model
    if not os.path.exists(model_folder + sep + "word_model.model"):
        cores = multiprocessing.cpu_count()
        word_model = gensim.models.Word2Vec(texts, vector_size=EMBEDDING_DIM, min_count=3,
                                            workers=cores - 1)  # default window = 5
        word_model.train(texts, total_examples=word_model.corpus_count, epochs=5)
        word_model.save(model_folder + sep + "word_model.model")
    # load
    else:
        print("found word_model")
        word_model = gensim.models.Word2Vec.load(model_folder + sep + "word_model.model")

    # create embedding matrix follow word2vec result
    embedding_matrix = np.zeros((len(word_index) + 1, EMBEDDING_DIM))
    for word, i in word_index.items():
        try:
            embedding_matrix[i] = word_model.wv[word]
        except KeyError:
            embedding_matrix[i] = np.random.normal(0, np.sqrt(0.25), EMBEDDING_DIM)

    # # train CNN model and save a model with the best val_acc
    sequence_length = X.shape[1]
    filter_sizes = [3, 4, 5]

    drop = 0.2
    num_filters = 298
    inputs = Input(shape=(sequence_length,))
    embedding = Embedding(len(word_index) + 1, EMBEDDING_DIM, weights=[embedding_matrix], trainable=True)(inputs)
    reshape = Reshape((sequence_length, EMBEDDING_DIM, 1))(embedding)
    print(reshape)
    conv_0 = Conv2D(num_filters, (filter_sizes[0], EMBEDDING_DIM), activation='relu')(reshape)
    conv_1 = Conv2D(num_filters, (filter_sizes[1], EMBEDDING_DIM), activation='relu')(reshape)
    conv_2 = Conv2D(num_filters, (filter_sizes[2], EMBEDDING_DIM), activation='relu')(reshape)
    conv_3 = Conv2D(num_filters, (filter_sizes[2], EMBEDDING_DIM), activation='relu')(reshape)
    conv_4 = Conv2D(num_filters, (filter_sizes[2], EMBEDDING_DIM), activation='relu')(reshape)

    maxpool_0 = MaxPooling2D((sequence_length - filter_sizes[0] + 1, 1), strides=(1, 1))(conv_0)
    maxpool_1 = MaxPooling2D((sequence_length - filter_sizes[1] + 1, 1), strides=(1, 1))(conv_1)
    maxpool_2 = MaxPooling2D((sequence_length - filter_sizes[2] + 1, 1), strides=(1, 1))(conv_2)
    maxpool_3 = MaxPooling2D((sequence_length - filter_sizes[2] + 1, 1), strides=(1, 1))(conv_3)
    maxpool_4 = MaxPooling2D((sequence_length - filter_sizes[2] + 1, 1), strides=(1, 1))(conv_4)

    merged_tensor = concatenate([maxpool_0, maxpool_1, maxpool_2, maxpool_3, maxpool_4], axis=1)
    flatten = Flatten()(merged_tensor)
    reshape = Reshape((5 * num_filters,))(flatten)
    dropout = Dropout(drop)(flatten)
    output = Dense(units=3, activation='softmax')(dropout)

    model = Model(inputs, output)

    model.summary()
    batch = 256
    epochs = 20
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['accuracy'])
    filepath = model_folder + sep + "predict_model.h5"
    checkpoint = ModelCheckpoint(filepath, save_best_only=True, verbose=1, monitor='val_accuracy', mode='auto')
    callbacks_list = [checkpoint]
    history_data = model.fit(X_train, y_train, batch_size=batch, epochs=epochs, callbacks=callbacks_list, verbose=2,
                             validation_data=(X_test, y_test))

    # create chart
    # plt.plot(history_data.history['accuracy'], label = "train_accuracy")
    plt.plot(history_data.history['val_accuracy'], label="val_accuracy")
    plt.xlabel('iteration')
    plt.ylabel('Accuracy')
    plt.legend()

    now = datetime.datetime.now()

    plt.savefig(result_folder + sep + now.strftime("%d-%m-%Y_full_data.png"))

from copyreg import pickle
import os, pickle

from keras.models import load_model
# from keras.preprocessing.text import Tokenizer
# from keras.models import Model

sep = os.sep

data_folder = "C:/Users/LENOVO/PycharmProjects/abc/Learning/Data/Full_Data/"
model_folder = "C:/Users/LENOVO/PycharmProjects/abc/Learning/Model/Full_Model/"
EMBEDDING_DIM = 300

def predict(sentence, h5_file = model_folder + sep + "predict_model.h5", dict_file = model_folder + sep + "tokenizer.pkl"):
    if not os.path.exists(dict_file):
        print('Can not found tokenizer model')
        return -1

    if not os.path.exists(h5_file):
        print('Can not found CNN model')
        return -1
    
    print("Tokenizer model found, load it!")
    file = open(dict_file, 'rb')
    tokenizer, word_index = pickle.load(file)
    file.close()

    print("CNN model found, load it!")
    model = load_model(h5_file)

    # predict
    arr = tokenizer.texts_to_sequences([sentence])
    print("\nĐộ dài câu: ", len(arr[0]))
    if len(arr[0]) == 0:
        print('Warning! Every words in this sentence couldn\'t found in current dictionary')
    #     return -2
    arr[0] = [0] * (model.layers[0].output_shape[0][1]-len(arr[0])) + arr[0]
    return model.predict(arr).argmax()


if __name__ == '__main__':
    print(predict('anh ta là 1 vị vua'))

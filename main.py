# from crypt import methods
from flask import Flask, render_template, request, json, redirect, url_for
import Model

from Learning import predict
from Model import connect
from Normalization import chuanhoachuTV as c, stopword as s, test
from underthesea import text_normalize
import os, datetime


app = Flask(__name__)
model_folder = "C:/Users/LENOVO/PycharmProjects/abc/Learning/Model/Full_Model/"
current_h5 = model_folder + 'predict_model.h5'
current_dict = model_folder + "tokenizer.pkl"


@app.route("/", methods=['POST', 'GET'])
def home():
    status = 2;
    popular_movies = connect.select_polular_movie()[:8]
    if request.method == 'GET':
        return render_template("index.html", popular_movies=popular_movies, status = 1,title="PHIM MỚI")
    if request.method == 'POST':
        res = connect.select_name_movie(request.form['search'])
        print(type(res))
        label = -1;
        if len(res) < 1:  # trong csdl không có > dùng hệ thống thông minh
            print("Input: ", request.form['search'])
            correct_sentence = c.remove_special_character(request.form['search'])
            correct_sentence = c.remove_consec_duplicates(correct_sentence)
            correct_sentence = text_normalize(correct_sentence)
            correct_sentence = s.deStopword(correct_sentence)

            if(len(correct_sentence) < 1):
                status = -1
            else:
                print("Input sau khi được xử lý: ", correct_sentence)
                label = predict.predict(correct_sentence, current_h5, current_dict)
                print("label: ", label)
                if label == 0:  # đây là màu đỏ
                    print("binh thuong")
                else:
                    if label == 1:  # hài hước thật sự
                        print("tich cuc")
                    else:  # hôm nay tôi buồn
                        print("tieu cuc")
                if label == -1 or label == -2:
                    res = False
                    status = -1
                else:
                    res = connect.select_movie(label)[:8]
        print("status", status)
        print("label", label)
        return render_template("index.html",  search=request.form['search'], title="KẾT QUẢ TÌM KIẾM", label = label, movie_list=res, status=2)


@app.route("/insertMovie", methods=['POST', 'GET'])
def form():
    if request.method == 'GET':
        return render_template("form.html")
    if request.method == 'POST':
        connect.insert_movie(request.form['movie_vn'], request.form['movie_en'], request.form['link'], request.form['rating'],
                             request.form['url_img'], request.form['label'])
        return redirect('/')




@app.route("/saveInputAndLabel", methods=['POST','GET'])
def saveInputAndLabel():
    if request.method == 'POST':
        print("saveInput")
        output = request.get_json()
        print("output", output)  # This is the output that was stored in the JSON within the browser
        result = json.loads(output)  # this converts the json output to a python dictionary
        label = result["label"]
        textt= result["text"]
        textt = c.remove_special_character(textt)
        textt = c.remove_consec_duplicates(textt)
        textt = text_normalize(textt)
        textt = s.deStopword(textt)
        if label == "0":  # đây là màu đỏ
            with open('C:/Users/LENOVO/PycharmProjects/abc/Learning/Data/Full_Data/binhthuong.txt',
            encoding="utf-8") as f:
                text = f.read()
            with open('C:/Users/LENOVO/PycharmProjects/abc/Learning/Data/Full_Data/binhthuong.txt', 'a',
            encoding="utf-8") as f:
                if not text.endswith('\n'):
                    f.write('\n')
                    f.write(textt)
                else:
                    f.write(textt)

        else:
            if label == "1":  # hài hước thật sự
                with open('C:/Users/LENOVO/PycharmProjects/abc/Learning/Data/Full_Data/tichcuc.txt',
                          encoding="utf-8") as f:
                    text = f.read()
                with open('C:/Users/LENOVO/PycharmProjects/abc/Learning/Data/Full_Data/tichcuc.txt', 'a',
                          encoding="utf-8") as f:
                    if not text.endswith('\n'):
                        f.write('\n')
                        f.write(textt)
                        print("Đã viết xong")
                    else:
                        f.write(textt)
                        return
            else:  # hôm nay tôi buồn
                print("tieu cuc")
                with open('C:/Users/LENOVO/PycharmProjects/abc/Learning/Data/Full_Data/tieucuc.txt', encoding="utf-8") as f:
                    text = f.read()
                    print("hello")
                with open('C:/Users/LENOVO/PycharmProjects/abc/Learning/Data/Full_Data/tieucuc.txt', 'a', encoding="utf-8") as f:
                    if not text.endswith('\n'):
                        f.write('\n')
                        f.write(textt)
                    else:
                        f.write(textt)

        return result


if __name__ == "__main__":
    app.run(debug=True)

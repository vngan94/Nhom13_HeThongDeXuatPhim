import re
import underthesea as u
def deStopword(content1):
    stopwords = []
    stopwords1 = []
    content = open('C:/Users/LENOVO/PycharmProjects/abc/Normalization/stopword.txt', 'r', encoding='UTF-8').read()
    res = content.split("\n")
    res1 = content1.split()
    res2 = []
    for i, word in enumerate(res1):
        if i < len(res1) -1:
            res2.append(res1[i] + ' ' +res1[i+1])

    len_stop1 = 1
    if len(list(set(res) & set(res1))) > 0:
        stopwords.append(list(set(res) & set(res1)))
    else:
        len_stop1 = 0

    len_stop = 1
    if len(list(set(res) & set(res2))) > 0:
        stopwords1.append(list(set(res) & set(res2)))
    else:
        len_stop = 0
    if len_stop != 0:
        for word in stopwords1[0]:
            if word in content1:
                content1 = content1.replace(word, '')

    if len_stop1 != 0:
        for word in stopwords[0]:
            if word in content1:
                content1 = content1.replace(word, '')
    content1 = re.sub(r"\s+", ' ', content1).strip()
    return content1

if __name__ == '__main__':
    s = 'rất quả'

    print(len(deStopword('rất quá')))







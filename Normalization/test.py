import re
import os
import sys


def ChuanHoaChuoi(word):
    mylist = list(word)
    for i in range(len(mylist)):
        for j in range(len(mylist)):
            if (j < len(mylist) - 1):
                if (mylist[j] == mylist[j + 1]):
                    mylist.pop(j + 1)
    mystring = "".join(mylist)
    return mystring
def isCheckTVchuan(words):
    chuoi =[]
    word = ChuanHoaChuoi(words)
    lt = word.split()
    print(lt)
    content = open('TVchuan.txt', 'r', encoding='UTF-8').read()
    res = content.split(" ")
    if  len(list(set(res) & set(lt))) < 1:
         return ' '
    else:
         chuoi.append(list(set(res) & set(lt)))
    return chuoi

stop_words= ['nước đến','những là','tự cao','đâu phải','vừa rồi','tự lượng','chứ lại','sau cuối','tớ','phỏng theo','được']
'''bỏ từ tôi rất '''
def remove_stop_words(corpus):
    results = []
    for text in corpus:
        tmp = text.split(' ')
        for stop_word in stop_words:
            if stop_word in tmp:
                tmp.remove(stop_word)
        results.append(" ".join(tmp))

    return results

if __name__ == '__main__':

    string = "mộttt nào khoong múng khi đó ngày "
    str1 = ChuanHoaChuoi(string)
    print(str1)
    st2 = isCheckTVchuan(string)

    print(st2)
    corpus = ['tôi ăn cơm hom qua', 'là một nhạc sĩ người Việt Nam', 'Ông được coi là một trong những nhạc',
              'Tuy nhiên số ca khúc của ông được biết đến ', 'Tên tuổi của Trịnh Công Sơn được nhiều người biết đến ']
    string1 = remove_stop_words(corpus)
    print(string1)


import sys
import pandas as pd
import numpy as np
import re
import random

def disc(word,dic):
    input_flag = 0
    for i in range(len(word)):
        if word[i] not in dic:
            input_flag = 1
    return input_flag


def End(num,word,next_word):
    if(word[num][-1] == "ン")  or next_word  != word[num][0]:
        return 1
    else:
        return 0
def conv(dic,next_word,word):
    if next_word in dic:
        return dic[next_word]
    else:
        return next_word

def delete(Katakana):
    Katakana.remove("ァ")
    Katakana.remove("ィ")
    Katakana.remove("ゥ")
    Katakana.remove("ェ")
    Katakana.remove("ォ")
    Katakana.remove("ッ")
    Katakana.remove("ャ")
    Katakana.remove("ュ")
    Katakana.remove("ョ")
    Katakana.remove("ヮ")
    Katakana.remove("ヰ")
    Katakana.remove("ヱ")
    
    return Katakana

def fin(word):
    for i in range(len(word)-1):
        print(word[i],"=> ",end="")
    print(word[-1])

#対応表
word_dict={"ァ":"ア","ィ":"イ","ゥ":"ウ","ェ":"エ","ォ":"オ","ッ":"ツ","ャ":"ヤ","ュ":"ユ","ョ":"ヨ"}
#read_csv
df = pd.read_csv("data/mecab-ipadic-2.7.0-20070801/Noun.csv", usecols= [11])
#############ア-ンの配列#############
Noun = []
Noun = df.values
Katakana = []
large_a = "30A1" #ア
large_n = "30F3" #ン
#ン-アまでの距離
length = int(large_n,16) - int(large_a,16) + 1
#カタカナを配列に移動
for i in range(length):
    Katakana.append(chr(int(large_a,16) + i))
delete(Katakana)

#単語辞書をアイウエオ順に並び替え
unique_arr = np.unique(Noun)
####dict={Katakana:unique_arr}を作る
num = 0
word_temp = []
word = []
#print(Katakana)
#print(unique_arr)
for i in range(len(unique_arr)):
    if re.match(Katakana[num], unique_arr[i]):
        word_temp.append(unique_arr[i])
    else:
        num += 1
        if num == len(Katakana):
            break
        if re.match(Katakana[num], unique_arr[i]):
            word.append(word_temp)
            word_temp=[]
enemy_dic ={key: val for key, val in zip(Katakana, word)}
word=[]  

#########
flag = 0
num=0
turn = 1

word_new = input("あなたの番です(カタカナで入力してね)>>")
while True:
        input_flag = disc(word_new,Katakana)
        if input_flag == 0:
            next_word = word_new[0]
            break
        else:
            word_new = input("あなたの番です(カタカナで入力してね)>>")

next_word = word_new[0]

while True:
    #あなたの入力の判定
    
    word.append(word_new)

    for i in range(len(word) -1 ):
        if word_new in word[i] and len(word_new) == len(word[i]):
            print("PCの勝利です")
            fin(word)
            flag = 1
            break
    if flag == 1:
        break
    if End(num,word,next_word):
        print("PCの勝利です")
        fin(word)
        break
    if(word[num][-1] == "ー"):
        next_word = word[num][-2]
    else:
        next_word = word[num][-1]

    next_word = conv(word_dict,next_word,word)
    num += 1

    ###############PC側の入力#################
    turn = 0
    print("あいて:",end="")
    data = enemy_dic[str(next_word)]
    rand_num = random.randint(0,len(data)-1)
    print(data[rand_num])
    word_new = data[rand_num]
    word.append(data[rand_num])

    #入力が過去にあるかどうか
    for i in range(len(word)-1):
        if word_new in word[i]:
            print("あなたの勝利です")
            fin(word)
            flag = 1
            break
    if flag == 1:
        break
    #入力した文字の最後が"ン"かどうか
    if End(num,word,next_word):
        print("あなたの勝利です")
        fin(word)
        break
    #入力した文字の最後が"-"かどうか
    if(word[num][-1] == "ー"):
        next_word = word[num][-2]
    else:
        next_word = word[num][-1]
    
    #次の文字を対応
    next_word = conv(word_dict,next_word,word)
    print("次の文字:",next_word)
    num += 1
    #あなたの入力
    word_new = input("あなたの番です(カタカナで入力してね)>>")

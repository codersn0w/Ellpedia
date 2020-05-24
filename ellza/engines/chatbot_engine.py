# coding: utf-8
from janome.tokenizer import Tokenizer
import os, re, json, random

dict_file = "./static/js/chatbot_data.json"
dic = {}
tokenizer = Tokenizer()

def make_sentence(head):
    if not head in dic: return ""
    ret = []
    if head != "@": ret.append(head)
    top = dic[head]
    w1 = word_choice(top)
    w2 = word_choice(top[w1])
    ret.append(w1)
    ret.append(w2)
    while True:
        if w1 in dic and w2 in dic[w1]:
            w3 = word_choice(dic[w1][w2])
        else:
            w3 = ""
        ret.append(w3)
        if w3 == "。" or w3 == "？" or w3 == "": break
        w1, w2 = w2, w3
    return "".join(ret)

def word_choice(sel):
    keys = sel.keys()
    return random.choice(list(keys))

def random_face():
    return random.choice(['(｀・∀・´)', '(｀・ω・´)', '(・∀・)', '(・ω・)'])

def random_reply(text):
    c = random.choice([1,2,3])
    if c == 1:
       return text + random_face() + ' (オウム返し中)'
    elif c == 2:
         return random.choice(['So...', 'WOW', 'Yo!', 'Well...'])
    else:
        return random.choice(['あなたの話ももっと聞かせてください (・∀・)',
                              'えーっとつまり... ( -ω-)zzz...( ﾟωﾟ) ﾊｯ!',
                              'すみません、今の私にはよくわかりません (´；ω；｀)'],)

def make_reply(text):
    if text[-1] != "。": text += "。"
    words = tokenizer.tokenize(text)
    ud_word = ""
    exepts = ["あなた", "お前", "僕", "君", "俺", "ぼく", "おれ", "私", "自分", "自分自身", "何"]
    for w in words:
        face = w.surface
        ps = w.part_of_speech.split(',')[0]
        if ps == "感動詞":
            reply = face + "。"
            return[{'chatbot': reply}]
        if ps == "名詞" or ps == "形容詞":
            if face in dic: return [{'chatbot': make_sentence(face)}]
        if ps == "名詞" and face not in dic and face not in exepts:
            ud_word = face
    if ud_word != "":
       d = random.choice([1, 2, 3])
       if d == 1:
          reply = "その「" + ud_word + "」というのは ( ・・)?"
          return [{'chatbot': reply}]
       else:
          return [{'chatbot': random_reply(text)}]
    else:
        return [{'chatbot': random_reply(text)}]

if os.path.exists(dict_file):
    dic = json.load(open(dict_file,"r"))


# Mecabで本文から地域名称を抽出してfieldに設定（後から付加する）
def location_name_mecab(sentence):
    t = mc.Tagger('-Ochasen -d /usr/local/Cellar/mecab/0.996/lib/mecab/dic/mecab-ipadic-neologd/')
    sentence = sentence.replace('\n', ' ')
    text = sentence.encode('utf-8') 
    node = t.parseToNode(text) 
    result_dict = defaultdict(list)
    for i in range(140):
        if node.surface != "":  # ヘッダとフッタを除外
            if (node.feature.split(",")[1] == "固有名詞") and (node.feature.split(",")[2] == "地域"):
                plain_word = node.feature.split(",")[6]
                if plain_word !="*":
                    result_dict[u'地域名称'].append(plain_word.decode('utf-8'))
        node = node.next
        if node is None:
            break
    return result_dict

for d in tweetdata.find({'spam':None},{'_id':1, 'text':1}):
    ret = location_name_mecab(d['text'])
    tweetdata.update({'_id' : d['_id']},{'$push': {'location_name':{'$each':ret[u'地域名称']}}})
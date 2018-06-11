# Tweet本文をMecabにかけて形態要素に分解
# Tweetデータに品詞ごとの属性noun, verb, adjective, adverbとして追加する。

# mecab 形態要素分解
def mecab_analysis(sentence):
    t = mc.Tagger('-Ochasen -d /usr/local/Cellar/mecab/0.996/lib/mecab/dic/mecab-ipadic-neologd/')
    #sentence = u"今日は良い天気ですが、雨ですね。クルマがほしいです。走ります。"
    sentence = sentence.replace('\n', ' ')
    text = sentence.encode('utf-8') 
    node = t.parseToNode(text) 
    result_dict = defaultdict(list)
    for i in range(140):
        if node.surface != "":  # ヘッダとフッタを除外
            word_type = node.feature.split(",")[0]
            if word_type in ["名詞", "形容詞", "動詞"]:
                plain_word = node.feature.split(",")[6]
                if plain_word !="*":
                    result_dict[word_type.decode('utf-8')].append(plain_word.decode('utf-8'))

            # 地域名称を独立のFieldとして格納
            if (node.feature.split(",")[1] == "固有名詞") and (node.feature.split(",")[2] == "地域"):
                plain_word = node.feature.split(",")[6]
                if plain_word !="*":
                    result_dict[u'地域名称'].append(plain_word.decode('utf-8'))
        node = node.next
        if node is None:
            break
    return result_dict


for d in tweetdata.find({'mecabed':False},{'_id':1, 'id':1, 'text':1,'noun':1,'verb':1,'adjective':1,'adverb':1}):

    res = mecab_analysis(unicodedata.normalize('NFKC', d['text'])) # 半角カナを全角カナに
    for k in res.keys():
        if k == u'形容詞': # adjective  
            adjective_list = []    
            for w in res[k]:
                adjective_list.append(w)
            tweetdata.update({'_id' : d['_id']},{'$push': {'adjective':{'$each':adjective_list}}})
        elif k == u'動詞': # verb
            verb_list = []
            for w in res[k]:
                #print k, w
                verb_list.append(w)
            tweetdata.update({'_id' : d['_id']},{'$push': {'verb':{'$each':verb_list}}})
        elif k == u'名詞': # noun
            noun_list = []
            for w in res[k]:
                noun_list.append(w)
            tweetdata.update({'_id' : d['_id']},{'$push': {'noun':{'$each':noun_list}}})
        elif k == u'副詞': # adverb
            adverb_list = []
            for w in res[k]:
                adverb_list.append(w)
            tweetdata.update({'_id' : d['_id']},{'$push': {'adverb':{'$each':adverb_list}}})
    # 形態要素分解済みとしてMecabedフラグの追加
    tweetdata.update({'_id' : d['_id']},{'$set': {'mecabed':True}})



# mecabで分解した単語を連結して文字列化する。
def get_mecabed_strings(from_date_str=None, to_date_str=None,include_rt=False):
    tweet_list = []
    tweet_texts = []

    from_date = str_to_date_jp_utc(from_date_str)
    to_date = str_to_date_jp_utc(to_date_str) 

    # 取得対象期間の条件設定
    if (from_date_str is not None) and (to_date_str is not None):
        query = {'created_datetime':{"$gte":from_date, "$lt":to_date}}
    elif (from_date_str is not None) and (to_date_str is None):
        query = {'created_datetime':{"$gte":from_date}}
    elif (from_date_str is None) and (to_date_str is not None):
        query = {'created_datetime':{"$lt":to_date}}
    else:
        query = {}

    # spam除去
    query['spam'] = None

    # リツイートを含むか否か
    if include_rt == False:
        query['retweeted_status'] = None
    else:
        query['retweeted_status'] = {"$ne": None}

    # 指定した条件のツイートを取得
    for d in tweetdata.find(query,{'noun':1, 'verb':1, 'adjective':1, 'adverb':1,'text':1}):
        tweet = ""
        # Mecabで分割済みの単語をのリストを作成
        if 'noun' in d:
            for word in d['noun']:
                tweet += word + " "
        if 'verb' in d:
            for word in d['verb']:
                tweet += word + " "
        if 'adjective' in d:
            for word in d['adjective']:
                tweet += word + " "
        if 'adverb' in d:
            for word in d['adverb']:
                tweet += word + " "
        tweet_list.append(tweet)
        tweet_texts.append(d['text'])
    return {"tweet_list":tweet_list,"tweet_texts":tweet_texts}
    
# "2015-03-18 00:00:00"以前
ret_before = get_mecabed_strings(to_date_str="2015-03-18 00:00:00")
tw_list_before = ret_before['tweet_list']

# "2015-03-18 00:00:00"以降
ret_after = get_mecabed_strings(from_date_str="2015-03-18 00:00:00")
tw_list_after= ret_after['tweet_list']

# 全期間
ret_all = get_mecabed_strings()
tw_list_all = ret_all['tweet_list']

c_vec = CountVectorizer(stop_words=[u"スタバ"])  # 「スタバ」は全Tweetに含まれるので除外
c_vec.fit(tw_list_all)                          # 全Tweetに含まれる単語の集合をここでセット
c_terms = c_vec.get_feature_names()             # 各ベクトル要素に対応する単語を表すベクトル

# 期間の前後でひとまとまりと考え、transformする
transformed = c_vec.transform([' '.join(tw_list_before),' '.join(tw_list_after)])

# afterからbeforeを引くことで増分をsubに代入
sub = transformed[1] - transformed[0]

# トップ50がどの位置にあるかを取り出す
arg_ind = np.argsort(sub.toarray())[0][:-50:-1]

# トップ50の表示
for i in arg_ind:
    print c_vec.get_feature_names()[i]
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# 3つの文章が対象
data=["This is a pen.",
      "This is also a pen. Pen is useful.",
      "These are pencils.",
     ]

c_vec   = CountVectorizer()           # CountVectorizerオブジェクトの生成
c_vec.fit(data)                       # 対象ツイート全体の単語の集合をセットする
c_terms = c_vec.get_feature_names()   # ベクトル変換後の各成分に対応する単語をベクトル表示
c_tran  = c_vec.transform([data[1]])  # 2つ目の文章の数を数える

print c_terms
print data[1]
print c_tran.toarray()
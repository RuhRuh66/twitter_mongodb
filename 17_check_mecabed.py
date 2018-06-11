# 各品詞がないレコードがあるか、カウントする
print tweetdata.find({'noun':None},{}).count()
print tweetdata.find({'verb':None},{}).count()
print tweetdata.find({'adjective':None},{}).count()
print tweetdata.find({'adverb':None},{}).count()

# 各品詞がないレコードにもフィールド追加
for w_type in ['noun', 'verb', 'adjective', 'adverb']:
    for d in tweetdata.find({w_type:None},{'_id':1}):
        tweetdata.update({'_id' : d['_id']},{'$push': {w_type:[]}})
    
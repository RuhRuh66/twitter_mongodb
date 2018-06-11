def is_include_word_list(text, word_list,f):
    for word in word_list:
        if text.find(word) > -1:
            return True
    return False


date_dict = defaultdict(int)

word_list = [u"新作", u"アーモンドミルク",u"ハニー", u"アーモンド", u"新しい", "with", u"クランチ"]

with open('armond.txt','w') as f:
    for d in tweetdata.find({'spam': None, 'retweeted_status': None},{'created_datetime':1,'text':1}):
        str_date = date_to_Japan_time(d['created_datetime']).strftime('%Y\t%m/%d %H %a') 

        text = d['text']
        if is_include_word_list(text, word_list,f):
            date_dict[str_date] += 1
            # マッチした対象をファイルに書き出す(for 検証用)
            ret_str = str_date +' '+ text.replace('\n', ' ')+'\n'
            f.write(ret_str.encode('utf-8'))

print "date_dict", len(date_dict)
print "階級数：", len(date_dict)
print "日付" + "\t\t\t" + "# of Tweet"
keys = date_dict.keys()
keys.sort()
for k in keys:
    print k  + "\t" +  str(date_dict[k]) 
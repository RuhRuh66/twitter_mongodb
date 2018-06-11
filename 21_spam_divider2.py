# Spamツイートの分離2 spamツイートをリツイートしている人をブロック

# spam accounts
spam_list = ['**********', '**********', '**********', '**********','**********',\
             '**********','**********','**********']


retweeted_name = ""
spam_twitter = set()

print tweetdata.find({'retweeted_status':{"$ne": None}}).count()
for d in tweetdata.find({'retweeted_status':{"$ne": None}}):

    try:
        retweeted_name = d['entities']['user_mentions'][0]['screen_name']
    except:
        pattern = r".*@([0-9a-zA-Z_]*).*"
        ite = re.finditer(pattern, d['text'])
        for it in ite:
            retweeted_name = it.group(1)
            break

    if retweeted_name in spam_list:
        spam_twitter.add(d['user']['screen_name'])

for user in spam_twitter:
    print user
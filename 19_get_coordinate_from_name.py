# 全国地名辞書・郵便番号辞書テキストのインポート
#http://www.odani.jp/dragon/ken-all.htm
#全国地名辞書・郵便番号辞書テキスト

import codecs
with codecs.open("timei-all.tsv",'r','shift_jis') as f:
    loc_dict = {l.split('\t')[1]: 0 for l in f.readlines()}
print len(loc_dict)

# すべての名詞を１つのリストに集約
noun_list = []
ex = noun_list.extend

for w in [d['noun'] for d in tweetdata.find({'coordinates':None,'spam':None},{'_id':1, 'noun':1})]:
    ex(w)

# 地理情報にマッチするものだけ抜き出し
def exist_place(word):
    if type(word) == list:
        return ""
    return word if word in loc_dict else ""
    
print len(noun_list)
res = np.array([exist_place(word) for word in noun_list])
    
res2 = np.array(map(len,res))
loc_list_in_tweet = np.unique(res[res2>0])

def get_coordinate_from_location(location_name):
    payload = {'appid': ＜ヤフーappid＞', 'output':'json'}   # please set your own appid.
    payload['query'] = location_name # e.g u'六本木'
    url = "http://geo.search.olp.yahooapis.jp/OpenLocalPlatform/V1/geoCoder"
    r = requests.get(url, params=payload)
    if r.status_code == 200:
        jdata = json.loads(r.content)

        # クエリで取得してた位置情報のリストから平均を算出してそれをその緯度経度とする。
        try:
            ret = np.array([map(float,j['Geometry']['Coordinates'].split(',')) for j in jdata['Feature']])
        except KeyError, e:
            "KeyError(%s)" % str(e)
            return []
            
        return np.average(ret,axis=0)
    else:
        print "%d: error." % r.status_code
        return []

# ツイートから抽出した地名に緯度経度を付与してmongoDBにインポート
for name in loc_list_in_tweet:
    loc = get_coordinate_from_location(name)
    if len(loc) > 0:
        location_dict.insert({"word":name,"latitude":loc[1],"longitude":loc[0]}) 
    
# インポートしたデータを取り出してリストに詰める
w_list = [loc for loc in location_dict.find({})]m
# ひらがな、カタカナだけの場合は地名じゃない可能性が高いので削除
import re
for loc in w_list:
    regex = u'^[ぁ-んァ-ン]*$'
    match = re.search(regex, loc['word'], re.U)
    if match:
        print match.group(), loc['longitude'], loc['latitude']
        location_dict.remove({"word":loc['word']})
    
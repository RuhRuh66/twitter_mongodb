#-------------繰り返しTweetデータを取得する-------------#
sid=-1
mid = -1 
count = 0

res = None
while(True):    
    try:
        count = count + 1
        sys.stdout.write("%d, "% count)
        res = getTweetData(u'スタバ', max_id=mid, since_id=sid)
        if res['result']==False:
            # 失敗したら終了する
            print "status_code", res['status_code']
            break
        
        if int(res['limit']) == 0:    # 回数制限に達したので休憩
            # 日付型の列'created_datetime'を付加する
            print "Adding created_at field."
            for d in tweetdata.find({'created_datetime':{ "$exists": False }},{'_id':1, 'created_at':1}):
                #print str_to_date_jp(d['created_at'])
                tweetdata.update({'_id' : d['_id']}, 
                     {'$set' : {'created_datetime' : str_to_date_jp(d['created_at'])}})
            #remove_duplicates()
            
            # 待ち時間の計算. リミット＋５秒後に再開する
            diff_sec = int(res['reset_time_unix']) - now_unix_time()
            print "sleep %d sec." % (diff_sec+5)
            if diff_sec > 0:
                time.sleep(diff_sec + 5)
        else:
            # metadata処理
            if len(res['statuses'])==0:
                sys.stdout.write("statuses is none. ")
            elif 'next_results' in res['metadata']:
                # 結果をmongoDBに格納する
                meta.insert({"metadata":res['metadata'], "insert_date": now_unix_time()})
                for s in res['statuses']:
                    tweetdata.insert(s)
                next_url = res['metadata']['next_results']
                pattern = r".*max_id=([0-9]*)\&.*"
                ite = re.finditer(pattern, next_url)
                for i in ite:
                    mid = i.group(1)
                    break
            else:
                sys.stdout.write("next is none. finished.")
                break
    except SSLError as (errno, request):
        print "SSLError({0}): {1}".format(errno, strerror)
        print "waiting 5mins"
        time.sleep(5*60)
    except ConnectionError as (errno, request):
        print "ConnectionError({0}): {1}".format(errno, strerror)
        print "waiting 5mins"
        time.sleep(5*60)
    except ReadTimeout as (errno, request):
        print "ReadTimeout({0}): {1}".format(errno, strerror)
        print "waiting 5mins"
        time.sleep(5*60)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        traceback.format_exc(sys.exc_info()[2])
        raise
    finally:
        info = sys.exc_info()
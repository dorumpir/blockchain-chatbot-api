import random
import datetime

random.seed(datetime.datetime)


class News:
    def __init__(self, es):
        self.es = es

    def get_news(self, kws, index, doc_type, es=None):
        if not es:
            es = self.es
        phrase = " ".join(kws)
        if phrase == "default":
            query = {
                "sort": {
                    "timstamp": {"order": "desc"},
                },
                "query": {
                        "match_all": {},
                    },
                    "size": 100,
            }
        # 脏代码
        elif phrase == '%&TokenviewNews':
            print('%&TokenviewNews')
            query = {
                "sort": {
                    "timstamp": {"order": "desc"},
                },
                "query": {
                    "multi_match": {
                        "query": "Tokenview  |数据 大额异动 行情 行情播报",
                        #"slop": 1,
                    }
                },
                "size": 80,
            }
        else:
            query = {
                "sort": {
                    "_score": "desc"
                },
                "query": {
                    "multi_match": {
                        "query": "%s" % phrase,
                        "slop": 1,
                    }
                },
                "size": 10,
            }
        results = es.search(index=index, doc_type=doc_type, body=query)
        if results:
            contents = []
            for result in results.get("hits").get("hits"):
                title = result.get("_source").get("title")
                content = result.get("_source").get("content")
                timestamp = result.get("_source").get("timstamp")
                id = result.get("_source").get("id")
                body = {
                    "id": id,
                    "title": title,
                    "content": content,
                    "timestamp": timestamp,
                }
                contents.append(body)
            try:
                prior_contents = []
                if phrase == '%&TokenviewNews':
                    contents = [cont for cont in contents if 'TOKENVIEW' in cont['content'].upper() or 'TOKENVIEW' in cont['title'].upper()]
                else:
                    contents = [cont for cont in contents if 'TOKENVIEW' not in cont['title'].upper()]
                    #contents = [cont for cont in contents if 'TOKENVIEW' not in cont['content'].upper() and 'TOKENVIEW' not in cont['title'].upper()]

                if phrase == 'default':
                    import time
                    from operator import itemgetter
                    from itertools import groupby
                    contents.sort(key=itemgetter('timestamp'), reverse=True)
                    # lambda： 距现在向前偏移GROUPBY_INTERVAL 秒
                    GROUPBY_INTERVAL = 1*60*60
                    divide_by_ts = lambda x: int((int(x['timestamp']) - int(time.time()) % GROUPBY_INTERVAL) / GROUPBY_INTERVAL)
                    for _, news_group in groupby(contents, key=divide_by_ts):
                        contents = list(news_group)
                        prior_contents = [cont for cont in contents if 'tokenview' in cont['content'].lower()]
                        contents = prior_contents or contents
                        break

                return_body = {
                    'success': 1,
                    'msg': "ok",
                    'news': random.choice(contents),
                }
                return return_body
            except:
                return_body = {
                    'success': 1,
                    'msg': "no search result",
                    'news': None
                 }
                return return_body    
        else:
            return_body = {
                'success': 1,
                'msg': "no search result",
                'news': None
             }
            return return_body
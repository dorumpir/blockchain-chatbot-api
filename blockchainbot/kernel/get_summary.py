from snownlp import SnowNLP
import random
import datetime
from blockchainbot.kernel.split_text import SplitText

random.seed(datetime.datetime)


class Summary:
    def __init__(self, es):
        self.es = es

    def get_summary(self, news, index, doc_type, es=None):
        if not es:
            es = self.es
        if len(news) <= 0:
            return_body = {
                'success': 0,
                'msg': 'no keywords',
                'summary': None,
            }
            return return_body
        s = SnowNLP(news)
        summary = s.summary()
        phrase = " ".join(summary)

        query = {
            "sort": {
                "_score": "desc"
            },
            "query": {
                "multi_match": {
                    "query": "%s" % phrase,
                    "slop": 1,
                }
            }
        }
        results = es.search(index=index, doc_type=doc_type, body=query)
        contents = []
        for result in results.get("hits").get("hits"):
            contents.append(result.get("_source").get("content"))
        a = ",".join(contents)
        newsp=SplitText()
        ss = SnowNLP(a)
        ss_summary = ss.summary()
        back_anwser = []
        for summary in ss_summary:
            sss = SnowNLP(summary.strip())
            sss_tags = [x for x in sss.tags]
            if sss_tags[0][1] in ["nz", "nt", "ns", "nr", "n"]:
                summary = summary.replace("，", "").replace(",", "")
                ssss = SnowNLP(summary)
                words = ssss.words
                back_anwser.append(words)
            else:
                pass
        if not back_anwser:
            try:
                content_summary = "我不太理解这条快讯,你可以给我讲讲什么是%s吗" % (random.choice(newsp.do_it(query["query"]["multi_match"]["query"])['bc_keywords']))
            except Exception as e:
                print(e)
                content_summary = "我不太理解这条快讯,你可以给我讲讲吗"
            back_anwser.append(content_summary)
        ss = SnowNLP(back_anwser)
        scores = ss.sim(s.words)
        best_anwser = "".join(back_anwser[scores.index(max(scores))])

        return_body = {
            "success": 1,
            "msg": "ok",
            "summary": best_anwser
        }
        return return_body
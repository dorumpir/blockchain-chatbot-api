from snownlp import SnowNLP


class Keywords:
    def __init__(self, es):
        self.es = es

    def get_keywords(self, news, es=None, cate=None):
        if not cate:
            if not news or len(news) < 0:
                return_body = {
                    'success': 1,
                    'msg': "didnt get news",
                    'keywords': None
                }
                return return_body
            s = SnowNLP(news)
            keywords = s.keywords()  # return 5 key words
            tags = set([tag for tag in s.tags])
            word_tag_dict = {}
            for word in keywords:
                for tag in tags:
                    if word == tag[0]:
                        word_tag_dict[word] = word_tag_dict.get(word, []) + [tag[1]]
                    else:
                        pass
            return_body = {
                'success': 1,
                'msg': "ok",
                'keywords': word_tag_dict,
            }
            return return_body

        if cate:
            pass
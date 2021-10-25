import os
import time

from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt


class WordCloudPic:
    def __init__(self, mongo, font_path, pic_path):
        self.mongo = mongo
        self.font_path = font_path
        self.pic_path = pic_path

    def get_word_cloud_pic(self, **kwargs):
        start_timestap = kwargs.get("start_timestamp")
        end_timestamp = kwargs.get("end_timestamp")
        if not start_timestap:
            ts = time.time()
            start_timestap = ts - ts % 86400
            # start_timestap = 1533139200
        if not end_timestamp:
            ts = time.time()
            end_timestamp = ts - ts % 86400 - 86400
            # end_timestamp = 1533052800
        path = self.pic_path
        if not path:
            return "Exception: need photo path"
        if not os.path.exists(path):
            return "Exception: path not found"
        pic_name = "%s-word-cloud.png" % start_timestap
        if os.path.exists(path=path + pic_name):
            return_pak = {
                'success': 1,
                "word_cloud_src": path + pic_name
            }
            return return_pak
        else:
            db = self.mongo.connection("ai_block_chain_crawler")
            cursor = db["eight_bit"].find({"timestamp": {"$gt": end_timestamp, "$lt": start_timestap}})
            contents = []
            for item in cursor:
                if item.get("data").get("content"):
                    contents.append(item.get("data").get("content"))
            articles = "。".join(contents)
            wordlist = jieba.cut(articles)
            wl = " ".join(wordlist)
            wc = WordCloud(background_color="white", width=800, height=600, font_path=self.font_path, max_font_size=200, random_state=30)
            myword = wc.generate(wl)
            plt.imshow(myword)
            plt.axis("off")
            plt.savefig(path + pic_name)
            return_pak = {
                'success': 1,
                "word_cloud_src": path + pic_name
            }
            return return_pak




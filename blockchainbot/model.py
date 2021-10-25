from . import es

from blockchainbot.kernel.qapairs import QAPairs
from blockchainbot.kernel.get_keywords import Keywords
from blockchainbot.kernel.get_news import News
from blockchainbot.kernel.get_summary import Summary
from blockchainbot.kernel.knowledge import Knowledge
from blockchainbot.kernel.coinsbar import CoinsBar
from blockchainbot.kernel.split_text import SplitText
from blockchainbot.kernel.get_word_cloud import WordCloudPic
from blockchainbot.kernel.get_price import CoinPrice

from blockchainbot.const import TS_TOKEN
from blockchainbot.const import IDC_PHOTO_DIR
from blockchainbot.const import MONGODB_HOST, MONGODB_PORT, MONGODB_PWD, MONGODB_USER, BI_MONGODB_HOST, BI_MONGODB_PORT, FONT_PATH

from blockchainbot.utils.mongo import Mongo

mongo = Mongo(host=MONGODB_HOST, port=MONGODB_PORT, user=MONGODB_USER, pwd=MONGODB_PWD)
mongo_block_info = Mongo(host=BI_MONGODB_HOST, port=BI_MONGODB_PORT)

qapairs = QAPairs(es)
keywords = Keywords(es=es)
news = News(es=es)
summary = Summary(es=es)
knowledge = Knowledge(es=es)
coinsbar = CoinsBar(ts_token=TS_TOKEN, mongo=mongo, pic_path=IDC_PHOTO_DIR)
coin_price = CoinPrice(mongo=mongo_block_info)
split_text = SplitText()
word_cloud = WordCloudPic(mongo=mongo_block_info, font_path=FONT_PATH, pic_path=IDC_PHOTO_DIR)

#from blockchainbot.kernel.test import A; a = A()
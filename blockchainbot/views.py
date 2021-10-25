from flask import jsonify
from flask import request
from flask import Blueprint

from blockchainbot import app

# 这里填入实现的类import，如下,model里声明实例
from blockchainbot.const import BLOCK_INFO_INDEX, BLOCK_INFO_DOC_TYPE
from blockchainbot.const import BLOCK_QA_PAIR_INDEX, BLOCK_KNOWLEDGE_INDEX
from blockchainbot.model import qapairs, keywords, news, summary, knowledge, coinsbar, split_text, word_cloud, coin_price



bc_view = Blueprint('bc_view', __name__)


# 测试路由
@bc_view.route('/', methods=['GET'])
def test():
	print(request.args)
	return jsonify({'test': 'blockchainbot', 'cuid': request.args.get('cuid', 'default'), 'args': request.args})



@bc_view.route('/api/v1/bc/news/keywords', methods=['GET'])
def get_news_keywords():
	decode_type = app.config.get('DECODE_TYPE', 'utf-8')
	data_news = request.data.decode(decode_type)
	if len(data_news) <= 0:
		return jsonify({'success': -1, 'msg': 'no news'})
	else:
		result = keywords.get_keywords(news=data_news)
		return jsonify(result)

@bc_view.route('/api/v1/bc/keywords', methods=['GET'])
def get_keywords():
	decode_type = app.config.get('DECODE_TYPE', 'utf-8')
	data_text = request.data.decode(decode_type)
	if len(data_text) <= 0:
		return jsonify({'success': -1, 'msg': 'no input'})
	else:
		result = split_text.do_it(text=data_text)
		return jsonify(result)

@bc_view.route('/api/v1/bc/summary', methods=['GET'])
def get_summary():
	decode_type = app.config.get('DECODE_TYPE', 'utf-8')
	data_news = request.data.decode(decode_type)
	if len(data_news) <= 0:
		return jsonify({'success': -1, 'msg': 'no news'})
	else:
		result = summary.get_summary(news=data_news, index=BLOCK_INFO_INDEX, doc_type=BLOCK_INFO_DOC_TYPE)
		return jsonify(result)

@bc_view.route('/api/v1/bc/sentence', methods=['GET'])
def get_sentence():
	qlist = request.args.get('keywords', '').split()
	if len(qlist) <= 0:
		return jsonify({'success': -1, 'msg': 'no keywords'})
	else:
		kws_str = "".join(qlist)
		result = summary.get_summary(news=data_news, index=BLOCK_INFO_INDEX, doc_type=BLOCK_INFO_DOC_TYPE)
		return jsonify(result)

@bc_view.route('/api/v1/bc/news', methods=['GET'])
def get_news():
	qlist = request.args.get('keywords', '').split()
	if len(qlist) <= 0:
		return jsonify({'success': -1, 'msg': 'no keywords'})
	else:
		result = news.get_news(kws=qlist, index=BLOCK_INFO_INDEX, doc_type=BLOCK_INFO_DOC_TYPE)
		return jsonify(result)


@bc_view.route('/api/v1/bc/qapairs', methods=['GET'])
def get_qapairs():
	qlist = request.args.get('qkeywords', '').split()  # 问题关键字列表
	if len(qlist) <= 0:
		return jsonify({'success': -1, 'msg': 'no keywords'})
	else:
		qa_pak = qapairs.que_query(keywords=qlist, index=BLOCK_QA_PAIR_INDEX)
		return jsonify(qa_pak)      # 返回数据,字典就是返回的json串


@bc_view.route('/api/v1/bc/knowledge', methods=['GET'])
def get_knowledge():
	qlist = request.args.get('questions', '').split()  # 问题关键字列表
	if len(qlist) <= 0:
		return jsonify({'success': 1, 'msg': 'no questions'})
	else:
		knowledge_pak = knowledge.query(questions=qlist, index=BLOCK_KNOWLEDGE_INDEX)
		return jsonify(knowledge_pak)



@bc_view.route('/api/v1/bc/trend', methods=['GET'])
def get_trend():
	coin = request.args.get('coin', '')
	if len(coin) <= 0:
		return jsonify({'success': 0, 'msg': 'no coin'})
	else:
		coin_trend_pak = coinsbar.get_trend(coin=coin)
		return jsonify(coin_trend_pak)



@bc_view.route('/api/v1/bc/price', methods=['GET'])
def get_price():
	coin = request.args.get('coin', '')
	if len(coin) <= 0:
		return jsonify({'success': 0, 'msg': 'no coin'})
	else:
		coin_price_pak = coin_price.get_average_price(coin=coin, database="block_chain_basedata", table="exchange_pairs")
		return jsonify(coin_price_pak)


@bc_view.route('/api/v1/bc/coin/<coin>', methods=['GET'])
def get_coin_all(coin):
	#coin = request.args.get('coin', '')
	if not coin:
		return jsonify({'success': 0, 'msg': 'no coin'})
	else:
		price = request.args.get('price', True) != 'False'
		trend = request.args.get('trend', True) != 'False'
		trend_pic = request.args.get('trend_pic', True) != 'False'
		coin_pak = coinsbar.query(coin=coin, price=price, trend=trend, trend_pic=trend_pic)
		return jsonify(coin_pak)



@bc_view.route('/api/v1/bc/wordcloud', methods=['GET'])
def get_wordcloud():
	word_cloud_pak = word_cloud.get_word_cloud_pic()
	return jsonify(word_cloud_pak)
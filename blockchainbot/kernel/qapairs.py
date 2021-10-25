import random
from datetime import datetime

class QAPairs:
	def __init__(self, es):
		self.es = es

	def _kw_query(self, **kwargs):
		kws = kwargs.get('keywords', None)
		if not kws:
			return 'no keywords'
		field = kwargs.get('field', None)
		if not isinstance(field, str):
			return 'wrong search field type: {}'.format(type(field))
		idx = kwargs.get('index', None)
		if not isinstance(idx, str):
			return 'not specify index'
		es = kwargs.get('es', None)
		if not es:
			es = self.es

		random.seed(datetime.now())
		kw = random.choice(kws)
		body = {
			"sort": {
				"_score": "desc"
			},
			"query": {
				#"multi_match": {
				"match": {
					field: kw,
				}
			},
			"size": 5,
		}
		result = es.search(index=idx, body=body)
		qapairs = result['hits']['hits']
		if len(qapairs) <= 0:
			qa_pak = {'success': -1, 'msg': "cannot find news by kw:{}".format(kw)}
		else:
			qa = qapairs[0]['_source']
			qa_pak = {'success': 0, 'qapairs': qa}
		return qa_pak

	def que_query(self, **kwargs):
		return self._kw_query(field='question', **kwargs)

	def ans_query(self, **kwargs):
		return self._kw_query(field='answer', **kwargs)

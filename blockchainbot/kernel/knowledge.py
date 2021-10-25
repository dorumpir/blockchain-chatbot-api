import random
from datetime import datetime
from functools import reduce

class Knowledge:
	def __init__(self, es):
		self.es = es

	def _field_query(self, **kwargs):
		questions = kwargs.get('questions', None)
		if not questions:
			return 'no questions'
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
		question = random.choice(questions)
		body = {
			"sort": {
				"_score": "desc"
			},
			"query": {
				#"multi_match": {
				"match": {
					field: question,
				}
			},
			"size": 5,
		}
		result = es.search(index=idx, body=body)
		knowledge_list = result['hits']['hits']
		if len(knowledge_list) <= 0:
			knowledge = "cannot find knowledge by question:{}".format(question)
			knowledge_pak = {'success': 1, 'msg': 'get no match answer from es'}
		else:
			knowledge = knowledge_list[0]['_source']['Answer']
			knowledge_pak = {'success': 0, 'data': knowledge}
		return knowledge_pak

	def _field_multi_query(self, **kwargs):
		keywords = kwargs.get('questions', None)
		if not keywords:
			return 'no questions'
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
		should_phase = [
							{ "match": {
								"Question": {
									"query": keyword,
									#"boost": 3 
								}
							}} 
							for keyword in keywords
					   ]
		body = {
					"sort": {
						"_score": "desc"
					},
					"query": {
						"bool": {
							"should": should_phase,
							#"minimum_should_match": "75%"
						}
					},
					"size": 5,
				}
		result = es.search(index=idx, body=body)
		knowledge_list = result['hits']['hits']
		answer_list = [answer 
						  for answer in 
						  [klg['_source']['Answer'] 
						   for klg in knowledge_list] 
						   if bool(reduce(lambda a, b: a or b, map(lambda w: w.upper() in answer.upper(), keywords)))]
		if len(answer_list) <= 0:
			knowledge = "cannot find knowledge by question:{}".format(keywords)
			knowledge_pak = {'success': 1, 'msg': 'get no match answer from es'}
		else:
			knowledge_pak = {'success': 0, 'data': answer_list}
		return knowledge_pak


	def query(self, **kwargs):
		return self._field_multi_query(field='Question', **kwargs)

"""
{
	"sort": {
		"_score": "desc"
	},
	"query": {
		"bool": {
			"should": [
				{ "match": {
					"Question": {
						"query": "tvt",
						"boost": 3 
					}
				}},
				{ "match": {
					"Question": {
						"query": "btc",
						"boost": 2 
					}
				}}
			],
			"minimum_should_match": "75%"
		}
	},
	"size": 5,
}



{
  "query": {
	"bool": {
	  "should": [
		{ "match": { "title": "brown" }},
		{ "match": { "title": "fox"   }},
		{ "match": { "title": "dog"   }}
	  ],
	  "minimum_should_match": 2 
	}
  }
}



{
	"sort": {
		"_score": "desc"
	},
	"query": {
		"match": {
			field: question,
		}
	},
	"size": 5,
}

"""
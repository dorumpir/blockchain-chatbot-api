import jieba

from ..const import JIEBA_WORD_DICT,JIEBA_WORD_DICTNEW


class SplitText:
	def __init__(self):
		jieba.load_userdict(str(JIEBA_WORD_DICTNEW))
		self.word_dict = self._get_dict(str(JIEBA_WORD_DICT))

	def _get_dict(self, dict_path=''):
		'''
		获取区块链字典
		'''
		word_dict = []
		with open(dict_path, 'r', encoding='utf-8-sig') as f:
			for line in f:
				word_dict.append(line.strip('\n').split()[0].split('\ufeff')[-1])
		return set(word_dict)

	def do_it(self, text=''):
		text = text.upper()
		kws_set = set(jieba.cut(text))
		bc_kws_set = set(kws_set & set(self.word_dict))
		kws_pak = {
			'success': 0,
			'keywords': list(kws_set),
			'bc_keywords': list(bc_kws_set),
		}
		return kws_pak

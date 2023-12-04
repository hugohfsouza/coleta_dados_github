import requests
import json
from PRAnalizer import PRAnalizer


from unittest import TestCase

class TryTesting(TestCase):

	def retornaJson(self, link):
		headers = {'Authorization': 'token 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', 'Accept': 'application/vnd.github.v3+json'}
		response = requests.get(link, headers=headers)

		for arquivo in json.loads(response.text):
			linkDocumentoCompleto = arquivo['raw_url']
			itensAlterados = arquivo['patch']
			aux = itensAlterados.split("\n");	

			analizer = PRAnalizer("Python")
			dadosDoPR  = analizer.retornaEstrutura();

			for item in aux:
				if(analizer.checkIfModifier(item.strip())):
					result 			= analizer.verify(item.strip())
					modifierType 	= analizer.checkModifierType(item.strip())
					dadosDoPR[result][modifierType] += 1
					dadosDoPR['all'][modifierType] += 1


		return dadosDoPR

	def test_always_passes(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/pandas-dev/pandas/pulls/38758/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 0, 'others': 0}, 'tests': {'removed': 0, 'added': 0, 'others': 0}, 'class': {'removed': 0, 'added': 0, 'others': 0}, 'code': {'removed': 25, 'added': 2, 'others': 0}, 'imports': {'removed': 4, 'added': 1, 'others': 0}, 'comments': {'removed': 6, 'added': 0, 'others': 0}, 'whiteLines': {'removed': 2, 'added': 0, 'others': 0}, 'all': {'removed': 37, 'added': 3, 'others': 0}})

	def test_002(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/pandas-dev/pandas/pulls/39785/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 0, 'others': 0}, 'tests': {'removed': 2, 'added': 2, 'others': 0}, 'class': {'removed': 0, 'added': 0, 'others': 0}, 'code': {'removed': 51, 'added': 65, 'others': 0}, 'imports': {'removed': 0, 'added': 0, 'others': 0}, 'comments': {'removed': 0, 'added': 0, 'others': 0}, 'whiteLines': {'removed': 4, 'added': 0, 'others': 0}, 'all': {'removed': 57, 'added': 67, 'others': 0}})

	def test_003(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/home-assistant/core/pulls/28449/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 0, 'others': 0}, 'tests': {'removed': 0, 'added': 0, 'others': 0}, 'class': {'removed': 0, 'added': 0, 'others': 0}, 'code': {'removed': 6, 'added': 6, 'others': 0}, 'imports': {'removed': 0, 'added': 0, 'others': 0}, 'comments': {'removed': 0, 'added': 0, 'others': 0}, 'whiteLines': {'removed': 0, 'added': 0, 'others': 0}, 'all': {'removed': 6, 'added': 6, 'others': 0}})

	def test_004(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/python/cpython/pulls/28175/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 24, 'others': 0}, 'tests': {'removed': 0, 'added': 46, 'others': 0}, 'class': {'removed': 0, 'added': 8, 'others': 0}, 'code': {'removed': 0, 'added': 52, 'others': 0}, 'imports': {'removed': 0, 'added': 0, 'others': 0}, 'comments': {'removed': 0, 'added': 0, 'others': 0}, 'whiteLines': {'removed': 0, 'added': 8, 'others': 0}, 'all': {'removed': 0, 'added': 138, 'others': 0}})

	def test_005(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/tensorflow/hub/pulls/115/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 0, 'others': 0}, 'tests': {'removed': 0, 'added': 0, 'others': 0}, 'class': {'removed': 0, 'added': 0, 'others': 0}, 'code': {'removed': 0, 'added': 1, 'others': 0}, 'imports': {'removed': 0, 'added': 0, 'others': 0}, 'comments': {'removed': 0, 'added': 1, 'others': 0}, 'whiteLines': {'removed': 0, 'added': 1, 'others': 0}, 'all': {'removed': 0, 'added': 3, 'others': 0}})

	def test_006(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/stamparm/maltrail/pulls/6801/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 0, 'others': 0}, 'tests': {'removed': 0, 'added': 0, 'others': 0}, 'class': {'removed': 0, 'added': 0, 'others': 0}, 'code': {'removed': 0, 'added': 2, 'others': 0}, 'imports': {'removed': 0, 'added': 0, 'others': 0}, 'comments': {'removed': 0, 'added': 1, 'others': 0}, 'whiteLines': {'removed': 0, 'added': 2, 'others': 0}, 'all': {'removed': 0, 'added': 5, 'others': 0}})

	def test_007(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/ZiniuLu/Python-100-Days/pulls/22/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 0, 'others': 0}, 'tests': {'removed': 0, 'added': 0, 'others': 0}, 'class': {'removed': 0, 'added': 0, 'others': 0}, 'code': {'removed': 0, 'added': 4, 'others': 0}, 'imports': {'removed': 0, 'added': 0, 'others': 0}, 'comments': {'removed': 0, 'added': 0, 'others': 0}, 'whiteLines': {'removed': 0, 'added': 3, 'others': 0}, 'all': {'removed': 0, 'added': 7, 'others': 0}})

	def test_007(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/ZiniuLu/Python-100-Days/pulls/23/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 0, 'others': 0}, 'tests': {'removed': 0, 'added': 0, 'others': 0}, 'class': {'removed': 0, 'added': 0, 'others': 0}, 'code': {'removed': 0, 'added': 8, 'others': 0}, 'imports': {'removed': 0, 'added': 0, 'others': 0}, 'comments': {'removed': 0, 'added': 3, 'others': 0}, 'whiteLines': {'removed': 0, 'added': 8, 'others': 0}, 'all': {'removed': 0, 'added': 19, 'others': 0}})

	def test_008(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/tensorflow/hub/pulls/16/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 0, 'others': 0}, 'tests': {'removed': 0, 'added': 0, 'others': 0}, 'class': {'removed': 0, 'added': 0, 'others': 0}, 'code': {'removed': 0, 'added': 4, 'others': 0}, 'imports': {'removed': 0, 'added': 0, 'others': 0}, 'comments': {'removed': 0, 'added': 0, 'others': 0}, 'whiteLines': {'removed': 0, 'added': 0, 'others': 0}, 'all': {'removed': 0, 'added': 4, 'others': 0}})

	def test_009_alterando_json(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/StevenBlack/hosts/pulls/1095/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 0, 'others': 0}, 'tests': {'removed': 0, 'added': 0, 'others': 0}, 'class': {'removed': 0, 'added': 0, 'others': 0}, 'code': {'removed': 4, 'added': 4, 'others': 0}, 'imports': {'removed': 0, 'added': 0, 'others': 0}, 'comments': {'removed': 0, 'added': 0, 'others': 0}, 'whiteLines': {'removed': 0, 'added': 0, 'others': 0}, 'all': {'removed': 4, 'added': 4, 'others': 0}})

	def test_010_alterando_um_monte_de_testes_no_mesmo_arquivo(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/blaze/blaze/pulls/112/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 0, 'others': 0}, 'tests': {'removed': 15, 'added': 22, 'others': 0}, 'class': {'removed': 0, 'added': 0, 'others': 0}, 'code': {'removed': 1, 'added': 7, 'others': 0}, 'imports': {'removed': 0, 'added': 1, 'others': 0}, 'comments': {'removed': 3, 'added': 5, 'others': 0}, 'whiteLines': {'removed': 0, 'added': 0, 'others': 0}, 'all': {'removed': 19, 'added': 35, 'others': 0}})

	def test_alterou_um_arquivo_de_teste_sem_adicionar_ou_remover_um_teste(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/statsmodels/statsmodels/pulls/2997/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 0, 'others': 0}, 'tests': {'removed': 0, 'added': 0, 'others': 0}, 'class': {'removed': 0, 'added': 0, 'others': 0}, 'code': {'removed': 12, 'added': 6, 'others': 0}, 'imports': {'removed': 3, 'added': 2, 'others': 0}, 'comments': {'removed': 0, 'added': 0, 'others': 0}, 'whiteLines': {'removed': 3, 'added': 0, 'others': 0}, 'all': {'removed': 18, 'added': 8, 'others': 0}})

	def test_adicionou_uma_classe_inteira_de_testes(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/saltstack/salt/pulls/19952/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 1, 'others': 0}, 'tests': {'removed': 0, 'added': 1, 'others': 0}, 'class': {'removed': 0, 'added': 1, 'others': 0}, 'code': {'removed': 0, 'added': 18, 'others': 0}, 'imports': {'removed': 0, 'added': 5, 'others': 0}, 'comments': {'removed': 0, 'added': 3, 'others': 0}, 'whiteLines': {'removed': 0, 'added': 6, 'others': 0}, 'all': {'removed': 0, 'added': 35, 'others': 0}} )

	def test_arquivo_completo_com_dois_asserts_apenas(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/pandas-dev/pandas/pulls/42989/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 1, 'others': 0}, 'tests': {'removed': 0, 'added': 2, 'others': 0}, 'class': {'removed': 0, 'added': 0, 'others': 0}, 'code': {'removed': 0, 'added': 438, 'others': 0}, 'imports': {'removed': 0, 'added': 0, 'others': 0}, 'comments': {'removed': 0, 'added': 4, 'others': 0}, 'whiteLines': {'removed': 0, 'added': 3, 'others': 0}, 'all': {'removed': 0, 'added': 448, 'others': 0}})

	def test_movimentou_os_testes_de_arquivo(self):
		dadosDoPR = self.retornaJson('https://api.github.com/repos/pandas-dev/pandas/pulls/43218/files')
		self.assertTrue(dadosDoPR == {'functions': {'removed': 0, 'added': 1, 'others': 0}, 'tests': {'removed': 0, 'added': 0, 'others': 0}, 'class': {'removed': 0, 'added': 0, 'others': 0}, 'code': {'removed': 0, 'added': 14, 'others': 0}, 'imports': {'removed': 0, 'added': 0, 'others': 0}, 'comments': {'removed': 0, 'added': 1, 'others': 0}, 'whiteLines': {'removed': 0, 'added': 2, 'others': 0}, 'all': {'removed': 0, 'added': 18, 'others': 0}})
import sqlite3
import configparser
import requests
import json
import time


config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

limiteInferior 	= config.get("GERAL", "limiteMaximoAntesDePararOsRequests")
tempoEspera 	= config.get("GERAL", "tempoEsperaProximaValidacaoToken")

class GithubConsumer:
	def __init__(self):
		self.connection = sqlite3.connect(config.get("SQLITE", "nomeArquivo"))
		self.cursor = self.connection.cursor()

	def getToken(self):
		sql = """
			SELECT token 
			FROM tokens 
			where requisicoes_restantes >= :limite
			order by requisicoes_restantes desc
			limit 1
			"""
		res = self.cursor.execute(sql, {"limite":limiteInferior })
		data = res.fetchone()
		if(data):
			return {
				'token': data[0],
				'espera': 0
			}
		else:
			return {
				'token': '',
				'espera': int(tempoEspera)
			}

	def requisitarGithub(self, urlBase):
		
		verificaToken = True
		while(verificaToken):
			dadosToken = self.getToken()
			if(dadosToken['espera'] != 0):
				time.sleep(dadosToken['espera'])
			else:
				verificaToken = False

		token = dadosToken['token']

		pagina = 1
		url = urlBase+"?per_page=100&page="+str(pagina)
		response = requests.get(url, headers={'Authorization': token, 'Accept': 'application/vnd.github.v3+json'})
		result = json.loads(response.text)
		listaArquivosPR = []

		while(len(result) > 0 and (not 'errors' in result) ):
			for file in result:
				listaArquivosPR.append(file)

			if(len(result) == 100):
				pagina += 1
				url = urlBase+"?per_page=100&page="+str(pagina)
				response = requests.get(url, headers={'Authorization': token, 'Accept': 'application/vnd.github.v3+json'})
				result = json.loads(response.text)
			else:
				result = []

		return listaArquivosPR


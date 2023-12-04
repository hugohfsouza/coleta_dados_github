import sqlite3
import configparser
import requests
import json
import time
import os

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

limiteInferior 	= config.get("GERAL", "limiteMaximoAntesDePararOsRequests")
tempoEspera 	= int(config.get("GERAL", "tempoEsperaProximaValidacaoToken"))

class ArquivosJson:
	def __init__(self):
		pass

	def salvar(self, pr_id, json, pasta):
		nomeArquivo = str(pr_id)+'.txt'
		caminho_completo = os.path.join(pasta, nomeArquivo)
		with open(caminho_completo, 'w') as arquivo:
			arquivo.write(json)


	def recuperar(self, pr_id, pasta):
		nomeArquivo = str(pr_id)+'.txt'
		caminho_completo = os.path.join(pasta, nomeArquivo)

		with open(caminho_completo, 'r') as arquivo:
			conteudo = arquivo.read()
			json_lido = json.loads(conteudo)
		return json_lido
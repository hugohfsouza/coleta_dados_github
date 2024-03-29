import requests
import json
import time
import sqlite3
from os import system
import datetime
import os
import configparser


config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

if os.path.exists(config.get("SQLITE", "nomeArquivo")):
  os.remove(config.get("SQLITE", "nomeArquivo"))

con = sqlite3.connect(config.get("SQLITE", "nomeArquivo"))
cur = con.cursor()
cur.execute('''CREATE TABLE tokens (token text, requisicoes_restantes int)''')

tokens = []
configuracao  = config.items("TOKENS")
for x in configuracao:
	tokens.append(x[1])
	cur.execute("INSERT INTO tokens VALUES ('"+str(x[1])+"',0)")
con.commit()

limiteMaximo 		= int(config.get("GERAL", "limiteMaximoAntesDePararOsRequests"))
limiteMaximo_search = int(config.get("GERAL", "limiteMaximoAntesDePararOsRequestsSearch"))


def diff_minutes(timestamp):
	now = datetime.datetime.now()
	dt_timestamp = datetime.datetime.fromtimestamp(timestamp)
	diff = (dt_timestamp - now).total_seconds() // 60
	return diff

def verificarUsoApiGithub():
	totalDisponivel = 0
	for token in tokens:
		headers = {'Authorization': token, 'Accept': 'application/vnd.github.v3+json'}
		url = "https://api.github.com/rate_limit"
		response = requests.get(url, headers=headers)
		y = json.loads(response.text)
		sql = "UPDATE tokens set requisicoes_restantes = " + str(0) + " where token = '" + str(token) + "'";

		if response.status_code == 200:
			sql = "UPDATE tokens set requisicoes_restantes = "+str(y["resources"]["core"]['remaining'])+" where token = '"+str(token)+"'";
			print(str(y["resources"]["core"]['remaining']) + " - Resentando em: "+ str(diff_minutes(y["resources"]["core"]['reset'])))
			totalDisponivel += y["resources"]["core"]['remaining']
		else:
			print("Erro ao consultar limites")

		cur.execute(sql)
		con.commit()
	print("Total Disponivel:" + str(totalDisponivel))
		


while(True):
	verificarUsoApiGithub()
	print("")
	time.sleep(20)
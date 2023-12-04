import requests
import json
import time
import sqlite3
from os import system
import os
import configparser
from datetime import datetime

system("title Check Requests Limits in GITHUB")

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




def verificarUsoApiGithub():
	for token in tokens:
		headers = {'Authorization': token, 'Accept': 'application/vnd.github.v3+json'}
		url = "https://api.github.com/rate_limit"
		response = requests.get(url, headers=headers)
		y = json.loads(response.text)
		
		if('message' in y):
			print(token+" "+y['message'])
		else:
			date_time = datetime.fromtimestamp(y["resources"]["core"]['reset'])
			d = date_time.strftime("%X")

			sql = "UPDATE tokens set requisicoes_restantes = "+str(y["resources"]["core"]['remaining'])+" where token = '"+str(token)+"'";

			print(token+"  "+str(y["resources"]["core"]['remaining']) + " resetando em: "+ str(d))

			cur.execute(sql)
			con.commit()
			


while(True):
	verificarUsoApiGithub()
	print("")
	time.sleep(20)
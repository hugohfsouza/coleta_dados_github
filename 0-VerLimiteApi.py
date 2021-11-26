import requests
import json
import time
import mysql.connector
from datetime import datetime
from os import system
import configparser

system("title Verifica Limites de Requests no GITHUB")

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


tokens = []
configuracao  = config.items("TOKENS")
for x in configuracao:
	tokens.append(x[1])

limiteMaximo 		= int(config.get("GERAL", "limiteMaximoAntesDePararOsRequests"))
limiteMaximo_search = int(config.get("GERAL", "limiteMaximoAntesDePararOsRequestsSearch"))

dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(pool_name = "mypool", pool_size = 1,**dbconfig)
cursor = conn.cursor();

def setStatusRequestV2(status, token):
        cursor.execute("""UPDATE startstop set continuar = %s where token like %s""", (status, token,) )
        conn.commit()

def setStatusRequestSearch(status, token):
        cursor.execute("""UPDATE startstop set continuarSearch = %s where token like %s""", (status, token,) )
        conn.commit()

def verificarExistenciaDeTokensNaBase(tokens):
	for token in tokens:
		cursor.execute("""SELECT 1 from startstop where token like %s""", (token,))
		if(not cursor.fetchone()):
			cursor.execute("""INSERT INTO startstop(token, continuar) VALUES (%s,0)""", (token,) )
			conn.commit()


def verificarUsoApiGithub():
	for token in tokens:
		headers = {'Authorization': token, 'Accept': 'application/vnd.github.v3+json'}
		url = "https://api.github.com/rate_limit"
		response = requests.get(url, headers=headers)
		y = json.loads(response.text)


		if(y["resources"]["core"]['remaining'] < limiteMaximo):
			setStatusRequestV2(0, token)
		else:
			setStatusRequestV2(1, token)


		if(y["resources"]["search"]['remaining'] < limiteMaximo_search):
			setStatusRequestSearch(0, token)
		else:
			setStatusRequestSearch(1, token)

		dt_object = datetime.fromtimestamp(y["resources"]["core"]['reset'])
		dt_object_search = datetime.fromtimestamp(y["resources"]["search"]['reset'])
		print("[R.N] "+str(y["resources"]["core"]['remaining']) + " [Reset] "+str(dt_object) )
		print("[R.S] "+str(y["resources"]["search"]['remaining']) + " [Reset] "+str(dt_object_search) )



verificarExistenciaDeTokensNaBase(tokens)

while(True):
	verificarUsoApiGithub()
	print("")
	time.sleep(2)
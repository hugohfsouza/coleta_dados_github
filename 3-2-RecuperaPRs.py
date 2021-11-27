import requests
import json
import time
import configparser
import math
import mysql.connector
import sys
from GetStatus import GetStatus
import pika

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


# CONFIGURAÇÕES DE FILA E TOKEN
tempoEspera 	= int(config.get("GERAL", "tempoEsperaSearch"))
token 			= config.get("TOKENS", sys.argv[1])
nomeFila 		= config.get("FILAS", "nomeFilaRecuperaPRs")

# CONFIGURAÇÕES GERAIS
headers = {'Authorization': token, 'Accept': 'application/vnd.github.v3+json'}
status	= GetStatus();

# CONFIGURAÇÃO DE FILAS
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=nomeFila, durable=True)


# CONFIGURAÇÃO BANCO
dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}
conn = mysql.connector.connect(pool_name = "verifica_testes", pool_size = 1,**dbconfig)
cursor = conn.cursor();


def registrarPRsEncontrados(repo_id):
	cursor.execute("""UPDATE repositorios set prs_recuperados = 1 where id = %s""", (repo_id,) )
	conn.commit()

def salvarPR(repo_id, number, state, url, user, created_at, updated_at, closed_at, merged_at):
	cursor.execute(
		"""
			INSERT INTO 
				pull_requests 
					(
						repo_id, 
						number, 
						state, 
						url, 
						user, 
						created_at, 
						updated_at,
						closed_at,
						merged_at
					)
				VALUES 
					( %s, %s, %s, %s, %s, %s, %s, %s, %s);


		""", (repo_id, number, state, url, user, created_at, updated_at, closed_at, merged_at) )
	conn.commit()

def requisitarGithub(url, headerExtra=None):
	while(True):

		if(status.getStatusRequest(token)['continuarSearch'] == 1):
			break
		else:
			print("esperando proxima janela")
			time.sleep(tempoEspera)

	url = "https://api.github.com/"+str(url)
	while(True):
		response = requests.get(url, headers=headers)
		if(response.status_code == 200 or response.status_code == 404 or response.status_code == 422):
			break
		else:
			print("["+str(response.status_code)+"]tempo espera request")
			time.sleep(tempoEspera)
	return json.loads(response.text)


def buscarPrs(repo):
	pagina = 1

	result = requisitarGithub("repos/"+str(repo['nameWithOwner'])+"/pulls?state=all&sort=created&direction=desc&per_page=100&page="+str(pagina))
	while(len(result) > 0):
		for pr in result:
			try:
				salvarPR(
					repo['id'], 
					pr['number'], 
					pr['state'], 
					pr['url'],
					pr['user']['login'], 
					pr['created_at'], 
					pr['updated_at'],
					pr['closed_at'],
					pr['merged_at']
				)
			except Exception as e:
				pass
				
		pagina += 1
		result = requisitarGithub("repos/"+str(repo['nameWithOwner'])+"/pulls?state=all&sort=created&direction=desc&per_page=100&page="+str(pagina))
		print("["+str(repo['nameWithOwner'])+"] pagina: "+str(pagina))

	registrarPRsEncontrados(repo['id'])
	print("["+str(repo['nameWithOwner'])+"] CONCLUIDO ")
	pass


def callback(ch, method, properties, body):	
	print(" [x] Received %r" % body.decode())
	print(" [x] Done")

	ch.basic_ack(delivery_tag=method.delivery_tag)
	jsonResponse = json.loads(body.decode())
	buscarPrs(jsonResponse)
	


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=nomeFila, on_message_callback=callback)
channel.start_consuming()
print("Esperando novos itens")


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



#  python .\3-2-RecuperaPRs.py token1
#  python .\3-2-RecuperaPRs.py token2
#  python .\3-2-RecuperaPRs.py token3
#  python .\3-2-RecuperaPRs.py token4
#  python .\3-2-RecuperaPRs.py token5
#  python .\3-2-RecuperaPRs.py token6
#  python .\3-2-RecuperaPRs.py token7
#  python .\3-2-RecuperaPRs.py token8
#  python .\3-2-RecuperaPRs.py token9
#  python .\3-2-RecuperaPRs.py token10
#  python .\3-2-RecuperaPRs.py token11
#  python .\3-2-RecuperaPRs.py token12


# CONFIGURAÇÕES GERAIS
headers = {'Authorization': token, 'Accept': 'application/vnd.github.v3+json'}
status	= GetStatus();




# CONFIGURAÇÃO BANCO
dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}
conn = mysql.connector.connect(**dbconfig)
# conn = mysql.connector.connect(pool_name = "verifica_testes"+str(sys.argv[1]), pool_size = 5,**dbconfig)
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

def salvarPRBulk(dados):
	cursor.executemany(
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


		""", (dados) )
	conn.commit()

def requisitarGithub(url, headerExtra=None):

	while(True):

		if(status.getStatusRequest(token)['continuar'] == 1):
			print('parou no primeiro')
			break
		else:
			print("esperando proxima janela")
			time.sleep(tempoEspera)

	url = "https://api.github.com/"+str(url)
	print(url)
	while(True):
		print('requisitando')
		response = requests.get(url, headers=headers)
		if(response.status_code == 200 or response.status_code == 404 or response.status_code == 422):
			print('resposta valida')
			break
		else:
			print("["+str(response.status_code)+"]tempo espera request")
			time.sleep(tempoEspera)
	return json.loads(response.text)


def buscarPrs(repo):

	print('iniciando os requests')
	pagina = 1

	result = requisitarGithub("repos/"+str(repo['nameWithOwner'])+"/pulls?state=all&sort=created&direction=desc&per_page=100&page="+str(pagina))
	print('iniciando inserção das prs no banco')
	while(len(result) > 0):
		dados = []
		print('inserindo')
		for pr in result:
			dados.append([repo['id'], 
				pr['number'], 
				pr['state'], 
				pr['url'],
				pr['user']['login'], 
				pr['created_at'], 
				pr['updated_at'],
				pr['closed_at'],
				pr['merged_at']
			])

		try:
			salvarPRBulk(
				dados
			)
		except Exception as e:
			print("erro ao salvar")
			print(e)
				
		pagina += 1
		result = requisitarGithub("repos/"+str(repo['nameWithOwner'])+"/pulls?state=all&sort=created&direction=desc&per_page=100&page="+str(pagina))
		print("["+str(repo['nameWithOwner'])+"] pagina: "+str(pagina))

	print('terminou a inserção')
	registrarPRsEncontrados(repo['id'])
	print('registrei como PR encontrado')

	print("["+str(repo['nameWithOwner'])+"] CONCLUIDO ")
	pass


def callback(ch, method, properties, body):	
	print(" [x] Received %r" % body.decode())
	print(" [x] Done")

	ch.basic_ack(delivery_tag=method.delivery_tag)
	jsonResponse = json.loads(body.decode())
	print('chamando funcao de recuperar')
	buscarPrs(jsonResponse)

# CONFIGURAÇÃO DE FILAS
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=False))
channel = connection.channel()
channel.queue_declare(queue=nomeFila, durable=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=nomeFila, on_message_callback=callback)
channel.start_consuming()
print("Esperando novos itens")


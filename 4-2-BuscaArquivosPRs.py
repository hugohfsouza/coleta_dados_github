import requests
import json
import time
import configparser
import ctypes
import mysql.connector
import sys
from GetStatus import GetStatus
import pika

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


# CONFIGURAÇÕES DE FILA E TOKEN
tempoEspera 	= int(config.get("GERAL", "tempoEsperaSearch"))
token 			= config.get("TOKENS", sys.argv[1])
nomeFila 		= config.get("FILAS", "nomeFilaRecuperaArquivos")

ctypes.windll.kernel32.SetConsoleTitleW(sys.argv[1])

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
conn = mysql.connector.connect(pool_name = "verifica_testes", pool_size = 1,**dbconfig)
cursor = conn.cursor();

def salvarFilesPRBulk(listaItens):

	try:
		sql = "INSERT INTO pull_request_files (pr_id, filename, additions, deletions, sha, status, changes, contents_url, patch) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s);"
		cursor.executemany(sql, listaItens )
		conn.commit()
	except Exception as e:
		print("fazendo um a um")
		try:
			for item in listaItens:
				sql = "INSERT INTO pull_request_files (pr_id, filename, additions, deletions, sha, status, changes, contents_url, patch) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s);"
				cursor.execute(sql, (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]) )
				conn.commit()
		except Exception as ex:
			print(ex)


	

def registraArquivosEncontrados(pullRequest):
    cursor.execute("""UPDATE pull_requests set analisado = 1 where id = %s""", (pullRequest['id'] ,) )
    conn.commit()

def requisitarGithub(url, headerExtra=None):
	while(True):

		if(status.getStatusRequest(token)['continuar'] == 1):
			break
		else:
			print("esperando proxima janela")
			time.sleep(tempoEspera)

	while(True):
		try:
			response = requests.get(url, headers=headers)
			print(url)
			if(response.status_code == 200 or response.status_code == 404 or response.status_code == 422 or response.status_code == 503):
				break
			else:
				print("["+str(response.status_code)+"]tempo espera request")
				time.sleep(tempoEspera)
		except:
			print("erro no request, esperando....")
			time.sleep(tempoEspera)
			pass

	return json.loads(response.text)


def buscarArquivos(pullRequest):
	print("Buscando PR: "+ str(pullRequest['id']))
	pagina = 1
	result = requisitarGithub(str(pullRequest['url'])+"/files?per_page=100&page="+str(pagina))
	
	while(len(result) > 0 and (not 'errors' in result) ):
		listaArquivosPR = []
		# print(pullRequest['id'])

		for file in result:
			patch = "";

			if ('patch' in file):
				patch = file['patch']

			listaArquivosPR.append(
				(
					pullRequest['id'], 
					file['filename'],
					file['additions'],
					file['deletions'],
					file['sha'],
					file['status'],
					file['changes'],
					file['contents_url'],
					patch
				)
			)

		try:
			salvarFilesPRBulk(listaArquivosPR)
		except Exception as e:
			print(e)
			pass
	
		if(len(result) == 100):
			pagina += 1
			result = requisitarGithub(str(pullRequest['url'])+"/files?per_page=100&page="+str(pagina))
		else:
			result = []


	registraArquivosEncontrados(pullRequest)
	pass




def callback(ch, method, properties, body):	
	# print(" [x] Received %r" % body.decode())
	# print(" [x] Done")

	ch.basic_ack(delivery_tag=method.delivery_tag)
	buscarArquivos(json.loads(body.decode()))


# CONFIGURAÇÃO DE FILAS
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=3600))
channel = connection.channel()
channel.queue_declare(queue=nomeFila, durable=True)

# python .\4-2-BuscaArquivosPRs.py token1
	
print("Esperando novos itens")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=nomeFila, on_message_callback=callback)
channel.start_consuming()



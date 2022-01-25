import requests
import json
import time
import configparser
import ctypes
import mysql.connector
import sys
from GetStatus import GetStatus
import pika
import os

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


def salvarDados(pr_id, dados):
	sql = "UPDATE pull_requests SET hasTest = %s, hasCode = %s, hasOutros = %s, qtdArqTest= %s , qtdArqCode= %s , qtdArqOutros= %s , qtdAdditions= %s , qtdDeletions = %s, datetime_analisado = now() where id = %s;"
	cursor.execute(sql, (
		dados['hasTest'],
		dados['hasCode'],
		dados['hasOutros'],
		dados['teste'],
		dados['codigo'],
		dados['outros'],
		dados['adicionadas'],
		dados['removidas'],
		pr_id,
	))
	conn.commit()



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
	listaArquivosPR = []

	while(len(result) > 0 and (not 'errors' in result) ):
		for file in result:
			patch = "";

			if ('patch' in file):
				patch = file['patch']
			try:
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
			except:
				pass
		
		if(len(result) == 100):
			pagina += 1
			result = requisitarGithub(str(pullRequest['url'])+"/files?per_page=100&page="+str(pagina))
		else:
			result = []

	return listaArquivosPR


def processar(pullRequest):

	alteracoes = buscarArquivos(pullRequest)

	extensoesArquivosCodigoTeste = {
		'JAVA': ['.java'],
		'C++': ['.cpp', '.c', '.h', '.hpp'],
		'Javascript': ['.js', '.ejs'],
		'Python': ['.py'],
		'C': ['.cpp', '.c', '.h', '.hpp'],
		'C#': ['.cs'],
		'Ruby': ['.rb'],
	}


	resultado = {
		'codigo': 0,
		'teste' : 0,
		'outros': 0,
		'adicionadas': 0,
		'removidas': 0,

		'hasTest': False,
		'hasCode': False,
		'hasOutros': False
	}

	for item in alteracoes:
		filename, file_extension = os.path.splitext(item[1])
		
		resultado['adicionadas'] += item[2]
		resultado['removidas'] += item[3]

		if(file_extension in extensoesArquivosCodigoTeste[pullRequest['linguagemReferencia']]):
			if('test' in filename or 'test' in item[7]):
				resultado['teste'] += 1
			else:
				resultado['codigo'] += 1

		else:
			resultado['outros'] += 1

	if(resultado['teste'] > 0):
		resultado['hasTest'] = True

	if(resultado['codigo'] > 0):
		resultado['hasCode'] = True

	if(resultado['outros'] > 0):
		resultado['hasOutros'] = True

	# print(resultado)
	salvarDados(pullRequest['id'], resultado)
	registraArquivosEncontrados(pullRequest)



# processar({'id': 1420662, 'url': 'https://api.github.com/repos/cake-build/cake/pulls/420', 'linguagemReferencia': 'C#'})




def callback(ch, method, properties, body):	
	# print(" [x] Received %r" % body.decode())
	# print(" [x] Done")

	ch.basic_ack(delivery_tag=method.delivery_tag)
	processar(json.loads(body.decode()))


# CONFIGURAÇÃO DE FILAS
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=60000))
channel = connection.channel()
channel.queue_declare(queue=nomeFila, durable=True)

# python .\4-3-BuscaArquivosPRsInteligente.py token1
	
print("Esperando novos itens")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=nomeFila, on_message_callback=callback)
channel.start_consuming()



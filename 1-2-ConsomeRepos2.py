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


tempoEspera 	= int(config.get("GERAL", "tempoEsperaSearch"))
token 			= config.get("TOKENS", sys.argv[1])
nomeFila 		= "repos_problematicos"
# linguagemReferencia = "Python"
linguagemReferencia = "Javascript"

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


queryInit = """ 
{
  repository(name: "#name#", owner: "#owner#") {
	id
	name
	nameWithOwner
	url
	isFork
	createdAt
	databaseId
	id
	languages(orderBy: {field: SIZE, direction: DESC}, first: 20) {
	  edges {
		node {
		  name
		}
	  }
	  totalCount
	}
	pullRequests {
	  totalCount
	}
  }
}"""




def requisitarGithub(nomeRepos):

	aux = nomeRepos.split("/")

	query 	= queryInit.replace('#name#', aux[1])
	query 	= query.replace('#owner#', aux[0])

	while(True):
		response = requests.post('https://api.github.com/graphql',json={'query': query}, headers=headers)
		if(response.status_code == 200 or response.status_code == 404 or response.status_code == 422):
			break
		else:
			print("["+str(response.status_code)+"] tempo espera request")
			time.sleep(tempoEspera)

	return response.json()



def insertRepositorio(name, nameWithOwner, createdAt, databaseId, qtdPRs ,languages):
	global conn
	global cursor
	global linguagemReferencia

	novo = False

	try:
		cursor.execute("""INSERT INTO repositorios(
			name, 
			nameWithOwner, 
			createdAt, 
			databaseId,  
			languages, 
			qtdPrs,
			linguagemReferencia) values (%s, %s, %s, %s, %s, %s, %s)""", 
			(name, nameWithOwner, createdAt, databaseId, languages, qtdPRs, linguagemReferencia) )
		conn.commit() 

		novo = True
	except Exception as e:
		pass

	if(novo):
		print("Adicionando repositorio novo")



def buscaInfos(repositorioGithub):
	print(repositorioGithub)

	repo = requisitarGithub(repositorioGithub)
	stringLinguagens = "";

	for linguagem in repo['data']['repository']['languages']['edges']:
		stringLinguagens  += ","+linguagem['node']['name']
	stringLinguagens = stringLinguagens[1:]
		
	insertRepositorio(
		repo['data']['repository']['name'],
		repo['data']['repository']['nameWithOwner'],
		repo['data']['repository']['createdAt'],
		repo['data']['repository']['databaseId'],
		repo['data']['repository']['pullRequests']['totalCount'],
		stringLinguagens
	)






def callback(ch, method, properties, body):	
	print(" [x] Received %r" % body.decode())
	print(" [x] Done")

	ch.basic_ack(delivery_tag=method.delivery_tag)
	buscaInfos(body.decode())
	


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=nomeFila, on_message_callback=callback)
channel.start_consuming()
print("Esperando novos itens")


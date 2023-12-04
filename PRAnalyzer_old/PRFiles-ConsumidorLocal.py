from Libs.GithubConsumer import GithubConsumer
import json
import sys
import pika
import configparser
import mysql.connector
from PRAnalizer import PRAnalizer
from Libs.TrataResponse import TrataResponse
import base64


# CONFIGURACOES 
config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")
queueName = config.get("QUEUES", "queueNameRetrievePRFilesLocal")



# CONFIGURAÇÃO BANCO
dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}
conn = mysql.connector.connect(pool_name = "verifica_testes", pool_size = 1,**dbconfig)
cursor = conn.cursor();


githubConsumer = GithubConsumer()
trataResponse = TrataResponse()

def analisarPR(arrayFiles, pr_id, linguagemReferencia):
	analizer = PRAnalizer(linguagemReferencia)
	dadosDoPR  = analizer.retornaEstrutura();

	for item in arrayFiles:
		if 'patch' in item:
			itensAlterados = item['patch']

			aux = itensAlterados.split("\n");	

			for item in aux:
				if(analizer.checkIfModifier(item.strip())):
					result 			= analizer.verify(item.strip())
					modifierType 	= analizer.checkModifierType(item.strip())
					dadosDoPR[result][modifierType] += 1
					dadosDoPR['all'][modifierType] += 1

	return dadosDoPR
	

def atualizaRegistro(dadosPR, pullRequest, arrayArquivosCompletos):
	cursor.execute(""" 
		update pull_requests set
			functions_removed = %s,
			functions_added = %s,
			functions_others = %s,

			tests_removed = %s,
			tests_added = %s,
			tests_others = %s,
			
			class_removed = %s,
			class_added = %s,
			class_others = %s,

			code_removed = %s,
			code_added = %s,
			code_others = %s,

			imports_removed = %s,
			imports_added = %s,
			imports_others = %s,

			comments_removed = %s,
			comments_added = %s,
			comments_others = %s,

			whitelines_removed = %s,
			whitelines_added = %s,
			whitelines_others = %s
		where id = %s
	
	""", (
		str(dadosPR['functions']['removed']),
		str(dadosPR['functions']['added']),
		str(dadosPR['functions']['others']),

		str(dadosPR['tests']['removed']),
		str(dadosPR['tests']['added']),
		str(dadosPR['tests']['others']),

		str(dadosPR['class']['removed']),
		str(dadosPR['class']['added']),
		str(dadosPR['class']['others']),

		str(dadosPR['code']['removed']),
		str(dadosPR['code']['added']),
		str(dadosPR['code']['others']),

		str(dadosPR['imports']['removed']),
		str(dadosPR['imports']['added']),
		str(dadosPR['imports']['others']),

		str(dadosPR['comments']['removed']),
		str(dadosPR['comments']['added']),
		str(dadosPR['comments']['others']),

		str(dadosPR['whiteLines']['removed']),
		str(dadosPR['whiteLines']['added']),
		str(dadosPR['whiteLines']['others']),

		pullRequest['id']
	))

	conn.commit()

def recuperarArquivosLocais(pullRequest):
	# cursor.execute("select UNCOMPRESS(json_files) from pull_requests where id = "+str(pullRequest['id']))
	cursor.execute("select UNCOMPRESS(json_files) from pull_requests where id = "+str(pullRequest['id']))
	arrayArquivos = cursor.fetchone()
	return json.loads(arrayArquivos[0])

def processar(pullRequest):
	# arrayArquivosCompletos = githubConsumer.requisitarGithub(pullRequest['url']+"/files");	

	arrayArquivosCompletos = recuperarArquivosLocais(pullRequest)
	dadosPR = analisarPR(arrayArquivosCompletos, pullRequest['id'], pullRequest['linguagem'])
	# print(dadosPR)
	# exit()
	atualizaRegistro(dadosPR, pullRequest, arrayArquivosCompletos)

	print(str(pullRequest['id'])+" processado")


def callback(ch, method, properties, body):	
	ch.basic_ack(delivery_tag=method.delivery_tag)
	processar(json.loads(body.decode()))


# CONFIGURAÇÃO DE FILAS
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=60000))
channel = connection.channel()
channel.queue_declare(queue=queueName, durable=True)

print("Esperando novos itens")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queueName, on_message_callback=callback)
channel.start_consuming()

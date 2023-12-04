from Libs.GithubConsumer import GithubConsumer
import json
import sys
import pika
import configparser
import mysql.connector
from PRAnalizer import PRAnalizer


# CONFIGURACOES 
config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")
nomeFila = config.get("FILAS", "nomeFilaRecuperarJsonPRsFiles")


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


def salvarJsonPRFiles(arrayFiles, pr_id):
	sql = "UPDATE pull_requests SET json_files = %s where id = %s"
	cursor.execute(sql, (
		json.dumps(arrayFiles),
		pr_id,
	))
	conn.commit()


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
	


def processar(pullRequest):
	try:
		arrayArquivosCompletos = githubConsumer.requisitarGithub(pullRequest['url']+"/files");
	except:
		arrayArquivosCompletos = githubConsumer.requisitarGithub(pullRequest['url'] + "/files");
	salvarJsonPRFiles(arrayArquivosCompletos, pullRequest['id'])
	dadosPR = analisarPR(arrayArquivosCompletos, pullRequest['id'], pullRequest['linguagem'])


	sql = "UPDATE pull_requests SET functions_removed = %s, " \
		  "functions_added = %s," \
		  "functions_others = %s, " \
		  "tests_removed = %s, " \
		  "tests_added = %s, " \
		  "tests_others = %s, " \
		  "class_removed = %s, " \
		  "class_added = %s, " \
		  "class_others = %s, " \
		  "code_removed = %s, " \
		  "code_added = %s, " \
		  "code_others = %s, " \
		  "imports_removed = %s, " \
		  "imports_added = %s, " \
		  "imports_others = %s, " \
		  "comments_removed = %s, " \
		  "comments_added = %s, " \
		  "comments_others = %s, " \
		  "whitelines_removed = %s, " \
		  "whitelines_added = %s, " \
		  "whitelines_others = %s " \
		  "where id = %s"
	cursor.execute(sql, (
		dadosPR['functions']['removed'],
		dadosPR['functions']['added'],
		dadosPR['functions']['others'],

		dadosPR['tests']['removed'],
		dadosPR['tests']['added'],
		dadosPR['tests']['others'],

		dadosPR['class']['removed'],
		dadosPR['class']['added'],
		dadosPR['class']['others'],

		dadosPR['code']['removed'],
		dadosPR['code']['added'],
		dadosPR['code']['others'],

		dadosPR['imports']['removed'],
		dadosPR['imports']['added'],
		dadosPR['imports']['others'],

		dadosPR['comments']['removed'],
		dadosPR['comments']['added'],
		dadosPR['comments']['others'],

		dadosPR['whiteLines']['removed'],
		dadosPR['whiteLines']['added'],
		dadosPR['whiteLines']['others'],
		pullRequest['id']
	))
	conn.commit()

	print("PR processado: "+ str(pullRequest['id']))



def callback(ch, method, properties, body):	
	ch.basic_ack(delivery_tag=method.delivery_tag)
	processar(json.loads(body.decode()))


# CONFIGURAÇÃO DE FILAS
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=60000))
channel = connection.channel()
channel.queue_declare(queue=nomeFila, durable=True)

	
print("Esperando novos itens")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=nomeFila, on_message_callback=callback)
channel.start_consuming()
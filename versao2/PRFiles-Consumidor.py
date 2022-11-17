from matplotlib.pyplot import cla
from pygit import pull
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
	arrayArquivosCompletos = githubConsumer.requisitarGithub(pullRequest['url']+"/files");

	salvarJsonPRFiles(arrayArquivosCompletos, pullRequest['id'])

	dadosPR = analisarPR(arrayArquivosCompletos, pullRequest['id'], pullRequest['linguagem'])

	



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
from Libs.GithubConsumer import GithubConsumer
import json
import sys
import pika
import configparser
import mysql.connector


# configurations
config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")
nomeFila = config.get("FILAS", "nomeFilRecuperarBodyPR")


# database configurations
dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}
conn = mysql.connector.connect(pool_name = "verifica_testes", pool_size = 1,**dbconfig)
cursor = conn.cursor(dictionary=True);

githubConsumer = GithubConsumer()

def mudarStatusPullRequest(pullRequestId):
	sql = "UPDATE pull_requests SET status_analise = 'aguardando-analise-body' where id = %s"
	cursor.execute(sql, (pullRequestId,))
	conn.commit()

def processar(array_dados):
	dados, status_code = githubConsumer.requisitaUrlUnica(array_dados['url'])

	# print(item['url'])
	print(array_dados['id'])
	sql = "UPDATE pull_requests SET json_request_pr = %s where id = %s"
	cursor.execute(sql, (json.dumps(dados),array_dados['id']))
	conn.commit()

	mudarStatusPullRequest(array_dados['id'])


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
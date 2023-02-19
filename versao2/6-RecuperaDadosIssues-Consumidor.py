from Libs.GithubConsumer import GithubConsumer
import json
import sys
import pika
import configparser
import mysql.connector


# CONFIGURACOES
config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")
nomeFila = config.get("FILAS", "nomeFilaRecuperaIssuesVinculadas")


# CONFIGURAÇÃO BANCO
dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}
conn = mysql.connector.connect(pool_name = "verifica_testes", pool_size = 1,**dbconfig)
cursor = conn.cursor(dictionary=True);

githubConsumer = GithubConsumer()


def montaUrlIssue(dados, issueCode):
	posicaoUltimoBarra = dados['url'].rfind('/')
	urlBase = dados['url'][0:posicaoUltimoBarra]
	urlBase = urlBase.replace('pulls', 'issues')
	urlBase = urlBase + "/" +str(issueCode.replace('#', ''))
	return urlBase


def buscaIssuesSalvas(pullRequestId):
	sql = """
		select issue_code
			from pull_request_issues
			where pull_request_id = %s
	"""
	cursor.execute(sql, (pullRequestId,))
	return cursor.fetchall()

def processar(array_dados):

	issuesVinculadas = buscaIssuesSalvas(array_dados['id'])

	for issue in issuesVinculadas:
		url_issue = montaUrlIssue(array_dados, issue['issue_code'])
		dados = githubConsumer.requisitaUrlUnica(url_issue)

		sql = "UPDATE pull_request_issues SET json_issue = %s where pull_request_id = %s and issue_code = %s"
		cursor.execute(sql, (
			json.dumps(dados),
			array_dados['id'],
			issue['issue_code']
		))
		conn.commit()



def callback(ch, method, properties, body):
	# ch.basic_ack(delivery_tag=method.delivery_tag)
	processar(json.loads(body.decode()))

# CONFIGURAÇÃO DE FILAS
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=60000))
channel = connection.channel()
channel.queue_declare(queue=nomeFila, durable=True)

print("Esperando novos itens")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=nomeFila, on_message_callback=callback)
channel.start_consuming()
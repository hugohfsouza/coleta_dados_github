from Libs.GithubConsumer import GithubConsumer
import json
import sys
import pika
import configparser
import mysql.connector


# configurations
config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")
nomeFila = config.get("FILAS", "nomeFilaRecuperaIssuesVinculadas")


# Database configuration
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
	sql = """select issue_code from pull_request_issues where pull_request_id = %s"""
	cursor.execute(sql, (pullRequestId,))
	return cursor.fetchall()


def mudarStatusPullRequest(pullRequestId):
	sql = "UPDATE pull_requests SET status_analise = 'dados-issues-extraidas' where id = %s"
	cursor.execute(sql, (pullRequestId,))
	conn.commit()

def processar(array_dados):
	print("processing: "+str(array_dados['id']))
	issuesVinculadas = buscaIssuesSalvas(array_dados['id'])

	countSuccess = 0
	for issue in issuesVinculadas:
		url_issue = montaUrlIssue(array_dados, issue['issue_code'])
		dados, status_code = githubConsumer.requisitaUrlUnica(url_issue)

		if status_code == 200:
			sql = "UPDATE pull_request_issues SET json_issue = %s where pull_request_id = %s and issue_code = %s"
			cursor.execute(sql, (
				json.dumps(dados),
				array_dados['id'],
				issue['issue_code']
			))
			conn.commit()
			countSuccess += 1

	# só altero o status do PR se eu encontrei as issues
	if countSuccess == len(issuesVinculadas):
		mudarStatusPullRequest(array_dados['id'])



def callback(ch, method, properties, body):
	ch.basic_ack(delivery_tag=method.delivery_tag)
	processar(json.loads(body.decode()))

# Queue Configurations
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=60000))
channel = connection.channel()
channel.queue_declare(queue=nomeFila, durable=True)

print("Wait new items")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=nomeFila, on_message_callback=callback)
channel.start_consuming()
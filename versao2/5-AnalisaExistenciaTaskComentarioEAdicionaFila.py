import configparser
import time
import re
import json
import mysql.connector
from Libs.Queue import Sender

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

nomeFila = config.get("FILAS", "nomeFilaRecuperaIssuesVinculadas")
sender = Sender(nomeFila)

dbconfig = {
	"host": config.get("MYSQL", "host"),
	"user": config.get("MYSQL", "user"),
	"passwd": config.get("MYSQL", "passwd"),
	"db": config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(pool_name="mypool", pool_size=1, **dbconfig)
cursor = conn.cursor(dictionary=True);

cursor.execute("""
	select pull_requests.id, pull_requests.json_request_pr, pull_requests.url
		from pull_requests 
		where 1=1 
		-- status_analise = 'aguardando-analise-body'
		and id = 3552
""")


def extrair_mencoes(texto):
	mencoes = []
	if texto != None:
		mencoes = re.findall(r'#\d+', texto)
	return mencoes


def mudarStatusPullRequest(pullRequestId):
	sql = "UPDATE pull_requests SET status_analise = 'para-extrair-dados-issues' where id = %s"
	cursor.execute(sql, (pullRequestId,))
	conn.commit()


def limparIssuesPR(pullRequestId):
	sql = "DELETE from pull_request_issues where pull_request_id = %s and json_issue is null "
	cursor.execute(sql, (pullRequestId,))
	conn.commit()


def adicionaIssues(pullRequestId, dados):
	for issue in dados:
		print(issue)
		sql = "INSERT pull_request_issues(pull_request_id, issue_code) values (%s, %s) "
		cursor.execute(sql, (pullRequestId, issue))
		conn.commit()


for item in cursor.fetchall():
	jsonDados = json.loads(item['json_request_pr'])
	dados = extrair_mencoes(jsonDados['body'])

	if len(dados) > 0:
		mudarStatusPullRequest(item['id'])
		limparIssuesPR(item['id'])
		adicionaIssues(item['id'], dados)
		textJson = '{"id": ' + str(item['id']) + ', "url": "' + str(item['url']) + '"}'
		sender.send(textJson)

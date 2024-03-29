import configparser
import time
import re
import json
import mysql.connector
from Libs.Queue import Sender

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")



dbconfig = {
	"host": config.get("MYSQL", "host"),
	"user": config.get("MYSQL", "user"),
	"passwd": config.get("MYSQL", "passwd"),
	"db": config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(pool_name="mypool", pool_size=1, **dbconfig)
cursor = conn.cursor(dictionary=True);




def extrair_mencoes(texto):
	mencoes = []
	if texto != None:
		# mencoes = re.findall(r'#\d+', texto)
		# mencoes = re.findall(r'(close|closed|fix|fixes|fixed|resolve|resolves|resolved)\s+\#\d+', texto)
		mencoes = re.findall(r'(?:close|closed|fix|fixes|fixed|resolve|resolves|resolved)\s+\#\d+', texto.lower())
	return mencoes

def extrair_mencoes_simples(texto):
	mencoes = []
	if texto != None:
		mencoes = re.findall(r'#\d+', texto)
	return mencoes




def mudarStatusPullRequest(pullRequestId, status = 'para-extrair-dados-issues'):
	sql = "UPDATE pull_requests SET status_analise = %s where id = %s"
	cursor.execute(sql, (status, pullRequestId))
	conn.commit()


def limparIssuesPR(pullRequestId):
	sql = "DELETE from pull_request_issues where pull_request_id = %s and json_issue is null "
	cursor.execute(sql, (pullRequestId,))
	conn.commit()


def adicionaIssues(pullRequestId, dados):
	for issue in dados:
		dadosExplodidos = dados[0].split()
		sql = "INSERT pull_request_issues(pull_request_id, issue_code, acao_pr) values (%s, %s, %s) "
		cursor.execute(sql, (pullRequestId, dadosExplodidos[1], dadosExplodidos[0]))
		conn.commit()

def adicionaIssuesSemAcao(pullRequestId, dados):
	for issue in dados:
		cursor.execute("""
			select  1 from pull_request_issues where pull_request_id = %s and issue_code = %s limit 1
		""", (pullRequestId, issue))
		existe = cursor.fetchone();

		if(existe == None):
			sql = "INSERT pull_request_issues(pull_request_id, issue_code) values (%s, %s) "
			cursor.execute(sql, (pullRequestId, issue))
			conn.commit()

cursor.execute("""
	select pull_requests.id, pull_requests.json_request_pr, pull_requests.url
		from pull_requests 
		where 1=1 
			and repo_id in (select id from repositorios where temTeste = 1 and educacional = 0 and stars_count >= 58142)
			and status_analise = 'aguardando-analise-body'
			-- and id between 1357943 and 2587412
			-- and id between 2587413 and 5581362
			-- and id between 5581363 and 6060032
		-- limit 30000
""")

nomeFila = config.get("FILAS", "nomeFilaRecuperaIssuesVinculadas")
sender = Sender(nomeFila)

for item in cursor.fetchall():
	print("Analisando body do :" + str(item['id']))
	jsonDados = json.loads(item['json_request_pr'])

	if 'body' in jsonDados:
		dados = extrair_mencoes(jsonDados['body'])
		if len(dados) > 0:
			limparIssuesPR(item['id'])
			adicionaIssues(item['id'], dados)
			mudarStatusPullRequest(item['id'])


		dadosSimples = extrair_mencoes_simples(jsonDados['body'])
		if len(dadosSimples) > 0:
			teste = 1
			adicionaIssuesSemAcao(item['id'], dadosSimples)

		if len(dados) <= 0 and len(dadosSimples) <= 0:
			teste = 1
			mudarStatusPullRequest(item['id'], 'body-sem-nenhuma-issue')
		else:
			mudarStatusPullRequest(item['id'], 'issues-extraidas')
			textJson = '{"id": ' + str(item['id']) + ', "url": "' + str(item['url']) + '"}'
			sender.send(textJson)
	else:
		mudarStatusPullRequest(item['id'], 'para-recuperar-body')



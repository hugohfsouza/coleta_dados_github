import configparser
import time
import mysql.connector
from Libs.Queue import Sender

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")




dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(pool_name="mypool", pool_size=1, **dbconfig)
cursor = conn.cursor(dictionary=True);

cursor.execute("""
	select pull_requests.id, pull_requests.url, repositorios.linguagemReferencia
		from pull_requests 
		inner join repositorios on (pull_requests.repo_id = repositorios.id)
		where 1=1
			and repo_id in (select id from repositorios where temTeste = 1 and educacional = 0 and stars_count >= 58142)
			-- and (status_analise = 'para-recuperar-body' or json_request_pr is null)
			and status_analise = 'para-recuperar-body'
			-- and json_request_pr is null
		limit 10000
""")

nomeFila = config.get("FILAS", "nomeFilRecuperarBodyPR")
sender = Sender(nomeFila)
def mudarStatusPullRequest(pullRequestId):
	sql = "UPDATE pull_requests SET status_analise = 'em-recuperacao-body' where id = %s"
	cursor.execute(sql, (pullRequestId,))
	conn.commit()

for item in cursor.fetchall():
	textJson = '{"id": '+str(item['id'])+', "url": "'+str(item['url'])+'", "linguagem": "'+str(item['linguagemReferencia'])+'"}'
	sender.send(textJson)
	mudarStatusPullRequest(item['id'])

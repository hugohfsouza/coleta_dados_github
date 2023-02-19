import configparser
import time
import mysql.connector
from Libs.Queue import Sender

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


nomeFila = config.get("FILAS", "nomeFilRecuperarBodyPR")
sender = Sender(nomeFila)

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
		where repositorios.temTeste = 1
		and pull_requests.hasTest = 1
""")

for item in cursor.fetchall():
	textJson = '{"id": '+str(item['id'])+', "url": "'+str(item['url'])+'", "linguagem": "'+str(item['linguagemReferencia'])+'"}'
	sender.send(textJson)

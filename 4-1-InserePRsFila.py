import configparser
import json
import time
import mysql.connector
from Queue import Sender

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


tempoEspera 	= int(config.get("GERAL", "tempoEsperaSearch"))
nomeFila 		= config.get("FILAS", "nomeFilaRecuperaArquivos")




dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(pool_name = "mypool", pool_size = 1,**dbconfig)
cursor = conn.cursor(dictionary=True);

cursor.execute("FLUSH QUERY CACHE;")
cursor.execute("RESET QUERY CACHE;")
cursor.execute("""select pr.id, pr.url, r.linguagemReferencia from pull_requests pr
					inner join repositorios r on (pr.repo_id = r.id)
					where 1=1 
					and pr.analisado = 0
					and r.temTeste = 1
					and r.educacional = 0;""") 


for item in cursor.fetchall():
	sender = Sender(nomeFila)
	textJson = '{"id": '+str(item['id'])+', "url": "'+str(item['url'])+'", "linguagemReferencia": "'+str(item['linguagemReferencia'])+'"}'
	sender.send(textJson)
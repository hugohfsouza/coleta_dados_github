import configparser
import json
import mysql.connector
from Queue import Sender

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


tempoEspera 	= int(config.get("GERAL", "tempoEsperaSearch"))
nomeFila 		= config.get("FILAS", "nomeFilaRecuperaArquivos")


sender = Sender(nomeFila)

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
cursor.execute("""select id, url from pull_requests where analisado = 0 ;""")
for item in cursor.fetchall():
	textJson = '{"id": '+str(item['id'])+', "url": "'+str(item['url'])+'"}'
	sender.send(textJson)
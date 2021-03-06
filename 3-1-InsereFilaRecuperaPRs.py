import configparser
import json
import time
import mysql.connector
from Queue import Sender

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


tempoEspera 	= int(config.get("GERAL", "tempoEsperaSearch"))
nomeFila 		= config.get("FILAS", "nomeFilaRecuperaPRs")


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
cursor.execute("""select id, nameWithOwner from repositorios where temTeste = 1 and prs_recuperados is null""")

totalParaEsperar = 100
totalAgora = 0

for item in cursor.fetchall():
	textJson = '{"id": '+str(item['id'])+', "nameWithOwner": "'+str(item['nameWithOwner'])+'"}'
	sender.send(textJson)

	# totalAgora += 1
	# if(totalAgora >= totalParaEsperar):
	# 	print("Aguardando respiro - 2min");
	# 	time.sleep(120)
	# 	totalAgora = 0
import configparser
import time
import mysql.connector
from Queue import Sender

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


tempoEspera 	= int(config.get("GERAL", "tempoEsperaSearch"))
nomeFila 		= config.get("FILAS", "nomeFilaVerificaTeste")


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
cursor.execute("""select id, nameWithOwner, linguagemReferencia from repositorios where qtdArquivosStringTeste is null""")
# cursor.execute("""select id, nameWithOwner, linguagemReferencia from repositorios where id =444 """)

totalParaEsperar = 200
totalAgora = 0

for item in cursor.fetchall():
	textJson = '{"id": '+str(item['id'])+', "nameWithOwner": "'+str(item['nameWithOwner'])+'", "linguagem": "'+str(item['linguagemReferencia'])+'"}'
	sender.send(textJson)
	totalAgora += 1

	# if(totalAgora >= totalParaEsperar):
	# 	print("Aguardando respiro");
	# 	time.sleep(60)
	# 	totalAgora = 0

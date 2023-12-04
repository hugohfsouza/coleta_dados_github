import configparser
import time
import mysql.connector
from Libs.ArquivosJson import ArquivosJson

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(pool_name = "mypool", pool_size = 1,**dbconfig)
cursor = conn.cursor(dictionary=True);

gerenciadorArquivos = ArquivosJson()

def select():
	cursor.execute("""select id, json_request_pr from pull_requests where id = 1""")
	for item in cursor.fetchall():
		print(str(item['json_request_pr']))
		gerenciadorArquivos.salvar(
			item['id'],
			item['json_request_pr'],
			"json_pull_requests"
		)
# select()

json = gerenciadorArquivos.recuperar(1, "json_pull_requests")
print(json['commits'])
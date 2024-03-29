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

conn = mysql.connector.connect(pool_name = "mypool", pool_size = 1,**dbconfig)
cursor = conn.cursor(dictionary=True);

def inserir():
	sql = "INSERT INTO TESTE(teste, comp) VALUES ('a', compress(%s))"
	cursor.execute(sql, ('aa',))
	conn.commit()

def select():
	cursor.execute("""select json_request_pr, uncompress(json_request_pr_comp) from pull_requests where id = 1""")
	for item in cursor.fetchall():
		print(str(item['uncompress(comp)']))

select()
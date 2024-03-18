import configparser
import time
import mysql.connector
from Libs.Queue import Sender

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


nomeFila = config.get("FILAS", "NAME_QUEU_ANALYZER_SECURITY")
sender = Sender(nomeFila)

dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(pool_name = "mypool", pool_size = 1,**dbconfig)
cursor = conn.cursor(dictionary=True);


# query that will return the prs to be analyzed
cursor.execute("""
	select id from pull_requests where json_files is not null limit 10
""")

totalStopBlock = 200
totalNow = 0

for item in cursor.fetchall():
	textJson = '{"id": '+str(item['id'])+'}'
	sender.send(textJson)
	totalNow += 1

	if(totalNow >= totalStopBlock):
		print("Aguardando respiro");
		time.sleep(60)
		totalNow = 0

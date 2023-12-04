import configparser
import time
import mysql.connector
from Libs.Queue import Sender

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


queueName = config.get("QUEUES", "queueNameRetrievePRFiles")
sender = Sender(queueName)

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
cursor.execute("""
	select 
	pull_requests.id, 
    pull_requests.url, 
    repositorios.linguagemReferencia,
    repositorios.nameWithOwner,
    pull_requests.number
		from pull_requests 
		inner join repositorios on (pull_requests.repo_id = repositorios.id)
		where repositorios.temTeste = 1 and repositorios.linguagemReferencia = 'Ruby' 
		and pull_requests.hasCode = 0
		and pull_requests.hasTest = 1
		and pull_requests.hasOutros = 0
		and json_files is null

""")

timeToWait = 10
count = 0

for item in cursor.fetchall():
	# textJson = '{"id": '+str(item['id'])+', "url": "'+str(item['url'])+'", "linguagem": "'+str(item['linguagemReferencia'])+'"}'
	textJson = '{"id":'+str(item['id'])+', "url":"'+str(item['url'])+'", "linguagem": "'+str(item['linguagemReferencia'])+'", "nameWithOwner": "'+str(item['nameWithOwner'])+'", "number":'+str(item['number'])+'}'
	sender.send(textJson)
	# time.sleep(0.5)
	# count += 1

	# if(count >= timeToWait):
	# 	print("Waiting for breath");
	# 	time.sleep(2)
	# 	count = 0

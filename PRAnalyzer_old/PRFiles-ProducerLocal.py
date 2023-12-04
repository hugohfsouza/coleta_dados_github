import configparser
import time
import mysql.connector
from Libs.Queue import Sender

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


queueName = config.get("QUEUES", "queueNameRetrievePRFilesLocal")
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
		where json_files is not null
		

""")

totalParaMostrar = 10000
count = 0
countParcial = 0

for item in cursor.fetchall():
	# textJson = '{"id": '+str(item['id'])+', "url": "'+str(item['url'])+'", "linguagem": "'+str(item['linguagemReferencia'])+'"}'
	textJson = '{"id":'+str(item['id'])+', "url":"'+str(item['url'])+'", "linguagem": "'+str(item['linguagemReferencia'])+'", "nameWithOwner": "'+str(item['nameWithOwner'])+'", "number":'+str(item['number'])+'}'
	sender.send(textJson,False)
	count += 1
	countParcial += 1

	if(countParcial == totalParaMostrar):
		countParcial = 0
		print("Inserido um total de: "+str(count))
	# time.sleep(0.5)
	# count += 1
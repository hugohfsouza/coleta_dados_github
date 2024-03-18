import json
import sys
import pika
import configparser
import mysql.connector


# CONFIGURACOES 
config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")
nomeFila = config.get("FILAS", "NAME_QUEU_ANALYZER_SECURITY")


# CONFIGURAÇÃO BANCO
dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}
conn = mysql.connector.connect(pool_name = "verifica_testes", pool_size = 1,**dbconfig)
cursor = conn.cursor(dictionary=True);


# GET TERMS
configTerms = config.get("TERMS", "vulnerability")
listTerms = configTerms.split("|")


def getDataPR(pr_id):
	cursor.execute("select json_request_pr from pull_requests where id = "+str(pr_id) )	
	return cursor.fetchone()

def verifyTerms(json_request_pr, pr_id):
	json_pr = json.loads(json_request_pr)

	numberAppearances = 0
	presentTerms = []
	
	# ANALISY BODY
	try:
		for term in listTerms:
			if term in json_pr['body']:
				numberAppearances += 1
				presentTerms.append(term)
	except:
		print("error PR: "+str(pr_id))

	return numberAppearances, presentTerms

	

def processar(pullRequest):
	dataPR = getDataPR(pullRequest['id'])
	numberAppearances, presentTerms = verifyTerms(dataPR['json_request_pr'], pullRequest['id'])


	sql = "UPDATE pull_requests SET amount_term_vulnerability = %s, " \
		  "terms_vulnerability = %s," \
		  "where id = %s"
	cursor.execute(sql, (
		str(numberAppearances),
		"|".join(presentTerms),
		pullRequest['id']
	))
	conn.commit()

	print("PR processado: "+ str(pullRequest['id']))



def callback(ch, method, properties, body):	
	ch.basic_ack(delivery_tag=method.delivery_tag)
	processar(json.loads(body.decode()))


# CONFIGURAÇÃO DE FILAS
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=60000))
channel = connection.channel()
channel.queue_declare(queue=nomeFila, durable=True)

	
print("WAITNG NEW ITENS")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=nomeFila, on_message_callback=callback)
channel.start_consuming()
import configparser
import time
import re
import json
import mysql.connector
from Libs.Queue import Sender

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

nomeFila = config.get("FILAS", "nomeFilaRecuperaIssuesVinculadas")
sender = Sender(nomeFila)

dbconfig = {
	"host": config.get("MYSQL", "host"),
	"user": config.get("MYSQL", "user"),
	"passwd": config.get("MYSQL", "passwd"),
	"db": config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(pool_name="mypool", pool_size=1, **dbconfig)
cursor = conn.cursor(dictionary=True);


def getTipoIssue(issue_code, repo_id):
	# print(issue_code)
	# print(repo_id)
	number = issue_code.replace("#", "")
	cursor.execute("""select 1 from pull_requests where repo_id = %s and number = %s""", (repo_id, number))
	existe = cursor.fetchone()
	if existe == None:
		return 'Issue'

	return 'PR'

cursor.execute("""
	select 
		pull_requests.id, 
		pull_request_issues.pull_request_id, 
		pull_request_issues.issue_code, 
		uncompress(pull_request_issues.json_issue) as 'json_issue_comp' , 
		pull_request_issues.json_issue as 'json_issue' , 
		pull_requests.repo_id
		from pull_requests 
        inner join pull_request_issues on (pull_requests.id = pull_request_issues.pull_request_id)
		where 1=1 
		and status_analise = 'dados-issues-extraidas'
		and pull_request_issues.bug_obvio is null
		and pull_request_issues.json_issue is not null
		-- and id = 3643
""")

for item in cursor.fetchall():
	print(item['repo_id'])
	try:
		jsonDados = json.loads(item['json_issue'])
	except:
		jsonDados = json.loads(item['json_issue_comp'])

	temBugObvio = 0
	labelsEncontradas = ""
	tipoIssue = getTipoIssue(item['issue_code'], item['repo_id'])


	count = 0
	for label in jsonDados['labels']:
		if count == 0:
			labelsEncontradas = label['name']
		else:
			labelsEncontradas = labelsEncontradas + "|" + label['name']
		count += 1
		if "bug" in label['name']:
			temBugObvio = 1

	# print(labelsEncontradas)

	# print(jsonDados['url'] + "    " + str(len(jsonDados['labels'])) + "   " + str(item['pull_request_id'])    )
	sql = "UPDATE pull_request_issues SET tipo = %s, bug_obvio = %s, labels = %s, status = %s where pull_request_id = %s and issue_code = %s"
	cursor.execute(sql, (
		tipoIssue,
		temBugObvio,
		labelsEncontradas,
		jsonDados['state'],
		item['pull_request_id'],
		item['issue_code']
	))
	conn.commit()

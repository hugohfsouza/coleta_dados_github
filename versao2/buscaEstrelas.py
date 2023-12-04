from Libs.GithubConsumer import GithubConsumer
import json
import sys
import pika
import configparser
import mysql.connector


# configurations
config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")
nomeFila = config.get("FILAS", "nomeFilRecuperarBodyPR")


# database configurations
dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}
conn = mysql.connector.connect(pool_name = "verifica_testes", pool_size = 1,**dbconfig)
cursor = conn.cursor(dictionary=True);

githubConsumer = GithubConsumer()

cursor.execute("""select * from repositorios where stars_count is null""")

for item in cursor.fetchall():
	url = "https://api.github.com/repos/"+item['nameWithOwner']
	dados, status_code = githubConsumer.requisitaUrlUnica(url)
	if 'stargazers_count' in dados:
		sql = "UPDATE repositorios SET json_request = compress(%s), stars_count = %s where id = %s"
		cursor.execute(sql, (json.dumps(dados),dados['stargazers_count'], item['id']))
		conn.commit()
		print("Fazendo repo: "+str(item['id']))


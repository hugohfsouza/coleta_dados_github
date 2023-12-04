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
connLocal = mysql.connector.connect(pool_name = "verifica_testes", pool_size = 1,**dbconfig)
cursorLocal = connLocal.cursor(dictionary=True);

dbconfig = {
	"host":     "108.179.253.73",
	"user":     "fourzc18_acesso",
	"passwd":   "ASDF123a@",
	"db":       "fourzc18_pesquisa",
}
connRemoto = mysql.connector.connect(**dbconfig)
cursorRemoto = connRemoto.cursor(dictionary=True);


cursorLocal.execute("""select * from repositorios""")

for item in cursorLocal.fetchall():
	print(item)
	exit()




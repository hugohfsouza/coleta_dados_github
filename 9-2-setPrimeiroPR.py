from ast import Try
import re
from unittest import result
import requests
import json
import time
import configparser
import mysql.connector
import sys


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


# BUSCA TODOS OS CONTRIBUIDORES
cursor.execute("""
	select distinct contribuidor from linha_tempo_contribuidor order by contribuidor desc
""") 
contribuidores = cursor.fetchall()

total = len(contribuidores)
agora = 0

print("TOTAL: "+str(total))

for contribuidor in contribuidores:
	agora +=1
	print("Executando: "+str(agora)+" de "+str(total)+" =>>>> "+str((agora/total)*100))    

	# ESCOPO LOCAL
	cursor.execute("""select * from linha_tempo_contribuidor where contribuidor = '"""+str(contribuidor['contribuidor'])+"""' and escopo = 'global' order by periodo  limit 1""") 
	resultado = cursor.fetchall()

	for res in resultado:
		cursor.execute("""update linha_tempo_contribuidor set primeiro_mes = 1 where contribuidor = %s and periodo = %s """, (
			contribuidor['contribuidor'],
			res['periodo'],
		))
		conn.commit() 

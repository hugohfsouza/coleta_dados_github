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
	select distinct user  from pull_requests
""") 
contribuidores = cursor.fetchall()

total = len(contribuidores)
agora = 0

print("TOTAL: "+str(total))

for contribuidor in contribuidores:
	agora +=1
	print("Executando: "+str(agora)+" de "+str(total)+" =>>>> "+str((agora/total)*100))    

	# # ESCOPO PROJETO
	# cursor.execute("""
	# 	 select 
	# 		date_format(str_to_date(created_at, '%Y-%m-%d'), '%Y-%m-01') as periodo, 
	# 		SUM(case when tipo_pr = 'Apenas Teste' then 1 else 0 end) as total_pr_teste,
	# 		SUM(case when tipo_pr = 'Teste e Codigo' then 1 else 0 end) as total_pr_codigo_teste,
	# 		SUM(case when tipo_pr = 'Apenas Codigo' then 1 else 0 end) as total_pr_codigo
	# 	from (
	# 		select 
	# 			created_at, 
	# 			case
	# 					WHEN hasTest > 0 and hasCode = 0 and hasOutros = 0 then 'Apenas Teste'
	# 					WHEN hasTest = 0 and hasCode > 0 and hasOutros = 0 then 'Apenas Codigo'
	# 					WHEN hasTest = 0 and hasCode = 0 and hasOutros > 0 then 'Apenas Codigo'
	# 					WHEN hasTest > 0 and hasCode > 0 and hasOutros = 0 then 'Teste e Codigo'
	# 					WHEN hasTest > 0 and hasCode = 0 and hasOutros > 0 then 'Teste e Codigo'
	# 					WHEN hasTest = 0 and hasCode > 0 and hasOutros > 0 then 'Apenas Codigo'
	# 					WHEN hasTest > 0 and hasCode > 0 and hasOutros > 0 then 'Teste e Codigo'
	# 					WHEN hasTest = 0 and hasCode = 0 and hasOutros = 0 then 'Sem alteracoes'
	# 				end as tipo_pr
	# 		from pull_requests where user = '"""+str(contribuidor['user'])+"""'
	# 	) as aux
	# 	group by date_format(str_to_date(created_at, '%Y-%m-%d'), '%Y-%m-01')
	# 	order by created_at
	# """) 
	# resultado = cursor.fetchall()

	# for res in resultado:
	# 	cursor.execute("""INSERT INTO linha_tempo_contribuidor(contribuidor,periodo,escopo,total_contribuicao_teste,total_contribuicao_codigo,total_contribuicao_codigo_teste) VALUES (%s,%s,%s,%s,%s,%s)""", (
	# 		contribuidor['user'],
	# 		res['periodo'],
	# 		'global',
	# 		res['total_pr_teste'],
	# 		res['total_pr_codigo'],
	# 		res['total_pr_codigo_teste']
	# 	))
	# 	conn.commit() 


	# ESCOPO LOCAL
	cursor.execute("""
		  select 
				date_format(str_to_date(created_at, '%Y-%m-%d'), '%Y-%m-01') as periodo, 
				nameWithOwner,
				SUM(case when tipo_pr = 'Apenas Teste' then 1 else 0 end) as total_pr_teste,
				SUM(case when tipo_pr = 'Teste e Codigo' then 1 else 0 end) as total_pr_codigo_teste,
				SUM(case when tipo_pr = 'Apenas Codigo' then 1 else 0 end) as total_pr_codigo
			from (
				select 
					pull_requests.created_at, 
					nameWithOwner,
					case
							WHEN hasTest > 0 and hasCode = 0 and hasOutros = 0 then 'Apenas Teste'
							WHEN hasTest = 0 and hasCode > 0 and hasOutros = 0 then 'Apenas Codigo'
							WHEN hasTest = 0 and hasCode = 0 and hasOutros > 0 then 'Apenas Codigo'
							WHEN hasTest > 0 and hasCode > 0 and hasOutros = 0 then 'Teste e Codigo'
							WHEN hasTest > 0 and hasCode = 0 and hasOutros > 0 then 'Teste e Codigo'
							WHEN hasTest = 0 and hasCode > 0 and hasOutros > 0 then 'Apenas Codigo'
							WHEN hasTest > 0 and hasCode > 0 and hasOutros > 0 then 'Teste e Codigo'
							WHEN hasTest = 0 and hasCode = 0 and hasOutros = 0 then 'Sem alteracoes'
						end as tipo_pr
				from pull_requests 
				inner join repositorios on (pull_requests.repo_id = repositorios.id)
				where user = '"""+str(contribuidor['user'])+"""'
			) as aux
			group by date_format(str_to_date(created_at, '%Y-%m-%d'), '%Y-%m-01'), nameWithOwner
			order by created_at
	""") 
	resultado = cursor.fetchall()

	for res in resultado:
		cursor.execute("""INSERT INTO linha_tempo_contribuidor(contribuidor,periodo,escopo,total_contribuicao_teste,total_contribuicao_codigo,total_contribuicao_codigo_teste, projeto) VALUES (%s,%s,%s,%s,%s,%s,%s)""", (
			contribuidor['user'],
			res['periodo'],
			'local',
			res['total_pr_teste'],
			res['total_pr_codigo'],
			res['total_pr_codigo_teste'],
			res['nameWithOwner'],
		))
		conn.commit() 
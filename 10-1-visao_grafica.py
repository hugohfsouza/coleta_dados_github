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


periodosSequencia = {}

dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(pool_name = "mypool", pool_size = 1,**dbconfig)
cursor = conn.cursor(dictionary=True);

def converteData(datetime):
	return str(datetime).replace(" 00:00:00", "")



# BUSCA TODOS OS CONTRIBUIDORES
cursor.execute("""
	select distinct periodo from linha_tempo_contribuidor order by periodo
""") 
periodos = cursor.fetchall()
contador = 1
for periodo in periodos:
	periodosSequencia[converteData(periodo['periodo'])] = contador
	contador = contador+1




cursor.execute("""
	select 
		contribuidor,
		periodo,		
		CASE
			WHEN total_contribuicao_teste > 0 and total_contribuicao_codigo > 0 and total_contribuicao_codigo_teste > 0  THEN "Codigo_teste"
			WHEN total_contribuicao_teste > 0 and total_contribuicao_codigo > 0 and total_contribuicao_codigo_teste = 0  THEN "Codigo_teste"
			WHEN total_contribuicao_teste > 0 and total_contribuicao_codigo = 0 and total_contribuicao_codigo_teste > 0  THEN "Codigo_teste"
			WHEN total_contribuicao_teste > 0 and total_contribuicao_codigo = 0 and total_contribuicao_codigo_teste = 0  THEN "Teste"
			
			WHEN total_contribuicao_teste = 0 and total_contribuicao_codigo > 0 and total_contribuicao_codigo_teste > 0  THEN "Codigo_teste"
			WHEN total_contribuicao_teste = 0 and total_contribuicao_codigo > 0 and total_contribuicao_codigo_teste = 0  THEN "Codigo"
			WHEN total_contribuicao_teste = 0 and total_contribuicao_codigo = 0 and total_contribuicao_codigo_teste > 0  THEN "Codigo_teste"
			WHEN total_contribuicao_teste = 0 and total_contribuicao_codigo = 0 and total_contribuicao_codigo_teste = 0  THEN "sem_alteracoes"
		END as tipo_contribuidor
	from linha_tempo_contribuidor 
		where escopo = 'global' 
		-- and contribuidor in ('Trott','miss-islington','jbrockmendel','vstinner','original-brownbear','blueyed','ghost','rallytime','s0undt3ch','findepi','copybara-service[bot]','paramat','mfussenegger','cachedout','niboshi','jayeshka','serhiy-storchaka','dbmalkovsky','timgraham','felixxm','alexlamsl','Donnerbart','izeye','twangboy','dwoz','benwtrent','reitermarkus','smitpatel','arunagw','tlrx','Ch3LL','normanmaurer','nerzhul','jdufresne','rwjblue','fw-bot','terrymanu','simonjayhawkins','dnhatn','charris','y-yagi','SmallJoker','yahonda','jreback','toslunar','memsharded','kokosing','rnveach','sancar','zentol','bluetech','dreis2211','anntzer','aaudiber','MishaDemianenko','cbuescher','alalek','ahmetmircik','unnonouno','paulmelnikow','kamipo','nik9000','mkordas','eps1lon','jkakavas','DaveCTurner','cclauss','arvidn','electrum','okuta','meeseeksmachine','cjihrig','terminalmage','balloob','alex','gfyoung','sapier','martijnvg','kmaehashi','vbekiaris','github-actions[bot]','hawkinsp','orpiske','dimitris-athanasiou','jzoldak','AlexKamaev','stuartwdouglas','ejona86','geoand','nicoddemus','krionbsd','MarcoFalke','rsimha','davidkyle','emontnemery','sfan5','reaperhulk','benpatterson','asi1024','addaleax')
		-- and contribuidor in ('Raj-Datta-Manohar','Diffblue-benchmarks','TheRealHaui','chaudum','simonbasle','oscerd','infraio','petrpleshachkov','metanet','dain','mraarif','tniessen','dbmalkovsky','gero3')
		-- and contribuidor in ('jayeshka', 'Zeno-', 'edsadr', 'rahulhan', 'zuhao', 'rupeshta', 'gregorycu', 'EricHetti', 'seangriff', 'sluk3r', 'simkam', 'eas5', 'jorander', 'larissayvette', 'choudhuryanupam', 'MengdiGao', 'OrDTesters', 'moink', 'lzx404243', 'sebastianplesciuc', 'izishared', 'fwhdzh', 'Anjali2019', 'MoonLiY', 'arturgvieira-zz', 'danglotb', 'GabrielBercaru', 'gvma', 'petersear', 'felixDulys', 'igaiga', 'MetaDucky', 'jian365066744', 'savilli', 'sleepy-owl', 'ZhangsuhuiWang', 'amresh-sahu', 'arianahl', 'cmecklenborg', 'ftrihardjo', 'hegderaj4', 'r-toroxel', 'sritej20', 'suminkimm', 'wjj2', 'yyfMichaelYan', 'adnanghaffar07', 'AlexRadch', 'CharlesZKQ', 'h314to', 'hellowdan', 'kawoolutions', 'radelmann', 't0suj4', 'vivekkumar7089', 'Cjh327', 'james-huston', 'JonathanShrek', 'jun-oka', 'krajatcl', 'LALAYANG', 'llk984145406', 'mchllweeks', 'nekoqqq', 'obneq', 'Slyrich', 'sycx2', 'TheItsyBitsySpider', 'TheTermos')
		-- and contribuidor in ('SaturnFromTitan')
		and total_contribuicao_teste + total_contribuicao_codigo + total_contribuicao_codigo_teste > 10
""") 
contribuidores = cursor.fetchall()


matrizContribuidor  = {}

for contribuidor in contribuidores:

	if(contribuidor['contribuidor'] not in matrizContribuidor):
		matrizContribuidor[contribuidor['contribuidor']] = {}
	
	codigoPeriodo = converteData(contribuidor['periodo'])

	if(codigoPeriodo not in matrizContribuidor[contribuidor['contribuidor']]):
		matrizContribuidor[contribuidor['contribuidor']][codigoPeriodo] = ""
	
	matrizContribuidor[contribuidor['contribuidor']][codigoPeriodo] = contribuidor['tipo_contribuidor']

stringHeader = "nome,"
for periodo in periodosSequencia:
	stringHeader += periodo + ","	

print(stringHeader)

for contribuidor in matrizContribuidor:
	nomeContribuidor = contribuidor
	stringLinha = nomeContribuidor

	for periodo in periodosSequencia:
	
		if(periodo not in matrizContribuidor[contribuidor]):
			stringLinha += ",-"
		else:
			stringLinha += ","+str(matrizContribuidor[contribuidor][periodo])

	print(stringLinha)
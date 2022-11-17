from ast import Try
import requests
import json
import time
import configparser
import mysql.connector
import sys

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")
token 	= "token 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"
headers = {'Authorization': token, 'Accept': 'application/vnd.github.v3+json'}


# CONFIGURAÇÃO BANCO
dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}
conn = mysql.connector.connect(pool_name = "verifica_testes", pool_size = 1,**dbconfig)
cursor = conn.cursor();


# CREATE TABLE `pesquisa`.`informacoes_adicionais` (
#   `nameWithOwner` VARCHAR(200) NOT NULL,
#   `json_resposta` TEXT NULL,
#   PRIMARY KEY (`nameWithOwner`));


cursor.execute("""
	select nameWithOwner from repositorios 
	where 
    nameWithOwner not in (select nameWithOwner from informacoes_adicionais)
    order by nameWithOwner;
""") 
repositorios = cursor.fetchall()

queryInit = """ 
{
  repository(name: "#name#", owner: "#owner#") {
    id
    name
    nameWithOwner
    url
    createdAt
    databaseId
    id
    diskUsage
    forkCount
    stargazerCount
    languages {
      totalCount
    }
    issues {
      totalCount
    }
    milestones {
      totalCount
    }
    releases {
      totalCount
    }
    watchers {
      totalCount
    }
  }
}"""




def requisitarGithub(nomeRepos):

	aux = nomeRepos.split("/")

	query 	= queryInit.replace('#name#', aux[1])
	query 	= query.replace('#owner#', aux[0])


	while(True):
		response = requests.post('https://api.github.com/graphql',json={'query': query}, headers=headers)
		if(response.status_code == 200 or response.status_code == 404 or response.status_code == 422):
			break
		else:
			print("["+str(response.status_code)+"] tempo espera request")
			time.sleep(30)

	return response.json()





def buscaInfos(repositorioGithub):

	response = requisitarGithub(repositorioGithub)

	try:

		cursor.execute("""INSERT INTO informacoes_adicionais(
				nameWithOwner, 
				json_resposta,

				diskUsage,
				forkCount,
				stargazerCount,
				totalLanguages,
				totalIssues,
				totalMilestones,
				totalReleases,
				totalWatchers
				) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
				(
					repositorioGithub, 
					json.dumps(response['data']),
					response['data']['repository']['diskUsage'],
					response['data']['repository']['forkCount'],
					response['data']['repository']['stargazerCount'],

					response['data']['repository']['languages']['totalCount'],
					response['data']['repository']['issues']['totalCount'],
					response['data']['repository']['milestones']['totalCount'],
					response['data']['repository']['releases']['totalCount'],
					response['data']['repository']['watchers']['totalCount'],
				))
		conn.commit() 
	
	except:
		print("erro")



for repositorio in repositorios:
	buscaInfos(repositorio[0])


	


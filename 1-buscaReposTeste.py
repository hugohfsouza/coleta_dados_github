import requests
import json
import time
import mysql.connector
import configparser
import sys
from datetime import date
import datetime


config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


token 	= config.get("TOKENS", "token1")
headers	= {'Authorization': token}

rangeInicial 	= "2000-01-01"
rangeFinal 		= "2021-11-26"



dbconfig = {
    "host":     config.get("MYSQL", "host"),
    "user":     config.get("MYSQL", "user"),
    "passwd":   config.get("MYSQL", "passwd"),
    "db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor();

# linguagemReferencia = "C++"
linguagemReferencia = "JAVA"
# linguagemReferencia = "Javascript"
# linguagemReferencia = "Python"
# linguagemReferencia = "C"
# linguagemReferencia = "C#"
# linguagemReferencia = "Ruby"


headers = {'Authorization': token,'Accept': 'application/vnd.github.v3+json'}


queryInit = """ 
{
  search(query: "is:public language:"""+ str(linguagemReferencia) +""" fork:false mirror:false archived:false stars:>3000 created:>#dataInicial# sort:stars-asc", type: REPOSITORY, first: 100, after: "#page#" ) {
    repositoryCount
    pageInfo {
      endCursor
      startCursor
      hasNextPage
    }
    edges {
      node {
        ... on Repository {
          name
          nameWithOwner
          url
          isFork
          createdAt
          databaseId
          id
          languages(orderBy: {field: SIZE, direction: DESC}, first: 20) {
            edges {
              node {
                name
              }
            }
            totalCount
          }
          pullRequests {
            totalCount
          }
        }
      }
    }
  }
}"""


def requisitarGithub(page, removePagina, dataInicial):
	global queryInit;

	if(removePagina):
		query 	= queryInit.replace(', after: "#page#"', "")
	else:
		query 	= queryInit.replace('#page#', page)

	query 	= query.replace('#dataInicial#', str(dataInicial))


	request = requests.post('https://api.github.com/graphql',json={'query': query}, headers=headers)
	
	if request.status_code == 200:
		return request.json()
	else:
		raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def busca(pagina):
	lista = []
	return lista
	pass



def insertRepositorio(name, nameWithOwner, createdAt, databaseId, qtdPRs ,languages):
	global conn
	global cursor
	global linguagemReferencia


	try:
		cursor.execute("""INSERT INTO repositorios(
			name, 
			nameWithOwner, 
			createdAt, 
			databaseId,  
			languages, 
			qtdPrs,
			linguagemReferencia) values (%s, %s, %s, %s, %s, %s, %s)""", 
			(name, nameWithOwner, createdAt, databaseId, languages, qtdPRs, linguagemReferencia) )
		conn.commit() 
	except Exception as e:
		pass
		

def verificarUsoApiGithub():
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=headers)
    y = json.loads(response.text)
    print("[Max Reqs] "+str(y["resources"]["graphql"]['remaining']))





def requisitarPorData(dataInicial):
	endCursor = ""
	lista 	= requisitarGithub(endCursor, True, dataInicial )

	hasNextPage = True
	countTestMacro = 0

	while(hasNextPage):
		endCursor 	= lista['data']['search']['pageInfo']['endCursor']
		startCuror 	= lista['data']['search']['pageInfo']['startCursor']
		hasNextPage = lista['data']['search']['pageInfo']['hasNextPage']

		print("---------------------------")
		print("endCursor: "+str(endCursor))
		print("startCuror: "+str(startCuror))
		print("hasNextPage: "+str(hasNextPage))
		print("---------------------------")


		for repo in lista['data']['search']['edges']:
			if(not repo['node']['isFork']):
				stringLinguagens = ""
				for linguagem in repo['node']['languages']['edges']:
					stringLinguagens  += ","+linguagem['node']['name']
				stringLinguagens = stringLinguagens[1:]
					
				countTestMacro += 1
				insertRepositorio(
					repo['node']['name'],
					repo['node']['nameWithOwner'],
					repo['node']['createdAt'],
					repo['node']['databaseId'],
					repo['node']['pullRequests']['totalCount'],
					stringLinguagens
				)
		if(hasNextPage):
			lista 	= requisitarGithub(endCursor, False, dataInicial)
		verificarUsoApiGithub()




data = date.fromisoformat(rangeInicial)
dataLimite = date.fromisoformat(rangeFinal)

while(data <= dataLimite):
	data = data + datetime.timedelta(days=5)
	# print(data)
	requisitarPorData(data)
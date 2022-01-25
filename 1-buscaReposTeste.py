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

tempoEspera = 10
token 	= config.get("TOKENS", sys.argv[1])
headers	= {'Authorization': token}

rangeInicial 	= "2001-03-01"
rangeFinal 		= "2021-11-26"


dbconfig = {
    "host":     config.get("MYSQL", "host"),
    "user":     config.get("MYSQL", "user"),
    "passwd":   config.get("MYSQL", "passwd"),
    "db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor();

# "JAVA" 			python .\1-buscaReposTeste.py token1 JAVA   819
# "C++" 			python .\1-buscaReposTeste.py token2 C++   471
# "Javascript" 		python .\1-buscaReposTeste.py token3 Javascript
# "Python" 			python .\1-buscaReposTeste.py token4 Python
# "C" 				python .\1-buscaReposTeste.py token5 C  369
# "C#" 				python .\1-buscaReposTeste.py token6 C#  220
# "Ruby" 			python .\1-buscaReposTeste.py token7 Ruby 226

linguagemReferencia = sys.argv[2]

headers = {'Authorization': token,'Accept': 'application/vnd.github.v3+json'}

# is:public language:JAVA fork:false mirror:false archived:false stars:>3000 sort:stars-asc
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


	# removePagina = True
	if(removePagina):
		query 	= queryInit.replace(', after: "#page#"', "")
	else:
		query 	= queryInit.replace('#page#', page)

	query 	= query.replace('#dataInicial#', str(dataInicial))

	# print(query)
	# request = requests.post('https://api.github.com/graphql',json={'query': query}, headers=headers)	
	# print("Request status code: "+ str(request.status_code))


	while(True):
		response = requests.post('https://api.github.com/graphql',json={'query': query}, headers=headers)
		if(response.status_code == 200 or response.status_code == 404 or response.status_code == 422):
			break
		else:
			print("["+str(response.status_code)+"] tempo espera request")
			time.sleep(tempoEspera)

	return response.json()



	# if request.status_code == 200:
	# 	return request.json()
	# else:
	# 	raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def busca(pagina):
	lista = []
	return lista
	pass



def insertRepositorio(name, nameWithOwner, createdAt, databaseId, qtdPRs ,languages):
	global conn
	global cursor
	global linguagemReferencia

	novo = False

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

		novo = True
	except Exception as e:
		pass

	if(novo):
		print("Adicionando repositorio novo")
		

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
				print(repo['node']['name'])
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
	print("Fazendo dia "+str(data))
	data = data + datetime.timedelta(days=90)
	# print(data)
	requisitarPorData(data)
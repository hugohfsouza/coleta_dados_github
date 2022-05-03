import mysql.connector
import configparser
from prettytable import PrettyTable

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(pool_name = "mypool", pool_size = 1,**dbconfig)
cursor = conn.cursor();

linguagens = ['JAVA', 'C++', 'Javascript', 'Python', 'C', 'C#', 'Ruby' ]




print("\n\n\n\n")
print("Quantidade de projetos com teste e sem teste em todas as linguagems e no geral APENAS PROJETOS  EDUCACIONAIS")
projetosEducacionais = PrettyTable()
projetosEducacionais.field_names = ["Linguagem", "Classificaçao", "Numero de Projetos", "% de projetos"]
geralComTeste = 0
geralSemTeste = 0

for linguagem in linguagens:
    cursor.execute(""" select count(1) from repositorios where linguagemReferencia = %s and (temTeste = 0 or temTeste is null) and educacional = 1""", (linguagem,)) 
    dadoSemTeste = cursor.fetchone()

    cursor.execute(""" select count(1) from repositorios where linguagemReferencia = %s and temTeste = 1 and educacional = 1""", (linguagem,)) 
    dadoComTeste = cursor.fetchone()

    total = dadoComTeste[0] + dadoSemTeste[0]

    projetosEducacionais.add_row([linguagem, "Com Teste", dadoComTeste[0] , (dadoComTeste[0]/total)*100 ])
    projetosEducacionais.add_row([linguagem, "Sem Teste", dadoSemTeste[0] , (dadoSemTeste[0]/total)*100 ])

print(projetosEducacionais)



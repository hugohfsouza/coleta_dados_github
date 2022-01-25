import configparser
import json
import time
import mysql.connector

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


def getCountComTeste(self, pr_id):
    retorno = 0
    cursor.execute("""SELECT count(1) from pull_request_files where pr_id = %s and filename like '%test%'""", (pr_id,))
    for result in cursor.fetchall():
        retorno = result[0]

    return retorno

def getCountSemTeste(self, pr_id):
    retorno = 0;
    linhas = cursor.execute("""SELECT count(1) from pull_request_files where pr_id = %s and filename not like '%test%'""", (pr_id,))
    for result in cursor.fetchall():
        retorno = result[0]

    return retorno



def ajustar(self):
    retorno = False;
    cursor.execute("""SELECT * from pull_requests where analisado = 1 and hasTest is null limit 1""")
    lista = cursor.fetchall()

    print("Ajustando: ["+str(len(lista))+"]")

    for prAberto in lista:

        qtdCodigo 	= getCountSemTeste(prAberto[0])
        qtdTeste 	= getCountComTeste(prAberto[0])
        
        temTeste = False
        temCodigo = False

        if qtdTeste > 0:
            temTeste = True

        if qtdCodigo > 0:
            temCodigo = True
        
        cursor.execute("""UPDATE analisegithub5.pull_requests set hasTest = %s, hasCode = %s, qtdArqTest = %s, qtdArqCode = %s where id = %s""", (temTeste, temCodigo, qtdTeste, qtdCodigo, prAberto[0] ,) )
        conn.commit()



cursor.execute("FLUSH QUERY CACHE;")
cursor.execute("RESET QUERY CACHE;")
cursor.execute("""
    select pr.id, r.linguagemReferencia from pull_requests pr
        inner join repositorios r on (r.id = pr.repo_id)
    where analisado = 1 
    and pr.id = 2;""")

count = 0
itens = cursor.fetchall()


def categorizarPR(id, linguagem):
    pass


for item in itens:
    categorizarPR(item['id'], item['linguagemReferencia'])
    # cursor.execute("""select id from pull_requests where repo_id = %s and number = %s order by id desc limit 1""", (item['repo_id'], item['number']) )
    # dadosItem = cursor.fetchone()

    # itemDeletado = dadosItem['id']
    # cursor.execute("""delete from pull_requests where id = %s """, (dadosItem['id'],))
    # conn.commit()

    # print(itemDeletado)
    


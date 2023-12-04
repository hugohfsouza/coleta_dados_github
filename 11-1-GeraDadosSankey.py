import configparser
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

cursor.execute(""" select distinct contribuidor from linha_tempo_contribuidor where escopo = 'global'""") 
contribuidores = cursor.fetchall()

resultado = {}
contadorQtdContribuidor = 1

for contribuidor in contribuidores:
    cursor.execute(""" select * from linha_tempo_contribuidor where contribuidor = %s and escopo = 'global'""", (contribuidor['contribuidor'],)) 
    contribuicoes = cursor.fetchall()
    for index in range(len(contribuicoes)-1):
        posicaoArray = contribuicoes[index]['tipo_contribuicao'] + ":"+ contribuicoes[index+1]['tipo_contribuicao']

        if posicaoArray in resultado:
            resultado[posicaoArray] = resultado[posicaoArray] + 1
        else:
            resultado[posicaoArray] = 1

    print(contadorQtdContribuidor)
    contadorQtdContribuidor +=1
        

print(resultado)

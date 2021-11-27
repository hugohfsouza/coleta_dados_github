import configparser
import mysql.connector

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


tempoEspera 	= int(config.get("GERAL", "tempoEsperaSearch"))
nomeFila 		= config.get("FILAS", "nomeFilaRecuperaPRs")



dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(pool_name = "mypool", pool_size = 1,**dbconfig)
cursor = conn.cursor(dictionary=True);

# PROJETOS JAVA
cursor.execute("""UPDATE REPOSITORIOS SET temTeste = 1 where linguagemReferencia = "JAVA" and qtdArquivosStringTeste > 1000""")
conn.commit()
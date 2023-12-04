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


cursor.execute(""" select * from linha_tempo_contribuidor where tipo_contribuicao is null""") 
dados = cursor.fetchall()

def defineTipoContribuidorPeriodo(total_teste, total_codigo, total_codigo_teste):
    if(total_teste > 0 and total_codigo<=0 and total_codigo_teste <=0):
        return "ContribuicaoTeste"
    
    if(total_teste <= 0 and total_codigo > 0 and total_codigo_teste <=0):
        return "ContribuicaoCodigo"
    
    if(total_teste <= 0 and total_codigo <= 0 and total_codigo_teste > 0):
        return "ContribuicaoCodigoTeste"
    
    if(total_teste <= 0 and total_codigo > 0 and total_codigo_teste > 0):
        return "ContribuicaoCodigoTeste"

    if(total_teste > 0 and total_codigo > 0 and total_codigo_teste > 0):
        return "ContribuicaoCodigoTeste"
    
    if(total_teste > 0 and total_codigo <= 0 and total_codigo_teste > 0):
        return "ContribuicaoCodigoTeste"

    if(total_teste <= 0 and total_codigo <= 0 and total_codigo_teste <= 0):
        return "ContribuicaoVazia"
    

    if(total_teste > 0 and total_codigo > 0 and total_codigo_teste <= 0):
        return "ContribuicaoCodigoTeste"
    
    return False

totalAgora = 0;

for item in dados:
    tipo = defineTipoContribuidorPeriodo(
        item['total_contribuicao_teste'],
        item['total_contribuicao_codigo'],
        item['total_contribuicao_codigo_teste']
    )
    if(tipo):
        totalAgora +=1
        # sql = )
        cursor.execute("UPDATE linha_tempo_contribuidor SET tipo_contribuicao = %s where id = %s", (tipo, item['id']))
        conn.commit()

        if(totalAgora >= 10000):
            print("+10.000")
            totalAgora = 0
        # print(item)
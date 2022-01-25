from tqdm import tqdm
import time
import datetime
import configparser
import ctypes
import mysql.connector

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


ctypes.windll.kernel32.SetConsoleTitleW("Performance")


# CONFIGURAÇÃO BANCO
dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(pool_name = "mypool", pool_size = 1,**dbconfig)
cursor = conn.cursor(dictionary=True)


def mediaUltimasTresHoras():
    cursor.execute("""select 
        DATE_FORMAT(datetime_analisado, '%d/%m/%Y %H') as hora,
        count(1)  as total
    from pull_requests 
    where analisado = 1 
    group by  DATE_FORMAT(datetime_analisado, '%d/%m/%Y %H')
    order by DATE_FORMAT(datetime_analisado, '%d/%m/%Y %H') desc
    limit 4""") 
    primeiro    = True
    total       = 0

    dadoRestante = cursor.fetchall()
    for item in dadoRestante:
        if(primeiro):
            primeiro = False
        else:
            total += item['total']
    
    if(total == 0):
        return 1

    return total/3


ultimaHora = 0

while(True):
    cursor.execute("FLUSH QUERY CACHE;")
    cursor.execute("RESET QUERY CACHE;")
    cursor.execute("""select count(1) as total from pull_requests""") 
    dadoTotal = cursor.fetchone()


    cursor.execute("FLUSH QUERY CACHE;")
    cursor.execute("RESET QUERY CACHE;")
    cursor.execute("""select count(1) as total from pull_requests where analisado = 1""") 
    dadoAnalisado = cursor.fetchone()


    cursor.execute("FLUSH QUERY CACHE;")
    cursor.execute("RESET QUERY CACHE;")
    cursor.execute("""select count(1) as total from pull_requests where analisado = 0""") 
    dadoRestante = cursor.fetchone()


    mediaUltimasHoras = mediaUltimasTresHoras()


    percentualConcluido = round((dadoAnalisado['total']/dadoTotal['total'])*100,2)
    horasRestantes = dadoRestante['total'] / mediaUltimasHoras

    if(ultimaHora != 0):
        qtdDesdeUltimaAnalise = dadoAnalisado['total'] -  ultimaHora
        ultimaHora = dadoAnalisado['total']
    else:
        ultimaHora = dadoAnalisado['total']
        qtdDesdeUltimaAnalise = 0

    print("============= {} ================".format(datetime.datetime.now()))
    print("Percentual Concluido: {}%".format(percentualConcluido))
    print("Horas restantes: {}hs".format(round(horasRestantes,0)))
    print("Média ultimas 3 horas: {}".format(round(mediaUltimasHoras,0)))
    print("Itens Processados: {} ({})".format(round(dadoAnalisado['total'],0), qtdDesdeUltimaAnalise))
    print("Itens Restantes: {}".format(round(dadoRestante['total'],0)))
    print("=========================================================")
    print("")
    time.sleep(900)

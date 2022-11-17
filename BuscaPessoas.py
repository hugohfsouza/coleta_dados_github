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



cursor.execute(""" 
    create temporary table PRs_classificados_quantidade_prs_projeto select 
	user, 
	case
		WHEN qtdTeste > 0 and qtdCodigo = 0 and qtdOutros = 0 then 'Apenas Teste'
		WHEN qtdTeste = 0 and qtdCodigo > 0 and qtdOutros = 0 then 'Apenas Codigo'
		WHEN qtdTeste = 0 and qtdCodigo = 0 and qtdOutros > 0 then 'Apenas Codigo'
		WHEN qtdTeste > 0 and qtdCodigo > 0 and qtdOutros = 0 then 'Teste e Codigo'
		WHEN qtdTeste > 0 and qtdCodigo = 0 and qtdOutros > 0 then 'Teste e Codigo'
		WHEN qtdTeste = 0 and qtdCodigo > 0 and qtdOutros > 0 then 'Apenas Codigo'
		WHEN qtdTeste > 0 and qtdCodigo > 0 and qtdOutros > 0 then 'Teste e Codigo'
		WHEN qtdTeste = 0 and qtdCodigo = 0 and qtdOutros = 0 then 'Sem alteracoes'
	end as tipoContribuidor, 
    linguagemReferencia,
    qtdPrs
 from (
	 select 
		pr.user, 
        r.id,
        r.linguagemReferencia,
		sum(hasTest) as qtdTeste,
		sum(hasCode) as qtdCodigo,
		sum(hasOutros) as qtdOutros,
        count(1) as qtdPRs
	from pull_requests pr
		inner join repositorios r on (pr.repo_id = r.id)
	where 
		r.temTeste = 1
		and r.educacional = 0
		and pr.isBot = 0
	group by pr.user, r.id
) as tabelaAuxiliar;
""") 


def apresentar(dados, tipo):
    total = 0;
    for item in dados:
        total += item[0]



    print(" ============================== {} ==============================".format(tipo))
    for item in dados:
        porcentagem = item[0]/total

        # print(str(item[0])+"|"+ str(item[1])+"|"+str(porcentagem).replace(".",",") )
        print(str(item[0])+"|"+str(porcentagem).replace(".",",")+"|"+ str(item[1]))

         

    print("\n\n\n")


tipos = [
    'Apenas Teste',
    'Apenas Codigo',
    'Teste e Codigo'
]

linguagens = [ 'C', 'C#', 'C++', 'JAVA', 'Javascript', 'Python', 'Ruby' ]

for linguagem in linguagens:
    print("=============================== "+str(linguagem)+" =============================== ")
    for tipo in tipos:
        cursor.execute(""" 
            select 
                count(1), 
                qtdPrs
            from PRs_classificados_quantidade_prs_projeto
            # where tipoContribuidor = 'Apenas Teste'
            # where tipoContribuidor = 'Apenas Codigo'
            where tipoContribuidor = '"""+str(tipo)+"""'
            and linguagemReferencia = '"""+str(linguagem)+"""'
            group by qtdPrs
        """) 
        dados = cursor.fetchall()
        apresentar(dados, tipo)
        dados = []

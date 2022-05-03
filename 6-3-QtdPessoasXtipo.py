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
    create temporary table PRs_classificados2 select 
        pr.user, 
        pr.repo_id,
        r.linguagemReferencia,
        case
            WHEN sum(hasTest) > 0 and sum(hasCode) = 0 and sum(hasOutros) = 0 then 'Apenas Teste'
            WHEN sum(hasTest) = 0 and sum(hasCode) > 0 and sum(hasOutros) = 0 then 'Apenas Codigo'
            WHEN sum(hasTest) = 0 and sum(hasCode) = 0 and sum(hasOutros) > 0 then 'Apenas Codigo'
            WHEN sum(hasTest) > 0 and sum(hasCode) > 0 and sum(hasOutros) = 0 then 'Teste e Codigo'
            WHEN sum(hasTest) > 0 and sum(hasCode) = 0 and sum(hasOutros) > 0 then 'Teste e Codigo'
            WHEN sum(hasTest) = 0 and sum(hasCode) > 0 and sum(hasOutros) > 0 then 'Apenas Codigo'
            WHEN sum(hasTest) > 0 and sum(hasCode) > 0 and sum(hasOutros) > 0 then 'Teste e Codigo'
            WHEN sum(hasTest) = 0 and sum(hasCode) = 0 and sum(hasOutros) = 0 then 'Sem alteracoes'
        end as tipoContribuidor
    from pull_requests pr
        inner join repositorios r on (pr.repo_id = r.id)
    where 
        r.temTeste = 1
        and r.educacional = 0
        and pr.isBot = 0
    group by pr.user, pr.repo_id
""") 


# cursor.execute(""" 
#     create temporary table PRs_classificados2 select 
#         pr.user, 
#         case
#             WHEN sum(hasTest) > 0 and sum(hasCode) = 0 and sum(hasOutros) = 0 then 'Apenas Teste'
#             WHEN sum(hasTest) = 0 and sum(hasCode) > 0 and sum(hasOutros) = 0 then 'Apenas Codigo'
#             WHEN sum(hasTest) = 0 and sum(hasCode) = 0 and sum(hasOutros) > 0 then 'Apenas Outros'
#             WHEN sum(hasTest) > 0 and sum(hasCode) > 0 and sum(hasOutros) = 0 then 'Teste e Codigo'
#             WHEN sum(hasTest) > 0 and sum(hasCode) = 0 and sum(hasOutros) > 0 then 'Teste e Outros'
#             WHEN sum(hasTest) = 0 and sum(hasCode) > 0 and sum(hasOutros) > 0 then 'Codigo e Outros'
#             WHEN sum(hasTest) > 0 and sum(hasCode) > 0 and sum(hasOutros) > 0 then 'Teste, Codigo e Outros'
#             WHEN sum(hasTest) = 0 and sum(hasCode) = 0 and sum(hasOutros) = 0 then 'Sem alteracoes'
#         end as tipoContribuidor
#     from pull_requests pr
#         inner join repositorios r on (pr.repo_id = r.id)
#     where 
#         r.temTeste = 1
#         and r.educacional = 0
#         and pr.isBot = 0
#     group by pr.user;
# """) 



def apresentar(dados, tipo):
    total = 0;
    for item in dados:
        total += item[0]



    print(" ============================== {} ==============================".format(tipo))
    for item in dados:
        porcentagem = item[0]/total

        print(str(item[0])+"|"+ str(item[1])+"|"+str(porcentagem).replace(".",",") )

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
                totalProjetos
            from (
                select 
                    user, 
                    count(1) totalProjetos
                from PRs_classificados2 
                where tipoContribuidor = '"""+str(tipo)+"""'
                and linguagemReferencia = '"""+str(linguagem    )+"""'
                group by user
            ) as tabelaAuxiliar
            group by totalProjetos

        """) 
        dados = cursor.fetchall()
        apresentar(dados, tipo)
        dados = []

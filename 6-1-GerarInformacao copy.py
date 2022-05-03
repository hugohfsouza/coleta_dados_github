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



# print("Quantidade de projetos com teste e sem teste em todas as linguagems e no geral")
# qtdProjetosComTeste = PrettyTable()
# qtdProjetosComTeste.field_names = ["Linguagem", "Classificaçao", "Numero de Projetos", "% de projetos"]
# geralComTeste = 0
# geralSemTeste = 0

# for linguagem in linguagens:
#     cursor.execute(""" select count(1) from repositorios where linguagemReferencia = %s and (temTeste = 0 or temTeste is null) and educacional = 0""", (linguagem,)) 
#     dadoSemTeste = cursor.fetchone()

#     cursor.execute(""" select count(1) from repositorios where linguagemReferencia = %s and temTeste = 1 and educacional = 0""", (linguagem,)) 
#     dadoComTeste = cursor.fetchone()

#     total = dadoComTeste[0] + dadoSemTeste[0]

#     qtdProjetosComTeste.add_row([linguagem, "Com Teste", dadoComTeste[0] , (dadoComTeste[0]/total)*100 ])
#     qtdProjetosComTeste.add_row([linguagem, "Sem Teste", dadoSemTeste[0] , (dadoSemTeste[0]/total)*100 ])

# print(qtdProjetosComTeste)


# print("\n\n\n\n")
# print("Quantidade de projetos com teste e sem teste em todas as linguagems e no geral APENAS PROJETOS  EDUCACIONAIS")
# projetosEducacionais = PrettyTable()
# projetosEducacionais.field_names = ["Linguagem", "Classificaçao", "Numero de Projetos", "% de projetos"]
# geralComTeste = 0
# geralSemTeste = 0

# for linguagem in linguagens:
#     cursor.execute(""" select count(1) from repositorios where linguagemReferencia = %s and (temTeste = 0 or temTeste is null) and educacional = 1""", (linguagem,)) 
#     dadoSemTeste = cursor.fetchone()

#     cursor.execute(""" select count(1) from repositorios where linguagemReferencia = %s and temTeste = 1 and educacional = 1""", (linguagem,)) 
#     dadoComTeste = cursor.fetchone()

#     total = dadoComTeste[0] + dadoSemTeste[0]

#     projetosEducacionais.add_row([linguagem, "Com Teste", dadoComTeste[0] , (dadoComTeste[0]/total)*100 ])
#     projetosEducacionais.add_row([linguagem, "Sem Teste", dadoSemTeste[0] , (dadoSemTeste[0]/total)*100 ])

# print(projetosEducacionais)



# Linguagem | Categoria | # TOTAL DE PRs | # PRs aceitas | % PRs aceitas
print("\n\n\n\n")
print("Linguagem | Categoria | # TOTAL DE PRs | # PRs aceitas | % PRs aceitas")
projetosEducacionais = PrettyTable()
projetosEducacionais.field_names = ["Linguagem", "Classificaçao", "TOTAL PRs", "Total PRs Aceitas" , "% de PRs aprovadas"]
geralComTeste = 0
geralSemTeste = 0

for linguagem in linguagens:
    
    # Apenas Teste
    cursor.execute("""
        select COUNT(1) from pull_requests pr
            inner join repositorios r on (pr.repo_id = r.id)
            where r.linguagemReferencia = %s
            AND PR.hasCode = 0
            and pr.hasTest = 1
            and pr.hasOutros = 0
            and r.educacional = 0
            and pr.isBot = 0
                
    """, (linguagem,)) 
    dadosApenasTeste = cursor.fetchone()

    # Apenas Teste APROVADO
    cursor.execute("""
        select COUNT(1) from pull_requests pr
            inner join repositorios r on (pr.repo_id = r.id)
            where r.linguagemReferencia = %s
            AND PR.hasCode = 0
            and pr.hasTest = 1
            and pr.hasOutros = 0
            and r.educacional = 0
            and pr.merged_at is not null
            and pr.isBot = 0
                
    """, (linguagem,)) 
    dadosApenasTesteAprovado = cursor.fetchone()

    # Apenas Codigo
    cursor.execute("""
        select COUNT(1) from pull_requests pr
            inner join repositorios r on (pr.repo_id = r.id)
            where r.linguagemReferencia = %s
            AND PR.hasCode = 1
            and pr.hasTest = 0
            and pr.hasOutros = 0
            and r.educacional = 0
            and pr.isBot = 0
                
    """, (linguagem,)) 
    dadosApenasCodigo = cursor.fetchone()

    # Apenas Codigo APROVADO
    cursor.execute("""
        select COUNT(1) from pull_requests pr
            inner join repositorios r on (pr.repo_id = r.id)
            where r.linguagemReferencia = %s
            AND PR.hasCode = 1
            and pr.hasTest = 0
            and pr.hasOutros = 0
            and r.educacional = 0
            and pr.merged_at is not null
            and pr.isBot = 0
                
    """, (linguagem,)) 
    dadosApenasCodigoAprovado = cursor.fetchone()


    # Apenas Outros
    cursor.execute("""
        select COUNT(1) from pull_requests pr
            inner join repositorios r on (pr.repo_id = r.id)
            where r.linguagemReferencia = %s
            AND PR.hasCode = 0
            and pr.hasTest = 0
            and pr.hasOutros = 1
            and r.educacional = 0
            and pr.isBot = 0
                
    """, (linguagem,)) 
    dadosApenasOutros = cursor.fetchone()

    # Apenas Outros APROVADO
    cursor.execute("""
        select COUNT(1) from pull_requests pr
            inner join repositorios r on (pr.repo_id = r.id)
            where r.linguagemReferencia = %s
            AND PR.hasCode = 0
            and pr.hasTest = 0
            and pr.hasOutros = 1
            and r.educacional = 0
            and pr.merged_at is not null
            and pr.isBot = 0
                
    """, (linguagem,)) 
    dadosApenasOutrosAprovado = cursor.fetchone()


    # Teste e Codigo ok
    cursor.execute("""
        select COUNT(1) from pull_requests pr
            inner join repositorios r on (pr.repo_id = r.id)
            where r.linguagemReferencia = %s
            AND PR.hasCode = 1
            and pr.hasTest = 1
            and pr.hasOutros = 0
            and r.educacional = 0
            and pr.isBot = 0
                
    """, (linguagem,)) 
    dadosTesteCodigo = cursor.fetchone()

    # Teste e Codigo ok APROVADO
    cursor.execute("""
        select COUNT(1) from pull_requests pr
            inner join repositorios r on (pr.repo_id = r.id)
            where r.linguagemReferencia = %s
            AND PR.hasCode = 1
            and pr.hasTest = 1
            and pr.hasOutros = 0
            and r.educacional = 0
            and pr.merged_at is not null
            and pr.isBot = 0
                
    """, (linguagem,)) 
    dadosTesteCodigoAprovado = cursor.fetchone()


    # TESTE E OUTROS
    cursor.execute("""
        select COUNT(1) from pull_requests pr
            inner join repositorios r on (pr.repo_id = r.id)
            where r.linguagemReferencia = %s
            AND PR.hasCode = 0
            and pr.hasTest = 1
            and pr.hasOutros = 1
            and r.educacional = 0
            and pr.isBot = 0
                
    """, (linguagem,)) 
    dadosTesteOutros = cursor.fetchone()

    # TESTE E OUTROS APROVADO
    cursor.execute("""
        select COUNT(1) from pull_requests pr
            inner join repositorios r on (pr.repo_id = r.id)
            where r.linguagemReferencia = %s
            AND PR.hasCode = 0
            and pr.hasTest = 1
            and pr.hasOutros = 1
            and r.educacional = 0
            and pr.merged_at is not null
            and pr.isBot = 0
                
    """, (linguagem,)) 
    dadosTesteOutrosAprovado = cursor.fetchone()

    # Codigo E OUTROS
    cursor.execute("""
        select COUNT(1) from pull_requests pr
            inner join repositorios r on (pr.repo_id = r.id)
            where r.linguagemReferencia = %s
            AND PR.hasCode = 1
            and pr.hasTest = 0
            and pr.hasOutros = 1
            and r.educacional = 0
            and pr.isBot = 0
                
    """, (linguagem,)) 
    dadosCodigoOutros = cursor.fetchone()

    # Codigo E OUTROS APROVADO
    cursor.execute("""
        select COUNT(1) from pull_requests pr
            inner join repositorios r on (pr.repo_id = r.id)
            where r.linguagemReferencia = %s
            AND PR.hasCode = 1
            and pr.hasTest = 0
            and pr.hasOutros = 1
            and r.educacional = 0
            and pr.merged_at is not null
            and pr.isBot = 0
                
    """, (linguagem,)) 
    dadosCodigoOutrosAprovado = cursor.fetchone()



    # Com teste ok
    # Com codigo ok
    # Outros ok

    # Teste e cODIGO ok
    # TESTE E OUTROS ok
    # CODIGO E OUTROS

    
    total = dadosApenasTeste[0] + dadosApenasCodigo[0] + dadosApenasOutros[0] + dadosTesteCodigo[0] + dadosTesteOutros[0] + dadosCodigoOutros[0]

    projetosEducacionais.field_names = ["Linguagem", "Classificaçao", "TOTAL PRs", "Total PRs Aceitas" , "% de PRs aprovadas"]

    
    projetosEducacionais.add_row([linguagem, "Apenas Teste",    dadosApenasTeste[0], dadosApenasTesteAprovado[0] , (dadosApenasTesteAprovado[0]/ dadosApenasTeste[0])*100 ])
    projetosEducacionais.add_row([linguagem, "Apenas Codigo",   dadosApenasCodigo[0], dadosApenasCodigoAprovado[0] , (dadosApenasCodigoAprovado[0]/ dadosApenasCodigo[0])*100 ])
    projetosEducacionais.add_row([linguagem, "Apenas Outros",   dadosApenasOutros[0], dadosApenasOutrosAprovado[0] , (dadosApenasOutrosAprovado[0]/ dadosApenasOutros[0])*100 ])
    projetosEducacionais.add_row([linguagem, "Teste e Codigo",  dadosTesteCodigo[0], dadosTesteCodigoAprovado[0] , (dadosTesteCodigoAprovado[0]/ dadosTesteCodigo[0])*100 ])
    projetosEducacionais.add_row([linguagem, "Teste e Outros",  dadosTesteOutros[0], dadosTesteOutrosAprovado[0] , (dadosTesteOutrosAprovado[0]/ dadosTesteOutros[0])*100 ])
    projetosEducacionais.add_row([linguagem, "Codigo e Outros", dadosCodigoOutros[0], dadosCodigoOutrosAprovado[0] , (dadosCodigoOutrosAprovado[0]/ dadosCodigoOutros[0])*100 ])

print(projetosEducacionais)

# Linguagem | Apenas Teste | Apenas Codigo | Codigo e teste




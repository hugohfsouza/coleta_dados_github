import mysql.connector
import configparser
from tqdm import tqdm

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


def retornarRepositorios(user):
    cursor.execute("""
        select distinct r.id, r.nameWithOwner from repositorios r
        inner join pull_requests pr on (r.id = pr.repo_id)
        where pr.user = %s
        and r.educacional = 0
        and r.temTeste = 1
        and pr.isBot = 1
    """, (user, )) 
    repositorios = cursor.fetchall()
    return repositorios

def calculaTotalPRs(user, repo_id):
    totalPRs            = 0
    totalPRsAceitas     = 0
    cursor.execute("select id, merged_at from pull_requests where user = '"+str(user)+"' and repo_id = "+str(repo_id)) 
    pullRequests = cursor.fetchall()
    for item in pullRequests:
        totalPRs += 1
        if(item['merged_at']):
            totalPRsAceitas += 1
    return totalPRs, totalPRsAceitas

def verificaOsHas(user,repo_id):
    temCodigo = 0
    temTeste  = 0
    temOutros = 0
    # print("{}, {}".format(user, repo_id))
    cursor.execute("select sum(hasTest) as temTeste, sum(hasCode) as temCodigo, sum(hasOutros) as temOutros from pull_requests where user = %s and repo_id =%s", (user, repo_id)) 
    pullRequests = cursor.fetchone()
    if(int(pullRequests['temCodigo']) > 0):
        temCodigo = 1
    if(pullRequests['temTeste'] > 0):
        temTeste = 1
    if(pullRequests['temOutros'] > 0):
        temOutros = 1

    return temCodigo, temTeste, temOutros

def verificaQtdArq(user,repo_id):
    qtdArqTest      = 0
    qtdArqCode      = 0
    qtdArqOutros    = 0
    cursor.execute("select sum(qtdArqTest) as qtdArqTest, sum(qtdArqCode) as qtdArqCode, sum(qtdArqOutros) as qtdArqOutros  from pull_requests where user = %s and repo_id =%s", (user, repo_id)) 
    pullRequests = cursor.fetchone()    
    
    qtdArqTest      = pullRequests['qtdArqTest']
    qtdArqCode      = pullRequests['qtdArqCode']
    qtdArqOutros    = pullRequests['qtdArqOutros']

    return qtdArqTest, qtdArqCode, qtdArqOutros


def devificarQtdPRs(user,repo_id):
    qtdPRsTeste         = 0
    qtdPRsTesteAceitas  = 0
    
    qtdPRsCodigo            = 0
    qtdPRsCodigoAceitas     = 0
    
    qtdPRsOutros            = 0
    qtdPRsOutrosAceitas     = 0

    qtdPRsTesteCodigo           = 0 
    qtdPRsTesteCodigoAceitas    = 0 

    qtdPRsCodigoOutros          = 0
    qtdPRsCodigoOutrosAceitas   = 0

    qtdPRsTesteOutros           = 0
    qtdPRsTesteOutrosAceitas    = 0

    qtdPRsCodigoTesteOutros         = 0
    qtdPRsCodigoTesteOutrosAceitas  = 0


    cursor.execute("select id, merged_at, hasTest, hasCode, hasOutros  from pull_requests where user = %s and repo_id = %s", (user, repo_id)) 
    # cursor.execute("select id, merged_at, hasTest, hasCode, hasOutros  from pull_requests where repo_id =1080") 
    pullRequests = cursor.fetchall()   

    for pr in pullRequests:
        # Só teste
        if( pr['hasTest'] > 0 and pr['hasCode'] == 0 and pr['hasOutros'] == 0 ):
            qtdPRsTeste += 1
            if(pr['merged_at']):
                qtdPRsTesteAceitas += 1

        # Só codigo
        if( pr['hasTest'] == 0 and pr['hasCode'] > 0 and pr['hasOutros'] == 0 ):
            qtdPRsCodigo += 1
            if(pr['merged_at']):
                qtdPRsCodigoAceitas += 1

        # Só outros
        if( pr['hasTest'] == 0 and pr['hasCode'] == 0 and pr['hasOutros'] > 0 ):
            qtdPRsOutros += 1
            if(pr['merged_at']):
                qtdPRsOutrosAceitas += 1

        # CODIGO E TESTE
        if( pr['hasTest'] > 0 and pr['hasCode'] > 0 and pr['hasOutros']  == 0 ):
            qtdPRsTesteCodigo += 1
            if(pr['merged_at']):
                qtdPRsTesteCodigoAceitas += 1


        # CODIGO E OUTROS
        if( pr['hasTest'] == 0 and pr['hasCode'] > 0 and pr['hasOutros']  > 0 ):
            qtdPRsCodigoOutros += 1
            if(pr['merged_at']):
                qtdPRsCodigoOutrosAceitas += 1

        # TESTE E OUTROS
        if( pr['hasTest'] > 0 and pr['hasCode'] == 0 and pr['hasOutros']  > 0 ):
            qtdPRsTesteOutros += 1
            if(pr['merged_at']):
                qtdPRsTesteOutrosAceitas += 1

        # CODIGO, TESTE E OUTROS
        if( pr['hasTest'] > 0 and pr['hasCode'] > 0 and pr['hasOutros']  > 0 ):
            qtdPRsCodigoTesteOutros += 1
            if(pr['merged_at']):
                qtdPRsCodigoTesteOutrosAceitas += 1

    retorno = {
        'teste': {
            'total': qtdPRsTeste,
            'aceitas': qtdPRsTesteAceitas
        },
        'codigo': {
            'total': qtdPRsCodigo,
            'aceitas': qtdPRsCodigoAceitas
        },
        'outros': {
            'total': qtdPRsOutros,
            'aceitas': qtdPRsOutrosAceitas
        },

        'codigoTeste': {
            'total': qtdPRsTesteCodigo,
            'aceitas': qtdPRsTesteCodigoAceitas
        },

        'codigoOutros': {
            'total': qtdPRsCodigoOutros,
            'aceitas': qtdPRsCodigoOutrosAceitas
        },

        'testeOutros': {
            'total': qtdPRsTesteOutros,
            'aceitas': qtdPRsTesteOutrosAceitas
        },

        'codigoTesteOutros': {
            'total': qtdPRsCodigoTesteOutros,
            'aceitas': qtdPRsCodigoTesteOutrosAceitas
        },
    }   

    return retorno
    





cursor.execute("""select distinct user from pull_requests where user not in ('aio-libs-github-bot[bot]', 'allcontributors[bot]', 'alluxio-bot', 'awesomerobot', 'azure-pipelines[bot]', 'backporting[bot]', 'blitzjs-bot[bot]', 'bridgecrew-develop[bot]', 'camperbot', 'chef-expeditor[bot]', 'CocosRobot', 'codesee-architecture-diagrams[bot]', 'copybara-service[bot]', 'deepsource-autofix[bot]', 'dependabot-preview[bot]', 'dependabot[bot]', 'depfu[bot]', 'dotnet-bot', 'Dotnet-GitSync-Bot', 'dotnet-maestro-bot', 'dotnet-maestro[bot]', 'edx-cache-uploader-bot', 'edx-requirements-bot', 'edx-status-bot', 'electron-bot', 'electron-roller[bot]', 'fit2bot', 'frappe-pr-bot', 'fw-bot', 'gcf-owl-bot[bot]', 'github-actions[bot]', 'gitlocalize-app[bot]', 'google-cloud-policy-bot[bot]', 'greenkeeperio-bot', 'greenkeeper[bot]', 'imgbot[bot]', 'iptv-bot[bot]', 'lingohub[bot]', 'meeseeksdev[bot]', 'mergify[bot]', 'metersphere-bot', 'node-migrator-bot', 'nodejs-github-bot', 'openapi-sdkautomation[bot]', 'p42-ai[bot]', 'patchback[bot]', 'pre-commit-ci[bot]', 'prettierci[bot]', 'pull[bot]', 'pyup-bot', 'qgis-bot', 'release-please[bot]', 'renovate-bot', 'renovate[bot]', 'restyled-io[bot]', 'reunion-maestro[bot]', 'robot-clickhouse', 'servarr[bot]', 'snyk-bot', 'sonatypeoss[bot]', 'sourcery-ai[bot]', 'spyder-bot', 'stickler-ci[bot]', 'transifex-integration[bot]', 'trax-robot', 'trop-devel[bot]', 'trop[bot]', 'vue-bot', 'whitesource-bolt-for-github[bot]', 'whitesource-for-github-com[bot]')""") 
usuarios = cursor.fetchall()

print("iniciando....")
totalUsers = 0
for x in usuarios:
    totalUsers += 1


with tqdm(total=totalUsers) as pbar:
    for usuario in usuarios:
        for repositorio in retornarRepositorios(usuario['user']):
            totalPRs, totalPRsAceitas = calculaTotalPRs(usuario['user'], repositorio['id'])   
            temCodigo, temTeste, temOutros = verificaOsHas(usuario['user'], repositorio['id'])   
            qtdArqTest, qtdArqCode, qtdArqOutros = verificaQtdArq(usuario['user'], repositorio['id'])
            dados = devificarQtdPRs(usuario['user'], repositorio['id'])

            cursor.execute("""
                INSERT INTO contribuidores
                (
                usuario,
                repo_id,
                qtdPRsTotal,
                qtdPRsAceitas,
                temCodigo,
                temTeste,
                temOutros,
                qtdArquivosTeste,
                qtdArquivosCodigo,
                qtdArquivosOutros,
                qtdPRsTeste,
                qtdPRsTesteAceita,
                qtdPRsCodigo,
                qtdPRsCodigoAceita,
                qtdPRsOutros,
                qtdPRsOutrosAceita,
                qtdPRsTesteCodigo,
                qtdPRsTesteCodigoAceita,
                qtdPRsCodigoOutros,
                qtdPRsCodigoOutrosAceita,
                qtdPRsTesteOutros,
                qtdPRsTesteOutrosAceita,
                qtdPRsTesteCodigoOutros,
                qtdPRsTesteCodigoOutrosAceita)
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """, (
                usuario['user'],
                repositorio['id'],
                totalPRs,
                totalPRsAceitas,
                temCodigo,
                temTeste,
                temOutros,
                qtdArqTest,
                qtdArqCode,
                qtdArqOutros,
                dados['teste']['total'],
                dados['teste']['aceitas'],
                dados['codigo']['total'],
                dados['codigo']['aceitas'],
                dados['outros']['total'],
                dados['outros']['aceitas'],
                dados['codigoTeste']['total'],
                dados['codigoTeste']['aceitas'],
                dados['codigoOutros']['total'],
                dados['codigoOutros']['aceitas'],
                dados['testeOutros']['total'],
                dados['testeOutros']['aceitas'],
                dados['codigoTesteOutros']['total'],
                dados['codigoTesteOutros']['aceitas'],
            ))
            conn.commit() 

        pbar.update(1)
/*
CREATE TABLE prs_classificados_teste (
  `user` VARCHAR(200) NOT NULL,
  `repo_id` INT NOT NULL,
  `linguagemReferencia` VARCHAR(200) NULL,
  `tipoContribuidor` VARCHAR(200) NULL,
  PRIMARY KEY (`user`, `repo_id`),
  INDEX `ix_repo_id` (`repo_id` ASC),
  INDEX `ix_classificacao` (`tipoContribuidor` ASC));
*/

# truncate table PRs_classificados_teste;

# DE MANEIRA POR PROJETO, para cada classificação quantas pessoas 
insert prs_classificados_teste select 
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


# DE MANEIRA POR PROJETO, para cada classificação quantas pessoas 
select 
	count(1), 
    totalProjetos 
from (
	select 
		user, 
        tipoContribuidor,
		count(1) totalProjetos
	from PRs_classificados_teste 
	where tipoContribuidor = 'Apenas Teste'
	# where tipoContribuidor ='Apenas Codigo'
	# where tipoContribuidor ='Teste e Codigo'
	group by user
) as tabelaAuxiliar
group by totalProjetos


############################################################################################### ESCOPO GERAL
drop table PRs_classificados_qtd_contribuidores;
create temporary table PRs_classificados_qtd_contribuidores select 
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
	end as tipoContribuidor
 from (
	 select 
		pr.user, 
		sum(hasTest) as qtdTeste,
		sum(hasCode) as qtdCodigo,
		sum(hasOutros) as qtdOutros
	from pull_requests pr
		inner join repositorios r on (pr.repo_id = r.id)
	where 
		r.temTeste = 1
		and r.educacional = 0
		and pr.isBot = 0
	group by pr.user
) as tabelaAuxiliar;

# DE MANEIRA POR PROJETO, para cada classificação quantas pessoas 
select 
	tipoContribuidor,
	count(1) totalPessoas
from PRs_classificados_qtd_contribuidores 
group by tipoContribuidor;
	
############################################################################################### ESCOPO GERAL: quantidade de PRs feitas para cada tipo
drop table PRs_classificados_quantidade_prs;
create temporary table PRs_classificados_quantidade_prs select 
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
    qtdPrs
 from (
	 select 
		pr.user, 
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
	group by pr.user
) as tabelaAuxiliar;


select 
	count(1), 
    user,
    qtdPrs
from PRs_classificados_quantidade_prs
 where tipoContribuidor = 'Apenas Teste'
# where tipoContribuidor = 'Apenas Codigo'
# where tipoContribuidor = 'Teste e Codigo'
group by qtdPrs,user



############################################################################################### ESCOPO GERAL: quantidade de PRs feitas para cada tipo POR LINGUAGEM
drop table PRs_classificados_quantidade_prs_projeto;
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

select 
	count(1), 
    qtdPrs
from PRs_classificados_quantidade_prs_projeto
# where tipoContribuidor = 'Apenas Teste'
# where tipoContribuidor = 'Apenas Codigo'
 where tipoContribuidor = '"""+str(tipo)+"""'
 and linguagemReferencia = '"""+str(linguagem    )+"""'
group by qtdPrs

# quatidade de projetos por linguagem
select linguagemReferencia, count(1) from pull_requests pr 
inner join repositorios r on (r.id = pr.repo_id)
where
r.temTeste = 1
group by linguagemReferencia;

select * from repositorios where nameWithOwner like '%redisson%'



#identificação de usuarios bots
select pr.user from pull_requests pr 
inner join repositorios r on (r.id = pr.repo_id)
where
r.temTeste = 1
and r.educacional = 0
and pr.isBot = 0
group by pr.user;



# Quantos projetos com teste
select 
	r1.linguagemReferencia, 
    count(1),
    (select count(1) from repositorios as r2 where r1.linguagemReferencia = r2.linguagemReferencia and educacional = 0) as totalRepositorios,
     count(1) / (select count(1) from repositorios as r2 where r1.linguagemReferencia = r2.linguagemReferencia and educacional = 0) as porcentagem
    from repositorios as r1
	where r1.temTeste = 1
    AND r1.educacional = 0
    group by r1.linguagemReferencia
    
    
# quantos projetos de ensino
select 
	r1.linguagemReferencia, 
    r1.temTeste,
    count(1),
    (select count(1) from repositorios as r2 where r1.linguagemReferencia = r2.linguagemReferencia) as totalRepositorios,
     (count(1) / (select count(1) from repositorios as r2 where r1.linguagemReferencia = r2.linguagemReferencia))*100 as porcentagem
    from repositorios as r1
	where r1.educacional = 1
    and r1.temTeste = 1
    group by r1.linguagemReferencia, r1.temTeste
    
    
#Base de dados final: Total de projetos
select linguagemReferencia, count(1) from  repositorios
where temTeste = 1
and educacional = 0
group by linguagemReferencia;

#Base de dados final: Total de PRs
select linguagemReferencia, count(1) from pull_requests pr 
inner join repositorios r on (r.id = pr.repo_id)
where
r.temTeste = 1
and r.educacional = 0
and pr.isBot = 0 
group by linguagemReferencia;

#Base de dados final: Total de contribuidores
select distinct pr.user from pull_requests pr 
inner join repositorios r on (r.id = pr.repo_id)
where
r.temTeste = 1
and r.educacional = 0
and pr.isBot = 0




select r.nameWithOwner, r.id, count(1) from pull_requests pr 
inner join repositorios r on (r.id = pr.repo_id)
where
r.temTeste = 1
and r.educacional = 0
and pr.isBot = 0 
group by r.nameWithOwner, r.id;



#Tempo médio até que a PR seja aprovada
select linguagemReferencia, tipoPR, FORMAT(avg(diffEmHoras),2, "pt_BR") from (
	select 
		pr.id,
		merged_at, 
		created_at, 
		TIMESTAMPDIFF(HOUR, created_at, merged_at) as diffEmHoras,
		r.linguagemReferencia,
        case
			WHEN hasTest > 0 and hasCode = 0 and hasOutros = 0 then 'Apenas Teste'
				WHEN hasTest = 0 and hasCode > 0 and hasOutros = 0 then 'Apenas Codigo'
				WHEN hasTest = 0 and hasCode = 0 and hasOutros > 0 then 'Apenas Codigo'
				WHEN hasTest > 0 and hasCode > 0 and hasOutros = 0 then 'Teste e Codigo'
				WHEN hasTest > 0 and hasCode = 0 and hasOutros > 0 then 'Teste e Codigo'
				WHEN hasTest = 0 and hasCode > 0 and hasOutros > 0 then 'Apenas Codigo'
				WHEN hasTest > 0 and hasCode > 0 and hasOutros > 0 then 'Teste e Codigo'
				WHEN hasTest = 0 and hasCode = 0 and hasOutros = 0 then 'Sem alteracoes'
        end as tipoPR
	from pull_requests pr
		inner join repositorios r on (pr.repo_id = r.id)
		where r.temTeste = 1
		and r.educacional = 0
		and pr.isBot = 0
        and merged_at is not null
) as tabelaAux
group by linguagemReferencia, tipoPR

#Tempo médio até que a PR seja aprovada: GERAL
select tipoPR, FORMAT(avg(diffEmHoras),2, "pt_BR") from (
	select 
		pr.id,
		merged_at, 
		created_at, 
		TIMESTAMPDIFF(HOUR, created_at, merged_at) as diffEmHoras,
		r.linguagemReferencia,
        case
			WHEN hasTest > 0 and hasCode = 0 and hasOutros = 0 then 'Apenas Teste'
				WHEN hasTest = 0 and hasCode > 0 and hasOutros = 0 then 'Apenas Codigo'
				WHEN hasTest = 0 and hasCode = 0 and hasOutros > 0 then 'Apenas Codigo'
				WHEN hasTest > 0 and hasCode > 0 and hasOutros = 0 then 'Teste e Codigo'
				WHEN hasTest > 0 and hasCode = 0 and hasOutros > 0 then 'Teste e Codigo'
				WHEN hasTest = 0 and hasCode > 0 and hasOutros > 0 then 'Apenas Codigo'
				WHEN hasTest > 0 and hasCode > 0 and hasOutros > 0 then 'Teste e Codigo'
				WHEN hasTest = 0 and hasCode = 0 and hasOutros = 0 then 'Sem alteracoes'
        end as tipoPR
	from pull_requests pr
		inner join repositorios r on (pr.repo_id = r.id)
		where r.temTeste = 1
		and r.educacional = 0
		and pr.isBot = 0
        and merged_at is not null
) as tabelaAux
group by tipoPR




# qtd de PRs aceitos nos diferentes tipos de PR
select linguagemReferencia, tipoPR, count(1), count(merged_at) from (
	select 
			r.linguagemReferencia,
			case
				WHEN hasTest > 0 and hasCode = 0 and hasOutros = 0 then 'Apenas Teste'
				WHEN hasTest = 0 and hasCode > 0 and hasOutros = 0 then 'Apenas Codigo'
				WHEN hasTest = 0 and hasCode = 0 and hasOutros > 0 then 'Apenas Codigo'
				WHEN hasTest > 0 and hasCode > 0 and hasOutros = 0 then 'Teste e Codigo'
				WHEN hasTest > 0 and hasCode = 0 and hasOutros > 0 then 'Teste e Codigo'
				WHEN hasTest = 0 and hasCode > 0 and hasOutros > 0 then 'Apenas Codigo'
				WHEN hasTest > 0 and hasCode > 0 and hasOutros > 0 then 'Teste e Codigo'
				WHEN hasTest = 0 and hasCode = 0 and hasOutros = 0 then 'Sem alteracoes'
			end as tipoPR,
			merged_at 
		from pull_requests pr
			inner join repositorios r on (pr.repo_id = r.id)
			where r.temTeste = 1
			and r.educacional = 0
			and pr.isBot = 0
) as tabelaAux
group by linguagemReferencia, tipoPR


# qtd de pessoas que contribuiram para cada quantidade de projetos: ESCOPO GERAL
select 
	user,
    repo_id,
	case
		WHEN hasTest > 0 and hasCode = 0 and hasOutros = 0 then 'Apenas Teste'
		WHEN hasTest = 0 and hasCode > 0 and hasOutros = 0 then 'Apenas Codigo'
		WHEN hasTest = 0 and hasCode = 0 and hasOutros > 0 then 'Apenas Outros'
		WHEN hasTest > 0 and hasCode > 0 and hasOutros = 0 then 'Teste e Codigo'
		WHEN hasTest > 0 and hasCode = 0 and hasOutros > 0 then 'Teste e Outros'
		WHEN hasTest = 0 and hasCode > 0 and hasOutros > 0 then 'Codigo e Outros'
		WHEN hasTest > 0 and hasCode > 0 and hasOutros > 0 then 'Teste, Codigo e Outros'
		WHEN hasTest = 0 and hasCode = 0 and hasOutros = 0 then 'Sem alteracoes'
	end as tipoContribuidor
from (
	select 
		user, 
        repo_id,
		sum(hasCode) as hasCode,
		sum(hasTest) as hasTest,
		sum(hasOutros) as hasOutros
	from pull_requests
    group by user, repo_id
) as tabelaAuxiliar;


select qtdRepos, count(1) from (
    select user, count(1) as qtdRepos from (
		   select 
				user, 
				repo_id,
				case
					WHEN sum(hasTest) > 0 and sum(hasCode) = 0 and sum(hasOutros) = 0 then 'Apenas Teste'
					WHEN sum(hasTest) = 0 and sum(hasCode) > 0 and sum(hasOutros) = 0 then 'Apenas Codigo'
					WHEN sum(hasTest) = 0 and sum(hasCode) = 0 and sum(hasOutros) > 0 then 'Apenas Outros'
					WHEN sum(hasTest) > 0 and sum(hasCode) > 0 and sum(hasOutros) = 0 then 'Teste e Codigo'
					WHEN sum(hasTest) > 0 and sum(hasCode) = 0 and sum(hasOutros) > 0 then 'Teste e Outros'
					WHEN sum(hasTest) = 0 and sum(hasCode) > 0 and sum(hasOutros) > 0 then 'Codigo e Outros'
					WHEN sum(hasTest) > 0 and sum(hasCode) > 0 and sum(hasOutros) > 0 then 'Teste, Codigo e Outros'
					WHEN sum(hasTest) = 0 and sum(hasCode) = 0 and sum(hasOutros) = 0 then 'Sem alteracoes'
				end as tipoContribuidor
			from pull_requests
			group by user, repo_id
		) as tabelaAuxiliar
		where tipoContribuidor = 'Apenas Outros'
		group by user
) tabelaAuxiliar2
group by qtdRepos



select pr.user from pull_requests pr 
inner join repositorios r on (r.id = pr.repo_id)
where
r.temTeste = 1
and r.educacional = 0
and pr.isBot = 0




# quantidade de projetos que cada contribuidor participou: Mais de um e igual a um
select user, count(1) from (
	select pr.user, pr.repo_id from pull_requests pr 
	inner join repositorios r on (r.id = pr.repo_id)
	where
	r.temTeste = 1
	and r.educacional = 0
	and pr.isBot = 0
	group by pr.user, pr.repo_id
) as tabelaAuxiliar 
group by user
having count(1) > 1






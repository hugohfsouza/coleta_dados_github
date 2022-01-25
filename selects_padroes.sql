-- Qtd de repositorios recuperados por linguagem
select linguagemReferencia, count(1) from repositorios group by linguagemReferencia



select 
    DATE_FORMAT(datetime_analisado, '%d/%m/%Y %H:%i'),
    count(1) 
from pull_requests 
where analisado = 1 
group by  DATE_FORMAT(datetime_analisado, '%d/%m/%Y %H:%i')
order by DATE_FORMAT(datetime_analisado, '%d/%m/%Y %H:%i') desc
1. Subir um servico do RabbitMQ

# latest RabbitMQ 3.13 - https://www.rabbitmq.com/docs/download
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management

2. aplicar alteracoes na base (change_database.sql)

3. executar o 1-PRFiles-Produtor.py

4. Executar o 2-PRFiles-Consumidor.py
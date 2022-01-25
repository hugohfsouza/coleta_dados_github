import configparser
import json
import time
import mysql.connector

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

cursor.execute("FLUSH QUERY CACHE;")
cursor.execute("RESET QUERY CACHE;")
cursor.execute("""select repo_id, number, count(1) from pull_requests group by repo_id, number having count(1)>1 """)

count = 0
itens = cursor.fetchall()

for item in itens:
    cursor.execute("""select id from pull_requests where repo_id = %s and number = %s order by id desc limit 1""", (item['repo_id'], item['number']) )
    dadosItem = cursor.fetchone()

    itemDeletado = dadosItem['id']
    cursor.execute("""delete from pull_requests where id = %s """, (dadosItem['id'],))
    conn.commit()

    print(itemDeletado)
    


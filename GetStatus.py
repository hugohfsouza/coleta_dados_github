import requests
import json
import time
import mysql.connector
import configparser
import math
import sys

	


class GetStatus():
    def __init__(self):
        config = configparser.ConfigParser(allow_no_value=True)
        config.read("config.ini")

        dbconfig = {
            "host":     config.get("MYSQL", "host"),
            "user":     config.get("MYSQL", "user"),
            "passwd":   config.get("MYSQL", "passwd"),
            "db":       config.get("MYSQL", "db"),
        }

        self.conn = mysql.connector.connect(pool_name = "mypool", pool_size = 1,**dbconfig)
        self.cursor = self.conn.cursor(dictionary=True);


    def getStatusRequest(self, token):
        retorno = 0;
        self.cursor.execute("FLUSH QUERY CACHE;")
        self.cursor.execute("RESET QUERY CACHE;")
        linhas = self.cursor.execute("""select * from startstop where token = %s limit 1;""", (token, ) )
        for linha in self.cursor.fetchall():
            retorno = linha
        return retorno;

from ast import Try
import re
from unittest import result
import requests
import json
import time
import configparser
import mysql.connector
import sys


config = configparser.ConfigParser(allow_no_value=True)
config.read("../config.ini")


periodosSequencia = {}

dbconfig = {
	"host":     config.get("MYSQL", "host"),
	"user":     config.get("MYSQL", "user"),
	"passwd":   config.get("MYSQL", "passwd"),
	"db":       config.get("MYSQL", "db"),
}

class Dados():
    def __init__(self):
        pass


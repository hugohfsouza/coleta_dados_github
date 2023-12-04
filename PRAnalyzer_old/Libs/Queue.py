#!/usr/bin/env python
import pika
import sys


class Sender():

    def __init__(self, nomeFila):
        self.nomeFila = nomeFila
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.nomeFila, durable=True)

    def send(self, message, showMessage = True):
        
        
        self.channel.basic_publish(
            exchange='',
            routing_key=self.nomeFila,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        if(showMessage):
            print(" [x] send to queue: "+str(self.nomeFila)+" %r" % message)
    

    def closeConnection(self):
        self.connection.close()
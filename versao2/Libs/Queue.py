#!/usr/bin/env python
import pika
import sys


class Sender():

    def __init__(self, nomeFila):
        self.nomeFila = nomeFila
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

    def send(self, message):

        channel = self.connection.channel()

        channel.queue_declare(queue=self.nomeFila, durable=True)

        channel.basic_publish(
            exchange='',
            routing_key=self.nomeFila,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        print(" [x] Enviado mensagem para fila "+str(self.nomeFila)+" %r" % message)
    

    def closeConnection(self):
        self.connection.close()
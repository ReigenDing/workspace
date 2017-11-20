#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Vin on 2017/6/6
import json
import pika
import time
import threading


class MQProducer(threading.Thread):
    def run(self):
        while True:
            if int(time.time()) % 5 == 0:
                producer()
                time.sleep(1)


class MQConsumer(threading.Thread):
    def run(self):
        consumer()


def producer():
    # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    url = 'amqp://admin:elecfans@queue.elecfans.net:5672/'
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    channel.queue_declare(queue='bbs_msg_queue', durable=True)
    data = {
        'uid': 'uid1233132',
        'username': 'username1231231',
        'id': 'id12312312321',
        'title': 'title123132',
        'thumb': 'thumb121313123',
        'type': 5,
        'quote_info': 'info121321',
        'class_hour': int(time.time()),
        'people_num': 0,
        'user': 'user1231231',
    }
    channel.basic_publish(exchange='',
                          routing_key='bbs_msg_queue',
                          body=json.dumps(data))
    print(" [x] Sent test data !!!")
    connection.close()


def consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(callback,
                          queue='hello',
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def main():
    MQProducer().start()
    # MQConsumer().start()


if __name__ == '__main__':
    main()

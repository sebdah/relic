#!/usr/bin/env python

"""
Example utilitiy to demonstrate how to send persistant
messages to a RabbitMQ queue
"""

import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.queue_declare(queue = 'sdtest', durable = True)

channel.basic_publish(  exchange = '',
                        routing_key = 'sdtest',
                        body = ' '.join(sys.argv[1:]),
                        properties = pika.BasicProperties(
                            delivery_mode = 2, # make message persistent
                        ))

print "Sent '%s'" % ' '.join(sys.argv[1:])

connection.close()

sys.exit(0)

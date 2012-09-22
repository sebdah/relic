#!/usr/bin/env python

"""
Example utilitiy to demonstrate how to send persistant
messages to a RabbitMQ queue

The script takes all command line args as a message
"""

import sys
import pika

# Create a connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# Open a channel, or create it if it doesn't exist
channel = connection.channel()
channel.queue_declare(queue = 'sdtest', durable = True)

# Publish the message to the queue
channel.basic_publish(  exchange = '',
                        routing_key = 'sdtest',
                        body = ' '.join(sys.argv[1:]),
                        properties = pika.BasicProperties(
                            delivery_mode = 2, # make message persistent
                        ))

print "Sent '%s'" % ' '.join(sys.argv[1:])

# Close the connection to RabbitMQ
connection.close()

sys.exit(0)

#!/usr/bin/env python

"""
Utilitiy to send messages to a RabbitMQ queue
"""

import sys
import pika
import time
import commander
from datetime import datetime

def callback(ch, method, properties, body):
    # Fetch the message
    sys.stdout.write("%s - Receiving message %r.. " % (datetime.utcnow(), body))
    sys.stdout.flush()
    time.sleep( body.count('.') )
    print "done"
    
    # Acknowledge the message
    ch.basic_ack(delivery_tag = method.delivery_tag)
    
    # Get the message parts
    if len(body.split('|')) > 2:
        cloud, command, args = body.split('|', 2)
    else:
        print "%s - %s is not a valid message. Throwing message.. " % \
                (datetime.utcnow(), body)
        return False
    
    # Execute the command
    try:
        cmd = commander.Commander(command, args)
    except AttributeError:
        print "%s - %s is not a valid command. Throwing message.. " % \
                (datetime.utcnow(), command)
        return False
    
    return True

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.queue_declare(queue = 'sdtest', durable = True)

channel.basic_consume(callback,
                      queue = 'sdtest')

channel.start_consuming()

connection.close()

sys.exit(0)

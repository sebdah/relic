#!/usr/bin/env python

"""
Utilitiy to send messages to a RabbitMQ queue
"""

import sys
import pika
import time
import commander
from datetime import datetime

def callback(channel, method, properties, body):
    """
    Callback function for recieved messages
    """
    # Fetch the message
    sys.stdout.write("%s - Receiving message %r.. " % (datetime.utcnow(), body))
    sys.stdout.flush()
    time.sleep(body.count('.'))
    print "done"
    
    # Acknowledge the message
    channel.basic_ack(delivery_tag = method.delivery_tag)
    
    # 
    # Get the message parts
    #
    # We expect x|x|x[|x|..]
    #
    if len(body.split('|')) > 2:
        cloud, command, args = body.split('|', 2)
    else:
        print "%s - %s is not a valid message. Throwing message.. " % \
                (datetime.utcnow(), body)
        return False
    
    # Execute the command
    try:
        commander.Commander(command, args)
    except AttributeError:
        print "%s - %s is not a valid command. Throwing message.. " % \
                (datetime.utcnow(), command)
        return False
    
    return True

# Create a connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# Open a new channel, if not previously existing
channel = connection.channel()
channel.queue_declare(queue = 'sdtest', durable = True)

# Define consumer
channel.basic_consume(callback, queue = 'sdtest')
channel.start_consuming()

# Close the connection to RabbitMQ
connection.close()

sys.exit(0)

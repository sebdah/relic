"""
Hermes worker implementation
"""

import sys
import pika
from optparse import make_option
from django.core.management.base import BaseCommand#, CommandError


class Commander():
    """
    Class for executing commands
    """
    def __init__(self, command, args):
        """
        Constructor
        """
        exec('self.%s("%s")' % (command, ", ".join(args)))
    
    def echo(self, *args):
        """
        Echo the message to the prompt
        
        args[0]:        message to print
        """
        print args[0]
        return True


class Command(BaseCommand):
    args = ''
    help = 'Send messages to Hermes'

    option_list = BaseCommand.option_list + (
        make_option('--message', action='store',
            dest='message', default='',
            help='Message to send to Hermes'),
        make_option('--host', action='store',
            dest='host', default='localhost',
            help='RabbitMQ hostname'),
        make_option('--port', action='store',
            dest='port', default=5672,
            help='RabbitMQ port number'),
        make_option('--queue', action='store',
            dest='queue', default='task_queue',
            help='RabbitMQ queue name'),)

    def handle(self, *args, **options):
        if options.get('message') is '':
            print "Error: --message must be set"
            sys.exit(1)
        
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=options.get('host'),
            port=options.get('port')))
        channel = connection.channel()

        channel.queue_declare(queue=options.get('queue'), durable=True)

        channel.basic_publish(exchange='',
                              routing_key=options.get('queue'),
                              body=options.get('message'),
                              properties=pika.BasicProperties(
                                 delivery_mode = 2, # make message persistent
                              ))
        print " [x] Sent %r" % (options.get('message'),)
        connection.close()

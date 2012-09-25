"""
Hermes worker implementation
"""

import sys
import pika
import time
from datetime import datetime
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
    help = 'Worker processing messages from RabbitMQ'

    option_list = BaseCommand.option_list + (
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
        self.queue_watcher(options.get('host'), options.get('port'), options.get('queue'))

    def queue_watcher(self, hostname, port, queue):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=hostname,
            port=port))
        channel = connection.channel()

        channel.queue_declare(queue=queue, durable=True)
        print ".__                                        "
        print "|  |__   ___________  _____   ____   ______"
        print "|  |  \_/ __ \_  __ \/     \_/ __ \ /  ___/"
        print "|   Y  \  ___/|  | \/  Y Y  \  ___/ \___ \ "
        print "|___|  /\___  >__|  |__|_|  /\___  >____  >"
        print "     \/     \/            \/     \/     \/ \n"
        print "Hermes worker started"
        print ' [*] Waiting for messages. To exit press CTRL+C'

        def callback(ch, method, properties, body):
            """
            Callback function for message processing
            """
            print " [x] Received %r" % (body,)
            time.sleep(body.count('.'))
            
            command = body.split('|')[0]
            arguments = body.split('|')[1:]
            
            # Execute the command
            try:
                Commander(command, arguments)
            except AttributeError:
                print "%s - %s is not a valid command. Throwing message.. " % (
                    datetime.utcnow(), command)
                return False
            
            print " [x] Done"
            ch.basic_ack(delivery_tag = method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback, queue=queue)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print "\nCaught exit signal. Exiting Hermes worker."
            sys.exit(0)


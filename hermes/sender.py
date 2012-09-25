#!/usr/bin/env python

"""
Command line utility to send messages to RabbitMQ
"""

import sys
import pika
import argparse


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(
        conflict_handler="resolve", 
        description="Send commands to RabbitMQ")
    parser.add_argument(
        '-m', '--message', action='store', type=str, 
        dest='message', default='',
        help='Message to send (required)')
    parser.add_argument(
        '-h', '--host', action='store', type=str, 
        dest='host', default='localhost',
        help='Hostname for RabbitMQ')
    parser.add_argument(
        '-p', '--port', action='store', type=int,
        dest='port', default=5672,
        help='Port for RabbitMQ')
    parser.add_argument(
        '-q', '--queue', action='store', type=str,
        dest='queue', default='task_queue',
        help='Queue name for the RabbitMQ queue')
    args = parser.parse_args()

    # Check that we got a message
    if args.message is '':
        print "Error: --message must be set\n"
        parser.print_help()
        sys.exit(1)

    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=args.host,
            port=args.port))
    channel = connection.channel()

    channel.queue_declare(queue=args.queue, durable=True)

    channel.basic_publish(exchange='',
                          routing_key=args.queue,
                          body=args.message,
                          properties=pika.BasicProperties(
                             delivery_mode = 2, # make message persistent
                          ))
    print " [x] Sent %r" % (args.message,)
    connection.close()


if __name__ == "__main__":
    main()

sys.exit(1)

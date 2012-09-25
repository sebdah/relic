#!/usr/bin/env python

"""
RabbitMQ worker reading messages in the work queue and executes them
"""

import sys
import pika
import time
import argparse

def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(
        conflict_handler="resolve", 
        description="Process messages from RabbitMQ")
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
        help='Queue name to watch')
    args = parser.parse_args()

    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=args.host,
            port=args.port))
    channel = connection.channel()

    channel.queue_declare(queue=args.queue, durable=True)
    print ' [*] Waiting for messages. To exit press CTRL+C'

    def callback(ch, method, properties, body):
        """
        Callback function for message processing
        """
        print " [x] Received %r" % (body,)
        time.sleep( body.count('.') )
        print " [x] Done"
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue=args.queue)

    channel.start_consuming()

if __name__ == "__main__":
    main()

sys.exit(1)

# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.core.management import BaseCommand
from easy_thumbnails.files import generate_all_aliases
from pika import BlockingConnection
from pika import ConnectionParameters


def callback(ch, method, properties, body):
    image_name = body.decode('UTF-8')
    logging.getLogger('imageprocessor').info('Received image {0} from {1}'.format(image_name, settings.BROKER_HOST))
    try:
        generate_all_aliases(image_name, True)
        logging.getLogger('imageprocessor').info('Done image %r' % image_name)
    except Exception as e:
        logging.getLogger('imageprocessor').info('Error processing image %r' % image_name)
        logging.getLogger('imageprocessor').info('%s (%s)' % (e, type(e)))
    ch.basic_ack(delivery_tag=method.delivery_tag)


class Command(BaseCommand):
    def handle(self, *args, **options):
        connection = BlockingConnection(ConnectionParameters(settings.BROKER_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=settings.RESPONSIVE_IMAGE_QUEUE, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            callback,
            queue=settings.RESPONSIVE_IMAGE_QUEUE,
        )
        logging.getLogger('imageprocessor').info('Waiting for images')
        channel.start_consuming()

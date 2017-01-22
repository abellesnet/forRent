# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from pika import BasicProperties
from pika import BlockingConnection
from pika import ConnectionParameters


def generate_responsive_room_main_photo_images(image):
    if image:
        logging.getLogger('forrent').info('Sending image {0} to {1}'.format(image.name, settings.BROKER_HOST))
        connection = BlockingConnection(ConnectionParameters(settings.BROKER_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=settings.RESPONSIVE_IMAGE_QUEUE, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=settings.RESPONSIVE_IMAGE_QUEUE,
            body=image.name,
            properties=BasicProperties(
                delivery_mode=2,  # make message persistent
            ),
        )
        logging.getLogger('forrent').info('Sent image {0} to {1}'.format(image.name, settings.BROKER_HOST))
        connection.close()

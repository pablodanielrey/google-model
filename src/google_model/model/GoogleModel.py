import os
import uuid
import datetime
import base64
import logging
import json
import logging
import sys
from signal import signal, SIGINT


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    sys.exit(0)

signal(SIGINT, handler)

import pulsar

from sqlalchemy import or_, and_, desc
from sqlalchemy.orm import joinedload, contains_eager, defer

PULSAR_URL = os.environ.get('PULSAR_URL', 'pulsar://localhost:6650')
PULSAR_TOPIC = os.environ.get('PULSAR_TOPIC', 'google')
PULSAR_SUBSCRIPTION = os.environ.get('PULSAR_SUBSCRIPTION', 'google')

class GoogleModel:

    def __init__(self):
        self.client = pulsar.Client(PULSAR_URL)

    def __del__(self):
        self.client.close()

    def listen(self):
        consumer = self.client.subscribe(PULSAR_TOPIC, 'google')
        while True:
            msg = consumer.receive()
            try:
                print(msg.data().decode('utf-8'), msg.message_id())
                consumer.acknowledge(msg)
            except:
                consumer.negative_acknowledge(msg)
        self.client.close()


    def send_message(self, msg):
        producer = self.client.create_producer(PULSAR_TOPIC)
        producer.send(msg.encode('utf-8'))
        producer.close()

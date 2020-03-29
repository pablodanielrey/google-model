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
from pulsar.schema import JsonSchema

PULSAR_URL = os.environ.get('PULSAR_URL', 'pulsar://localhost:6650')
PULSAR_TOPIC = os.environ.get('PULSAR_TOPIC', 'google')
PULSAR_SUBSCRIPTION = os.environ.get('PULSAR_SUBSCRIPTION', 'google')

from .google.SyncGoogleModel import SyncGoogleModel, UserNotFoundException

from login.model.entities.Login import LoginEvent, LoginEventTypes

class GoogleModel:

    def __init__(self):
        self.client = pulsar.Client(PULSAR_URL)
        self.errors = {}
        self.give_up_errors = 5
        self.syncGoogle = SyncGoogleModel()

    def __del__(self):
        self.client.close()

    def listen(self):
        consumer = self.client.subscribe(PULSAR_TOPIC, PULSAR_SUBSCRIPTION, schema=JsonSchema(LoginEvent))
        while True:
            try:
                msg = consumer.receive(timeout_millis=5000)
                try:
                    event = msg.value()
                    username = event.username
                    credentials = event.credentials
                    if username not in self.errors:
                        self.errors[username] = 0

                    if self.errors[username] >= self.give_up_errors:
                        consumer.acknowledge(msg)
                        continue

                    try:
                        self.syncGoogle.sync_login(username, credentials)
                        consumer.acknowledge(msg)

                    except UserNotFoundException:
                        self.errors[username] = self.give_up_errors
                        consumer.acknowledge(msg)

                    except:
                        self.errors[username] = self.errors[username] + 1
                        consumer.negative_acknowledge(msg)
                    
                except:
                    consumer.negative_acknowledge(msg)
            except:
                pass
        self.client.close()


    def send_message(self, msg):
        producer = self.client.create_producer(PULSAR_TOPIC)
        producer.send(msg.encode('utf-8'))
        producer.close()

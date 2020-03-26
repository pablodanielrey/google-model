import os
import uuid
import datetime
import base64
import logging
import json
import logging

import pulsar

from sqlalchemy import or_, and_, desc
from sqlalchemy.orm import joinedload, contains_eager, defer

from .entities.Google import 


PULSAR_URL = os.environ.get('PULSAR_URL', 'pulsar://localhost:6650')
PULSAR_TOPIC = os.environ.get('PULSAR_TOPIC', 'google')

class GoogleModel:

    def __init__(self):
        client = pulsar.Client(PULSAR_URL)
        consumer = client.subscribe('my-topic', 'my-subscription')

while True:
    msg = consumer.receive()
    try:
        print("Received message '%s' id='%s'", msg.data().decode('utf-8'), msg.message_id())
        consumer.acknowledge(msg)
    except:
        consumer.negative_acknowledge(msg)

client.close()

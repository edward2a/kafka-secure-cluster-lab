#!/usr/bin/env python3

import argparse
import os
from datetime import datetime
from kafka import KafkaProducer
from time import sleep

# Some cmdline args
p = argparse.ArgumentParser()
p.add_argument('-t', '--topic', required=True, default='test-topic',
    help='The kafka topic for the client')
p.add_argument('-e', '--endpoint', required=False, default='localhost:9092',
    help='The kafka endpoint for initial cluster conneciton')
p.add_argument('-s', '--ssl-ca', required=False, default='ca.crt',
    help='The CA or self-signed certificate to trust')
p.add_argument('-c', '--counter', required=False, default=False, action='store_true',
    help='Continusly send timestamps to kafka per second')
p.add_argument('-S', '--ssl-verify', required=False, default=True, action='store_false',
    help='Disable SSL hostname verification')

args = p.parse_args()

# Check if the certificate exists
if not os.path.exists(args.ssl_ca):
    print('ERROR: The SSL trusted cert {} cannot be found.'.format(args.ssl_ca))
    exit(1)

# Client config
kafka_security = 'SASL_SSL'
kafka_authn_type = 'PLAIN'
kafka_authn_user = 'tester'
kafka_authn_pass = 'Just4Pass!'
#kafka_authn_user = 'admin'
#kafka_authn_pass = 'admin-secret'

# Create client
producer = KafkaProducer(
    bootstrap_servers=args.endpoint,
    max_block_ms=1000,
    request_timeout_ms=1000,
    security_protocol=kafka_security,
    ssl_check_hostname=args.ssl_verify,
    ssl_cafile=args.ssl_ca,
    sasl_mechanism=kafka_authn_type,
    sasl_plain_username=kafka_authn_user,
    sasl_plain_password=kafka_authn_pass)

# Produce
if args.counter:
    while True:
        producer.send(args.topic, value=str(datetime.utcnow()).encode() + b' : Test message.')
        producer.flush(timeout=1000)
        sleep(1)
else:
    while True:
        producer.send(args.topic, value=input('Message: ').encode())
        producer.flush(timeout=1000)


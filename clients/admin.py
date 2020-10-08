#!/usr/bin/env python3

import argparse
import os
from kafka import errors
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.admin.config_resource import ConfigResource

# Some cmdline args
p = argparse.ArgumentParser()
p.add_argument('-e', '--endpoint', required=False, default='localhost:9092',
    help='The kafka endpoint for initial cluster conneciton')
p.add_argument('-s', '--ssl-ca', required=False, default='ca.crt',
    help='The CA or self-signed certificate to trust')
p.add_argument('-S', '--ssl-verify', required=False, default=True, action='store_false',
    help='Disable SSL hostname verification')

s = p.add_subparsers(dest='module', required=True)

# Topic and topic subparsers
topic = s.add_parser('topic', description='Topic operations module')
topic_sub = topic.add_subparsers(dest='action', required=True)

topic_sub_create = topic_sub.add_parser('create')
topic_sub_delete = topic_sub.add_parser('delete')
topic_sub_describe = topic_sub.add_parser('describe')
topic_sub_update = topic_sub.add_parser('update')
topic_sub_list = topic_sub.add_parser('list')

# Topic create subparser
topic_sub_create.add_argument('-t', '--topic', required=True,
    help='The topic name', type=str)
topic_sub_create.add_argument('-p', '--partitions', required=False,
    default=1, type=int, help='Number of partitions to create')
topic_sub_create.add_argument('-r', '--replication-factor', required=False,
    default=1, type=int, help='Number of partiiton  replicas')

# Topic delete subparser
topic_sub_delete.add_argument('-t', '--topic', required=True,
    help='The topic name', type=str)

# Topic desribe subparser
topic_sub_describe.add_argument('-t', '--topic', required=True,
    help='The topic name', type=str)

# Topic update subparser
topic_sub_update.add_argument('-t', '--topic', required=True,
    help='The topic name', type=str)
topic_sub_update.add_argument('-p', '--partitions', required=False,
    default=1, type=int, help='New number of partitions')
topic_sub_update.add_argument('-r', '--replication-factor', required=False,
    default=1, type=int, help='New number of partition replicas')

# Topic list subparser
topic_sub_list.add_argument('-f', '--filter', required=False,
    type=str, help='Regex string filter')

# ACL and ACL subparsers
acl = s.add_parser('acl', description='ACL operations module')
acl_sub = acl.add_subparsers(dest='action', required=True)

acl_sub_create = acl_sub.add_parser('create')
acl_sub_delete = acl_sub.add_parser('delete')
acl_sub_describe = acl_sub.add_parser('describe')
acl_sub_update = acl_sub.add_parser('update')

# ACL actions subparsers



# Actions
def topic_create(client, args):
    try:
        return(client.create_topics([NewTopic(
            name=args.topic,
            num_partitions=args.partitions,
            replication_factor=args.replication_factor)]).topic_errors[0][1]) # return error_code

    except Exception as e:
        print(err_msg, '\t{} | {}\n'.format(e.errno, e.description))
        return(1)

def topic_delete(client, args):
    try:
        return(client.delete_topics([args.topic]).topic_error_codes[0][1])

    except Exception as e:
        print(err_msg, '\t{} | {}\n'.format(e.errno, e.description))
        return(1)

def topic_desribe(client, args):
    print(info_msg,
        '\tNot yet implemented.\n')

    r = client.describe_configs(ConfigResource('topic', args.topic))

def topic_update(client, args):
    print(info_msg,
        '\tNot yet implemented.\n')

def topic_list(client, args):
    for t in client.list_topics():
        print(t)

#def topic_handle_response(obj):
#    if obj.topic_errors[0][1] == 0:
#        return(0)
#    else:
#        print('\n\t==== ERROR ====\n',
#            '\tCode: {} | {}'.format(
#                obj.topic_errors[0][1],     # print error_code
#                obj.topic_errors[0][2]))    # print error_message
#        return(1)


# Poor man's switch
arg_mapper = {
    'topic': {
        'create': topic_create,
        'delete': topic_delete,
        'describe': topic_desribe,
        'update': topic_update,
        'list': topic_list
    },

    'acl': {

    }
}

# Client config
kafka_security = 'SASL_SSL'
kafka_authn_type = 'PLAIN'
kafka_authn_user = 'admin'
kafka_authn_pass = 'admin-secret'

# Other configs
err_msg = '\n\t==== ERROR ====\n'
info_msg = '\n\t==== INFO ====\n'
warn_msg = '\n\t==== WARN ====\n'

# Main
args = p.parse_args()
client = KafkaAdminClient(
    bootstrap_servers=args.endpoint,
    security_protocol=kafka_security,
    ssl_check_hostname=args.ssl_verify,
    ssl_cafile=args.ssl_ca,
    sasl_mechanism=kafka_authn_type,
    sasl_plain_username=kafka_authn_user,
    sasl_plain_password=kafka_authn_pass)


r = arg_mapper[args.module][args.action](client, args)
if r == 0:
    print('Done!')
exit(r)


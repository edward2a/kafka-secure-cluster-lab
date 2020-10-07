#!/usr/bin/env python3

import argparse
import os
from kafka import KafkaAdminClient

# Some cmdline args
p = argparse.ArgumentParser()
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
    print(args)

def topic_delete(client, args):
    print(args)

def topic_desribe(client, args):
    print(args)

def topic_update(client, args):
    print(args)

def topic_list(client, args):
    print(args)

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

# Main
args = p.parse_args()
client = object() # temporary
arg_mapper[args.module][args.action](client, args)


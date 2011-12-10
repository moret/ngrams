import re
import tempfile

import boto
from boto.sqs.message import Message

import cult.ngram as ngram

class Worker(object):
    def map_and_push(self):
        s3_conn = boto.connect_s3()
        sqs_conn = boto.connect_sqs()

        bucket_name, bucket_key = re.match('^s3://([\w\d_-]*)/(.*)$',
                's3://ngrams_cult/in/').groups()

        sqs = sqs_conn.get_queue('cult')
        if sqs == None:
            sqs = sqs_conn.create_queue('cult')

        for key in s3_conn.get_bucket(bucket_name).get_all_keys():
            if key.size > 0:
                key_url = 's3://' + key.bucket.name + '/' + key.name
                sqs.write(Message(body=key_url))

    def pop_and_process(self):
        s3_conn = boto.connect_s3()
        sqs_conn = boto.connect_sqs()

        sqs = sqs_conn.get_queue('cult')
        sqs_message = sqs.read()

        while sqs_message:
            aws_bucket_uri = sqs_message.get_body()
            bucket_name, bucket_key = re.match('^s3://([\w\d_-]*)/(.*)$',
                    aws_bucket_uri).groups()

            key = s3_conn.get_bucket(bucket_name).get_key(bucket_key)

            local_file_handler, local_filename = tempfile.mkstemp()
            key.get_contents_to_filename(local_filename)

            ngram.run_file(local_filename, 2011)

            sqs.delete_message(sqs_message)
            sqs_message = sqs.read()

worker = Worker()

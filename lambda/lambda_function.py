import os

import boto3
import psycopg2
from psycopg2.extras import execute_batch


def lambda_handler(event, context):
    s3_client = boto3.client(
        "s3",
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        endpoint_url=os.environ.get('AWS_ENDPOINT'),
    )

    data = s3_client.get_object(Bucket=event['bucket'], Key=event['key'])
    customer_data = [
        d.split(',') for d in data['Body'].read().decode('utf-8').split('\n')
    ]

    # Todo: Use warehouse_connection context manager
    try:
        conn = psycopg2.connect(
            host=os.environ.get('WAREHOUSE_HOST'),
            database=os.environ.get('WAREHOUSE_DB'),
            user=os.environ.get('WAREHOUSE_USER'),
            password=os.environ.get('WAREHOUSE_PASSWORD'),
        )
        conn.autocommit = True
        cur = conn.cursor()

        execute_batch(
            cur,
            "INSERT INTO products.customers(customer_id, zipcode, city, state_code, datetime_created, datetime_updated) VALUES(%s, %s, %s, %s, %s, %s)",
            customer_data,
        )
    finally:
        cur.close()
        conn.close()

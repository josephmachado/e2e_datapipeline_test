import io
import os
import shutil
import zipfile
from dataclasses import asdict

import boto3
import pytest
import psycopg2
from botocore.exceptions import ClientError

from datapipelines.load_customer_data import generate_load_customer_data
from datapipelines.utils.sde_config import get_aws_connection, get_warehouse_connection, DBConnection
from datapipelines.utils.db import warehouse_connection


@pytest.fixture
def s3_client():
    return boto3.client("s3", **asdict(get_aws_connection()))


@pytest.fixture
def iam_client():
    iam = boto3.client('iam', **asdict(get_aws_connection()))
    return iam


@pytest.fixture
def mocked_lambda_client(s3_client, iam_client):
    bucket_name = "landing-zone"

    # create lambda deployment package
    shutil.make_archive("./lambda/my-deployment-package", "zip", "lambda")
    
    # put deployment package in S3
    s3_client.create_bucket(Bucket=bucket_name)
    s3_client.upload_file(
        "./lambda/my-deployment-package.zip",
        bucket_name,
        "my-deployment-package.zip",
    )

    # create iam role for lambda
    if "lambda-s3-role" in [
        e["RoleName"] for e in iam_client.list_roles().get("Roles", [])
    ]:
        iam_client.delete_role(RoleName="lambda-s3-role")
    iam_role = iam_client.create_role(
        RoleName="lambda-s3-role",
        AssumeRolePolicyDocument="""{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:ListObject"
                    ],
                    "Resource": "arn:aws:s3:::landing-zone/*"
                }
            ]
        }""",
    )
    
    # create lambda function
    warehouse_creds = get_warehouse_connection()
    lambda_client = boto3.client("lambda", **asdict(get_aws_connection()))
    lambda_client.create_function(
        FunctionName="custom-lambda-function",
        Runtime="python3.8",
        Role=iam_role["Role"]["Arn"],
        Handler="lambda_function.lambda_handler",
        Code={
            "S3Bucket": bucket_name,
            "S3Key": "my-deployment-package.zip",
        },
        Environment={
                'Variables': {
                    'PYTHONPATH': '/moto/src',
                    'AWS_ENDPOINT': 'http://host.docker.internal:5000',
                    'WAREHOUSE_USER': warehouse_creds.user,
                    'WAREHOUSE_PASSWORD': warehouse_creds.password,
                    'WAREHOUSE_HOST': 'host.docker.internal',
                    'WAREHOUSE_DB': warehouse_creds.db
                }
        },
    )
    
    # We can add S3 event notification on object create but this is not implemented in Moto
    return lambda_client


@pytest.fixture
def set_up_tear_down():
    # no setup
    yield
    # clean up final table
    with warehouse_connection(get_warehouse_connection()) as db_cur:
        db_cur.execute('truncate table products.customers')
    

def test_generate_load_customer_data(s3_client, mocked_lambda_client, set_up_tear_down):
    generate_load_customer_data("upload/customer.csv", "landing-zone", "customer.csv")

    # we manually trigger lambda since S3 object create trigger is not implemented in Moto
    # The payload to lambda will consist of more information when invoked on AWS
    mocked_lambda_client.invoke(FunctionName="custom-lambda-function", Payload='{"bucket": "landing-zone", "key": "customer.csv"}')

    # check number of inserted rows is 5
    expected_result = 5

    with warehouse_connection(get_warehouse_connection()) as db_cur:
        db_cur.execute('select count(*) from products.customers')
        result = db_cur.fetchall()[0][0]
    
    assert result == expected_result

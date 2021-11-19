from dataclasses import asdict
from tempfile import NamedTemporaryFile

import boto3

from datapipelines.utils.sde_config import get_aws_connection, get_sftp_creds
from datapipelines.utils.sftp import sftp_connection


def sftp_to_s3(sftp_file: str, bucket_name: str, file_name: str) -> None:
    s3_client = boto3.client("s3", **asdict(get_aws_connection()))
    with NamedTemporaryFile() as lcl_f:
        with sftp_connection(get_sftp_creds()) as sftp_conn:
            sftp_conn.get(sftp_file, lcl_f.name)
        s3_client.upload_file(lcl_f.name, bucket_name, file_name)


def generate_risk_prediction(sftp_file: str, bucket_name: str, file_name: str):
    sftp_to_s3(sftp_file, bucket_name, file_name)

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class SFTPConnection:
    username: str
    password: str
    host: str
    port: int = 22


def get_sftp_creds() -> SFTPConnection:
    return SFTPConnection(
        username=os.getenv('SFTP_USERNAME', ''),
        password=os.getenv('SFTP_PASSWORD', ''),
        host=os.getenv('SFTP_HOST', ''),
        port=22,
    )


@dataclass
class AWSCloudConnection:
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str
    endpoint_url: Optional[str]


def get_aws_connection() -> AWSCloudConnection:
    return AWSCloudConnection(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', ''),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', ''),
        region_name=os.getenv('AWS_REGION_NAME', ''),
        endpoint_url=os.getenv('AWS_ENDPOINT_URL', ''),
    )


@dataclass
class DBConnection:
    db: str
    user: str
    password: str
    host: str
    port: int = 5432


def get_warehouse_connection() -> DBConnection:
    return DBConnection(
        db=os.getenv('WAREHOUSE_DB', ''),
        user=os.getenv('WAREHOUSE_USER', ''),
        password=os.getenv('WAREHOUSE_PASSWORD', ''),
        host=os.getenv('WAREHOUSE_HOST', ''),
    )

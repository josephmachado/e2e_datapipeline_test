from dataclasses import dataclass
from typing import Optional

from dotenv import dotenv_values

config = dotenv_values(".env.local")


@dataclass
class SFTPConnection:
    username: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: int = 22


def get_sftp_creds() -> SFTPConnection:
    return SFTPConnection(
        username=config.get('SFTP_USERNAME', ''),
        password=config.get('SFTP_PASSWORD', ''),
        host=config.get('SFTP_HOST', ''),
        port=22,
    )


@dataclass
class AWSCloudConnection:
    aws_access_key_id: Optional[str]
    aws_secret_access_key: Optional[str]
    region_name: Optional[str]
    endpoint_url: Optional[str]


def get_aws_connection() -> AWSCloudConnection:
    return AWSCloudConnection(
        aws_access_key_id=config.get('AWS_ACCESS_KEY_ID', ''),
        aws_secret_access_key=config.get('AWS_SECRET_ACCESS_KEY', ''),
        region_name=config.get('AWS_REGION_NAME', ''),
        endpoint_url=config.get('AWS_ENDPOINT_URL', ''),
    )


@dataclass
class DBConnection:
    db: Optional[str]
    user: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: int = 5432


def get_warehouse_connection() -> DBConnection:
    return DBConnection(
        db=config.get('WAREHOUSE_DB', ''),
        user=config.get('WAREHOUSE_USER', ''),
        password=config.get('WAREHOUSE_PASSWORD', ''),
        host=config.get('WAREHOUSE_HOST', ''),
    )

from contextlib import contextmanager
from dataclasses import asdict

import pysftp

from datapipelines.utils.sde_config import SFTPConnection


@contextmanager
def sftp_connection(sftp_conn: SFTPConnection):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp_conn = pysftp.Connection(
        **asdict(sftp_conn), private_key=".ppk", cnopts=cnopts
    )
    try:
        yield sftp_conn
    finally:
        sftp_conn.close()

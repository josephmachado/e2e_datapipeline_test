## End to End data pipeline test

### Prerequisites & Setup

To run, you will need

1. Docker
2. Python3.9

Clone this repo and setup a virtual environment within it.

```bash
git clone
python -m venv ./env
source env/bin/activate
pip install -r requirements.txt
```

We will use [Moto](https://docs.getmoto.org/en/latest/docs/getting_started.html) to mock out our AWS services. Since we will be using Lambda functions and interacting with a warehouse, we would need to start a moto server. Use the below command to start a moto server.

We will mock Redshift using Postgres.

We will use open source SFTP server as our SFTP.

```bash
make up
```

### Run tests

We can run our tests using `pytest`.

```bash
export PYTHONPATH=${PYTHONPATH}:./src # set path to enable imports
pytest
```

Clean up

```bash
make ci
```

### Tear down

```bash
make down
```

## End to End data pipeline test

Code for the post [Setting up end-to-end tests for cloud data pipelines](https://www.startdataengineering.com/post/setting-up-e2e-tests/)

### Architecture

This is what our data pipeline architecture looks like.

![Architecture](/assets/images/arch.png)

For our local setup, we will use

1. Open source sftp server
2. Moto server to mock S3 and Lambda
3. Postgres as a substitute for AWS Redshift

![Local Architecture](/assets/images/arch-lcl.png)

### Prerequisites & Setup

To run, you will need

1. [Docker](https://docs.docker.com/engine/install/)
2. [Python3.6 or above](https://www.python.org/downloads/)

Clone, create a virtual env, set up python path, spin up containers and run tests as shown below.

```bash
git clone https://github.com/josephmachado/e2e_datapipeline_test.git
python -m venv ./env
source env/bin/activate # use virtual environment
pip install -r requirements.txt
make up # spins up the SFTP, Motoserver, Warehouse docker containers
export PYTHONPATH=${PYTHONPATH}:./src # set path to enable imports
```

### Run tests

We can run our tests using `pytest`.

```bash
pytest # runs all tests under the ./test folder
```

Clean up

```bash
make ci
```

### Tear down

```bash
make down # spins down the docker containers
deactivate # stop using the virtual environment
```

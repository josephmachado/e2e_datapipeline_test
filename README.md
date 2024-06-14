
* [End to End data pipeline test](#end-to-end-data-pipeline-test)
    * [Architecture](#architecture)
    * [Run on codespaces](#run-on-codespaces)
    * [Prerequisites & Setup](#prerequisites--setup)
    * [Run tests](#run-tests)
    * [Tear down](#tear-down)

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

### Run on codespaces

You can run this data pipeline using GitHub codespaces. Follow the instructions below.

1. Create codespaces by going to the **[e2e_datapipelin_test](https://github.com/josephmachado/e2e_datapipeline_test)** repository, cloning(or fork) it and then clicking on `Create codespaces on main` button.
2. Wait for codespaces to start and for codespaces to automatically install the libraries in `requirements.txt`, then in the terminal type `make up && export PYTHONPATH=${PYTHONPATH}:./src `.
3. Wait for the above to complete.
4. Now you can run our event pipeline end to end test using `pytest` command and you can clean up code with the `make ci` command

**NOTE**: The screenshots below, show the general process to start codespaces, please follow the instructions shown above for this project.

![codespace start](./assets/images/cs1.png)
![codespace make up](./assets/images/cs2.png)
![codespace access ui](./assets/images/cs3.png)

**Note** Make sure to switch off codespaces instance, you only have limited free usage; see docs [here](https://github.com/features/codespaces#pricing).

### Prerequisites & Setup

To run, you will need

1. [Docker](https://docs.docker.com/engine/install/)
2. [Python3.6 or above](https://www.python.org/downloads/)

Clone, create a virtual env, set up python path, spin up containers and run tests as shown below.

```bash
git clone https://github.com/josephmachado/e2e_datapipeline_test.git
cd e2e_datapipeline_test
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

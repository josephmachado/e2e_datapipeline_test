motoserver:
	docker run -d --rm -t --name motoserver -e TEST_SERVER_MODE=true -e AWS_SECRET_ACCESS_KEY=testing -e AWS_ACCESS_KEY_ID=testing -p 5000:5000 -v `pwd`:/moto -v /var/run/docker.sock:/var/run/docker.sock motoserver/moto

sftp:
	docker run -d --rm -t --name sftp -v `pwd`/test/fixtures/sftp:/home/sde/upload -p 22:22 atmoz/sftp sde:password:1001

warehouse:
	docker run -d --rm -t --name warehouse -e POSTGRES_USER=sde -e POSTGRES_PASSWORD=password -e POSTGRES_DB=finance -v `pwd`/containers/warehouse:/docker-entrypoint-initdb.d -v /var/run/docker.sock:/var/run/docker.sock -p 5432:5432 postgres:13

up: motoserver sftp warehouse

down:
	docker stop motoserver sftp warehouse

lint:
	isort ./lambda/lambda_function.py
	isort ./src
	black -S --line-length 79 ./lambda/lambda_function.py
	black -S --line-length 79 ./src

typing-check:
	mypy --ignore-missing-imports ./src

static-analysis:
	flake8 ./src

ci: lint typing-check static-analysis
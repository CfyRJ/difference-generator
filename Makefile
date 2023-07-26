install:
	poetry install

gendiff-help:
	poetry run gendiff -h

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-uninstall-hc:
	pip uninstall hexlet-code
	rm -r dist

lint:
	poetry run flake8 gendiff

pytest:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml
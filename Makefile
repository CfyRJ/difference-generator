install:
	poetry install

gendiff:
	poetry run gendiff

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
	poetry run pytest --cov
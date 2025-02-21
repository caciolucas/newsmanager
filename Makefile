.PHONY: test

test:
	python manage.py test newsmanager/apps

compile-requirements:
	pip-compile requirements.in -o requirements.txt -q --strip-extras
	echo "Requirements compiled"

compile-dev-requirements:
	pip-compile requirements.in requirements-dev.in -o requirements.txt -q --strip-extras

install-requirements:
	pip install -r requirements.txt -q

dev-requirements: compile-dev-requirements install-requirements
requirements: compile-requirements install-requirements

lint:
	ruff check --fix
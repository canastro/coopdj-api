test: lint test-python

lint:
	@echo "Linting Python files"
	flake8 --ignore=E121,W404,F403,E501 --exclude=./env/*,.git . || exit 1
	@echo ""

test-python:
	@echo "Running coopdj tests"
	python manage.py test

server:
	python manage.py runserver

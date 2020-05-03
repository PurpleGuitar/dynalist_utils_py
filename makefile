.PHONY: test lint watch edit clean

test:
	coverage run --branch --source . --omit "test_*" -m unittest discover -s test
	coverage report
	coverage html

lint:
	pylint *.py test/*.py
	mypy *.py test/*.py

watch:
	while inotifywait -e close_write,moved_to,create . test; do clear; make lint; make test; done

edit:
	vim makefile dl*.py *.py test/*.py

clean:
	rm -rf __pycache__
	rm -f .coverage
	rm -rf htmlcov
	rm -f *.json

# vim: foldmethod=indent

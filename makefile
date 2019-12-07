.PHONY: test lint watch edit clean

test:
	coverage run --branch --source . --omit "test_*" -m unittest discover -s test
	coverage report
	coverage html

lint:
	pylint *.py test/*.py

watch:
	while inotifywait -e close_write,moved_to,create . test; do clear; make lint; make test; done

edit:
	vim dl*.py *.py test/*.py makefile

clean:
	rm -rf __pycache__
	rm -f .coverage
	rm -rf htmlcov

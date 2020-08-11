.PHONY: test lint watch edit clean

test:
	export PYTHONPATH=..:${PYTHONPATH}; coverage run --branch --source . --omit "test_*" -m unittest discover -s test
	coverage report
	coverage html

lint:
	export pythonpath=..:${pythonpath}; pylint *.py test/*.py
	export mypypath=..; mypy *.py test/*.py

watch:
	while inotifywait -e close_write,moved_to,create . test; do clear; make lint; make test; done

edit:
	${EDITOR} makefile *.py test/*.py

clean:
	rm -rf __pycache__
	rm -rf test/__pycache__
	rm -f .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -f *.json

# vim: foldmethod=indent

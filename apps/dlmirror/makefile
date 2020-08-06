.PHONY: edit lint

edit:
	${EDITOR} makefile *.py

lint:
	export PYTHONPATH=../../lib:${PYTHONPATH}; pylint *.py
	export MYPYPATH=../../lib; mypy *.py


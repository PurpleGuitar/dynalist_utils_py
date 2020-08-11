.PHONY: edit lint

edit:
	${EDITOR} makefile *.py dlmirror

lint:
	export PYTHONPATH=../../lib:${PYTHONPATH}; pylint *.py
	export MYPYPATH=../../lib; mypy *.py


.PHONY: lint

lint:
	export PYTHONPATH=../../lib:${PYTHONPATH}; pylint *.py
	export MYPYPATH=../../lib; mypy *.py 
	

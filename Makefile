.PHONY: all test clean

test:
	coverage run -m pytest 
	coverage report

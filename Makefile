.PHONY: all test clean

test:
	coverage run --relative_files -m pytest 
	coverage report
	coveralls

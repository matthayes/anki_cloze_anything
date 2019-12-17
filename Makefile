init:
	pip install -r requirements.txt

flake8:
	flake8

release:
	./release.sh
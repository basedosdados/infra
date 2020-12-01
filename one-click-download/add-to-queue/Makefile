.PHONY: create-env update-env

REPO=$(shell basename $(CURDIR))

create-env:
	python3 -m venv .$(REPO);
	. .$(REPO)/bin/activate; \
			pip3 install --upgrade  -r requirements.txt; 

update-env:
	. .$(REPO)/bin/activate; \
	pip3 install --upgrade -r requirements.txt;


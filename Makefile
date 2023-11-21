SHELL = /bin/bash

define PROJECT_HELP_MSG
Usage:\n
  make help      \t show this message\n
  make clean     \t remove intermediate files (see CLEANUP)\n
  \n
  make ${AWS_CDK}\t install AWS cdk command package\n
  make install   \t install python packages in requirements.txt\n
  \n
  make tests     \t run listbuckets test script to list all S3 buckets\n
\n
\n
Press Q to exit.
endef
export PROJECT_HELP_MSG

help:
	@echo -e $$PROJECT_HELP_MSG | less

AWS_CDK := $(or $(realpath $(shell command -v cdk)),cdk)
export VIRTUAL_ENV := $(abspath .venv)
export PATH := ${VIRTUAL_ENV}/bin:${PATH}

${AWS_CDK}:
	sudo npm install -g aws-cdk
	@cdk --version

install: requirements.txt ${VIRTUAL_ENV} ${AWS_CDK}
	. ${VIRTUAL_ENV}/bin/activate && pip3 install -r requirements.txt

tests: tests/test_*.py
	pytest -vv tests

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

.PHONY: tests install configure clean
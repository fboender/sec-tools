.PHONY: doc 
PROG=sec-tools

fake:
	# NOOP

doc:
	scripts/make_man.sh

clean:
	find ./ -name "*.state" -delete
	find ./ -name "*.pyc" -delete

test:
	flake8 --exclude src/sec-gather-misconfigs.d/ --ignore=E501 src/*
	flake8 --ignore=E501,F821 src/sec-gather-misconfigs.d/*

install: clean
	scripts/install.sh

uninstall: clean
	scripts/uninstall.sh

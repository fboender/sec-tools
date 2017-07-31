.PHONY: doc 
PROG=sec-tools

fake:
	# NOOP

doc:
	scripts/make_man.sh

clean:
	find ./ -name "*.state" -delete
	find ./ -name "*.pyc" -delete

.PHONY: doc 
PROG=sec-tools

fake:
	# NOOP

doc:
	scripts/make_man.sh

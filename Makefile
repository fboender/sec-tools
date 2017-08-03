.PHONY: doc 
PROG=sec-tools

fake:
	# NOOP

doc:
	scripts/make_man.sh

clean:
	find ./ -name "*.state" -delete
	find ./ -name "*.pyc" -delete

install:
	install src/* /usr/bin/
	install docs/man/*.1 /usr/share/man/man1

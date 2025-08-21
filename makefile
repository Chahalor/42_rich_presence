

run:
	bash run.sh

stop:
	bash stop.sh

install:
	pip install -r requirements.txt

update:
	git pull

uninstall:
	pip uninstall -r requirements.txt

.PHONY: run stop install update uninstall
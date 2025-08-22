PYTHON	:= python3
MAIN	:= main.py

start:
	$(PYTHON) $(MAIN) start

stop:
	$(PYTHON) $(MAIN) stop

status:
	$(PYTHON) $(MAIN) status

uninstall:
	pip uninstall -r requirements.txt

install:
	pip install -r requirements.txt

update:
	$(PYTHON) $(MAIN) update


.PHONY: start stop status install update uninstall
SUPERVISOR_CONF = search-asr-bot
RUN_PYTHON_FILE = app.py
VENV = .venv/bin/python

.PHONY: restart
restart:
	supervisorctl restart $(SUPERVISOR_CONF)

.PHONY: stop
stop:
	supervisorctl stop $(SUPERVISOR_CONF)

.PHONY: startlocal
startlocal:
	$(VENV) $(RUN_PYTHON_FILE)
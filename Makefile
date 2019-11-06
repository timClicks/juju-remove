# leave this file alone, edit the .env instead
PYTHON = /usr/bin/env python3

requirements.txt: setup.py juju_remove.py
	$(PYTHON) -m pip freeze > $@
	sed -i -e '/juju-remove/d' $@




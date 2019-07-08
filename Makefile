.PHONY: all


runserver:
	.env/bin/python back/manage.py migrate
	.env/bin/python back/manage.py runserver

install:
	.env/bin/pip install -r requirements.txt
	.env/bin/python back/manage.py migrate


reinstall:
	rm db/db.sqlite3
	.env/bin/pip install -r requirements.txt
	.env/bin/python back/manage.py migrate


generate:
	.env/bin/python back/manage.py generate


reinstall_and_generate:
	rm db/db.sqlite3
	.env/bin/pip install -r requirements.txt
	.env/bin/python back/manage.py migrate
	.env/bin/python back/manage.py generate

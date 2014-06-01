all: build

build:
	echo 'do nothing'

clean:
	find . -name \*.pyc | xargs rm

run:
	python manage.py supervisor

startall:
	python manage.py supervisor start all

stopall:
	python manage.py supervisor stop all

daemonize:
	python manage.py supervisor --daemonize

static:
	python manage.py collectstatic

ssh:
	ssh eka@lokerhub.com

push:
	git push origin master

pull:
	git pull origin master

process:
	ps aux | grep python
all: build

build:
	lessc -x ui/static/less/soulbox.less > ui/static/css/soulbox.min.css

clean:
	find . -name \*.pyc | xargs rm

run:
	./manage.py supervisor

startall:
	./manage.py supervisor start all

stopall:
	./manage.py supervisor stop all

daemonize:
	./manage.py supervisor --daemonize

static:
	./manage.py collectstatic

ssh:
	ssh eka@lokerhub.com

push:
	git push origin master

pull:
	git pull origin master
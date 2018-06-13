#!/bin/sh

set -e
set -u
set -x

DIR="$(dirname $0)"

dc() {
	docker-compose -p gastest -f ${DIR}/docker-compose.yml $*
}


trap 'dc kill ; dc rm -f' EXIT

dc down
dc rm
dc build

echo "Placeholder for signals-export test suite."

dc run tests /deploy/docker-wait.sh
dc run tests /deploy/docker-migrate.sh
dc run tests python manage.py test --noinput

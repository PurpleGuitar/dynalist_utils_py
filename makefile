.PHONY: build test bash dlreminder

build:
	docker build --tag dynalist_utils .

test:
	docker run --rm \
		--env DYNALIST_TOKEN \
		--env DYNALIST_URL \
		--interactive --tty \
		dynalist_utils /bin/bash -c 'cd lib/dynalist_utils; make test'

bash:
	docker run --rm \
		--env DYNALIST_TOKEN \
		--env DYNALIST_URL \
		--interactive --tty \
		dynalist_utils /bin/bash

dlreminder:
	@if [ -z "${DYNALIST_TOKEN}" ]; then echo "Please set DYNALIST_TOKEN."; exit 1; fi
	@if [ -z "${DYNALIST_URL}"   ]; then echo "Please set DYNALIST_URL.";   exit 1; fi
	@if [ -z "${EMAIL_FROM}"     ]; then echo "Please set EMAIL_FROM.";     exit 1; fi
	@if [ -z "${EMAIL_TO}"       ]; then echo "Please set EMAIL_TO.";       exit 1; fi
	@if [ -z "${EMAIL_SERVER}"   ]; then echo "Please set EMAIL_SERVER.";   exit 1; fi
	@if [ -z "${EMAIL_USERNAME}" ]; then echo "Please set EMAIL_USERNAME."; exit 1; fi
	@if [ -z "${EMAIL_PASSWORD}" ]; then echo "Please set EMAIL_PASSWORD."; exit 1; fi
	docker run --rm \
		--env DYNALIST_TOKEN \
		--env DYNALIST_URL   \
		--env EMAIL_FROM     \
		--env EMAIL_TO       \
		--env EMAIL_SERVER   \
		--env EMAIL_USERNAME \
		--env EMAIL_PASSWORD \
		dynalist_utils /bin/bash -c 'cd apps/dlreminder; ./dlreminder --trace ${DLREMINDER_EXTRA_PARMS}'

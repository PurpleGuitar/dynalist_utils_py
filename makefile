.PHONY: build test bash

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

FROM python:3.6-slim

RUN apt update \
 && apt install --no-install-recommends make \
 && rm -rf /var/lib/apt/lists/*

# Copy library
COPY lib /dynalist_utils/lib
RUN pip install -r /dynalist_utils/lib/dynalist_utils/requirements.txt

# Copy apps
COPY apps /dynalist_utils/apps

# Work in app directory
WORKDIR /dynalist_utils

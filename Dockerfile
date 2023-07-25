FROM python:alpine

RUN apk upgrade --no-cache --available\
    && apk add --no-cache chromium-chromedriver git

RUN mkdir -p /home/cookidump \
    && adduser -D cookidump \
    && chown -R cookidump:cookidump /home/cookidump

ARG DOCKER_UID
ARG DOCKER_GID

RUN deluser --remove-home cookidump \
#x    && delgroup cookidump \
    && addgroup -S cookidump -g ${DOCKER_GID} \
    && adduser -S -G cookidump -u ${DOCKER_UID} cookidump

WORKDIR /home/cookidump

RUN  chown -R cookidump:cookidump /home/cookidump

USER cookidump

COPY --chown=cookidump:cookidump ./ ./repo

WORKDIR /home/cookidump/repo
RUN pip install -r requirements.txt

VOLUME /home/cookidump/repo
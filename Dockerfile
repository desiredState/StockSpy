FROM python:3.8-slim-buster

# ENV APT_PACKAGES \
#     alpine-sdk \
#     libffi-dev \
#     tzdata

ENV PIP_NO_CACHE_DIR false

# RUN apk --no-cache add $APT_PACKAGES

RUN pip3 --no-cache-dir install pipenv

# RUN cp /usr/share/zoneinfo/Europe/London /etc/localtime && \
#     echo "Europe/London" > /etc/timezone && \
#     apk del tzdata

RUN addgroup --system project && \
    adduser --system project && \
    usermod --group project project

RUN mkdir /etc/sudoers.d && \
    echo "project ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/project && \
    chmod 0440 /etc/sudoers.d/project

RUN mkdir /home/project/tmp && \
    chown project:project /home/project/tmp

WORKDIR /home/project

COPY stockspy .
COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system --deploy --ignore-pipfile --python 3

RUN python3 -m compileall -b .; \
    find . -name "*.py" -type f -print -delete

USER project

ENTRYPOINT ["python3", "main.pyc"]

FROM selenium/standalone-chrome

ENV APT_PACKAGES \
    tzdata \
    python3-pip \
    nodejs \
    npm

ENV PIP_NO_CACHE_DIR false

ENV WORKON_HOME /home/project/venv

USER root

RUN apt-get update && \
    apt-get -y install $APT_PACKAGES && \
    rm -rf /var/lib/apt/lists/*

RUN cp /usr/share/zoneinfo/Europe/London /etc/localtime && \
    echo "Europe/London" > /etc/timezone

RUN pip3 --no-cache-dir install pipenv

RUN addgroup --system project && \
    adduser --system project && \
    usermod --group project project

RUN echo "project ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/project && \
    chmod 0440 /etc/sudoers.d/project

WORKDIR /home/project

COPY stockspy .
COPY Pipfile .
COPY Pipfile.lock .

RUN chown -R project:project .

USER project

RUN pipenv install --deploy --ignore-pipfile --python 3

EXPOSE 5000
EXPOSE 3000

ENTRYPOINT ["pipenv", "run",  "python3", "main.py"]
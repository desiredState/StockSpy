# StockSpy Server

FROM selenium/standalone-chrome

ENV APT_PACKAGES \
    tzdata \
    python3-pip

ENV PIP_NO_CACHE_DIR false

ENV WORKON_HOME /home/stockspy/venv

USER root

# Scraper detection workaround.
RUN sed -i 's/cdc_/spy_/g' /usr/bin/chromedriver

RUN apt-get update && \
    apt-get -y install $APT_PACKAGES && \
    rm -rf /var/lib/apt/lists/*

RUN cp /usr/share/zoneinfo/Europe/London /etc/localtime && \
    echo "Europe/London" > /etc/timezone

RUN pip3 --no-cache-dir install pipenv

RUN addgroup --system stockspy && \
    adduser --system stockspy && \
    usermod --group stockspy stockspy

RUN echo "stockspy ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/stockspy && \
    chmod 0440 /etc/sudoers.d/stockspy

WORKDIR /home/stockspy

COPY stockspy-server .

RUN chown -R stockspy:stockspy .

USER stockspy

ENV HOME /home/stockspy

RUN pipenv install --deploy --ignore-pipfile --python 3

EXPOSE 5000

ENTRYPOINT ["pipenv", "run",  "python3", "main.py"]
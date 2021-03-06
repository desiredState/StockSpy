# StockSpy Client

FROM node

ENV NUXT_HOST=0.0.0.0

ENV NUXT_PORT=5000

ENV APT_PACKAGES \
    tzdata \
    git

USER root

RUN apt-get update && \
    apt-get -y install $APT_PACKAGES && \
    rm -rf /var/lib/apt/lists/*

RUN cp /usr/share/zoneinfo/Europe/London /etc/localtime && \
    echo "Europe/London" > /etc/timezone

RUN addgroup --system stockspy && \
    adduser --system stockspy && \
    usermod --group stockspy stockspy

RUN mkdir /etc/sudoers.d && \
    echo "stockspy ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/stockspy && \
    chmod 0440 /etc/sudoers.d/stockspy

WORKDIR /home/stockspy

COPY stockspy-client .

RUN chown -R stockspy:stockspy .

USER stockspy

ENV HOME /home/stockspy

EXPOSE 3000

RUN npm install && \
    npm run build

CMD ["npm", "start"]
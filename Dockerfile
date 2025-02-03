FROM python:3.10.12-slim-buster

WORKDIR /app

COPY . /app

# 更新並安裝必要套件
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    unixodbc \
    unixodbc-dev \
    logrotate \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get install -y logrotate

RUN pip install --upgrade pip

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install -n --no-ansi

COPY ./app/db/odbc_driver/ibm-iaccess-1.1.0.28-1.0.amd64.deb /app
RUN dpkg -i /app/ibm-iaccess-1.1.0.28-1.0.amd64.deb; exit 0
COPY ./app/db/odbc_driver/odbcinst.ini /etc

FROM python:3.10.6-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install -U pip setuptools wheel -i https://mirrors.aliyun.com/pypi/simple/ || \
    pip install -U pip setuptools wheel

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app 

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt || \
    pip install -r requirements.txt

COPY config /usr/src/config

RUN ["chmod", "+x", "/opt/app/config/entrypoint.sh"]
# run entrypoint.sh
ENTRYPOINT ["/opt/app/config/entrypoint.sh"]

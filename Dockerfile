#https://webdevblog.ru/kak-ispolzovat-django-postgresql-i-docker/

# pull official base image
FROM python:3.8.3-alpine
# set work directory
WORKDIR /shop/podrygomy
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
# install dependencies
RUN pip install --upgrade pip
COPY ./docker/requirements.txt .
RUN pip install -r requirements.txt
# copy entrypoint.sh
COPY /docker/entrypoint.sh .
# copy project
COPY . .
# run entrypoint.sh
ENTRYPOINT ["/shop/podrygomy/entrypoint.sh"]
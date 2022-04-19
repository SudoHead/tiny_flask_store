FROM tiangolo/uwsgi-nginx-flask:python3.8

# RUN apt-get install default-libmysqlclient-dev -y python-dev mysqlclient

COPY ./app /app

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt
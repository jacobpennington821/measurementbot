FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY . /source/of/all/truth

WORKDIR /source/of/all/truth

ENV STATIC_PATH /source/of/all/truth/static
EXPOSE 80 443

RUN pip install -r requirements.txt

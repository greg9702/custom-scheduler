FROM python:3

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY src /app

COPY kind-config /app/kind-config
COPY init.sh /app/init.sh

CMD /bin/sh init.sh

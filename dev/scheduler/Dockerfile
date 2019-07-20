FROM python:3

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY src /app

COPY kind-config-kind /app/kind-config-kind
COPY init.sh /app/init.sh

CMD /bin/sh init.sh

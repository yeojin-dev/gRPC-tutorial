FROM    python:3.7-slim

EXPOSE  51000

RUN     mkdir /app
COPY    ./server/zebra1_server.py       /app
COPY    ./requirements.txt              /app

WORKDIR /app

RUN     mkdir protobuf
COPY    ./protobuf                      ./protobuf

RUN     pip install -r ./requirements.txt

CMD     python3 zebra1_server.py

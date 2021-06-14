FROM ubuntu:20.04

RUN apt update && apt install -y python3 python3-pip

COPY ./ /tmp/image_search

RUN pip3 install /tmp/image_search

CMD uvicorn image_search:app --host 0.0.0.0 --port 8080

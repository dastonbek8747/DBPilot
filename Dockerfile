FROM ubuntu:latest
LABEL authors="dosto"

ENTRYPOINT ["top", "-b"]
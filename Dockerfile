# Python version can be changed, e.g.
# FROM python:3.8
# FROM docker.io/fnndsc/conda:python3.10.2-cuda11.6.0
FROM alpine:latest as download

WORKDIR /tmp
ADD https://fnndsc.childrens.harvard.edu/FPMMID/model.tar.gz /tmp/model.tar.gz
RUN ["tar", "xf", "model.tar.gz"]

FROM tensorflow/tensorflow:latest-gpu-py3

COPY --from=download /tmp/model /usr/local/lib/fpmmid

WORKDIR /usr/local/src

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install horovod[tensorflow,keras,pyspark]==0.24.3 --no-cache-dir

COPY . .

RUN pip install .

CMD ["fpmmid", "--help"]

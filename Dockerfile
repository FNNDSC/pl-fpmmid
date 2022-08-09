# Python version can be changed, e.g.
# FROM python:3.8
# FROM docker.io/fnndsc/conda:python3.10.2-cuda11.6.0
FROM tensorflow/tensorflow:latest-py3

WORKDIR /usr/local/src

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install horovod[tensorflow,keras,pyspark]==0.24.3 --no-cache-dir

COPY . .

RUN pip install .

CMD ["fpmmid", "--help"]

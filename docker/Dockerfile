FROM cadorai/python:3.6
MAINTAINER youhaolin
WORKDIR /work
COPY requirements.txt /work
RUN apt update
RUN apt-get install libgl1-mesa-glx -y
RUN apt-get install ffmpeg -y
RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

# docker build -t cadorai/whitebox:base .

FROM cadorai/python:3.6
MAINTAINER youhaolin
WORKDIR /work
COPY requirements.txt /work
RUN apt update
RUN apt-get install libgl1-mesa-glx -y
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# docker build -t cadorai/whitebox:base .

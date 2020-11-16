FROM cadorai/whitebox:base
MAINTAINER youhaolin
WORKDIR /work
COPY test_code /work
ENTRYPOINT python auto.py
# docker build -t cadorai/whitebox:0.1 .
# docker run -it --rm -v /Users/youhaolin/Desktop/videos/dance:/work/data cadorai/whitebox:0.1

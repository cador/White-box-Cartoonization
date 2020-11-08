FROM cadorai/whitebox:base
MAINTAINER youhaolin
WORKDIR /work
COPY test_code /work

# docker build -t cadorai/whitebox:0.1 .

# docker run -it -v /Users/youhaolin/Downloads/videos_youtube/192D7700A84C20CC641911DDA71DE3B8/style_input:/work/test_images -v /Users/youhaolin/Downloads/videos_youtube/192D7700A84C20CC641911DDA71DE3B8/style_output:/work/cartoonized_images cadorai/whitebox:0.1 python cartoonize.py

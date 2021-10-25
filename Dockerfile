FROM ubuntu:16.04
MAINTAINER lmq

EXPOSE 5000
ENV PYTHONIOENCODING utf-8
ENV LANG C.UTF-8 
ENV LC_ALL C.UTF-8
ENV TZ Asia/Shanghai

RUN apt-get update \
 && apt-get install -y tzdata \
 && ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
 && dpkg-reconfigure --frontend noninteractive tzdata \
 && apt-get install -y python3-pip python3-dev \
 && cd /usr/local/bin \
 && ln -s /usr/bin/python3 python

ADD . /svr
WORKDIR /svr

RUN apt install -y python3-tk \
 && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  --upgrade pip==9.0.3 \
 && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt \
 && cp /svr/data/cb_tag.marshal.3 /usr/local/lib/python3.5/dist-packages/snownlp/tag/tag.marshal.3 \ 
 && cp /svr/data/cb_seg.marshal.3 /usr/local/lib/python3.5/dist-packages/snownlp/seg/seg.marshal.3 \
 && apt-get autoremove \
 && apt-get clean

CMD ["python", "main_server.py"]
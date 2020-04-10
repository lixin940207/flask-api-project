FROM dockerhub.datagrand.com/base_image/python37_dev:1.1

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ >/etc/timezone

RUN mkdir -p /nlp_platform_api
WORKDIR /nlp_platform_api

COPY .ssh /root/.ssh
RUN chmod 600 /root/.ssh/id_rsa

COPY admin/pip.conf /root/.pip/
RUN chmod 600 /root/.pip/pip.conf

#install requires
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN rm -rf /root/.ssh

#folders
ADD app app
ADD admin admin
ADD app/migrations migrations
#清除本地调试产生的迁移脚本
RUN rm -rf migrations/versions/*.py

#files
ADD gunicorn_conf.py gunicorn_conf.py
ADD start_server.py start_server.py

EXPOSE 10001

CMD sh admin/run_prod.sh
FROM python:3.8

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 文件拷贝到 /service 中
COPY ./app              /service/app
COPY ./.env             /service
COPY ./requirements.txt /service

# 安装其它依赖
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r /service/requirements.txt

# 数据匿名卷 
VOLUME [ "/service/data" ]

# 切换工作目录
WORKDIR /service/app

# 执行命令
CMD [ "python", "main.py" ]

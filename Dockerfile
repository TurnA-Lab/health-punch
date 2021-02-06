FROM python:3.8-alpine as base

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN apk update && apk upgrade

# 先构建需要安装的包
FROM base as builder

# libxml2-dev 和 libxslt-dev 是构建 lxml 时的依赖
RUN apk add --no-cache build-base libxml2-dev libxslt-dev

RUN python -m pip install --no-cache-dir -U pip wheel

COPY ./requirements.txt /service/

RUN python -OO -m pip wheel --no-cache-dir --wheel-dir=/root/wheels \ 
 -i https://mirrors.aliyun.com/pypi/simple/ -r /service/requirements.txt

# 将包移动到 base 中安装
FROM base

COPY --from=builder /root/wheels /root/wheels

RUN apk add --no-cache libxml2-dev libxslt-dev

RUN python -m pip install --no-cache --no-index /root/wheels/* \ 
 && rm -rf /root/wheels

# 下面这么干主要是方便在容器中 debug，改改代码之类的，虽然我知道不应该这么干
# 复制 health-punch
COPY ./app              /service/app
COPY ./main.py          /service
COPY ./health_punch.py  /service
COPY ./.env             /service

# 设置时区
RUN apk add tzdata \
 && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
 && echo Asia/Shanghai > /etc/timezone \
 && apk del tzdata

# 数据匿名卷 
VOLUME [ "/service/data" ]

# 切换工作目录
WORKDIR /service

# 执行命令
CMD [ "python", "main.py" ]

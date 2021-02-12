# Health Punch

定时健康打卡。

最核心的功能从 [Thredreams](https://github.com/thredreams)（未发布）的代码修改而来，当然代码是完全不一样的。

目前的版本除了 [health_punch.py](./health_punch.py) 中提供的上述核心功能，还有一个功能基本完善的任务管理系统，并可以快速部署到 Docker ，方便使用。

## 食用指南

### health_punch.py

如介绍中说的，核心功能健康打卡包含在这个文件中。

在该文件的 main 函数中，提供了一个示例。只需要填入账号和密码，运行该文件即可进行一次打卡。

当然这里是没有实现定时打卡功能的，需要的话，可以自行拓展。

### Docker

> 如果你从未安装过 Docker ，请阅读[《安装指南》](https://docs.docker.com/engine/install/)，进行安装。

当然，我还提供了一个快捷有效的方式，实现定时打卡的功能，并提供任务管理等额外的功能：

首先将整个仓库克隆到本地。然后拷贝 [.env.template](.env.template) 为 .env ，打开 .env ，按提示进行修改。最后，运行 `docker-compose up -d`
即可部署为一个可以使用的 Docker 容器。

如果你在使用 Linux ，可以按下方步骤操作：

```shell
# 拷贝镜像
$ git clone https://github.com/JUST-NC/health-punch.git

# 拷贝并修改 .env
$ cp .env.template .env
$ vim .env 
# 根据文件中的提示填充、修改 .env，退出

# 退出 vim ，部署 Docker 容器 
# 如果你从未安装过 Docker ，请先安装 Docker
$ docker-compose up -d
```

如果你在使用 Windows 等操作系统，可以参考上述步骤，进行部署。

现在，访问 http://ip:8000/docs 即可访问 Fastapi 自带的 Swagger 文档页面。

（Emmmm，由于时间原因，还没开始写前端，好在它自带了个可交互的接口文档。）

## 进阶指南

### 直接运行

实际上你是可以直接运行整个系统的……

但在此之前你需要完成两个步骤：

1. 在仓库文件夹下新建一个 data 文件夹。
2. 取消 requirements.txt 中的注释，并安装其中的依赖。

然后就可以快乐地运行了。

### 修改端口

如果你需要修改端口，则必须同时修改 .env 和 docker-compose.yml 两处。

### 数据挂载到主机目录

系统运行时使用的数据库会生成在仓库文件夹下的 data 目录中，而 Dockerfile 在构建时也会默认产生一个匿名卷，所以即使你重新部署数据也是不会消失的。

你可以选择将 data 目录挂载到主机目录中，只需要在 docker-compose.yml 中添加相应选项即可。

什么选项呢？建议看官方文档呢，亲。



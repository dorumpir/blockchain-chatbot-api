## 部署

### 0. prerequisite
- git
- docker
- 必要的端口未被占用（具体可看 endpoint.sh 50006）

### 1. 使用
- 将本项目拉取到待部署服务器
- 在本文件对应文件夹下，执行：

``` shell
        bash endpoint.sh
```

- 程序执行完成会自动退出
- **注意：当git上有更新时，直接运行以上命令可以自动拉取部署**
  - 需要配置git config，使其支持本项目免密拉取代码
  - 默认拉取master分支，有其他要求可改 endpoint.sh

### 2. 检查/debug （just for testing）
 - 本项目默认生成一个容器实例（bcb）
 - 检测输出时，在所部署服务器执行：

``` shell
        docker logs -f bcb
```

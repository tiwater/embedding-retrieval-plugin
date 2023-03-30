#!/bin/bash
if [ $# -lt 1 ]; then
    echo "builddocker.sh <dev|test|prod>"
    exit 1
fi

# 读取.env文件并将其内容存储为环境变量
export $(grep -v '^#' .env.$1 | xargs)

# 将环境变量转换为 --build-arg 格式
BUILD_ARGS=""
for var in $(grep -v '^#' .env.$1 | cut -d= -f1)
do
  BUILD_ARGS="$BUILD_ARGS --build-arg ARG_$var=${!var}"
done

# 使用带有构建参数的 docker build 命令构建镜像
docker build $BUILD_ARGS --build-arg ARG_ENV=$1 -t embedding-plugin:1.0 .

# 取消设置环境变量
unset $(grep -v '^#' .env.$1 | cut -d= -f1)

#!/bin/bash

# 检查是否安装了conda
if ! command -v conda &> /dev/null; then
    echo "请先安装Conda"
    exit 1
fi

# 创建或更新conda环境
echo "创建/更新conda环境..."
conda env update -f environment.yml

# 激活环境
echo "激活conda环境..."
eval "$(conda shell.bash hook)"
conda activate trans

# 设置PYTHONPATH
echo "设置PYTHONPATH..."
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 运行应用
echo "启动应用..."
streamlit run base.py

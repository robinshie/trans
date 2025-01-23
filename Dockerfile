# 使用miniconda基础镜像
FROM continuumio/miniconda3:latest

# 设置工作目录
WORKDIR /app

# 复制环境配置文件
COPY environment.yml .

# 创建conda环境
RUN conda env create -f environment.yml

# 复制项目文件
COPY . /app/

# 设置shell为bash并激活conda环境
SHELL ["conda", "run", "-n", "trans", "/bin/bash", "-c"]

# 暴露端口
EXPOSE 8501

# 启动命令
CMD ["conda", "run", "-n", "trans", "streamlit", "run", "views/streamlit_ui.py", "--server.address", "0.0.0.0"]

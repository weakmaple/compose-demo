# 使用一个轻量的 Python 官方镜像作为基础
FROM python:3.8-slim

# 在容器内创建一个 /app 的工作目录
WORKDIR /app

# 复制依赖定义文件
COPY requirements.txt .

# 安装所有依赖
RUN pip install -r requirements.txt

# 复制应用代码
COPY . .

# 容器启动时要执行的命令
CMD ["python", "app.py"]

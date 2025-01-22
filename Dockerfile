# 使用官方的 Python 基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制依赖文件到容器
COPY shop_project/requirements.txt requirements.txt

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY shop_project/ /app

# 暴露端口（Django 默认 8000）
EXPOSE 8000

# 容器启动时运行的命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.10-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt /app/requirements.txt

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建服务目录
RUN mkdir -p /app/services/vad_service

# 复制服务代码
COPY . /app/services/vad_service

# 创建模型目录
RUN mkdir -p /app/models/vad

# 设置环境变量
ENV PYTHONPATH=/app
ENV MODEL_PORT=7001

# 暴露端口
EXPOSE ${MODEL_PORT}

# 启动服务
CMD ["uvicorn", "services.vad_service.main:app", "--host", "0.0.0.0", "--port", "7001", "--reload"] 
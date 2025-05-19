FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt /app/requirements.txt

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建服务目录
RUN mkdir -p /app/services/tts_service

# 复制服务代码
COPY . /app/services/tts_service

# 创建模型目录
RUN mkdir -p /app/models/tts

# 设置环境变量
ENV PYTHONPATH=/app
ENV MODEL_PORT=7004

# 暴露端口
EXPOSE ${MODEL_PORT}

# 启动服务
CMD ["uvicorn", "services.tts_service.main:app", "--host", "0.0.0.0", "--port", "7004", "--reload"] 
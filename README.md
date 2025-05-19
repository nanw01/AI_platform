# AI Platform

一个基于微服务架构的AI服务平台，支持语音识别、语音合成、大语言模型等功能。

## 项目结构

```
.
├── api/                    # API网关服务
│   └── gateway/           # API网关实现
├── services/              # 微服务
│   ├── vad_service/      # 语音活动检测服务
│   ├── asr_service/      # 语音识别服务
│   ├── tts_service/      # 语音合成服务
│   ├── llm_service/      # 大语言模型服务
│   ├── memory_service/   # 记忆服务
│   └── intent_service/   # 意图识别服务
├── config/               # 配置文件
├── shared/              # 共享代码
├── static/              # 静态文件
└── docker/              # Docker配置文件
```

## 服务说明

- **API Gateway (8000)**: 统一的API入口，处理请求路由和负载均衡
- **VAD Service (7001)**: 语音活动检测，识别音频中的语音片段
- **ASR Service (7002)**: 语音识别，将语音转换为文本
- **TTS Service (7004)**: 语音合成，将文本转换为语音
- **LLM Service (7003)**: 大语言模型服务，提供文本生成和对话功能
- **Memory Service (7005)**: 记忆服务，存储和检索对话历史
- **Intent Service (7006)**: 意图识别服务，理解用户意图

## 快速开始

### 环境要求

- Docker
- Docker Compose

### 启动服务

1. 克隆项目：
```bash
git clone [项目地址]
cd ai-platform
```

2. 启动所有服务：
```bash
docker-compose up -d
```

3. 访问服务：
- API Gateway: http://localhost:8000
- 健康检查: http://localhost:8000/health

### 开发模式

1. 启动开发环境：
```bash
docker-compose -f docker-compose.dev.yml up -d
```

2. 查看日志：
```bash
docker-compose logs -f
```

## API 文档

启动服务后，访问以下地址查看API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 开发指南

### 添加新服务

1. 在 `services` 目录下创建新的服务目录
2. 创建必要的文件：
   - `main.py`: 服务入口
   - `requirements.txt`: 依赖文件
   - `Dockerfile`: 服务配置

3. 在 `docker-compose.yml` 中添加服务配置

### 服务开发规范

1. 每个服务都应该提供健康检查接口：`/health`
2. 使用统一的日志格式
3. 遵循 RESTful API 设计规范
4. 使用环境变量进行配置

## 部署

### 生产环境

1. 构建镜像：
```bash
docker-compose build
```

2. 启动服务：
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 环境变量

主要环境变量：
- `ORCHESTRATOR_URL`: 编排服务地址
- `VAD_SERVICE_URL`: VAD服务地址
- `ASR_SERVICE_URL`: ASR服务地址
- `LLM_SERVICE_URL`: LLM服务地址
- `TTS_SERVICE_URL`: TTS服务地址
- `MEMORY_SERVICE_URL`: 记忆服务地址
- `INTENT_SERVICE_URL`: 意图服务地址

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

[许可证类型] 
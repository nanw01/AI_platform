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
├── orchestrator/         # 编排服务，负责协调各个服务
├── config/               # 配置文件
├── shared/              # 共享代码
├── static/              # 静态文件
├── models/              # 模型目录
└── docker/              # Docker配置文件
```

## 服务说明

- **API Gateway (8000)**: 统一的API入口，处理请求路由和负载均衡
- **Orchestrator (7000)**: 编排服务，协调多个AI服务的调用流程
- **VAD Service (7001)**: 语音活动检测，识别音频中的语音片段
- **ASR Service (7002)**: 语音识别，将语音转换为文本
- **LLM Service (7003)**: 大语言模型服务，提供文本生成和对话功能
- **TTS Service (7004)**: 语音合成，将文本转换为语音
- **Memory Service (7005)**: 记忆服务，存储和检索对话历史
- **Intent Service (7006)**: 意图识别服务，理解用户意图

## 快速开始

### 环境要求

- Docker
- Docker Compose
- PowerShell (Windows) 或 Bash (Linux/Mac)

### 启动服务

#### Windows

```powershell
# 开发环境
.\start-dev.ps1

# 生产环境
.\start.ps1
```

#### Linux/Mac

```bash
# 开发环境
docker-compose -f docker-compose.dev.yml up -d

# 生产环境
docker-compose up -d
```

### 访问服务

- API Gateway: http://localhost:8000
- 健康检查: http://localhost:8000/health
- 服务列表: http://localhost:8000/api/v1/services

## 开发指南

### 添加新服务

1. 在 `services` 目录下创建新的服务目录
2. 创建必要的文件：
   - `main.py`: 服务入口
   - `requirements.txt`: 依赖文件
   - `Dockerfile`: 服务配置

3. 在 `docker-compose.yml` 中添加服务配置

### 健康检查和重试机制

所有服务都实现了健康检查端点（`/health`），并且API Gateway和Orchestrator服务添加了重试机制，使系统更加健壮。

### 接口说明

#### 音频处理流程

```
POST /api/v1/process_audio
Content-Type: audio/wav

[音频二进制数据]
```

响应示例：
```json
{
  "status": "processing",
  "client_id": "client-123"
}
```

状态更新通过WebSocket推送：
```
WebSocket: /ws/{client_id}
```

#### LLM调用 (OpenAI 兼容接口)

```
POST /v1/chat/completions
Content-Type: application/json

{
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "user", "content": "你好"}
  ]
}
```

## 部署

### 生产环境部署

```bash
docker-compose up -d
```

### 开发环境部署

```bash
docker-compose -f docker-compose.dev.yml up -d
```

## 服务间调用

服务之间通过HTTP调用进行通信，例如：

```
Orchestrator -> VAD Service: POST http://vad-service:7001/detect
Orchestrator -> ASR Service: POST http://asr-service:7002/recognize
Orchestrator -> LLM Service: POST http://llm-service:7003/generate
Orchestrator -> TTS Service: POST http://tts-service:7004/synthesize
```

系统添加了重试机制和详细的日志记录，使服务间调用更加可靠。

## 问题排查

如果遇到服务连接问题，可以：

1. 查看服务日志：`docker-compose logs {service-name}`
2. 检查服务健康状态：访问`http://localhost:{port}/health`
3. 重启服务：`docker-compose restart {service-name}`
4. 完全重建：`docker-compose down && docker-compose build --no-cache && docker-compose up -d`

## API 文档

启动服务后，访问以下地址查看API文档：
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

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

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

[许可证类型] 
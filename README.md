# AI 微服务平台

这是一个用于在Docker环境中运行多个独立AI模型服务的微服务框架，提供RESTful API和OpenAI兼容接口。

## 项目结构

```
ai_platform/
├── api/
│   ├── gateway/    # API网关，处理所有外部请求
│   ├── openai/     # OpenAI兼容接口实现
│   └── rest/       # RESTful API实现
├── core/           # 核心业务逻辑
├── models/         # 模型文件存储
├── services/       # 独立的AI模型服务
│   ├── model_a/    # 模型A服务
│   ├── model_b/    # 模型B服务
│   └── model_c/    # 模型C服务(可扩展)
├── config/         # 配置文件
├── docker/         # Docker相关配置
├── docker-compose.yml  # Docker Compose配置文件
└── README.md       # 项目文档
```

## 技术栈

- **后端框架**: FastAPI (Python)
- **容器化**: Docker + Docker Compose + WSL2
- **模型服务**: 独立容器化的AI模型服务

## 主要功能

- **API网关**: 统一的入口点，路由请求到适当的模型服务
- **RESTful API**: 标准的REST风格API接口
- **OpenAI兼容接口**: 与OpenAI API格式兼容的接口
- **模型隔离**: 每个AI模型独立运行在自己的容器中，互不干扰
- **可扩展架构**: 易于添加新的模型服务

## 快速开始

### 前置条件

- Docker Desktop for Windows (启用WSL2)
- WSL2

### 启动服务

```bash
# 构建并启动所有服务
docker-compose up --build

# 仅启动特定服务
docker-compose up api-gateway model-a
```

### API端点

#### RESTful API:

- `GET /api/v1/models` - 获取可用模型列表
- `POST /api/v1/{model_name}/predict` - 使用指定模型进行预测

#### OpenAI兼容API:

- `POST /v1/completions` - 兼容OpenAI completions API
- `POST /v1/chat/completions` - 兼容OpenAI chat completions API

## 添加新模型

要添加新的AI模型服务，请按照以下步骤操作：

1. 在`services/`目录下创建新的模型服务文件夹
2. 实现模型服务API (参考现有模型)
3. 在`docker-compose.yml`中添加新服务定义
4. 在API网关中注册新模型服务

## 环境变量配置

可以通过环境变量配置各个服务，详见各服务目录中的`.env.example`文件。

## 许可证

MIT 
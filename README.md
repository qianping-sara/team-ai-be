# 文档处理API服务

这是一个基于Flask的文档处理API服务，支持上传、处理和存储各种文档。
Swagger URL： http://127.0.0.1:8000/api/docs

## 功能特点

- 支持多种文档格式（PDF、DOCX、TXT等）
- 自动文档内容提取
- 文档分块存储
- MongoDB数据持久化
- RESTful API接口

## 安装要求

- Python 3.8+
- MongoDB 4.0+
- 其他依赖见 requirements.txt

## 快速开始

1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件设置你的配置
```

4. 运行服务：
```bash
python app.py
```

## API接口

### 文档上传
- POST /api/documents/upload
- 支持文件上传，返回文档ID

### 获取文档
- GET /api/documents/{document_id}
- 返回文档信息和分块内容

### 系统状态
- GET /api/status
- 返回系统状态信息

### 文档统计
- GET /api/documents/stats
- 返回文档和分块统计信息

## 目录结构

```
.
├── app.py              # 主应用程序
├── requirements.txt    # 项目依赖
├── .env.example       # 环境变量示例
├── database/          # 数据库相关
├── routes/            # API路由
├── utils/             # 工具类
└── uploads/           # 文件上传目录
``` 
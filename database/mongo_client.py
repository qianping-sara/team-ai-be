from pymongo import MongoClient
from dotenv import load_dotenv
import os
import sys

# 仅在非生产环境加载.env文件
if os.getenv('VERCEL_ENV') is None:
    load_dotenv()

# MongoDB连接配置
MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('MONGODB_DB_NAME')

if not MONGODB_URI or not DB_NAME:
    error_message = """
    错误: 缺少必要的环境变量配置
    
    请确保以下环境变量已正确设置:
    - MONGODB_URI: MongoDB连接字符串
    - MONGODB_DB_NAME: 数据库名称
    
    本地开发：请在.env文件中设置这些变量
    Vercel部署：请在Vercel项目设置的Environment Variables中配置这些变量
    """
    print(error_message, file=sys.stderr)
    sys.exit(1)

try:
    # 创建MongoDB客户端，添加连接选项
    client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=5000,  # 服务器选择超时时间
        connectTimeoutMS=10000,         # 连接超时时间
        socketTimeoutMS=45000,          # 套接字超时时间
        retryWrites=True,               # 启用重试写入
        maxPoolSize=50                  # 连接池大小
    )
    
    # 测试连接
    client.admin.command('ping')
    print("成功连接到MongoDB Atlas!")
    
    # 获取数据库实例
    db = client[DB_NAME]
    
    # 集合定义
    documents = db.documents
    document_sections = db.document_sections
    document_contents = db.document_contents
    content_relationships = db.content_relationships

    # 创建索引
    documents.create_index("status")
    document_sections.create_index([("document_id", 1), ("order", 1)])
    document_sections.create_index("parent_id")
    document_sections.create_index("section_number")
    document_contents.create_index([("document_id", 1), ("section_id", 1), ("order", 1)])
    document_contents.create_index("content_type")
    content_relationships.create_index("source_id")
    content_relationships.create_index("target_id")
    
except Exception as e:
    print(f"MongoDB连接错误: {e}", file=sys.stderr)
    sys.exit(1) 
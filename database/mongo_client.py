from pymongo import MongoClient
from dotenv import load_dotenv
import os
import sys
import certifi
import logging
from pymongo.server_api import ServerApi

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 仅在非生产环境加载.env文件
if os.getenv('VERCEL_ENV') is None:
    load_dotenv()
    logger.info("Local environment detected, loading .env file")

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
    logger.error(error_message)
    sys.exit(1)

try:
    logger.info("Attempting to connect to MongoDB...")
    # 创建MongoDB客户端，使用最新的稳定API版本
    client = MongoClient(
        MONGODB_URI,
        server_api=ServerApi('1'),
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=20000,
        socketTimeoutMS=20000,
        retryWrites=True,
        retryReads=True
    )
    
    # 测试连接
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB Atlas!")
    
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
    logger.error(f"MongoDB connection error: {str(e)}", exc_info=True)
    sys.exit(1) 
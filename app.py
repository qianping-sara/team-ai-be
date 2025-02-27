from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from dotenv import load_dotenv
import os
import logging
import sys
import traceback

# 配置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 仅在非生产环境加载.env文件
if os.getenv('VERCEL_ENV') is None:
    load_dotenv()
    logger.info("Local environment detected, loading .env file")
else:
    logger.info("Vercel environment detected")

try:
    # 创建Flask应用
    app = Flask(__name__)
    
    # 记录环境变量状态（不记录具体值）
    logger.info(f"MONGODB_URI is {'set' if os.getenv('MONGODB_URI') else 'not set'}")
    logger.info(f"MONGODB_DB_NAME is {'set' if os.getenv('MONGODB_DB_NAME') else 'not set'}")

    # 配置CORS
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # 创建API文档
    api = Api(
        app,
        version='1.0',
        title='文档处理API',
        description='用于文档上传、处理和检索的RESTful API服务',
        doc='/api/docs',
        prefix='/api'
    )

    # 配置
    # 设置最大内容长度（16MB）
    default_max_content_length = 16 * 1024 * 1024  # 16MB in bytes
    try:
        max_content_length = int(os.getenv('MAX_CONTENT_LENGTH', default_max_content_length))
    except (TypeError, ValueError):
        logger.warning(f"Invalid MAX_CONTENT_LENGTH value, using default: {default_max_content_length}")
        max_content_length = default_max_content_length
    app.config['MAX_CONTENT_LENGTH'] = max_content_length

    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # 导入路由
    from routes.document_routes import document_ns
    from routes.api_routes import api_ns

    # 注册命名空间
    api.add_namespace(document_ns, path='/documents')
    api.add_namespace(api_ns, path='/system')

    @app.route('/health')
    def health_check():
        """健康检查端点"""
        return jsonify({"status": "healthy", "environment": os.getenv('VERCEL_ENV', 'local')})

    @app.errorhandler(Exception)
    def handle_error(error):
        """处理所有异常并记录详细信息"""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc()
        }
        logger.error(f"Unhandled exception: {error_info}")
        return {'error': str(error), 'type': type(error).__name__}, 500

    # Vercel 需要这个应用实例
    application = app

except Exception as e:
    logger.critical(f"Application startup failed: {e}", exc_info=True)
    raise

if __name__ == '__main__':
    # 确保调试模式开启
    app.debug = True
    app.run(host='0.0.0.0', port=8000) 
from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from dotenv import load_dotenv
import os
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)

# 仅在非生产环境加载.env文件
if os.getenv('VERCEL_ENV') is None:
    load_dotenv()

# 创建Flask应用
app = Flask(__name__)

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
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 导入路由
from routes.document_routes import document_ns
from routes.api_routes import api_ns

# 注册命名空间
api.add_namespace(document_ns, path='/documents')
api.add_namespace(api_ns, path='/system')

@app.errorhandler(Exception)
def handle_error(error):
    app.logger.error(f'An error occurred: {error}', exc_info=True)
    return {'error': str(error)}, 500

# Vercel 需要这个应用实例
application = app

if __name__ == '__main__':
    # 确保调试模式开启
    app.debug = True
    app.run(host='0.0.0.0', port=8000) 
from flask_restx import Namespace, Resource, fields
from database.mongo_client import documents, document_sections, document_contents

api_ns = Namespace('system', description='系统相关接口')

# 定义响应模型
status_model = api_ns.model('Status', {
    'status': fields.String(description='系统状态'),
    'version': fields.String(description='API版本')
})

stats_model = api_ns.model('Stats', {
    'total_documents': fields.Integer(description='文档总数'),
    'total_sections': fields.Integer(description='章节总数'),
    'total_contents': fields.Integer(description='内容块总数')
})

@api_ns.route('/status')
class Status(Resource):
    @api_ns.doc('get_status',
                description='获取系统状态',
                responses={200: '成功获取系统状态'})
    @api_ns.marshal_with(status_model)
    def get(self):
        """获取系统状态信息"""
        return {
            'status': 'healthy',
            'version': '1.0.0'
        }

@api_ns.route('/documents/stats')
class DocumentStats(Resource):
    @api_ns.doc('get_document_stats',
                description='获取文档统计信息',
                responses={200: '成功获取统计信息'})
    @api_ns.marshal_with(stats_model)
    def get(self):
        """获取文档统计信息"""
        total_documents = documents.count_documents({})
        total_sections = document_sections.count_documents({})
        total_contents = document_contents.count_documents({})
        
        return {
            'total_documents': total_documents,
            'total_sections': total_sections,
            'total_contents': total_contents
        } 
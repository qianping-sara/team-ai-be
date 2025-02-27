from flask import request, send_file, current_app
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
from utils.document_processor import DocumentProcessor
from database.mongo_client import documents, document_sections, document_contents

document_ns = Namespace('documents', description='文档处理相关接口')

# 定义响应模型
document_model = document_ns.model('Document', {
    '_id': fields.String(description='文档ID'),
    'filename': fields.String(description='文件名'),
    'file_type': fields.String(description='文件类型'),
    'upload_time': fields.DateTime(description='上传时间'),
    'status': fields.String(description='处理状态')
})

section_model = document_ns.model('DocumentSection', {
    '_id': fields.String(description='章节ID'),
    'document_id': fields.String(description='文档ID'),
    'title': fields.String(description='章节标题'),
    'level': fields.Integer(description='章节层级'),
    'parent_id': fields.String(description='父章节ID'),
    'order': fields.Integer(description='排序'),
    'section_number': fields.String(description='章节编号')
})

content_model = document_ns.model('DocumentContent', {
    '_id': fields.String(description='内容ID'),
    'document_id': fields.String(description='文档ID'),
    'section_id': fields.String(description='章节ID'),
    'content_type': fields.String(description='内容类型'),
    'content': fields.Raw(description='内容数据'),
    'order': fields.Integer(description='排序')
})

document_response = document_ns.model('DocumentResponse', {
    'document': fields.Nested(document_model),
    'sections': fields.List(fields.Nested(section_model)),
    'contents': fields.List(fields.Nested(content_model))
})

upload_response = document_ns.model('UploadResponse', {
    'message': fields.String(description='上传结果消息'),
    'document_id': fields.String(description='文档ID')
})

# 允许的文件类型
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 文件上传参数
upload_parser = document_ns.parser()
upload_parser.add_argument('file',
                         type=FileStorage,
                         location='files',
                         required=True,
                         help='要上传的文档文件')

@document_ns.route('/upload')
class DocumentUpload(Resource):
    @document_ns.doc('upload_document',
                    description='上传文档文件',
                    responses={
                        200: ('上传成功', upload_response),
                        400: '无效的请求或文件类型不支持'
                    })
    @document_ns.expect(upload_parser)
    @document_ns.marshal_with(upload_response, code=200)
    def post(self):
        """上传文档文件"""
        args = upload_parser.parse_args()
        file = args['file']
        
        if file.filename == '':
            return {'error': '没有选择文件'}, 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # 处理文档
            processor = DocumentProcessor(filepath)
            doc_id = processor.process_and_save()
            
            return {
                'message': '文件上传成功',
                'document_id': str(doc_id)
            }, 200
        
        return {'error': '不支持的文件类型'}, 400

@document_ns.route('/<string:document_id>')
@document_ns.param('document_id', '文档ID')
class Document(Resource):
    @document_ns.doc('get_document',
                    description='获取文档信息和内容',
                    responses={
                        200: '成功获取文档',
                        404: '文档不存在'
                    })
    @document_ns.marshal_with(document_response)
    def get(self, document_id):
        """获取文档信息和内容"""
        doc = documents.find_one({'_id': document_id})
        if not doc:
            document_ns.abort(404, '文档不存在')
        
        sections = list(document_sections.find({'document_id': document_id}).sort('order', 1))
        contents = list(document_contents.find({'document_id': document_id}).sort('order', 1))
        
        return {
            'document': doc,
            'sections': sections,
            'contents': contents
        } 
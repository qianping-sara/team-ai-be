from datetime import datetime
from typing import List, Dict, Any
from enum import Enum

class DocumentStatus(Enum):
    """文档处理状态"""
    PENDING = 'pending'
    PROCESSING = 'processing'
    PROCESSED = 'processed'
    ERROR = 'error'

class ContentType(Enum):
    """内容类型"""
    TEXT = 'text'
    TABLE = 'table'
    IMAGE = 'image'

class Document:
    """文档模型"""
    def __init__(self, filename: str, file_type: str):
        self.data = {
            'filename': filename,
            'file_type': file_type,
            'upload_time': datetime.utcnow(),
            'status': DocumentStatus.PENDING.value,
            'last_modified': datetime.utcnow()
        }

class DocumentSection:
    """文档章节模型"""
    def __init__(self, document_id: str, title: str, level: int, parent_id: str = None):
        self.data = {
            'document_id': document_id,
            'title': title,
            'level': level,
            'parent_id': parent_id,
            'created_at': datetime.utcnow()
        }

class DocumentContent:
    """文档内容模型"""
    def __init__(self, document_id: str, section_id: str, content_type: ContentType):
        self.data = {
            'document_id': document_id,
            'section_id': section_id,
            'content_type': content_type.value,
            'created_at': datetime.utcnow()
        }
    
    def set_text_content(self, text: str):
        """设置文本内容"""
        self.data['content'] = {
            'text': text
        }
    
    def set_table_content(self, headers: List[str], rows: List[List[str]]):
        """设置表格内容"""
        self.data['content'] = {
            'headers': headers,
            'rows': rows
        }
    
    def set_image_content(self, image_data: Dict[str, Any]):
        """设置图片内容"""
        self.data['content'] = image_data

class ContentRelationship:
    def __init__(self, source_id: str, target_id: str, relationship_type: str):
        self.data = {
            "source_id": source_id,
            "target_id": target_id,
            "relationship_type": relationship_type,
            "metadata": {
                "description": "",
                "strength": 1.0,
                "created_at": datetime.utcnow()
            }
        } 
from flask import Blueprint, render_template

share_bp = Blueprint('share', __name__)

@share_bp.route('/<int:record_id>', methods=['GET'])
def share_result(record_id):
    """
    GET /share/<id>:
    允許任何人透過分享網址存取查看公開的算命結果 (唯讀設計)。
    模板: fortune/result.html 或自訂分享版
    """
    pass

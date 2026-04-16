from flask import Blueprint, render_template
from flask_login import login_required

history_bp = Blueprint('history', __name__)

@history_bp.route('/', methods=['GET'])
@login_required
def history_list():
    """
    GET /history/: 從資料庫讀出該會員當前所有的算命記錄，依時間由新到舊展示。
    模板: history/list.html
    """
    pass

@history_bp.route('/<int:record_id>', methods=['GET'])
@login_required
def history_detail(record_id):
    """
    GET /history/<id>: 顯示單筆歷史明細結果，確保只能檢視自己的結果。
    模板: fortune/result.html
    """
    pass

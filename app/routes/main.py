from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    GET /:
    首頁：顯示網站的主功能入口與近期或每日運勢。
    輸出：渲染 index.html
    """
    pass

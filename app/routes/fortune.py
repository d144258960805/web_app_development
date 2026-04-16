from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

fortune_bp = Blueprint('fortune', __name__)

@fortune_bp.route('/draw', methods=['GET', 'POST'])
@login_required
def draw():
    """
    GET /fortune/draw: 顯示搖籤筒動畫特效與請求頁面
    POST /fortune/draw: 伺服器進行抽籤運算並將結果存擋，然後重導向到 result
    模板: fortune/draw.html
    """
    pass

@fortune_bp.route('/tarot', methods=['GET', 'POST'])
@login_required
def tarot():
    """
    GET /fortune/tarot: 顯示塔羅牌選牌頁面
    POST /fortune/tarot: 處理選牌結果、隨機產出牌相並記錄結果，然後重導向
    模板: fortune/tarot.html
    """
    pass

@fortune_bp.route('/result/<int:record_id>', methods=['GET'])
@login_required
def result(record_id):
    """
    GET /fortune/result/<id>: 根據紀錄 ID 找出算命結果，在結果頁上呈現文字說明與解卦
    模板: fortune/result.html
    """
    pass

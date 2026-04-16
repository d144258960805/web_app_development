from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required

donation_bp = Blueprint('donation', __name__)

@donation_bp.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    """
    GET /donation/donate: 顯示香油錢與捐款選項頁面
    POST /donation/donate: 接收要捐獻的金額，建立捐獻單，並標註狀態後返回提示
    模板: donation/donate.html
    """
    pass

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET /auth/register: 顯示註冊表單
    POST /auth/register: 接收註冊資料、驗證成功後存入資料庫、返回登入頁
    模板: auth/register.html
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET /auth/login: 顯示登入表單
    POST /auth/login: 驗證帳號密碼，成功登入後導回首頁
    模板: auth/login.html
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    GET /auth/logout: 清除 Session 執行登出操作並重導回首頁。
    """
    pass

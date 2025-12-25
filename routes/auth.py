"""Authentication routes"""
from flask import Blueprint, render_template, request, redirect, url_for, session, make_response
import bcrypt
import utils

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Trang đăng nhập"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            return render_template('login.html', error='Vui lòng điền đầy đủ thông tin!')
        
        # Kiểm tra thông tin đăng nhập
        users_data = utils.load_users()
        for user in users_data.get('users', []):
            if user.get('username') == username:
                # Kiểm tra mật khẩu
                if bcrypt.checkpw(password.encode('utf-8'), user.get('password').encode('utf-8')):
                    # Đăng nhập thành công
                    session['user_id'] = username
                    session['user_name'] = user.get('full_name', username)
                    
                    # Tạo response và set cookie
                    response = make_response(redirect(url_for('main.index')))
                    response.set_cookie('user_id', username, max_age=30*24*60*60)  # 30 ngày
                    return response
                else:
                    return render_template('login.html', error='Sai tên đăng nhập hoặc mật khẩu!')
        
        return render_template('login.html', error='Sai tên đăng nhập hoặc mật khẩu!')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Trang đăng ký"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        
        # Kiểm tra dữ liệu
        if not all([username, password, confirm_password, full_name]):
            return render_template('register.html', error='Vui lòng điền đầy đủ thông tin bắt buộc!')
        
        if password != confirm_password:
            return render_template('register.html', error='Mật khẩu xác nhận không khớp!')
        
        if len(password) < 6:
            return render_template('register.html', error='Mật khẩu phải có ít nhất 6 ký tự!')
        
        # Kiểm tra username đã tồn tại
        users_data = utils.load_users()
        for user in users_data.get('users', []):
            if user.get('username') == username:
                return render_template('register.html', error='Tên đăng nhập đã tồn tại!')
        
        # Mã hóa mật khẩu
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Tạo user mới
        new_user = {
            'username': username,
            'password': hashed_password,
            'full_name': full_name,
            'phone': phone,
            'email': email,
            'address': address,
            'created_at': utils.get_current_time()
        }
        
        # Lưu user
        if 'users' not in users_data:
            users_data['users'] = []
        users_data['users'].append(new_user)
        utils.save_users(users_data)
        
        # Tự động đăng nhập
        session['user_id'] = username
        session['user_name'] = full_name
        
        response = make_response(redirect(url_for('main.index')))
        response.set_cookie('user_id', username, max_age=30*24*60*60)
        return response
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    """Đăng xuất"""
    session.clear()
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie('user_id', '', expires=0)
    return response

@auth_bp.route('/profile')
@utils.login_required
def profile():
    """Trang thông tin cá nhân"""
    user_info = utils.get_user_info(session)
    return render_template('profile.html', user=user_info)
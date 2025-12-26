"""Routes cho chức năng admin"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import utils
import bcrypt
import os
from datetime import datetime
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator kiểm tra quyền admin"""
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Vui lòng đăng nhập để truy cập trang này.', 'error')
            return redirect(url_for('auth.login'))
        
        users = utils.load_users()
        current_user = next((u for u in users['users'] if u['username'] == session['user']), None)
        
        if not current_user or current_user.get('role') != 'admin':
            flash('Bạn không có quyền truy cập trang này.', 'error')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/')
@admin_required
def dashboard():
    """Trang dashboard admin"""
    # Thống kê tổng quan
    data = utils.load_data()
    users = utils.load_users()
    
    stats = {
        'total_products': len(data['products']),
        'total_users': len(users['users']),
        'admin_users': len([u for u in users['users'] if u.get('role') == 'admin']),
        'regular_users': len([u for u in users['users'] if u.get('role') != 'admin']),
        'recent_products': sorted(data['products'], key=lambda x: x.get('created_at', ''), reverse=True)[:5]
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/users')
@admin_required
def manage_users():
    """Quản lý người dùng"""
    users = utils.load_users()
    return render_template('admin/users.html', users=users['users'])

@admin_bp.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Tạo người dùng mới"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()
        role = request.form.get('role', 'user')
        
        if not username or not password or not full_name:
            flash('Vui lòng điền đầy đủ thông tin.', 'error')
            return render_template('admin/create_user.html')
        
        users = utils.load_users()
        
        # Kiểm tra username đã tồn tại
        if any(u['username'] == username for u in users['users']):
            flash('Tên đăng nhập đã tồn tại.', 'error')
            return render_template('admin/create_user.html')
        
        # Tạo user mới
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = {
            'username': username,
            'password': hashed_password,
            'full_name': full_name,
            'role': role,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        users['users'].append(new_user)
        utils.save_users(users)
        
        flash(f'Đã tạo người dùng {username} thành công.', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/create_user.html')

@admin_bp.route('/users/<username>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(username):
    """Chỉnh sửa người dùng"""
    users = utils.load_users()
    user = next((u for u in users['users'] if u['username'] == username), None)
    
    if not user:
        flash('Không tìm thấy người dùng.', 'error')
        return redirect(url_for('admin.manage_users'))
    
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        role = request.form.get('role', 'user')
        new_password = request.form.get('new_password', '').strip()
        
        if not full_name:
            flash('Vui lòng nhập họ tên.', 'error')
            return render_template('admin/edit_user.html', user=user)
        
        # Cập nhật thông tin
        user['full_name'] = full_name
        user['role'] = role
        
        # Cập nhật mật khẩu nếu có
        if new_password:
            user['password'] = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        utils.save_users(users)
        flash(f'Đã cập nhật thông tin người dùng {username}.', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/edit_user.html', user=user)

@admin_bp.route('/users/<username>/delete', methods=['POST'])
@admin_required
def delete_user(username):
    """Xóa người dùng"""
    if username == session.get('user'):
        flash('Không thể xóa tài khoản của chính mình.', 'error')
        return redirect(url_for('admin.manage_users'))
    
    users = utils.load_users()
    users['users'] = [u for u in users['users'] if u['username'] != username]
    utils.save_users(users)
    
    flash(f'Đã xóa người dùng {username}.', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/products')
@admin_required
def manage_products():
    """Quản lý sản phẩm"""
    data = utils.load_data()
    return render_template('admin/products.html', products=data['products'])

@admin_bp.route('/products/<product_id>/delete', methods=['POST'])
@admin_required
def delete_product(product_id):
    """Xóa sản phẩm"""
    data = utils.load_data()
    
    # Tìm và xóa sản phẩm
    product = next((p for p in data['products'] if p['id'] == product_id), None)
    if product:
        # Xóa file QR code
        qr_path = os.path.join('static/qrcodes', f'{product_id}.png')
        if os.path.exists(qr_path):
            os.remove(qr_path)
        
        # Xóa thư mục upload
        upload_dirs = ['static/uploads/production', 'static/uploads/harvest']
        for upload_dir in upload_dirs:
            product_dir = os.path.join(upload_dir, product_id)
            if os.path.exists(product_dir):
                import shutil
                shutil.rmtree(product_dir)
        
        # Xóa khỏi data
        data['products'] = [p for p in data['products'] if p['id'] != product_id]
        utils.save_data(data)
        
        flash(f'Đã xóa sản phẩm {product.get("name", product_id)}.', 'success')
    else:
        flash('Không tìm thấy sản phẩm.', 'error')
    
    return redirect(url_for('admin.manage_products'))

@admin_bp.route('/system')
@admin_required
def system_info():
    """Thông tin hệ thống"""
    import sys
    import platform
    
    info = {
        'python_version': sys.version,
        'platform': platform.platform(),
        'flask_env': os.environ.get('FLASK_ENV', 'development'),
        'port': os.environ.get('PORT', '5000'),
        'data_files': {
            'products': os.path.exists('data/data.json'),
            'users': os.path.exists('data/users.json')
        }
    }
    
    return render_template('admin/system.html', info=info)
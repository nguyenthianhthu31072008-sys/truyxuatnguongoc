"""Utility functions"""
import json
import os
import qrcode
import time
from functools import wraps
from flask import session, redirect, url_for, request
from werkzeug.utils import secure_filename
import config
import bcrypt

def init_directories():
    """Khởi tạo các thư mục cần thiết"""
    directories = [
        config.DATA_DIR,
        config.QRCODE_DIR,
        config.UPLOAD_DIR,
        os.path.join(config.UPLOAD_DIR, 'production'),
        os.path.join(config.UPLOAD_DIR, 'harvest')
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def load_data():
    """Load dữ liệu từ file JSON"""
    if not os.path.exists(config.DATA_FILE):
        # Tạo file data.json mới nếu chưa có
        initial_data = {
            'products': []
        }
        save_data(initial_data)
        return initial_data
    
    try:
        with open(config.DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {'products': []}

def save_data(data):
    """Lưu dữ liệu vào file JSON"""
    with open(config.DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_users():
    """Load dữ liệu users từ file JSON"""
    if not os.path.exists(config.USERS_FILE):
        # Tạo file users.json mới nếu chưa có
        initial_users = {
            'users': []
        }
        save_users(initial_users)
        return initial_users
    
    try:
        with open(config.USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {'users': []}

def save_users(users_data):
    """Lưu dữ liệu users vào file JSON"""
    with open(config.USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)

def generate_qrcode(product_id, base_url):
    """Tạo mã QR cho sản phẩm"""
    # URL để xem sản phẩm
    product_url = f"{base_url}product/{product_id}"
    
    # Tạo QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(product_url)
    qr.make(fit=True)
    
    # Tạo hình ảnh
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Lưu file
    qr_filename = f"{product_id}.png"
    qr_path = os.path.join(config.QRCODE_DIR, qr_filename)
    img.save(qr_path)
    
    return qr_path

def allowed_file(filename):
    """Kiểm tra file có được phép upload không"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def save_uploaded_files(files, product_id, file_type):
    """Lưu các file được upload"""
    saved_files = []
    
    for file in files:
        if file and file.filename and allowed_file(file.filename):
            # Tạo tên file an toàn
            filename = secure_filename(file.filename)
            timestamp = str(int(time.time() * 1000))
            filename = f"{filename.rsplit('.', 1)[0]}_{timestamp}.{filename.rsplit('.', 1)[1]}"
            
            # Tạo thư mục cho sản phẩm
            product_dir = os.path.join(config.UPLOAD_DIR, file_type, product_id)
            if not os.path.exists(product_dir):
                os.makedirs(product_dir)
            
            # Lưu file
            file_path = os.path.join(product_dir, filename)
            file.save(file_path)
            
            # Thêm vào danh sách (relative path)
            relative_path = os.path.join('uploads', file_type, product_id, filename).replace('\\', '/')
            saved_files.append(relative_path)
    
    return saved_files

def delete_product_files(product_id):
    """Xóa các file liên quan đến sản phẩm"""
    # Xóa QR code
    qr_path = os.path.join(config.QRCODE_DIR, f"{product_id}.png")
    if os.path.exists(qr_path):
        os.remove(qr_path)
    
    # Xóa thư mục upload
    for file_type in ['production', 'harvest']:
        product_dir = os.path.join(config.UPLOAD_DIR, file_type, product_id)
        if os.path.exists(product_dir):
            import shutil
            shutil.rmtree(product_dir)

def login_required(f):
    """Decorator yêu cầu đăng nhập"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    """Hash password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    """Kiểm tra password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def get_current_time():
    """Lấy thời gian hiện tại"""
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_user_info(session):
    """Lấy thông tin user từ session"""
    if 'user_id' not in session:
        return None
    
    users_data = load_users()
    for user in users_data.get('users', []):
        if user.get('username') == session['user_id']:
            return {
                'username': user.get('username'),
                'full_name': user.get('full_name', user.get('username')),
                'email': user.get('email', ''),
                'phone': user.get('phone', ''),
                'address': user.get('address', '')
            }
    return None
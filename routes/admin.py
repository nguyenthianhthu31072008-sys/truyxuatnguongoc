"""Admin routes"""
from flask import Blueprint, render_template, session, redirect, url_for
import utils

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@utils.login_required
def dashboard():
    """Admin dashboard"""
    # Kiểm tra quyền admin (có thể thêm logic kiểm tra admin sau)
    user_info = utils.get_user_info(session)
    
    # Lấy thống kê
    data = utils.load_data()
    users_data = utils.load_users()
    
    stats = {
        'total_products': len(data.get('products', [])),
        'total_users': len(users_data.get('users', [])),
        'total_scans': sum(p.get('scan_count', 0) for p in data.get('products', []))
    }
    
    return render_template('admin/dashboard.html', user=user_info, stats=stats)

@admin_bp.route('/farmers')
@utils.login_required
def farmers():
    """Danh sách nông dân"""
    user_info = utils.get_user_info(session)
    users_data = utils.load_users()
    farmers = users_data.get('users', [])
    
    return render_template('admin/farmers.html', user=user_info, farmers=farmers)

@admin_bp.route('/farmer/<username>')
@utils.login_required
def farmer_detail(username):
    """Chi tiết nông dân"""
    user_info = utils.get_user_info(session)
    
    # Tìm thông tin nông dân
    users_data = utils.load_users()
    farmer = None
    for user in users_data.get('users', []):
        if user.get('username') == username:
            farmer = user
            break
    
    if not farmer:
        return redirect(url_for('admin.farmers'))
    
    # Lấy sản phẩm của nông dân
    data = utils.load_data()
    products = [p for p in data.get('products', []) if p.get('created_by') == username]
    
    return render_template('admin/farmer_detail.html', user=user_info, farmer=farmer, products=products)

@admin_bp.route('/products')
@utils.login_required
def products():
    """Danh sách sản phẩm"""
    user_info = utils.get_user_info(session)
    data = utils.load_data()
    products = data.get('products', [])
    
    # Sắp xếp theo thời gian tạo
    products.sort(key=lambda x: x.get('id', 0), reverse=True)
    
    return render_template('admin/products.html', user=user_info, products=products)
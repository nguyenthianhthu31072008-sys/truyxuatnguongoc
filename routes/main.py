"""Main routes"""
from flask import Blueprint, render_template, request
import utils

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Trang chủ"""
    # Lấy thông tin user nếu đã đăng nhập
    user_info = utils.get_user_info(request.cookies) if 'user_id' in request.cookies else None
    
    # Lấy danh sách sản phẩm mới nhất
    data = utils.load_data()
    products = data.get('products', [])
    
    # Sắp xếp theo thời gian tạo (mới nhất trước)
    products.sort(key=lambda x: x.get('id', 0), reverse=True)
    
    # Lấy 6 sản phẩm mới nhất
    recent_products = products[:6]
    
    return render_template('index.html', products=recent_products, user=user_info)

@main_bp.route('/search')
def search():
    """Tìm kiếm sản phẩm"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return render_template('index.html', products=[], search_query='')
    
    data = utils.load_data()
    products = data.get('products', [])
    
    # Tìm kiếm theo tên sản phẩm, tên nông dân, khu vực
    results = []
    query_lower = query.lower()
    
    for product in products:
        if (query_lower in product.get('product_name', '').lower() or
            query_lower in product.get('farmer_name', '').lower() or
            query_lower in product.get('production_area', '').lower()):
            results.append(product)
    
    # Sắp xếp kết quả
    results.sort(key=lambda x: x.get('id', 0), reverse=True)
    
    user_info = utils.get_user_info(request.cookies) if 'user_id' in request.cookies else None
    
    return render_template('index.html', products=results, search_query=query, user=user_info)
# Hướng dẫn Deploy lên Railway

## ✅ Đã hoàn thành
- [x] Code đã được push lên GitHub: `leminhvu950/truyxuatnguongoc`
- [x] Đã tạo file cấu hình Railway (`railway.toml`, `Procfile`)
- [x] Đã cập nhật code để tương thích với Railway
- [x] Đã tạo `.gitignore` và `README.md`

## 🚀 Bước tiếp theo - Deploy lên Railway

### 1. Truy cập Railway
- Vào [railway.app](https://railway.app)
- Đăng nhập bằng GitHub account của bạn

### 2. Tạo Project mới
- Click **"New Project"**
- Chọn **"Deploy from GitHub repo"**
- Tìm và chọn repository: `leminhvu950/truyxuatnguongoc`

### 3. Railway sẽ tự động:
- Detect Flask application
- Install dependencies từ `requirements.txt`
- Chạy với Gunicorn server
- Tạo domain miễn phí (dạng: `yourapp.railway.app`)

### 4. Kiểm tra Deploy
- Sau 2-3 phút, Railway sẽ cung cấp URL
- Truy cập URL để test ứng dụng
- Tất cả tính năng sẽ hoạt động bình thường

## 🔧 Cấu hình bổ sung (Tùy chọn)

### Environment Variables
Trong Railway dashboard > Settings > Environment:
- `SECRET_KEY`: Railway tự động generate
- Có thể thêm các biến khác nếu cần

### Custom Domain
- Trong Settings > Domains
- Có thể add domain riêng nếu muốn

## 📱 Tính năng hoạt động
- ✅ Đăng ký/Đăng nhập
- ✅ Tạo sản phẩm với QR code
- ✅ Upload hình ảnh
- ✅ Quét QR code xem thông tin
- ✅ Quản lý sản phẩm
- ✅ Tìm kiếm

## 💡 Lưu ý
- Railway free tier: 500 hours/tháng
- Files upload sẽ được lưu trữ persistent
- Database JSON sẽ không bị mất
- Tự động SSL certificate

## 🆘 Nếu gặp lỗi
1. Check logs trong Railway dashboard
2. Đảm bảo `requirements.txt` đầy đủ
3. Kiểm tra Python version trong `runtime.txt`
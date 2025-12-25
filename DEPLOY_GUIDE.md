# Hướng dẫn Deploy lên Railway

## ✅ Đã hoàn thành
- [x] Code đã được push lên GitHub: `leminhvu950/truyxuatnguongoc`
- [x] Đã tạo file cấu hình Railway (`railway.toml`, `Procfile`)
- [x] Đã cập nhật code để tương thích với Railway
- [x] Đã tạo `.gitignore` và `README.md`
- [x] Đã tích hợp OpenAI API cho phân tích AI

## 🚀 Bước tiếp theo - Deploy lên Railway

### 1. Truy cập Railway
- Vào [railway.app](https://railway.app)
- Đăng nhập bằng GitHub account của bạn

### 2. Tạo Project mới
- Click **"New Project"**
- Chọn **"Deploy from GitHub repo"**
- Tìm và chọn repository: `leminhvu950/truyxuatnguongoc`

### 3. Cấu hình OpenAI API (Bắt buộc cho tính năng AI)
Trong Railway dashboard > Settings > Environment Variables:
- `OPENAI_API_KEY`: API key từ OpenAI (lấy tại [platform.openai.com](https://platform.openai.com/api-keys))
- `OPENAI_MODEL`: `gpt-3.5-turbo` (hoặc `gpt-4` nếu có quyền truy cập)
- `OPENAI_MAX_TOKENS`: `1500`
- `OPENAI_TEMPERATURE`: `0.7`

### 4. Railway sẽ tự động:
- Detect Flask application
- Install dependencies từ `requirements.txt`
- Chạy với Gunicorn server
- Tạo domain miễn phí (dạng: `yourapp.railway.app`)

### 5. Kiểm tra Deploy
- Sau 2-3 phút, Railway sẽ cung cấp URL
- Truy cập URL để test ứng dụng
- Tất cả tính năng sẽ hoạt động bình thường

## 🤖 Tính năng AI mới

### Báo cáo phân tích AI
- **Phân tích minh bạch**: Đánh giá độ đầy đủ thông tin sản phẩm
- **Tuân thủ tiêu chuẩn số hóa**: Kiểm tra mức độ số hóa
- **Phân tích thị trường**: Gợi ý giá cả và kênh phân phối
- **Đánh giá chất lượng**: Phân tích chất lượng sản xuất
- **Phân tích mùa vụ**: Tác động thời tiết và thời điểm tối ưu
- **Gợi ý cải thiện**: Khuyến nghị cụ thể để nâng cao chất lượng
- **Đề xuất chứng nhận**: Các chứng nhận cần thiết
- **Marketing số**: Gợi ý quảng bá trực tuyến

### Cách sử dụng
1. Đăng nhập vào hệ thống
2. Vào "Quản lý sản phẩm"
3. Chọn sản phẩm cần phân tích
4. Click "🤖 Tạo báo cáo truy xuất AI"
5. Xem báo cáo chi tiết với gợi ý từ AI

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
- ✅ **Báo cáo phân tích AI** (Mới)

## 💰 Chi phí OpenAI API
- GPT-3.5-turbo: ~$0.002/1K tokens
- Mỗi báo cáo AI: ~$0.01-0.03
- Có thể giới hạn số lần gọi API để kiểm soát chi phí

## 💡 Lưu ý
- Railway free tier: 500 hours/tháng
- Files upload sẽ được lưu trữ persistent
- Database JSON sẽ không bị mất
- Tự động SSL certificate
- **OpenAI API key cần được cấu hình để sử dụng tính năng AI**

## 🆘 Nếu gặp lỗi
1. Check logs trong Railway dashboard
2. Đảm bảo `requirements.txt` đầy đủ
3. Kiểm tra Python version trong `runtime.txt`
4. **Kiểm tra OpenAI API key có hợp lệ không**
5. **Đảm bảo tài khoản OpenAI có đủ credit**
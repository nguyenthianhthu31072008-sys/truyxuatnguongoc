# Hệ thống Truy xuất Nguồn gốc Nông sản

Ứng dụng Flask để quản lý và truy xuất nguồn gốc nông sản thông qua mã QR với tính năng phân tích AI.

## Tính năng

- 🔐 Đăng ký/Đăng nhập người dùng
- 📦 Tạo và quản lý sản phẩm nông sản
- 📱 Tạo mã QR cho từng sản phẩm
- 📸 Upload hình ảnh quá trình sản xuất và thu hoạch
- 🔍 Tìm kiếm sản phẩm
- 🤖 **Phân tích AI với OpenAI** (Mới)
  - Đánh giá tính minh bạch
  - Phân tích tuân thủ tiêu chuẩn số hóa
  - Gợi ý thị trường và giá cả
  - Đánh giá chất lượng sản phẩm
  - Phân tích mùa vụ và thời tiết
  - Gợi ý cải thiện và chứng nhận
  - Khuyến nghị marketing số

## Deploy lên Railway

### Bước 1: Chuẩn bị GitHub Repository

1. Tạo repository mới trên GitHub: `leminhvu950/truyxuatnguongoc`
2. Clone repository về máy hoặc push code hiện tại lên

### Bước 2: Deploy lên Railway

1. Truy cập [railway.app](https://railway.app)
2. Đăng nhập bằng GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Chọn repository `leminhvu950/truyxuatnguongoc`
5. Railway sẽ tự động detect Flask app và deploy

### Bước 3: Cấu hình OpenAI API (Bắt buộc cho tính năng AI)

Trong Railway dashboard > Settings > Environment Variables:

```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=1500
OPENAI_TEMPERATURE=0.7
```

**Lấy OpenAI API Key:**
1. Truy cập [platform.openai.com](https://platform.openai.com/api-keys)
2. Đăng nhập/Đăng ký tài khoản OpenAI
3. Tạo API key mới
4. Copy và paste vào Railway environment variables

### Bước 4: Cấu hình Environment Variables khác (Tùy chọn)

- `SECRET_KEY`: Railway sẽ tự động generate

## Chạy Local

### Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Cấu hình OpenAI (Tùy chọn)
Tạo file `.env` từ `.env.example`:
```bash
cp .env.example .env
```

Chỉnh sửa `.env` và thêm OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Chạy ứng dụng
```bash
python app.py
```

## Sử dụng tính năng AI

1. Đăng nhập vào hệ thống
2. Tạo hoặc chọn sản phẩm cần phân tích
3. Click "🤖 Tạo báo cáo truy xuất AI"
4. Xem báo cáo chi tiết với:
   - Điểm minh bạch từ AI
   - Phân tích tuân thủ tiêu chuẩn số hóa
   - Gợi ý thị trường và giá cả
   - Đánh giá chất lượng
   - Phân tích mùa vụ
   - Gợi ý cải thiện cụ thể

## Chi phí OpenAI API

- GPT-3.5-turbo: ~$0.002/1K tokens
- Mỗi báo cáo AI: ~$0.01-0.03
- Có thể giới hạn số lần gọi API để kiểm soát chi phí

## Cấu trúc Project

```
├── app.py              # Main Flask application
├── config.py           # Configuration (bao gồm OpenAI config)
├── utils.py            # Utility functions
├── ai_analysis.py      # AI analysis module (OpenAI integration)
├── routes/             # Route blueprints
├── templates/          # HTML templates
│   └── ai_report.html  # Template báo cáo AI
├── static/             # Static files (CSS, uploads, QR codes)
├── data/               # JSON database files
├── requirements.txt    # Python dependencies (bao gồm openai)
├── railway.toml        # Railway configuration
├── Procfile           # Process configuration
├── .env.example       # Environment variables template
└── DEPLOY_GUIDE.md    # Hướng dẫn deploy chi tiết
```

## Test API Connection

Truy cập `/test-ai` để kiểm tra kết nối OpenAI API (cần đăng nhập).
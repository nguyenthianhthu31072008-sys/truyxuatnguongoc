"""Cấu hình OpenAI API"""
import config

def get_openai_client():
    """Lấy OpenAI client với API key từ config"""
    api_key = config.OPENAI_API_KEY
    if not api_key or len(api_key) < 20:
        print(f"OpenAI API key không hợp lệ hoặc chưa được cấu hình")
        return None
    
    try:
        # Thử import OpenAI mới trước
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            print("Sử dụng OpenAI client mới")
            return client
        except ImportError:
            # Fallback cho phiên bản cũ
            import openai
            openai.api_key = api_key
            print("Sử dụng OpenAI client cũ")
            return openai
    except Exception as e:
        print(f"Lỗi khởi tạo OpenAI client: {e}")
        return None

def is_openai_available():
    """Kiểm tra xem OpenAI API có sẵn không"""
    client = get_openai_client()
    if not client:
        return False
    
    try:
        # Test với một request đơn giản
        if hasattr(client, 'models'):
            # OpenAI client mới
            client.models.list()
        else:
            # OpenAI client cũ
            client.Model.list()
        return True
    except Exception as e:
        print(f"OpenAI API test failed: {e}")
        return False

def get_openai_config():
    """Lấy cấu hình OpenAI"""
    return {
        'model': config.OPENAI_MODEL,
        'max_tokens': config.OPENAI_MAX_TOKENS,
        'temperature': config.OPENAI_TEMPERATURE
    }
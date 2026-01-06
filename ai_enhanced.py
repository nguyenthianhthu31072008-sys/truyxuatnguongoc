"""AI nâng cao với Mock AI Engine - không cần OpenAI API"""
import json
from datetime import datetime
from openai_config import get_openai_client, is_openai_available, get_openai_config
import ai_analysis
from ai_mock import mock_ai

def analyze_product_with_openai(product):
    """Phân tích sản phẩm với AI - ưu tiên Mock AI"""
    
    # Lấy phân tích cơ bản trước
    basic_analysis = ai_analysis.analyze_product_ai(product)
    
    # Sử dụng Mock AI thay vì OpenAI
    try:
        print("=== Sử dụng Mock AI Engine ===")
        mock_analysis = mock_ai.analyze_product(product)
        
        # Kết hợp với phân tích cơ bản
        enhanced_analysis = basic_analysis.copy()
        enhanced_analysis.update({
            'ai_enhanced': True,
            'mock_ai_used': True,
            'openai_suggestions': mock_analysis['detailed_analysis'],
            'improvement_plan': mock_analysis['improvement_plan'],
            'market_analysis': mock_analysis['market_analysis'],
            'standards_compliance': mock_analysis['standards_compliance'],
            'recommendations': mock_analysis['recommendations'],
            'analysis_timestamp': mock_analysis['analysis_timestamp']
        })
        
        return enhanced_analysis
        
    except Exception as e:
        print(f"Lỗi Mock AI: {e}")
        # Fallback về phân tích cơ bản
        basic_analysis['ai_enhanced'] = False
        basic_analysis['mock_ai_error'] = str(e)
        return basic_analysis

def get_digitization_standards_suggestions(product):
    """Lấy gợi ý tiêu chuẩn số hóa từ Mock AI"""
    try:
        analysis = mock_ai.analyze_product(product)
        return {
            'available': True,
            'suggestions': analysis['standards_compliance']
        }
    except Exception as e:
        return {
            'available': False,
            'error': str(e),
            'suggestions': []
        }

def get_market_analysis(product):
    """Phân tích thị trường với Mock AI"""
    try:
        analysis = mock_ai.analyze_product(product)
        return {
            'available': True,
            'analysis': analysis['market_analysis']
        }
    except Exception as e:
        return {
            'available': False,
            'error': str(e),
            'analysis': None
        }

def generate_improvement_plan(product, basic_analysis):
    """Tạo kế hoạch cải thiện với Mock AI"""
    try:
        analysis = mock_ai.analyze_product(product)
        return {
            'available': True,
            'plan': analysis['improvement_plan']
        }
    except Exception as e:
        return {
            'available': False,
            'error': str(e),
            'plan': []
        }
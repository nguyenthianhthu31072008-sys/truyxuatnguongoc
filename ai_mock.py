"""AI Mock Engine - Phân tích thông minh không cần OpenAI API"""
import random
from datetime import datetime
import json

class MockAIEngine:
    """Engine AI giả lập với phân tích thông minh"""
    
    def __init__(self):
        self.product_types = {
            'seasonal': 'cây thời vụ',
            'perennial': 'cây lâu năm'
        }
        
        self.analysis_templates = {
            'quality_assessment': [
                "Sản phẩm có thông tin cơ bản đầy đủ",
                "Cần bổ sung thêm thông tin về quy trình sản xuất",
                "Thông tin truy xuất nguồn gốc rõ ràng và minh bạch",
                "Dữ liệu sản phẩm đạt tiêu chuẩn cơ bản"
            ],
            'improvement_suggestions': [
                "Nên bổ sung thêm hình ảnh quá trình sản xuất",
                "Cần ghi chép chi tiết hơn về phương pháp canh tác",
                "Nên có chứng nhận VietGAP hoặc organic",
                "Cần cập nhật thông tin liên hệ đầy đủ"
            ],
            'market_insights': [
                "Sản phẩm có tiềm năng tốt trên thị trường nội địa",
                "Phù hợp với xu hướng tiêu dùng xanh hiện tại",
                "Có thể phát triển thương hiệu riêng",
                "Nên tập trung vào kênh bán lẻ và online"
            ]
        }
    
    def analyze_product(self, product):
        """Phân tích sản phẩm với AI giả lập"""
        
        # Tính điểm chất lượng dựa trên thông tin có sẵn
        quality_score = self._calculate_quality_score(product)
        
        # Tạo phân tích chi tiết
        analysis = {
            'ai_enhanced': True,
            'quality_score': quality_score,
            'analysis_timestamp': datetime.now().isoformat(),
            'detailed_analysis': self._generate_detailed_analysis(product, quality_score),
            'improvement_plan': self._generate_improvement_plan(product, quality_score),
            'market_analysis': self._generate_market_analysis(product),
            'standards_compliance': self._check_standards_compliance(product),
            'recommendations': self._generate_recommendations(product)
        }
        
        return analysis
    
    def _calculate_quality_score(self, product):
        """Tính điểm chất lượng dựa trên thông tin sản phẩm"""
        score = 0
        
        # Kiểm tra thông tin cơ bản (40 điểm)
        if product.get('product_name'): score += 10
        if product.get('farmer_name'): score += 10
        if product.get('production_area'): score += 10
        if product.get('plant_type'): score += 10
        
        # Kiểm tra thông tin thời gian (20 điểm)
        if product.get('planting_date'): score += 10
        if product.get('harvest_date'): score += 10
        
        # Kiểm tra quy trình (20 điểm)
        if product.get('production_process'): score += 10
        if product.get('harvest_process'): score += 10
        
        # Kiểm tra media (20 điểm)
        if product.get('production_media'): score += 10
        if product.get('harvest_media'): score += 10
        
        return min(score, 100)
    
    def _generate_detailed_analysis(self, product, score):
        """Tạo phân tích chi tiết"""
        product_name = product.get('product_name', 'sản phẩm')
        plant_type = self.product_types.get(product.get('plant_type', ''), 'cây trồng')
        
        analysis = f"""
## Phân tích chất lượng sản phẩm: {product_name}

### Đánh giá tổng quan
Sản phẩm {product_name} là {plant_type} với điểm chất lượng thông tin **{score}/100**.

### Điểm mạnh
"""
        
        strengths = []
        if product.get('production_area'):
            strengths.append(f"- Có thông tin rõ ràng về khu vực sản xuất: {product['production_area']}")
        if product.get('production_process'):
            strengths.append("- Có mô tả quy trình sản xuất chi tiết")
        if product.get('harvest_process'):
            strengths.append("- Có thông tin về quy trình thu hoạch")
        if product.get('production_media') or product.get('harvest_media'):
            strengths.append("- Có hình ảnh/video minh chứng")
        
        if not strengths:
            strengths.append("- Có thông tin cơ bản về sản phẩm")
        
        analysis += "\n".join(strengths)
        
        analysis += "\n\n### Khuyến nghị cải thiện\n"
        
        improvements = []
        if score < 60:
            improvements.append("- Cần bổ sung thêm thông tin cơ bản về sản phẩm")
        if not product.get('production_media'):
            improvements.append("- Nên thêm hình ảnh quá trình sản xuất")
        if not product.get('harvest_media'):
            improvements.append("- Nên thêm hình ảnh quá trình thu hoạch")
        if not product.get('storage_method'):
            improvements.append("- Cần thông tin về phương pháp bảo quản")
        
        if not improvements:
            improvements.append("- Sản phẩm đã có thông tin khá đầy đủ")
        
        analysis += "\n".join(improvements)
        
        return analysis
    
    def _generate_improvement_plan(self, product, score):
        """Tạo kế hoạch cải thiện"""
        plans = []
        
        if score < 70:
            plans.append({
                'priority': 'Cao',
                'action': 'Bổ sung thông tin cơ bản',
                'description': 'Cập nhật đầy đủ thông tin về tên sản phẩm, người sản xuất, khu vực',
                'timeline': '1-2 ngày'
            })
        
        if not product.get('production_media'):
            plans.append({
                'priority': 'Trung bình',
                'action': 'Thêm hình ảnh sản xuất',
                'description': 'Chụp ảnh/quay video quá trình canh tác, chăm sóc cây trồng',
                'timeline': '1 tuần'
            })
        
        if not product.get('harvest_media'):
            plans.append({
                'priority': 'Trung bình',
                'action': 'Thêm hình ảnh thu hoạch',
                'description': 'Ghi lại quá trình thu hoạch, sơ chế sản phẩm',
                'timeline': '1 tuần'
            })
        
        plans.append({
            'priority': 'Thấp',
            'action': 'Xin chứng nhận chất lượng',
            'description': 'Đăng ký VietGAP, GlobalGAP hoặc chứng nhận organic',
            'timeline': '2-3 tháng'
        })
        
        return plans
    
    def _generate_market_analysis(self, product):
        """Phân tích thị trường"""
        product_name = product.get('product_name', 'sản phẩm')
        
        return {
            'market_potential': 'Tốt',
            'target_customers': ['Gia đình có thu nhập trung bình', 'Người quan tâm sức khỏe', 'Nhà hàng organic'],
            'price_range': 'Trung bình - Cao',
            'distribution_channels': ['Chợ truyền thống', 'Siêu thị', 'Bán online', 'Cửa hàng organic'],
            'competitive_advantage': f'{product_name} có nguồn gốc rõ ràng, truy xuất được',
            'marketing_suggestions': [
                'Nhấn mạnh tính minh bạch và truy xuất nguồn gốc',
                'Sử dụng mã QR để khách hàng dễ dàng kiểm tra',
                'Xây dựng thương hiệu cá nhân của nông dân',
                'Tham gia các hội chợ nông sản sạch'
            ]
        }
    
    def _check_standards_compliance(self, product):
        """Kiểm tra tuân thủ tiêu chuẩn"""
        standards = [
            {
                'name': 'Thông tin cơ bản',
                'status': 'complete' if all([
                    product.get('product_name'),
                    product.get('farmer_name'),
                    product.get('production_area')
                ]) else 'partial',
                'description': 'Tên sản phẩm, người sản xuất, khu vực'
            },
            {
                'name': 'Thông tin thời gian',
                'status': 'complete' if all([
                    product.get('planting_date'),
                    product.get('harvest_date')
                ]) else 'partial',
                'description': 'Ngày trồng, ngày thu hoạch'
            },
            {
                'name': 'Quy trình sản xuất',
                'status': 'complete' if product.get('production_process') else 'missing',
                'description': 'Mô tả chi tiết quy trình canh tác'
            },
            {
                'name': 'Hình ảnh minh chứng',
                'status': 'complete' if (product.get('production_media') or product.get('harvest_media')) else 'missing',
                'description': 'Ảnh/video quá trình sản xuất'
            }
        ]
        
        return standards
    
    def _generate_recommendations(self, product):
        """Tạo khuyến nghị cụ thể"""
        recommendations = []
        
        # Khuyến nghị dựa trên loại cây
        plant_type = product.get('plant_type')
        if plant_type == 'seasonal':
            recommendations.append("Với cây thời vụ, nên lập kế hoạch luân canh để tối ưu hóa đất đai")
        elif plant_type == 'perennial':
            recommendations.append("Với cây lâu năm, nên đầu tư vào hệ thống tưới tiêu bền vững")
        
        # Khuyến nghị về marketing
        if product.get('production_area'):
            recommendations.append(f"Tận dụng thương hiệu vùng miền {product['production_area']} trong marketing")
        
        # Khuyến nghị về chất lượng
        recommendations.append("Nên tham gia các chương trình đào tạo về nông nghiệp sạch")
        recommendations.append("Xây dựng mối quan hệ với các nhà phân phối uy tín")
        
        return recommendations

# Khởi tạo engine
mock_ai = MockAIEngine()
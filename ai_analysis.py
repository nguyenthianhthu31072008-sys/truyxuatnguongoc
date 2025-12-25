"""Logic phân tích AI cho sản phẩm sử dụng OpenAI API"""
from datetime import datetime as dt
import openai
import config
import json
import logging

# Cấu hình OpenAI
if config.OPENAI_API_KEY:
    openai.api_key = config.OPENAI_API_KEY

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_openai_analysis(product_data):
    """Gọi OpenAI API để phân tích sản phẩm nông nghiệp"""
    if not config.OPENAI_API_KEY:
        logger.warning("OpenAI API key không được cấu hình")
        return None
    
    try:
        # Chuẩn bị dữ liệu sản phẩm cho AI
        product_summary = {
            'tên_sản_phẩm': product_data.get('product_name', ''),
            'tên_nông_dân': product_data.get('farmer_name', ''),
            'khu_vực_sản_xuất': product_data.get('production_area', ''),
            'ngày_gieo_trồng': product_data.get('planting_date', ''),
            'ngày_thu_hoạch': product_data.get('harvest_date', ''),
            'quy_trình_sản_xuất': product_data.get('production_process', ''),
            'quy_trình_thu_hoạch': product_data.get('harvest_process', ''),
            'phương_pháp_bảo_quản': product_data.get('storage_method', ''),
            'số_lượt_quét': product_data.get('scan_count', 0),
            'có_media_sản_xuất': len(product_data.get('production_media', [])) > 0,
            'có_media_thu_hoạch': len(product_data.get('harvest_media', [])) > 0
        }

        prompt = f"""
Bạn là chuyên gia phân tích nông nghiệp và tiêu chuẩn số hóa. Hãy phân tích sản phẩm nông nghiệp sau và đưa ra đánh giá chi tiết:

Thông tin sản phẩm:
{json.dumps(product_summary, ensure_ascii=False, indent=2)}

Hãy phân tích và trả về kết quả JSON với các thông tin sau:

1. **transparency_score** (0-100): Điểm minh bạch dựa trên đầy đủ thông tin
2. **digitization_compliance**: Đánh giá tuân thủ tiêu chuẩn số hóa
   - level: "Xuất sắc", "Tốt", "Trung bình", "Cần cải thiện"
   - score: 0-100
   - missing_elements: danh sách các yếu tố còn thiếu
3. **market_analysis**: Phân tích thị trường
   - current_market_trend: xu hướng thị trường hiện tại
   - price_prediction: dự đoán giá cả
   - target_customers: khách hàng mục tiêu
   - distribution_channels: kênh phân phối đề xuất
4. **quality_assessment**: Đánh giá chất lượng
   - production_quality: chất lượng sản xuất
   - traceability_level: mức độ truy xuất nguồn gốc
   - safety_compliance: tuân thủ an toàn thực phẩm
5. **improvement_suggestions**: Gợi ý cải thiện (tối đa 5 gợi ý)
6. **certification_recommendations**: Đề xuất chứng nhận cần thiết
7. **digital_marketing_tips**: Gợi ý marketing số

Trả về kết quả bằng tiếng Việt, định dạng JSON hợp lệ.
"""

        response = openai.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia phân tích nông nghiệp và tiêu chuẩn số hóa tại Việt Nam. Hãy trả lời bằng tiếng Việt và định dạng JSON hợp lệ."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=config.OPENAI_MAX_TOKENS,
            temperature=config.OPENAI_TEMPERATURE
        )

        ai_response = response.choices[0].message.content.strip()
        
        # Xử lý response để đảm bảo là JSON hợp lệ
        if ai_response.startswith('```json'):
            ai_response = ai_response[7:]
        if ai_response.endswith('```'):
            ai_response = ai_response[:-3]
        
        return json.loads(ai_response)
        
    except json.JSONDecodeError as e:
        logger.error(f"Lỗi parse JSON từ OpenAI: {e}")
        return None
    except Exception as e:
        logger.error(f"Lỗi gọi OpenAI API: {e}")
        return None


def get_seasonal_insights(product_data):
    """Phân tích mùa vụ và thời tiết sử dụng AI"""
    if not config.OPENAI_API_KEY:
        return None
    
    try:
        prompt = f"""
Phân tích mùa vụ và đưa ra lời khuyên cho sản phẩm nông nghiệp:

Sản phẩm: {product_data.get('product_name', '')}
Khu vực: {product_data.get('production_area', '')}
Ngày gieo trồng: {product_data.get('planting_date', '')}
Ngày thu hoạch: {product_data.get('harvest_date', '')}

Hãy trả về JSON với:
1. **season_analysis**: Phân tích mùa vụ
2. **weather_impact**: Tác động thời tiết
3. **optimal_timing**: Thời điểm tối ưu cho chu kỳ tiếp theo
4. **yield_prediction**: Dự đoán năng suất
5. **climate_recommendations**: Khuyến nghị về khí hậu

Trả lời bằng tiếng Việt, định dạng JSON.
"""

        response = openai.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia khí tượng nông nghiệp tại Việt Nam."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.6
        )

        ai_response = response.choices[0].message.content.strip()
        if ai_response.startswith('```json'):
            ai_response = ai_response[7:]
        if ai_response.endswith('```'):
            ai_response = ai_response[:-3]
        
        return json.loads(ai_response)
        
    except Exception as e:
        logger.error(f"Lỗi phân tích mùa vụ: {e}")
        return None


def analyze_product_ai(product):
    """Phân tích sản phẩm bằng AI - kết hợp phân tích cơ bản và OpenAI"""
    # Phân tích cơ bản (giữ nguyên logic cũ)
    analysis = get_basic_analysis(product)
    
    # Thêm phân tích từ OpenAI
    openai_analysis = get_openai_analysis(product)
    if openai_analysis:
        analysis['ai_insights'] = openai_analysis
        
        # Cập nhật điểm số từ AI nếu có
        if 'transparency_score' in openai_analysis:
            analysis['ai_transparency_score'] = openai_analysis['transparency_score']
        
        # Thêm gợi ý từ AI
        if 'improvement_suggestions' in openai_analysis:
            analysis['ai_recommendations'] = openai_analysis['improvement_suggestions']
    
    # Phân tích mùa vụ từ AI
    seasonal_insights = get_seasonal_insights(product)
    if seasonal_insights:
        analysis['ai_seasonal_insights'] = seasonal_insights
    
    return analysis


def get_basic_analysis(product):
    """Phân tích cơ bản (logic cũ được giữ lại)"""
    analysis = {
        'transparency': {},
        'recommendations': [],
        'score': 0,
        'stats': {},
        'season_analysis': {},
        'standards_compliance': {},
        'market_suggestions': []
    }

    # Đánh giá tính minh bạch
    has_basic_info = bool(product.get('product_name') and product.get('farmer_name') and product.get('production_area'))
    has_production_process = bool(product.get('production_process') and len(product.get('production_process', '')) > 10)
    has_harvest_process = bool(product.get('harvest_process') and len(product.get('harvest_process', '')) > 10)
    has_storage_method = bool(product.get('storage_method') and len(product.get('storage_method', '')) > 10)
    has_production_media = bool(product.get('production_media') and len(product.get('production_media', [])) > 0)
    has_harvest_media = bool(product.get('harvest_media') and len(product.get('harvest_media', [])) > 0)
    has_dates = bool(product.get('planting_date') and product.get('harvest_date'))

    analysis['transparency'] = {
        'basic_info': has_basic_info,
        'production_process': has_production_process,
        'harvest_process': has_harvest_process,
        'storage_method': has_storage_method,
        'production_media': has_production_media,
        'harvest_media': has_harvest_media,
        'dates': has_dates
    }

    # Tính điểm minh bạch
    score = 0
    if has_basic_info: score += 15
    if has_production_process: score += 15
    if has_harvest_process: score += 15
    if has_storage_method: score += 10
    if has_production_media: score += 15
    if has_harvest_media: score += 15
    if has_dates: score += 15

    analysis['score'] = score

    # Phân tích mùa vụ và năng suất dự kiến
    planting_date = product.get('planting_date')
    harvest_date = product.get('harvest_date')
    production_area = product.get('production_area', '')

    season_info = {
        'season': 'Không xác định',
        'growth_period': None,
        'yield_prediction': 'Trung bình',
        'harvest_timing': 'Phù hợp'
    }

    if planting_date and harvest_date:
        try:
            plant = dt.strptime(planting_date, '%Y-%m-%d')
            harvest = dt.strptime(harvest_date, '%Y-%m-%d')
            growth_days = (harvest - plant).days

            # Xác định mùa vụ
            month = plant.month
            if month in [1, 2, 3]:
                season_info['season'] = 'Đông Xuân'
            elif month in [4, 5, 6]:
                season_info['season'] = 'Xuân Hè'
            elif month in [7, 8, 9]:
                season_info['season'] = 'Hè Thu'
            else:
                season_info['season'] = 'Thu Đông'

            season_info['growth_period'] = f"{growth_days} ngày"

            # Phân tích theo loại sản phẩm để đánh giá thời gian sinh trưởng
            product_name_lower = product.get('product_name', '').lower()

            # Xác định loại sản phẩm và đánh giá phù hợp
            if any(x in product_name_lower for x in ['lúa', 'rice', 'gạo']):
                # Lúa: 90-120 ngày là bình thường
                if growth_days < 80:
                    season_info['yield_prediction'] = 'Ngắn ngày (có thể ảnh hưởng năng suất)'
                elif growth_days > 150:
                    season_info['yield_prediction'] = 'Dài ngày (năng suất cao)'
                else:
                    season_info['yield_prediction'] = 'Phù hợp (90-120 ngày)'
            elif any(x in product_name_lower for x in ['rau', 'vegetable', 'cải', 'xà lách', 'cà chua', 'ớt', 'dưa']):
                # Rau củ: 30-90 ngày
                if growth_days < 20:
                    season_info['yield_prediction'] = 'Quá ngắn (có thể chưa đủ thời gian)'
                elif growth_days > 120:
                    season_info['yield_prediction'] = 'Dài ngày (có thể là cây lâu năm)'
                else:
                    season_info['yield_prediction'] = 'Phù hợp với rau củ (30-90 ngày)'
            elif any(x in product_name_lower for x in
                     ['trái cây', 'fruit', 'nho', 'táo', 'cam', 'chuối', 'xoài', 'bòn bon']):
                # Trái cây: 60-180 ngày hoặc lâu hơn
                if growth_days < 40:
                    season_info['yield_prediction'] = 'Ngắn ngày (có thể là cây non)'
                elif growth_days > 200:
                    season_info['yield_prediction'] = 'Cây lâu năm (năng suất ổn định)'
                else:
                    season_info['yield_prediction'] = 'Phù hợp với cây ăn trái'
            elif any(x in product_name_lower for x in ['cà phê', 'coffee', 'hồ tiêu', 'pepper', 'quế', 'cinnamon']):
                # Cây công nghiệp: thường > 180 ngày
                if growth_days < 100:
                    season_info['yield_prediction'] = 'Ngắn ngày (có thể là giai đoạn đầu)'
                else:
                    season_info['yield_prediction'] = 'Phù hợp với cây công nghiệp'
            else:
                # Nông sản khác: đánh giá chung
                if growth_days < 60:
                    season_info['yield_prediction'] = 'Thời gian sinh trưởng ngắn'
                elif growth_days > 180:
                    season_info['yield_prediction'] = 'Thời gian sinh trưởng dài'
                else:
                    season_info['yield_prediction'] = 'Thời gian sinh trưởng trung bình'

            # Đánh giá thời điểm thu hoạch
            current_date = dt.now()
            if harvest < current_date:
                days_since_harvest = (current_date - harvest).days
                if days_since_harvest > 30:
                    season_info['harvest_timing'] = f'Đã thu hoạch {days_since_harvest} ngày trước'
                else:
                    season_info['harvest_timing'] = 'Vừa thu hoạch'
            else:
                days_to_harvest = (harvest - current_date).days
                if days_to_harvest < 7:
                    season_info['harvest_timing'] = f'Gần đến ngày thu hoạch (còn {days_to_harvest} ngày)'
                else:
                    season_info['harvest_timing'] = f'Còn {days_to_harvest} ngày đến ngày thu hoạch'
        except:
            pass

    analysis['season_analysis'] = season_info

    # Đánh giá tuân thủ tiêu chuẩn số hóa
    standards = {
        'has_digital_records': has_dates and has_production_process,
        'has_media_evidence': has_production_media or has_harvest_media,
        'has_complete_info': has_basic_info and has_production_process and has_harvest_process,
        'has_storage_info': has_storage_method,
        'compliance_level': 'Cơ bản'
    }

    compliance_score = 0
    if standards['has_digital_records']: compliance_score += 25
    if standards['has_media_evidence']: compliance_score += 25
    if standards['has_complete_info']: compliance_score += 30
    if standards['has_storage_info']: compliance_score += 20

    if compliance_score >= 80:
        standards['compliance_level'] = 'Xuất sắc'
    elif compliance_score >= 60:
        standards['compliance_level'] = 'Tốt'
    elif compliance_score >= 40:
        standards['compliance_level'] = 'Trung bình'
    else:
        standards['compliance_level'] = 'Cần cải thiện'

    standards['compliance_score'] = compliance_score
    analysis['standards_compliance'] = standards

    # Gợi ý thị trường và giá cả - phân tích theo nhiều loại nông sản
    market_suggestions = []
    product_name_lower = product.get('product_name', '').lower()

    # Phân tích theo loại sản phẩm
    if any(x in product_name_lower for x in ['lúa', 'rice', 'gạo']):
        market_suggestions.append({
            'type': 'Thị trường',
            'suggestion': 'Giá lúa gạo hiện tại ổn định. Nên bán vào thời điểm sau thu hoạch để đạt giá tốt nhất. Thị trường nội địa ổn định. Có thể mở rộng xuất khẩu nếu đạt tiêu chuẩn chất lượng.'
        })
    elif any(x in product_name_lower for x in
             ['rau', 'vegetable', 'cải', 'xà lách', 'cà chua', 'ớt', 'dưa chuột', 'bắp cải']):
        market_suggestions.append({
            'type': 'Thị trường',
            'suggestion': 'Rau củ tươi có giá trị cao, đặc biệt là rau sạch có truy xuất nguồn gốc. Nên bán tại chợ, siêu thị hoặc kênh online. Thị trường rau sạch đang phát triển mạnh. Người tiêu dùng sẵn sàng trả giá cao cho rau có nguồn gốc rõ ràng.'
        })
    elif any(x in product_name_lower for x in
             ['trái cây', 'fruit', 'nho', 'táo', 'cam', 'chuối', 'xoài', 'bòn bon', 'mít', 'sầu riêng']):
        market_suggestions.append({
            'type': 'Thị trường',
            'suggestion': 'Trái cây tươi có giá trị cao, đặc biệt là trái cây đặc sản địa phương. Nên bán trực tiếp hoặc qua kênh online để tăng lợi nhuận. Tập trung vào chất lượng và truy xuất nguồn gốc để xây dựng thương hiệu.'
        })
    elif any(x in product_name_lower for x in ['cà phê', 'coffee']):
        market_suggestions.append({
            'type': 'Thị trường',
            'suggestion': 'Cà phê có giá trị xuất khẩu cao. Nên chú trọng chất lượng và chứng nhận để đạt giá tốt nhất. Thị trường cà phê trong nước và xuất khẩu đều phát triển. Có thể kết nối với các nhà rang xay và xuất khẩu.'
        })
    elif any(x in product_name_lower for x in ['hồ tiêu', 'pepper', 'tiêu']):
        market_suggestions.append({
            'type': 'Thị trường',
            'suggestion': 'Hồ tiêu có giá trị xuất khẩu cao. Chất lượng và truy xuất nguồn gốc là yếu tố quan trọng. Thị trường hồ tiêu chủ yếu là xuất khẩu. Nên đảm bảo chất lượng và tiêu chuẩn để đạt giá tốt.'
        })
    elif any(x in product_name_lower for x in ['quế', 'cinnamon']):
        market_suggestions.append({
            'type': 'Thị trường',
            'suggestion': 'Quế là đặc sản địa phương có giá trị cao. Quế Tiên Phước nổi tiếng, nên quảng bá thương hiệu địa phương. Quế có thể tiêu thụ trong nước và xuất khẩu. Tập trung vào chất lượng và quảng bá thương hiệu địa phương.'
        })
    elif any(x in product_name_lower for x in ['bòn bon', 'langsat']):
        market_suggestions.append({
            'type': 'Thị trường',
            'suggestion': 'Bòn bon Tiên Châu là đặc sản nổi tiếng. Nên quảng bá thương hiệu địa phương để tăng giá trị. Bòn bon Tiên Châu có thể tiêu thụ tại địa phương và các thành phố lớn. Truy xuất nguồn gốc giúp tăng niềm tin.'
        })
    else:
        # Nông sản khác
        market_suggestions.append({
            'type': 'Thị trường',
            'suggestion': 'Nông sản có truy xuất nguồn gốc thường có giá cao hơn 15-30% so với sản phẩm thông thường. Hãy tận dụng điều này. Người tiêu dùng ngày càng quan tâm đến nguồn gốc sản phẩm. Hãy tận dụng mã QR để quảng bá và kết nối trực tiếp với người tiêu dùng.'
        })

    # Gợi ý theo khu vực
    if production_area:
        area_lower = production_area.lower()
        if any(x in area_lower for x in ['long an', 'đồng bằng sông cửu long', 'miền tây']):
            market_suggestions.append({
                'type': 'Khu vực',
                'suggestion': 'Khu vực Đồng bằng sông Cửu Long có thị trường tiêu thụ lớn. Nên kết nối với các siêu thị và cửa hàng thực phẩm sạch.'
            })
        elif any(x in area_lower for x in ['quảng nam', 'tiên phước', 'tiên châu']):
            market_suggestions.append({
                'type': 'Khu vực',
                'suggestion': 'Khu vực Quảng Nam có nhiều đặc sản địa phương. Hãy quảng bá thương hiệu địa phương như bòn bon Tiên Châu, quế Tiên Phước.'
            })

    analysis['market_suggestions'] = market_suggestions

    # Thống kê
    analysis['stats'] = {
        'scan_count': product.get('scan_count', 0),
        'production_media_count': len(product.get('production_media', [])),
        'harvest_media_count': len(product.get('harvest_media', [])),
        'has_contact_info': False
    }

    # Tạo khuyến nghị cải thiện
    if not has_production_process or len(product.get('production_process', '')) < 50:
        analysis['recommendations'].append(
            "Nên bổ sung thêm thông tin chi tiết về quy trình sản xuất, phân bón, thuốc bảo vệ thực vật để tăng tính minh bạch và niềm tin của người tiêu dùng"
        )

    if not has_harvest_process or len(product.get('harvest_process', '')) < 50:
        analysis['recommendations'].append(
            "Nên mô tả rõ ràng quá trình thu hoạch, phương pháp và thời điểm thu hoạch để người tiêu dùng hiểu rõ hơn về chất lượng sản phẩm"
        )

    if not has_production_media:
        analysis['recommendations'].append(
            "Nên thêm video hoặc hình ảnh về quá trình sản xuất để tăng độ tin cậy và minh bạch, giúp người tiêu dùng tin tưởng hơn"
        )

    if not has_harvest_media:
        analysis['recommendations'].append(
            "Nên thêm video hoặc hình ảnh về quá trình thu hoạch để người tiêu dùng có thể xem trực quan quy trình sản xuất"
        )

    if not has_storage_method or len(product.get('storage_method', '')) < 30:
        analysis['recommendations'].append(
            "Nên cung cấp thông tin chi tiết về cách bảo quản sản phẩm, nhiệt độ, độ ẩm để đảm bảo chất lượng và an toàn thực phẩm"
        )

    if analysis['stats']['scan_count'] == 0:
        analysis['recommendations'].append(
            "Sản phẩm chưa có lượt quét QR nào. Hãy chia sẻ mã QR trên bao bì, mạng xã hội để tăng độ nhận diện và tin cậy của sản phẩm"
        )
    elif analysis['stats']['scan_count'] < 5:
        analysis['recommendations'].append(
            f"Sản phẩm đã có {analysis['stats']['scan_count']} lượt quét. Hãy tiếp tục quảng bá để tăng mức độ quan tâm và kết nối với người tiêu dùng"
        )

    if compliance_score < 60:
        analysis['recommendations'].append(
            "Cần cải thiện mức độ tuân thủ tiêu chuẩn số hóa. Hãy bổ sung đầy đủ thông tin, media và quy trình để đạt tiêu chuẩn cao hơn"
        )

    if not analysis['recommendations']:
        analysis['recommendations'].append(
            "Sản phẩm của bạn đã có đầy đủ thông tin minh bạch. Tiếp tục duy trì và cập nhật thông tin định kỳ để giữ được niềm tin của người tiêu dùng."
        )

    return analysis


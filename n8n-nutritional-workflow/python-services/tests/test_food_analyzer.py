"""
Unit tests for Food Image Analyzer
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from PIL import Image
import numpy as np
from food_image_analyzer import FoodImageAnalyzer


class TestFoodImageAnalyzer:
    """Test suite for FoodImageAnalyzer class"""
    
    @pytest.fixture
    def analyzer(self):
        """Create FoodImageAnalyzer instance for testing"""
        return FoodImageAnalyzer()
    
    @pytest.fixture
    def sample_image(self):
        """Create a sample PIL image for testing"""
        return Image.new('RGB', (224, 224), color='red')
    
    def test_initialization(self, analyzer):
        """Test that analyzer initializes correctly"""
        assert analyzer is not None
        assert analyzer.device is not None
        assert analyzer.nutrition_db is not None
        assert 'chicken_breast' in analyzer.nutrition_db
    
    def test_nutrition_database_structure(self, analyzer):
        """Test nutrition database has correct structure"""
        for food, data in analyzer.nutrition_db.items():
            assert 'calories' in data
            assert 'protein' in data
            assert 'carbs' in data
            assert 'fats' in data
            assert 'common_portions' in data
            assert isinstance(data['common_portions'], dict)
    
    def test_detect_foods(self, analyzer, sample_image):
        """Test food detection returns expected structure"""
        detected_foods = analyzer.detect_foods(sample_image)
        
        assert isinstance(detected_foods, list)
        assert len(detected_foods) > 0
        
        for food in detected_foods:
            assert 'food_name' in food
            assert 'display_name' in food
            assert 'confidence' in food
            assert 'portion_size' in food
            assert 0 <= food['confidence'] <= 1
    
    def test_estimate_portion_size(self, analyzer, sample_image):
        """Test portion size estimation"""
        portion = analyzer.estimate_portion_size(sample_image, 'chicken_breast')
        
        assert portion in ['small', 'medium', 'large']
    
    def test_calculate_nutrition(self, analyzer):
        """Test nutrition calculation"""
        detected_foods = [
            {
                'food_name': 'chicken_breast',
                'display_name': 'Chicken Breast',
                'confidence': 0.9,
                'portion_size': 'medium'
            },
            {
                'food_name': 'rice',
                'display_name': 'White Rice',
                'confidence': 0.85,
                'portion_size': 'medium'
            }
        ]
        
        nutrition = analyzer.calculate_nutrition(detected_foods)
        
        assert 'total_calories' in nutrition
        assert 'macros' in nutrition
        assert 'food_details' in nutrition
        
        assert nutrition['total_calories'] > 0
        assert nutrition['macros']['protein'] > 0
        assert nutrition['macros']['carbs'] > 0
        assert nutrition['macros']['fats'] >= 0
        
        assert len(nutrition['food_details']) == 2
    
    def test_check_allergens_none(self, analyzer):
        """Test allergen checking with no allergies"""
        detected_foods = [
            {
                'food_name': 'chicken_breast',
                'display_name': 'Chicken Breast',
                'confidence': 0.9
            }
        ]
        
        warnings = analyzer.check_allergens(detected_foods, 'none')
        
        assert isinstance(warnings, list)
        assert len(warnings) == 0
    
    def test_check_allergens_with_match(self, analyzer):
        """Test allergen checking with allergen present"""
        detected_foods = [
            {
                'food_name': 'salmon',
                'display_name': 'Salmon',
                'confidence': 0.9
            }
        ]
        
        warnings = analyzer.check_allergens(detected_foods, 'seafood')
        
        assert isinstance(warnings, list)
        assert len(warnings) > 0
        assert 'salmon' in warnings[0].lower()
    
    def test_check_allergens_multiple(self, analyzer):
        """Test allergen checking with multiple allergens"""
        detected_foods = [
            {
                'food_name': 'salmon',
                'display_name': 'Salmon',
                'confidence': 0.9
            }
        ]
        
        warnings = analyzer.check_allergens(detected_foods, 'nuts, seafood, dairy')
        
        assert len(warnings) > 0
    
    @patch('food_image_analyzer.requests.get')
    def test_download_telegram_image(self, mock_get, analyzer):
        """Test Telegram image download"""
        # Mock response
        mock_response = Mock()
        mock_response.content = b'fake_image_data'
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Mock Image.open
        with patch('food_image_analyzer.Image.open') as mock_image_open:
            mock_image = Mock(spec=Image.Image)
            mock_image.convert = Mock(return_value=mock_image)
            mock_image_open.return_value = mock_image
            
            result = analyzer.download_telegram_image(
                'photos/file_1.jpg',
                'test_token'
            )
            
            assert result is not None
            mock_get.assert_called_once()
    
    def test_analyze_success(self, analyzer):
        """Test complete analysis workflow"""
        # Mock methods
        with patch.object(analyzer, 'download_telegram_image') as mock_download, \
             patch.object(analyzer, 'detect_foods') as mock_detect, \
             patch.object(analyzer, 'calculate_nutrition') as mock_nutrition, \
             patch.object(analyzer, 'check_allergens') as mock_allergens:
            
            # Setup mocks
            mock_download.return_value = Image.new('RGB', (224, 224))
            mock_detect.return_value = [
                {
                    'food_name': 'chicken_breast',
                    'display_name': 'Chicken Breast',
                    'confidence': 0.9,
                    'portion_size': 'medium'
                }
            ]
            mock_nutrition.return_value = {
                'total_calories': 330,
                'macros': {'protein': 62, 'carbs': 0, 'fats': 7.2},
                'food_details': []
            }
            mock_allergens.return_value = []
            
            # Run analysis
            results = analyzer.analyze(
                'photos/file_1.jpg',
                'test_token',
                'file_id_123',
                'none'
            )
            
            # Verify results
            assert results['success'] is True
            assert 'detected_foods' in results
            assert 'total_calories' in results
            assert 'macros' in results
            assert results['total_calories'] == 330
    
    def test_analyze_error_handling(self, analyzer):
        """Test error handling in analysis"""
        # Mock to raise exception
        with patch.object(analyzer, 'download_telegram_image', side_effect=Exception("Network error")):
            results = analyzer.analyze(
                'photos/file_1.jpg',
                'test_token',
                'file_id_123'
            )
            
            assert results['success'] is False
            assert 'error' in results
            assert results['total_calories'] == 0


class TestNutritionDatabase:
    """Test nutrition database content"""
    
    @pytest.fixture
    def analyzer(self):
        return FoodImageAnalyzer()
    
    def test_all_foods_have_required_fields(self, analyzer):
        """Test all foods have required nutritional data"""
        required_fields = ['calories', 'protein', 'carbs', 'fats', 'common_portions']
        
        for food_name, nutrition in analyzer.nutrition_db.items():
            for field in required_fields:
                assert field in nutrition, f"{food_name} missing {field}"
    
    def test_portion_sizes_valid(self, analyzer):
        """Test all foods have valid portion sizes"""
        valid_portions = ['small', 'medium', 'large']
        
        for food_name, nutrition in analyzer.nutrition_db.items():
            portions = nutrition['common_portions']
            for portion_size in portions.keys():
                assert portion_size in valid_portions, \
                    f"{food_name} has invalid portion size: {portion_size}"
    
    def test_nutrition_values_positive(self, analyzer):
        """Test all nutrition values are non-negative"""
        for food_name, nutrition in analyzer.nutrition_db.items():
            assert nutrition['calories'] >= 0, f"{food_name} has negative calories"
            assert nutrition['protein'] >= 0, f"{food_name} has negative protein"
            assert nutrition['carbs'] >= 0, f"{food_name} has negative carbs"
            assert nutrition['fats'] >= 0, f"{food_name} has negative fats"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

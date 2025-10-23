"""
Food Image Analysis Service
Uses computer vision models for food recognition and calorie estimation
Recommended Models:
- YOLO v8 fine-tuned on Food-101 dataset for food detection
- Nutrition5k or Food2k for calorie estimation
- ResNet50 or EfficientNet for food classification
"""

import os
import requests
import numpy as np
from PIL import Image
from io import BytesIO
from typing import Dict, List, Any
import torch
from torchvision import transforms, models
import json

# For production, replace with actual model implementations
# This is a demonstration with pseudo-code logic


class FoodImageAnalyzer:
    """
    Main class for food image analysis using computer vision models
    """
    
    def __init__(self):
        """Initialize the food recognition models"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load food classification model (e.g., ResNet50 fine-tuned on Food-101)
        self.food_classifier = self._load_food_classifier()
        
        # Load portion size estimation model
        self.portion_estimator = self._load_portion_estimator()
        
        # Food nutrition database (simplified)
        self.nutrition_db = self._load_nutrition_database()
        
        # Image preprocessing pipeline
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    def _load_food_classifier(self):
        """
        Load pre-trained food classification model
        
        In production, use:
        - Fine-tuned ResNet50/EfficientNet on Food-101 dataset
        - YOLOv8 for multi-food detection
        - Custom CNN trained on nutrition datasets
        """
        # Pseudo-code: Load your trained model
        # model = torch.load('models/food_classifier.pth')
        # model.eval()
        # return model
        
        # For demonstration, using pre-trained ResNet
        model = models.resnet50(pretrained=True)
        model.eval()
        return model
    
    def _load_portion_estimator(self):
        """
        Load portion size estimation model
        
        In production, use depth estimation or reference object detection
        """
        # Pseudo-code: Load portion estimation model
        # model = torch.load('models/portion_estimator.pth')
        # return model
        return None  # Placeholder
    
    def _load_nutrition_database(self) -> Dict:
        """
        Load comprehensive nutrition database
        
        In production, use USDA FoodData Central API or custom database
        """
        # Simplified nutrition database (per 100g)
        return {
            "chicken_breast": {
                "calories": 165,
                "protein": 31,
                "carbs": 0,
                "fats": 3.6,
                "common_portions": {"small": 150, "medium": 200, "large": 250}
            },
            "rice": {
                "calories": 130,
                "protein": 2.7,
                "carbs": 28,
                "fats": 0.3,
                "common_portions": {"small": 100, "medium": 150, "large": 200}
            },
            "broccoli": {
                "calories": 34,
                "protein": 2.8,
                "carbs": 7,
                "fats": 0.4,
                "common_portions": {"small": 75, "medium": 100, "large": 150}
            },
            "salmon": {
                "calories": 208,
                "protein": 20,
                "carbs": 0,
                "fats": 13,
                "common_portions": {"small": 150, "medium": 200, "large": 250}
            },
            "pasta": {
                "calories": 131,
                "protein": 5,
                "carbs": 25,
                "fats": 1.1,
                "common_portions": {"small": 150, "medium": 200, "large": 300}
            },
            "salad": {
                "calories": 15,
                "protein": 1.2,
                "carbs": 3,
                "fats": 0.2,
                "common_portions": {"small": 100, "medium": 150, "large": 200}
            }
        }
    
    def download_telegram_image(self, file_path: str, telegram_token: str) -> Image.Image:
        """
        Download image from Telegram servers
        
        Args:
            file_path: File path from Telegram getFile API
            telegram_token: Bot token for authentication
        
        Returns:
            PIL Image object
        """
        url = f"https://api.telegram.org/file/bot{telegram_token}/{file_path}"
        response = requests.get(url)
        response.raise_for_status()
        
        image = Image.open(BytesIO(response.content))
        return image.convert('RGB')
    
    def detect_foods(self, image: Image.Image) -> List[Dict[str, Any]]:
        """
        Detect food items in the image using computer vision
        
        Args:
            image: PIL Image object
        
        Returns:
            List of detected food items with confidence scores
        
        In production, replace with:
        - YOLOv8 or Detectron2 for object detection
        - Fine-tuned food recognition model
        - Multi-label classification for mixed dishes
        """
        # Preprocess image
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # PSEUDO-CODE: Actual implementation would use trained food detection model
        # with torch.no_grad():
        #     predictions = self.food_classifier(input_tensor)
        #     top_predictions = torch.topk(predictions, k=5)
        
        # For demonstration, return mock detections
        # In production, this would be actual model predictions
        detected_foods = [
            {
                "food_name": "chicken_breast",
                "display_name": "Chicken Breast",
                "confidence": 0.92,
                "portion_size": "medium"
            },
            {
                "food_name": "rice",
                "display_name": "White Rice",
                "confidence": 0.88,
                "portion_size": "medium"
            },
            {
                "food_name": "broccoli",
                "display_name": "Broccoli",
                "confidence": 0.85,
                "portion_size": "small"
            }
        ]
        
        return detected_foods
    
    def estimate_portion_size(self, image: Image.Image, food_item: str) -> str:
        """
        Estimate portion size using depth estimation or reference objects
        
        Args:
            image: PIL Image object
            food_item: Detected food item name
        
        Returns:
            Portion size category (small/medium/large)
        
        In production, use:
        - Depth estimation models (MiDaS, DPT)
        - Reference object detection (plate, utensils)
        - Semantic segmentation for area calculation
        """
        # PSEUDO-CODE: Actual implementation
        # depth_map = self.portion_estimator(image)
        # food_area = calculate_food_area(depth_map, food_item)
        # portion = classify_portion_size(food_area)
        
        # For demonstration, return medium as default
        return "medium"
    
    def calculate_nutrition(self, detected_foods: List[Dict]) -> Dict[str, Any]:
        """
        Calculate total nutrition from detected foods
        
        Args:
            detected_foods: List of detected food items with portions
        
        Returns:
            Dictionary with total calories and macronutrients
        """
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fats = 0
        
        food_details = []
        
        for food in detected_foods:
            food_name = food['food_name']
            portion_size = food['portion_size']
            
            if food_name in self.nutrition_db:
                nutrition = self.nutrition_db[food_name]
                
                # Get portion weight in grams
                portion_weight = nutrition['common_portions'].get(portion_size, 150)
                
                # Calculate nutrition based on portion (per 100g reference)
                multiplier = portion_weight / 100
                
                calories = nutrition['calories'] * multiplier
                protein = nutrition['protein'] * multiplier
                carbs = nutrition['carbs'] * multiplier
                fats = nutrition['fats'] * multiplier
                
                total_calories += calories
                total_protein += protein
                total_carbs += carbs
                total_fats += fats
                
                food_details.append({
                    "name": food['display_name'],
                    "portion_grams": portion_weight,
                    "calories": round(calories, 1),
                    "protein": round(protein, 1),
                    "carbs": round(carbs, 1),
                    "fats": round(fats, 1)
                })
        
        return {
            "total_calories": round(total_calories, 1),
            "macros": {
                "protein": round(total_protein, 1),
                "carbs": round(total_carbs, 1),
                "fats": round(total_fats, 1)
            },
            "food_details": food_details
        }
    
    def check_allergens(self, detected_foods: List[Dict], user_allergies: str) -> List[str]:
        """
        Check for potential allergens in detected foods
        
        Args:
            detected_foods: List of detected food items
            user_allergies: User's allergy information
        
        Returns:
            List of allergy warnings
        """
        if not user_allergies or user_allergies.lower() == 'none':
            return []
        
        # Common allergen mapping
        allergen_map = {
            "nuts": ["peanut", "almond", "cashew", "walnut"],
            "dairy": ["milk", "cheese", "yogurt", "butter", "cream"],
            "gluten": ["wheat", "bread", "pasta", "flour"],
            "seafood": ["fish", "salmon", "tuna", "shrimp", "shellfish"],
            "eggs": ["egg"],
            "soy": ["soy", "tofu", "soy_sauce"]
        }
        
        warnings = []
        user_allergy_list = [a.strip().lower() for a in user_allergies.split(',')]
        
        for food in detected_foods:
            food_name = food['food_name'].lower()
            
            for allergy in user_allergy_list:
                if allergy in allergen_map:
                    allergen_foods = allergen_map[allergy]
                    if any(allergen in food_name for allergen in allergen_foods):
                        warnings.append(
                            f"⚠️ {food['display_name']} may contain {allergy}!"
                        )
        
        return warnings
    
    def analyze(self, image_path: str, telegram_token: str, 
                telegram_file_id: str, user_allergies: str = None) -> Dict[str, Any]:
        """
        Main analysis function - orchestrates the entire food analysis pipeline
        
        Args:
            image_path: Path to the image file from Telegram
            telegram_token: Telegram bot token
            telegram_file_id: Telegram file ID
            user_allergies: User's allergy information
        
        Returns:
            Complete analysis results with nutrition and warnings
        """
        try:
            # Download and load image
            image = self.download_telegram_image(image_path, telegram_token)
            
            # Detect food items
            detected_foods = self.detect_foods(image)
            
            # Calculate nutrition
            nutrition_results = self.calculate_nutrition(detected_foods)
            
            # Check for allergens
            allergy_warnings = self.check_allergens(detected_foods, user_allergies)
            
            # Compile results
            results = {
                "success": True,
                "detected_foods": [food['display_name'] for food in detected_foods],
                "total_calories": nutrition_results['total_calories'],
                "macros": nutrition_results['macros'],
                "food_details": nutrition_results['food_details'],
                "allergy_warnings": allergy_warnings,
                "confidence_scores": {
                    food['display_name']: food['confidence'] 
                    for food in detected_foods
                }
            }
            
            return results
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "detected_foods": [],
                "total_calories": 0,
                "macros": {"protein": 0, "carbs": 0, "fats": 0},
                "allergy_warnings": []
            }


# Flask API wrapper for n8n integration
if __name__ == "__main__":
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    analyzer = FoodImageAnalyzer()
    
    @app.route('/analyze-food-image', methods=['POST'])
    def analyze_food_image():
        """
        API endpoint for food image analysis
        
        Expected JSON payload:
        {
            "image_url": "telegram_file_path",
            "telegram_file_id": "file_id",
            "user_allergies": "nuts, dairy" (optional)
        }
        """
        data = request.json
        
        image_url = data.get('image_url')
        telegram_file_id = data.get('telegram_file_id')
        user_allergies = data.get('user_allergies', None)
        
        # Get Telegram token from environment
        telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        
        if not image_url or not telegram_token:
            return jsonify({
                "success": False,
                "error": "Missing required parameters"
            }), 400
        
        results = analyzer.analyze(
            image_url, 
            telegram_token, 
            telegram_file_id,
            user_allergies
        )
        
        return jsonify(results)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({"status": "healthy", "service": "food_image_analyzer"})
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)

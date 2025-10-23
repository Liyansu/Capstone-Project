"""
Advanced Food Recognition and Calorie Estimation Module
This module provides computer vision capabilities for food recognition and nutritional analysis.
"""

import base64
import requests
import json
from typing import Dict, List, Tuple, Optional
import numpy as np
from PIL import Image
import io

class FoodRecognitionModel:
    """
    Advanced food recognition model using state-of-the-art computer vision techniques.
    Supports multiple backends: Hugging Face, AWS SageMaker, Google Vision API.
    """
    
    def __init__(self, api_type: str = "huggingface", **kwargs):
        """
        Initialize the food recognition model.
        
        Args:
            api_type: Type of API to use ('huggingface', 'aws', 'google')
            **kwargs: API-specific configuration parameters
        """
        self.api_type = api_type
        self.config = kwargs
        
        if api_type == "huggingface":
            self.api_key = kwargs.get("api_key")
            self.model_name = kwargs.get("model_name", "microsoft/food-101")
            self.base_url = "https://api-inference.huggingface.co/models"
        elif api_type == "aws":
            self.aws_access_key = kwargs.get("aws_access_key")
            self.aws_secret_key = kwargs.get("aws_secret_key")
            self.aws_region = kwargs.get("aws_region", "us-east-1")
            self.endpoint_name = kwargs.get("endpoint_name")
        elif api_type == "google":
            self.project_id = kwargs.get("project_id")
            self.credentials_path = kwargs.get("credentials_path")
    
    def preprocess_image(self, image_data: str) -> str:
        """
        Preprocess image for optimal model performance.
        
        Args:
            image_data: Base64 encoded image or image path
            
        Returns:
            Processed image data
        """
        try:
            # Decode base64 image
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Resize to optimal size for food recognition
            image = image.resize((224, 224), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert back to base64
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=95)
            processed_image = base64.b64encode(buffer.getvalue()).decode()
            
            return processed_image
            
        except Exception as e:
            raise ValueError(f"Image preprocessing failed: {str(e)}")
    
    def recognize_foods_huggingface(self, image_data: str) -> Dict:
        """
        Recognize foods using Hugging Face Transformers API.
        
        Args:
            image_data: Base64 encoded image
            
        Returns:
            Dictionary containing food recognition results
        """
        try:
            processed_image = self.preprocess_image(image_data)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": processed_image,
                "parameters": {
                    "top_k": 10,
                    "threshold": 0.1
                }
            }
            
            response = requests.post(
                f"{self.base_url}/{self.model_name}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                results = response.json()
                return self._process_huggingface_results(results)
            else:
                raise Exception(f"Hugging Face API error: {response.status_code}")
                
        except Exception as e:
            raise Exception(f"Food recognition failed: {str(e)}")
    
    def recognize_foods_aws(self, image_data: str) -> Dict:
        """
        Recognize foods using AWS SageMaker endpoint.
        
        Args:
            image_data: Base64 encoded image
            
        Returns:
            Dictionary containing food recognition results
        """
        try:
            import boto3
            
            processed_image = self.preprocess_image(image_data)
            
            # Initialize SageMaker client
            sagemaker_client = boto3.client(
                'sagemaker-runtime',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region
            )
            
            # Prepare payload for SageMaker endpoint
            payload = {
                "image": processed_image,
                "model_type": "food_recognition"
            }
            
            response = sagemaker_client.invoke_endpoint(
                EndpointName=self.endpoint_name,
                ContentType='application/json',
                Body=json.dumps(payload)
            )
            
            results = json.loads(response['Body'].read())
            return self._process_aws_results(results)
            
        except Exception as e:
            raise Exception(f"AWS SageMaker recognition failed: {str(e)}")
    
    def recognize_foods_google(self, image_data: str) -> Dict:
        """
        Recognize foods using Google Vision API.
        
        Args:
            image_data: Base64 encoded image
            
        Returns:
            Dictionary containing food recognition results
        """
        try:
            from google.cloud import vision
            from google.oauth2 import service_account
            
            # Initialize Google Vision client
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path
            )
            client = vision.ImageAnnotatorClient(credentials=credentials)
            
            processed_image = self.preprocess_image(image_data)
            image_bytes = base64.b64decode(processed_image)
            
            # Perform food detection
            image = vision.Image(content=image_bytes)
            response = client.label_detection(image=image)
            labels = response.label_annotations
            
            # Filter food-related labels
            food_labels = [label for label in labels if self._is_food_related(label.description)]
            
            return self._process_google_results(food_labels)
            
        except Exception as e:
            raise Exception(f"Google Vision recognition failed: {str(e)}")
    
    def _is_food_related(self, label: str) -> bool:
        """Check if a label is food-related."""
        food_keywords = [
            'food', 'meal', 'dish', 'cuisine', 'ingredient', 'vegetable',
            'fruit', 'meat', 'chicken', 'beef', 'fish', 'pasta', 'rice',
            'bread', 'salad', 'soup', 'pizza', 'burger', 'sandwich'
        ]
        return any(keyword in label.lower() for keyword in food_keywords)
    
    def _process_huggingface_results(self, results: List) -> Dict:
        """Process Hugging Face API results."""
        identified_foods = []
        total_confidence = 0
        
        for result in results:
            if isinstance(result, dict) and 'label' in result and 'score' in result:
                food_name = result['label']
                confidence = result['score']
                
                if confidence > 0.1:  # Threshold for food recognition
                    nutritional_data = self._get_nutritional_data(food_name)
                    identified_foods.append({
                        'name': food_name,
                        'confidence': confidence,
                        'estimatedWeight': nutritional_data['estimatedWeight'],
                        'calories': nutritional_data['calories'],
                        'protein': nutritional_data['protein'],
                        'carbs': nutritional_data['carbs'],
                        'fat': nutritional_data['fat'],
                        'fiber': nutritional_data['fiber']
                    })
                    total_confidence += confidence
        
        return self._calculate_totals(identified_foods)
    
    def _process_aws_results(self, results: Dict) -> Dict:
        """Process AWS SageMaker results."""
        # Implementation depends on your specific SageMaker model output format
        identified_foods = []
        
        if 'predictions' in results:
            for prediction in results['predictions']:
                food_name = prediction.get('food_name', 'unknown')
                confidence = prediction.get('confidence', 0.0)
                portion_size = prediction.get('portion_size', 100)  # grams
                
                nutritional_data = self._get_nutritional_data(food_name, portion_size)
                identified_foods.append({
                    'name': food_name,
                    'confidence': confidence,
                    'estimatedWeight': portion_size,
                    'calories': nutritional_data['calories'],
                    'protein': nutritional_data['protein'],
                    'carbs': nutritional_data['carbs'],
                    'fat': nutritional_data['fat'],
                    'fiber': nutritional_data['fiber']
                })
        
        return self._calculate_totals(identified_foods)
    
    def _process_google_results(self, labels: List) -> Dict:
        """Process Google Vision API results."""
        identified_foods = []
        
        for label in labels:
            food_name = label.description
            confidence = label.score
            
            if confidence > 0.1:
                nutritional_data = self._get_nutritional_data(food_name)
                identified_foods.append({
                    'name': food_name,
                    'confidence': confidence,
                    'estimatedWeight': nutritional_data['estimatedWeight'],
                    'calories': nutritional_data['calories'],
                    'protein': nutritional_data['protein'],
                    'carbs': nutritional_data['carbs'],
                    'fat': nutritional_data['fat'],
                    'fiber': nutritional_data['fiber']
                })
        
        return self._calculate_totals(identified_foods)
    
    def _get_nutritional_data(self, food_name: str, portion_size: int = 100) -> Dict:
        """
        Get nutritional data for a specific food item.
        In production, this would query a comprehensive food database.
        """
        # Simplified nutritional database (in production, use USDA FoodData Central or similar)
        nutritional_db = {
            'chicken breast': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0},
            'grilled chicken': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0},
            'broccoli': {'calories': 34, 'protein': 2.8, 'carbs': 6.6, 'fat': 0.4, 'fiber': 2.6},
            'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3, 'fiber': 0.4},
            'brown rice': {'calories': 111, 'protein': 2.3, 'carbs': 23, 'fat': 0.9, 'fiber': 1.8},
            'salmon': {'calories': 208, 'protein': 25, 'carbs': 0, 'fat': 12, 'fiber': 0},
            'pasta': {'calories': 131, 'protein': 5, 'carbs': 25, 'fat': 1.1, 'fiber': 1.8},
            'bread': {'calories': 265, 'protein': 9, 'carbs': 49, 'fat': 3.2, 'fiber': 2.7},
            'apple': {'calories': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2, 'fiber': 2.4},
            'banana': {'calories': 89, 'protein': 1.1, 'carbs': 23, 'fat': 0.3, 'fiber': 2.6},
            'yogurt': {'calories': 59, 'protein': 10, 'carbs': 3.6, 'fat': 0.4, 'fiber': 0},
            'milk': {'calories': 42, 'protein': 3.4, 'carbs': 5, 'fat': 1, 'fiber': 0},
            'cheese': {'calories': 113, 'protein': 7, 'carbs': 1, 'fat': 9, 'fiber': 0},
            'egg': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11, 'fiber': 0},
            'potato': {'calories': 77, 'protein': 2, 'carbs': 17, 'fat': 0.1, 'fiber': 2.2},
            'sweet potato': {'calories': 86, 'protein': 1.6, 'carbs': 20, 'fat': 0.1, 'fiber': 3},
            'carrot': {'calories': 41, 'protein': 0.9, 'carbs': 10, 'fat': 0.2, 'fiber': 2.8},
            'spinach': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4, 'fiber': 2.2},
            'tomato': {'calories': 18, 'protein': 0.9, 'carbs': 3.9, 'fat': 0.2, 'fiber': 1.2},
            'onion': {'calories': 40, 'protein': 1.1, 'carbs': 9.3, 'fat': 0.1, 'fiber': 1.7}
        }
        
        # Find best match in database
        food_name_lower = food_name.lower()
        best_match = None
        best_score = 0
        
        for db_food, nutrition in nutritional_db.items():
            # Simple string matching (in production, use fuzzy matching)
            if db_food in food_name_lower or food_name_lower in db_food:
                score = len(set(db_food.split()) & set(food_name_lower.split()))
                if score > best_score:
                    best_match = nutrition
                    best_score = score
        
        if best_match:
            # Scale nutrition data based on portion size
            scale_factor = portion_size / 100
            return {
                'calories': round(best_match['calories'] * scale_factor),
                'protein': round(best_match['protein'] * scale_factor, 1),
                'carbs': round(best_match['carbs'] * scale_factor, 1),
                'fat': round(best_match['fat'] * scale_factor, 1),
                'fiber': round(best_match['fiber'] * scale_factor, 1),
                'estimatedWeight': portion_size
            }
        else:
            # Default nutritional values for unknown foods
            return {
                'calories': round(100 * portion_size / 100),
                'protein': round(5 * portion_size / 100, 1),
                'carbs': round(15 * portion_size / 100, 1),
                'fat': round(3 * portion_size / 100, 1),
                'fiber': round(2 * portion_size / 100, 1),
                'estimatedWeight': portion_size
            }
    
    def _calculate_totals(self, identified_foods: List[Dict]) -> Dict:
        """Calculate total nutritional values for all identified foods."""
        totals = {
            'totalCalories': 0,
            'totalProtein': 0,
            'totalCarbs': 0,
            'totalFat': 0,
            'totalFiber': 0
        }
        
        for food in identified_foods:
            totals['totalCalories'] += food['calories']
            totals['totalProtein'] += food['protein']
            totals['totalCarbs'] += food['carbs']
            totals['totalFat'] += food['fat']
            totals['totalFiber'] += food['fiber']
        
        # Round totals
        totals['totalCalories'] = round(totals['totalCalories'])
        totals['totalProtein'] = round(totals['totalProtein'], 1)
        totals['totalCarbs'] = round(totals['totalCarbs'], 1)
        totals['totalFat'] = round(totals['totalFat'], 1)
        totals['totalFiber'] = round(totals['totalFiber'], 1)
        
        return {
            'identifiedFoods': identified_foods,
            **totals
        }
    
    def recognize_foods(self, image_data: str) -> Dict:
        """
        Main method to recognize foods in an image.
        
        Args:
            image_data: Base64 encoded image
            
        Returns:
            Dictionary containing food recognition results
        """
        if self.api_type == "huggingface":
            return self.recognize_foods_huggingface(image_data)
        elif self.api_type == "aws":
            return self.recognize_foods_aws(image_data)
        elif self.api_type == "google":
            return self.recognize_foods_google(image_data)
        else:
            raise ValueError(f"Unsupported API type: {self.api_type}")


# Example usage and testing
if __name__ == "__main__":
    # Initialize the model
    model = FoodRecognitionModel(
        api_type="huggingface",
        api_key="your_hugging_face_api_key",
        model_name="microsoft/food-101"
    )
    
    # Example image data (base64 encoded)
    sample_image = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
    
    try:
        results = model.recognize_foods(sample_image)
        print("Food Recognition Results:")
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
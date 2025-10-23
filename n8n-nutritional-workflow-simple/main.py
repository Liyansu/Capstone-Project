"""
N8N Nutritional Planning Workflow - Python Main Service
This is a simplified FastAPI service that provides food recognition and dietary planning APIs.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
import json
import base64
from io import BytesIO
from PIL import Image
from typing import Dict, List, Optional
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="N8N Nutritional Planning API",
    description="Food recognition and dietary planning service for n8n workflow",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Food database with nutritional information
FOOD_DATABASE = {
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
    'onion': {'calories': 40, 'protein': 1.1, 'carbs': 9.3, 'fat': 0.1, 'fiber': 1.7},
    'avocado': {'calories': 160, 'protein': 2, 'carbs': 9, 'fat': 15, 'fiber': 7},
    'almonds': {'calories': 579, 'protein': 21, 'carbs': 22, 'fat': 50, 'fiber': 12},
    'oats': {'calories': 68, 'protein': 2.4, 'carbs': 12, 'fat': 1.4, 'fiber': 1.7},
    'quinoa': {'calories': 120, 'protein': 4.4, 'carbs': 22, 'fat': 1.9, 'fiber': 2.8},
    'pizza': {'calories': 266, 'protein': 11, 'carbs': 33, 'fat': 10, 'fiber': 2.3},
    'burger': {'calories': 354, 'protein': 16, 'carbs': 33, 'fat': 17, 'fiber': 2.1},
    'salad': {'calories': 25, 'protein': 2, 'carbs': 5, 'fat': 0.5, 'fiber': 2},
    'soup': {'calories': 50, 'protein': 3, 'carbs': 8, 'fat': 1, 'fiber': 1.5},
    'pasta': {'calories': 131, 'protein': 5, 'carbs': 25, 'fat': 1.1, 'fiber': 1.8},
    'fish': {'calories': 206, 'protein': 22, 'carbs': 0, 'fat': 12, 'fiber': 0},
    'beef': {'calories': 250, 'protein': 26, 'carbs': 0, 'fat': 15, 'fiber': 0},
    'pork': {'calories': 242, 'protein': 27, 'carbs': 0, 'fat': 14, 'fiber': 0}
}

# Activity level multipliers for TDEE calculation
ACTIVITY_MULTIPLIERS = {
    'sedentary': 1.2,
    'light': 1.375,
    'moderate': 1.55,
    'active': 1.725,
    'very_active': 1.9
}

def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor equation."""
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        # Average of male and female formulas for unknown gender
        male_bmr = 10 * weight + 6.25 * height - 5 * age + 5
        female_bmr = 10 * weight + 6.25 * height - 5 * age - 161
        bmr = (male_bmr + female_bmr) / 2
    
    return round(bmr, 1)

def calculate_tdee(bmr: float, activity_level: str) -> float:
    """Calculate Total Daily Energy Expenditure."""
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level.lower(), 1.55)
    return round(bmr * multiplier, 1)

def determine_caloric_goal(tdee: float, goals: str) -> int:
    """Determine daily caloric goal based on user's weight goals."""
    goals_lower = goals.lower()
    
    if any(keyword in goals_lower for keyword in ['lose', 'weight loss', 'reduce']):
        # Weight loss: 500 calorie deficit
        return max(int(tdee - 500), 1200)
    elif any(keyword in goals_lower for keyword in ['gain', 'weight gain', 'bulk', 'muscle']):
        # Weight gain: 300 calorie surplus
        return int(tdee + 300)
    else:
        # Weight maintenance
        return int(tdee)

def calculate_macronutrient_goals(caloric_goal: int, goals: str) -> Dict:
    """Calculate optimal macronutrient distribution."""
    goals_lower = goals.lower()
    
    # Adjust macronutrient ratios based on goals
    if any(keyword in goals_lower for keyword in ['muscle', 'strength', 'bulk']):
        protein_ratio = 0.35
        carb_ratio = 0.40
        fat_ratio = 0.25
    elif any(keyword in goals_lower for keyword in ['lose', 'weight loss', 'cut']):
        protein_ratio = 0.30
        carb_ratio = 0.35
        fat_ratio = 0.35
    else:
        protein_ratio = 0.30
        carb_ratio = 0.40
        fat_ratio = 0.30
    
    # Calculate macronutrient grams
    protein_calories = caloric_goal * protein_ratio
    carb_calories = caloric_goal * carb_ratio
    fat_calories = caloric_goal * fat_ratio
    
    protein_grams = protein_calories / 4  # 4 calories per gram
    carb_grams = carb_calories / 4        # 4 calories per gram
    fat_grams = fat_calories / 9          # 9 calories per gram
    
    return {
        'calories': caloric_goal,
        'protein': round(protein_grams, 1),
        'carbs': round(carb_grams, 1),
        'fat': round(fat_grams, 1),
        'fiber': max(25, 30)  # Minimum fiber recommendation
    }

def recognize_foods_simple(image_data: bytes) -> Dict:
    """Simple food recognition using mock data."""
    # In a real implementation, this would use computer vision APIs
    # For now, we'll return mock data based on common food items
    
    # Mock food recognition results
    mock_foods = [
        {
            'name': 'grilled chicken breast',
            'confidence': 0.92,
            'estimatedWeight': 150,
            'calories': 231,
            'protein': 43.5,
            'carbs': 0,
            'fat': 5.0,
            'fiber': 0
        },
        {
            'name': 'steamed broccoli',
            'confidence': 0.88,
            'estimatedWeight': 100,
            'calories': 34,
            'protein': 2.8,
            'carbs': 6.6,
            'fat': 0.4,
            'fiber': 2.6
        },
        {
            'name': 'brown rice',
            'confidence': 0.85,
            'estimatedWeight': 80,
            'calories': 111,
            'protein': 2.3,
            'carbs': 23,
            'fat': 0.9,
            'fiber': 1.8
        }
    ]
    
    # Calculate totals
    total_calories = sum(food['calories'] for food in mock_foods)
    total_protein = sum(food['protein'] for food in mock_foods)
    total_carbs = sum(food['carbs'] for food in mock_foods)
    total_fat = sum(food['fat'] for food in mock_foods)
    total_fiber = sum(food['fiber'] for food in mock_foods)
    
    return {
        'identifiedFoods': mock_foods,
        'totalCalories': total_calories,
        'totalProtein': round(total_protein, 1),
        'totalCarbs': round(total_carbs, 1),
        'totalFat': round(total_fat, 1),
        'totalFiber': round(total_fiber, 1)
    }

def generate_meal_plan(nutritional_goals: Dict) -> Dict:
    """Generate a simple 7-day meal plan."""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    meal_plan = {}
    
    for day in days:
        meal_plan[day] = {
            'breakfast': {
                'calories': int(nutritional_goals['calories'] * 0.25),
                'protein': round(nutritional_goals['protein'] * 0.25, 1),
                'carbs': round(nutritional_goals['carbs'] * 0.25, 1),
                'fat': round(nutritional_goals['fat'] * 0.25, 1),
                'fiber': round(nutritional_goals['fiber'] * 0.30, 1),
                'foods': ['Oatmeal with berries', 'Greek yogurt', 'Almonds']
            },
            'lunch': {
                'calories': int(nutritional_goals['calories'] * 0.35),
                'protein': round(nutritional_goals['protein'] * 0.35, 1),
                'carbs': round(nutritional_goals['carbs'] * 0.35, 1),
                'fat': round(nutritional_goals['fat'] * 0.35, 1),
                'fiber': round(nutritional_goals['fiber'] * 0.35, 1),
                'foods': ['Grilled chicken salad', 'Quinoa', 'Mixed vegetables']
            },
            'dinner': {
                'calories': int(nutritional_goals['calories'] * 0.30),
                'protein': round(nutritional_goals['protein'] * 0.30, 1),
                'carbs': round(nutritional_goals['carbs'] * 0.30, 1),
                'fat': round(nutritional_goals['fat'] * 0.30, 1),
                'fiber': round(nutritional_goals['fiber'] * 0.30, 1),
                'foods': ['Salmon fillet', 'Sweet potato', 'Steamed broccoli']
            },
            'snacks': {
                'calories': int(nutritional_goals['calories'] * 0.10),
                'protein': round(nutritional_goals['protein'] * 0.10, 1),
                'carbs': round(nutritional_goals['carbs'] * 0.10, 1),
                'fat': round(nutritional_goals['fat'] * 0.10, 1),
                'fiber': round(nutritional_goals['fiber'] * 0.10, 1),
                'foods': ['Apple with almond butter', 'Protein shake']
            }
        }
    
    return meal_plan

def generate_safety_warnings(allergies: List[str], meal_plan: Dict) -> List[Dict]:
    """Generate safety warnings based on allergies."""
    warnings = []
    
    if not allergies:
        return warnings
    
    # Check for common allergens in meal plan
    allergen_keywords = {
        'nuts': ['almond', 'walnut', 'peanut', 'cashew', 'pistachio'],
        'dairy': ['milk', 'cheese', 'yogurt', 'butter', 'cream'],
        'gluten': ['wheat', 'bread', 'pasta', 'flour', 'oats'],
        'eggs': ['egg', 'mayonnaise', 'custard'],
        'soy': ['soy', 'tofu', 'tempeh', 'soy sauce'],
        'fish': ['salmon', 'tuna', 'cod', 'fish'],
        'shellfish': ['shrimp', 'crab', 'lobster', 'shellfish']
    }
    
    for allergy in allergies:
        allergy_lower = allergy.lower()
        keywords = allergen_keywords.get(allergy_lower, [allergy_lower])
        found_allergens = []
        
        # Check all meals in the plan
        for day, meals in meal_plan.items():
            for meal_type, meal in meals.items():
                for food in meal['foods']:
                    for keyword in keywords:
                        if keyword in food.lower():
                            found_allergens.append(f"{food} (in {day} {meal_type})")
        
        if found_allergens:
            warnings.append({
                'type': 'allergy_warning',
                'allergen': allergy,
                'found_in': found_allergens,
                'severity': 'high',
                'recommendation': f'Please avoid foods containing {allergy} or consult with a healthcare provider.'
            })
    
    return warnings

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "nutritional-planning-api"}

@app.post("/recognize-foods")
async def recognize_foods(
    image: UploadFile = File(...),
    user_data: str = Form(...)
):
    """Recognize foods in an uploaded image and return nutritional analysis."""
    try:
        # Parse user data
        user_info = json.loads(user_data)
        
        # Read and process image
        image_content = await image.read()
        
        # Simple food recognition (mock implementation)
        recognition_result = recognize_foods_simple(image_content)
        
        return JSONResponse(content={
            "success": True,
            "data": recognition_result,
            "user_data": user_info
        })
        
    except Exception as e:
        logger.error(f"Food recognition error: {e}")
        raise HTTPException(status_code=500, detail=f"Food recognition failed: {str(e)}")

@app.post("/generate-meal-plan")
async def generate_meal_plan_endpoint(user_data: Dict):
    """Generate a personalized 7-day meal plan based on user profile."""
    try:
        # Extract user profile data
        weight = float(user_data.get("weight", 70))
        height = float(user_data.get("height", 175))
        age = int(user_data.get("age", 30))
        gender = user_data.get("gender", "female")
        activity_level = user_data.get("activity_level", "moderate")
        goals = user_data.get("goals", "")
        allergies = user_data.get("allergies", [])
        
        # Calculate BMR and TDEE
        bmr = calculate_bmr(weight, height, age, gender)
        tdee = calculate_tdee(bmr, activity_level)
        caloric_goal = determine_caloric_goal(tdee, goals)
        
        # Calculate nutritional goals
        nutritional_goals = calculate_macronutrient_goals(caloric_goal, goals)
        
        # Generate meal plan
        meal_plan = generate_meal_plan(nutritional_goals)
        
        # Generate safety warnings
        safety_warnings = generate_safety_warnings(allergies, meal_plan)
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "bmr": bmr,
                "tdee": tdee,
                "caloric_goal": caloric_goal,
                "nutritional_goals": nutritional_goals,
                "meal_plan": meal_plan,
                "safety_warnings": safety_warnings
            }
        })
        
    except Exception as e:
        logger.error(f"Meal plan generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Meal plan generation failed: {str(e)}")

@app.post("/analyze-meal")
async def analyze_meal(meal_data: Dict, user_data: Dict):
    """Analyze a specific meal and provide nutritional breakdown."""
    try:
        # Extract user profile data
        weight = float(user_data.get("weight", 70))
        height = float(user_data.get("height", 175))
        age = int(user_data.get("age", 30))
        gender = user_data.get("gender", "female")
        activity_level = user_data.get("activity_level", "moderate")
        goals = user_data.get("goals", "")
        
        # Calculate nutritional goals
        bmr = calculate_bmr(weight, height, age, gender)
        tdee = calculate_tdee(bmr, activity_level)
        caloric_goal = determine_caloric_goal(tdee, goals)
        nutritional_goals = calculate_macronutrient_goals(caloric_goal, goals)
        
        # Calculate progress metrics
        current_calories = meal_data.get('totalCalories', 0)
        current_protein = meal_data.get('totalProtein', 0)
        current_carbs = meal_data.get('totalCarbs', 0)
        current_fat = meal_data.get('totalFat', 0)
        
        progress_metrics = {
            'currentMealCalories': current_calories,
            'dailyCalorieGoal': caloric_goal,
            'remainingCalories': caloric_goal - current_calories,
            'proteinProgress': (current_protein / nutritional_goals['protein']) * 100 if nutritional_goals['protein'] > 0 else 0,
            'carbProgress': (current_carbs / nutritional_goals['carbs']) * 100 if nutritional_goals['carbs'] > 0 else 0,
            'fatProgress': (current_fat / nutritional_goals['fat']) * 100 if nutritional_goals['fat'] > 0 else 0,
            'calorieProgress': (current_calories / caloric_goal) * 100 if caloric_goal > 0 else 0
        }
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "meal_analysis": meal_data,
                "progress_metrics": progress_metrics,
                "nutritional_goals": nutritional_goals
            }
        })
        
    except Exception as e:
        logger.error(f"Meal analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Meal analysis failed: {str(e)}")

@app.get("/food-database")
async def get_food_database():
    """Get the food database for reference."""
    return JSONResponse(content={
        "success": True,
        "data": FOOD_DATABASE
    })

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
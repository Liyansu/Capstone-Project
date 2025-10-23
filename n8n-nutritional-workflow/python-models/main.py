"""
FastAPI service for advanced food recognition and dietary planning.
This service provides REST API endpoints for the n8n nutritional workflow.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from typing import Dict, List, Optional
import json
import base64
from io import BytesIO
from PIL import Image

from food_recognition import FoodRecognitionModel
from dietary_planning import DietaryPlanner, UserProfile, Gender, ActivityLevel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Nutritional Planning API",
    description="Advanced food recognition and dietary planning service for n8n workflow",
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

# Initialize services
food_recognition_model = None
dietary_planner = DietaryPlanner()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global food_recognition_model
    
    try:
        # Initialize food recognition model
        # You can configure this based on your preferred API
        food_recognition_model = FoodRecognitionModel(
            api_type="huggingface",  # or "aws", "google"
            api_key="your_api_key_here"
        )
        logger.info("Food recognition model initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize food recognition model: {e}")
        food_recognition_model = None

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "nutritional-planning-api",
        "version": "1.0.0"
    }

@app.post("/recognize-foods")
async def recognize_foods(
    image: UploadFile = File(...),
    user_data: str = Form(...)
):
    """
    Recognize foods in an uploaded image and return nutritional analysis.
    
    Args:
        image: Uploaded image file
        user_data: JSON string containing user dietary information
        
    Returns:
        Dictionary containing identified foods and nutritional data
    """
    try:
        # Parse user data
        user_info = json.loads(user_data)
        
        # Read and process image
        image_content = await image.read()
        image_base64 = base64.b64encode(image_content).decode('utf-8')
        
        # Add data URL prefix
        image_data_url = f"data:image/{image.content_type.split('/')[-1]};base64,{image_base64}"
        
        # Recognize foods
        if food_recognition_model:
            recognition_result = food_recognition_model.recognize_foods(image_data_url)
        else:
            # Fallback to mock data if model not available
            recognition_result = {
                "identifiedFoods": [
                    {
                        "name": "sample food",
                        "confidence": 0.8,
                        "estimatedWeight": 150,
                        "calories": 200,
                        "protein": 10,
                        "carbs": 20,
                        "fat": 8,
                        "fiber": 2
                    }
                ],
                "totalCalories": 200,
                "totalProtein": 10,
                "totalCarbs": 20,
                "totalFat": 8,
                "totalFiber": 2
            }
        
        return JSONResponse(content={
            "success": True,
            "data": recognition_result,
            "user_data": user_info
        })
        
    except Exception as e:
        logger.error(f"Food recognition error: {e}")
        raise HTTPException(status_code=500, detail=f"Food recognition failed: {str(e)}")

@app.post("/generate-meal-plan")
async def generate_meal_plan(user_data: Dict):
    """
    Generate a personalized 7-day meal plan based on user profile.
    
    Args:
        user_data: Dictionary containing user profile information
        
    Returns:
        Dictionary containing the generated meal plan
    """
    try:
        # Parse user profile
        profile = UserProfile(
            weight=float(user_data.get("weight", 70)),
            height=float(user_data.get("height", 175)),
            age=int(user_data.get("age", 30)),
            gender=Gender(user_data.get("gender", "female")),
            activity_level=ActivityLevel(user_data.get("activity_level", "moderate")),
            allergies=user_data.get("allergies", []),
            goals=user_data.get("goals", ""),
            medical_conditions=user_data.get("medical_conditions", []),
            dietary_restrictions=user_data.get("dietary_restrictions", [])
        )
        
        # Calculate BMR and TDEE
        bmr = dietary_planner.calculate_bmr(profile)
        tdee = dietary_planner.calculate_tdee(profile)
        caloric_goal = dietary_planner.determine_caloric_goal(profile)
        
        # Calculate nutritional goals
        nutritional_goals = dietary_planner.calculate_macronutrient_goals(caloric_goal, profile)
        
        # Generate meal plan
        meal_plan = dietary_planner.generate_meal_plan(profile, nutritional_goals)
        
        # Generate safety warnings
        safety_warnings = dietary_planner.generate_safety_warnings(profile, meal_plan)
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "bmr": bmr,
                "tdee": tdee,
                "caloric_goal": caloric_goal,
                "nutritional_goals": {
                    "calories": nutritional_goals.calories,
                    "protein": nutritional_goals.protein,
                    "carbs": nutritional_goals.carbs,
                    "fat": nutritional_goals.fat,
                    "fiber": nutritional_goals.fiber
                },
                "meal_plan": meal_plan,
                "safety_warnings": safety_warnings
            }
        })
        
    except Exception as e:
        logger.error(f"Meal plan generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Meal plan generation failed: {str(e)}")

@app.post("/analyze-meal")
async def analyze_meal(
    meal_data: Dict,
    user_data: Dict
):
    """
    Analyze a specific meal and provide nutritional breakdown.
    
    Args:
        meal_data: Dictionary containing meal nutritional information
        user_data: Dictionary containing user profile information
        
    Returns:
        Dictionary containing meal analysis and progress metrics
    """
    try:
        # Parse user profile
        profile = UserProfile(
            weight=float(user_data.get("weight", 70)),
            height=float(user_data.get("height", 175)),
            age=int(user_data.get("age", 30)),
            gender=Gender(user_data.get("gender", "female")),
            activity_level=ActivityLevel(user_data.get("activity_level", "moderate")),
            allergies=user_data.get("allergies", []),
            goals=user_data.get("goals", ""),
            medical_conditions=user_data.get("medical_conditions", []),
            dietary_restrictions=user_data.get("dietary_restrictions", [])
        )
        
        # Calculate nutritional goals
        caloric_goal = dietary_planner.determine_caloric_goal(profile)
        nutritional_goals = dietary_planner.calculate_macronutrient_goals(caloric_goal, profile)
        
        # Calculate progress metrics
        progress_metrics = dietary_planner.calculate_progress_metrics(meal_data, nutritional_goals)
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "meal_analysis": meal_data,
                "progress_metrics": progress_metrics,
                "nutritional_goals": {
                    "calories": nutritional_goals.calories,
                    "protein": nutritional_goals.protein,
                    "carbs": nutritional_goals.carbs,
                    "fat": nutritional_goals.fat,
                    "fiber": nutritional_goals.fiber
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Meal analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Meal analysis failed: {str(e)}")

@app.post("/calculate-bmr-tdee")
async def calculate_bmr_tdee(user_data: Dict):
    """
    Calculate BMR and TDEE for a user profile.
    
    Args:
        user_data: Dictionary containing user profile information
        
    Returns:
        Dictionary containing BMR and TDEE calculations
    """
    try:
        # Parse user profile
        profile = UserProfile(
            weight=float(user_data.get("weight", 70)),
            height=float(user_data.get("height", 175)),
            age=int(user_data.get("age", 30)),
            gender=Gender(user_data.get("gender", "female")),
            activity_level=ActivityLevel(user_data.get("activity_level", "moderate")),
            allergies=user_data.get("allergies", []),
            goals=user_data.get("goals", ""),
            medical_conditions=user_data.get("medical_conditions", []),
            dietary_restrictions=user_data.get("dietary_restrictions", [])
        )
        
        # Calculate BMR and TDEE
        bmr = dietary_planner.calculate_bmr(profile)
        tdee = dietary_planner.calculate_tdee(profile)
        caloric_goal = dietary_planner.determine_caloric_goal(profile)
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "bmr": bmr,
                "tdee": tdee,
                "caloric_goal": caloric_goal,
                "activity_level": profile.activity_level.value,
                "profile": {
                    "weight": profile.weight,
                    "height": profile.height,
                    "age": profile.age,
                    "gender": profile.gender.value
                }
            }
        })
        
    except Exception as e:
        logger.error(f"BMR/TDEE calculation error: {e}")
        raise HTTPException(status_code=500, detail=f"BMR/TDEE calculation failed: {str(e)}")

@app.get("/food-database")
async def get_food_database():
    """
    Get the food database for reference.
    
    Returns:
        Dictionary containing the food database
    """
    try:
        return JSONResponse(content={
            "success": True,
            "data": dietary_planner.food_database
        })
    except Exception as e:
        logger.error(f"Food database retrieval error: {e}")
        raise HTTPException(status_code=500, detail=f"Food database retrieval failed: {str(e)}")

@app.get("/meal-templates")
async def get_meal_templates():
    """
    Get available meal templates.
    
    Returns:
        Dictionary containing meal templates
    """
    try:
        return JSONResponse(content={
            "success": True,
            "data": dietary_planner.meal_templates
        })
    except Exception as e:
        logger.error(f"Meal templates retrieval error: {e}")
        raise HTTPException(status_code=500, detail=f"Meal templates retrieval failed: {str(e)}")

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "status_code": 500
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
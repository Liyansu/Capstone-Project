"""
Dietary Planning Service
Generates personalized 7-day meal plans based on user data and nutritional goals
Calculates BMR, TDEE, and provides tailored recommendations
"""

import json
import random
from typing import Dict, List, Any
from datetime import datetime, timedelta


class DietaryPlanner:
    """
    Main class for generating personalized dietary plans
    """
    
    def __init__(self):
        """Initialize the dietary planner with meal database"""
        self.meal_database = self._load_meal_database()
        self.activity_levels = {
            "sedentary": 1.2,
            "lightly_active": 1.375,
            "moderately_active": 1.55,
            "very_active": 1.725,
            "extremely_active": 1.9
        }
    
    def _load_meal_database(self) -> Dict[str, List[Dict]]:
        """
        Load comprehensive meal database with nutritional information
        
        In production, connect to a proper database or API
        """
        return {
            "breakfast": [
                {
                    "name": "Oatmeal with Berries and Almonds",
                    "calories": 350,
                    "protein": 12,
                    "carbs": 55,
                    "fats": 10,
                    "allergens": ["nuts"]
                },
                {
                    "name": "Scrambled Eggs with Whole Wheat Toast",
                    "calories": 320,
                    "protein": 20,
                    "carbs": 30,
                    "fats": 12,
                    "allergens": ["eggs", "gluten"]
                },
                {
                    "name": "Greek Yogurt Parfait with Granola",
                    "calories": 280,
                    "protein": 18,
                    "carbs": 40,
                    "fats": 6,
                    "allergens": ["dairy"]
                },
                {
                    "name": "Protein Smoothie Bowl",
                    "calories": 310,
                    "protein": 25,
                    "carbs": 38,
                    "fats": 8,
                    "allergens": ["dairy"]
                },
                {
                    "name": "Avocado Toast with Poached Eggs",
                    "calories": 380,
                    "protein": 16,
                    "carbs": 35,
                    "fats": 20,
                    "allergens": ["eggs", "gluten"]
                }
            ],
            "lunch": [
                {
                    "name": "Grilled Chicken Salad with Quinoa",
                    "calories": 450,
                    "protein": 38,
                    "carbs": 42,
                    "fats": 14,
                    "allergens": []
                },
                {
                    "name": "Salmon with Sweet Potato and Asparagus",
                    "calories": 520,
                    "protein": 35,
                    "carbs": 48,
                    "fats": 18,
                    "allergens": ["seafood"]
                },
                {
                    "name": "Turkey and Veggie Wrap",
                    "calories": 420,
                    "protein": 32,
                    "carbs": 45,
                    "fats": 12,
                    "allergens": ["gluten"]
                },
                {
                    "name": "Lentil Soup with Whole Grain Bread",
                    "calories": 380,
                    "protein": 18,
                    "carbs": 62,
                    "fats": 6,
                    "allergens": ["gluten"]
                },
                {
                    "name": "Chicken Stir-Fry with Brown Rice",
                    "calories": 480,
                    "protein": 36,
                    "carbs": 52,
                    "fats": 14,
                    "allergens": ["soy"]
                }
            ],
            "dinner": [
                {
                    "name": "Lean Beef with Roasted Vegetables",
                    "calories": 510,
                    "protein": 42,
                    "carbs": 38,
                    "fats": 20,
                    "allergens": []
                },
                {
                    "name": "Baked Cod with Quinoa and Broccoli",
                    "calories": 440,
                    "protein": 38,
                    "carbs": 45,
                    "fats": 12,
                    "allergens": ["seafood"]
                },
                {
                    "name": "Grilled Chicken Breast with Wild Rice",
                    "calories": 480,
                    "protein": 45,
                    "carbs": 48,
                    "fats": 10,
                    "allergens": []
                },
                {
                    "name": "Vegetarian Buddha Bowl",
                    "calories": 420,
                    "protein": 16,
                    "carbs": 62,
                    "fats": 14,
                    "allergens": []
                },
                {
                    "name": "Turkey Meatballs with Whole Wheat Pasta",
                    "calories": 495,
                    "protein": 38,
                    "carbs": 54,
                    "fats": 14,
                    "allergens": ["gluten", "eggs"]
                }
            ],
            "snacks": [
                {
                    "name": "Apple with Almond Butter",
                    "calories": 180,
                    "protein": 4,
                    "carbs": 22,
                    "fats": 9,
                    "allergens": ["nuts"]
                },
                {
                    "name": "Protein Bar",
                    "calories": 200,
                    "protein": 20,
                    "carbs": 18,
                    "fats": 6,
                    "allergens": ["nuts", "dairy"]
                },
                {
                    "name": "Carrot Sticks with Hummus",
                    "calories": 120,
                    "protein": 4,
                    "carbs": 16,
                    "fats": 5,
                    "allergens": []
                },
                {
                    "name": "Greek Yogurt with Honey",
                    "calories": 150,
                    "protein": 12,
                    "carbs": 20,
                    "fats": 2,
                    "allergens": ["dairy"]
                },
                {
                    "name": "Mixed Nuts (30g)",
                    "calories": 170,
                    "protein": 6,
                    "carbs": 8,
                    "fats": 14,
                    "allergens": ["nuts"]
                }
            ]
        }
    
    def calculate_bmr(self, weight: float, height: float, age: int, gender: str) -> float:
        """
        Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation
        
        Args:
            weight: Weight in kilograms
            height: Height in centimeters
            age: Age in years
            gender: 'male' or 'female'
        
        Returns:
            BMR in kcal/day
        
        Mifflin-St Jeor Equation:
        Men: BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) + 5
        Women: BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) - 161
        """
        bmr = (10 * weight) + (6.25 * height) - (5 * age)
        
        if gender.lower() == 'male':
            bmr += 5
        else:  # female
            bmr -= 161
        
        return round(bmr, 1)
    
    def calculate_tdee(self, bmr: float, activity_level: str = "moderately_active") -> float:
        """
        Calculate Total Daily Energy Expenditure
        
        Args:
            bmr: Basal Metabolic Rate
            activity_level: Activity level category
        
        Returns:
            TDEE in kcal/day
        """
        multiplier = self.activity_levels.get(activity_level, 1.55)
        tdee = bmr * multiplier
        return round(tdee, 1)
    
    def determine_calorie_target(self, tdee: float, goal: str) -> Dict[str, Any]:
        """
        Determine daily calorie target based on user's goal
        
        Args:
            tdee: Total Daily Energy Expenditure
            goal: User's fitness goal
        
        Returns:
            Dictionary with target calories and timeline
        """
        goal_lower = goal.lower()
        
        # Parse goal for weight change amount
        if 'lose' in goal_lower or 'cut' in goal_lower:
            # Weight loss: 500 kcal deficit = ~0.5 kg/week
            target_calories = tdee - 500
            weekly_change = -0.5
            goal_type = "weight_loss"
        elif 'gain' in goal_lower or 'bulk' in goal_lower:
            # Weight gain: 500 kcal surplus = ~0.5 kg/week
            target_calories = tdee + 500
            weekly_change = 0.5
            goal_type = "weight_gain"
        elif 'maintain' in goal_lower:
            # Maintenance
            target_calories = tdee
            weekly_change = 0
            goal_type = "maintenance"
        else:
            # Default to maintenance
            target_calories = tdee
            weekly_change = 0
            goal_type = "maintenance"
        
        # Extract target weight change if specified
        import re
        weight_match = re.search(r'(\d+\.?\d*)\s*kg', goal_lower)
        target_weight_change = float(weight_match.group(1)) if weight_match else 5
        
        # Calculate timeline (weeks)
        if weekly_change != 0:
            weeks_needed = abs(target_weight_change / weekly_change)
            timeline = f"{int(weeks_needed)} weeks ({int(weeks_needed/4)} months)"
        else:
            timeline = "Ongoing maintenance"
        
        return {
            "target_calories": round(target_calories, 0),
            "weekly_change": weekly_change,
            "goal_type": goal_type,
            "timeline": timeline,
            "target_weight_change": target_weight_change
        }
    
    def calculate_macro_targets(self, target_calories: float, goal_type: str) -> Dict[str, float]:
        """
        Calculate macronutrient targets based on calorie goal
        
        Args:
            target_calories: Daily calorie target
            goal_type: Type of fitness goal
        
        Returns:
            Dictionary with protein, carbs, and fats in grams
        
        Macro distributions:
        - Weight loss: 40% protein, 30% carbs, 30% fats
        - Weight gain: 30% protein, 40% carbs, 30% fats
        - Maintenance: 30% protein, 40% carbs, 30% fats
        """
        if goal_type == "weight_loss":
            protein_ratio, carbs_ratio, fats_ratio = 0.40, 0.30, 0.30
        elif goal_type == "weight_gain":
            protein_ratio, carbs_ratio, fats_ratio = 0.30, 0.40, 0.30
        else:  # maintenance
            protein_ratio, carbs_ratio, fats_ratio = 0.30, 0.40, 0.30
        
        # Convert calories to grams (protein: 4 kcal/g, carbs: 4 kcal/g, fats: 9 kcal/g)
        protein_grams = (target_calories * protein_ratio) / 4
        carbs_grams = (target_calories * carbs_ratio) / 4
        fats_grams = (target_calories * fats_ratio) / 9
        
        return {
            "protein": round(protein_grams, 1),
            "carbs": round(carbs_grams, 1),
            "fats": round(fats_grams, 1)
        }
    
    def filter_meals_by_allergies(self, meal_category: str, allergies: str) -> List[Dict]:
        """
        Filter meals to exclude allergens
        
        Args:
            meal_category: Category of meal (breakfast, lunch, dinner, snacks)
            allergies: User's allergies
        
        Returns:
            Filtered list of safe meals
        """
        if not allergies or allergies.lower() == 'none':
            return self.meal_database[meal_category]
        
        allergy_list = [a.strip().lower() for a in allergies.split(',')]
        
        safe_meals = []
        for meal in self.meal_database[meal_category]:
            meal_allergens = [a.lower() for a in meal.get('allergens', [])]
            
            # Check if any user allergies are in meal allergens
            has_allergen = any(allergy in meal_allergens for allergy in allergy_list)
            
            if not has_allergen:
                safe_meals.append(meal)
        
        return safe_meals if safe_meals else self.meal_database[meal_category]
    
    def generate_daily_plan(self, target_calories: float, allergies: str = None) -> Dict[str, Any]:
        """
        Generate a balanced daily meal plan
        
        Args:
            target_calories: Daily calorie target
            allergies: User's allergies
        
        Returns:
            Complete daily meal plan
        """
        # Typical calorie distribution: Breakfast 20%, Lunch 35%, Dinner 35%, Snacks 10%
        breakfast_target = target_calories * 0.20
        lunch_target = target_calories * 0.35
        dinner_target = target_calories * 0.35
        snacks_target = target_calories * 0.10
        
        # Select meals closest to targets
        breakfast_options = self.filter_meals_by_allergies('breakfast', allergies)
        lunch_options = self.filter_meals_by_allergies('lunch', allergies)
        dinner_options = self.filter_meals_by_allergies('dinner', allergies)
        snacks_options = self.filter_meals_by_allergies('snacks', allergies)
        
        breakfast = min(breakfast_options, key=lambda x: abs(x['calories'] - breakfast_target))
        lunch = min(lunch_options, key=lambda x: abs(x['calories'] - lunch_target))
        dinner = min(dinner_options, key=lambda x: abs(x['calories'] - dinner_target))
        snacks = min(snacks_options, key=lambda x: abs(x['calories'] - snacks_target))
        
        # Calculate daily totals
        total_calories = breakfast['calories'] + lunch['calories'] + dinner['calories'] + snacks['calories']
        total_protein = breakfast['protein'] + lunch['protein'] + dinner['protein'] + snacks['protein']
        total_carbs = breakfast['carbs'] + lunch['carbs'] + dinner['carbs'] + snacks['carbs']
        total_fats = breakfast['fats'] + lunch['fats'] + dinner['fats'] + snacks['fats']
        
        return {
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner,
            "snacks": snacks,
            "total_calories": total_calories,
            "macros": {
                "protein": round(total_protein, 1),
                "carbs": round(total_carbs, 1),
                "fats": round(total_fats, 1)
            }
        }
    
    def generate_weekly_plan(self, target_calories: float, allergies: str = None) -> List[Dict]:
        """
        Generate a 7-day meal plan with variety
        
        Args:
            target_calories: Daily calorie target
            allergies: User's allergies
        
        Returns:
            List of 7 daily meal plans
        """
        weekly_plan = []
        used_meals = {
            'breakfast': set(),
            'lunch': set(),
            'dinner': set(),
            'snacks': set()
        }
        
        for day in range(7):
            # Generate daily plan with variety
            daily_plan = self.generate_daily_plan(target_calories, allergies)
            
            # Try to ensure variety (no repeated meals within 3 days)
            attempts = 0
            while attempts < 10:
                needs_regeneration = False
                
                for meal_type in ['breakfast', 'lunch', 'dinner', 'snacks']:
                    meal_name = daily_plan[meal_type]['name']
                    if meal_name in used_meals[meal_type]:
                        needs_regeneration = True
                        break
                
                if not needs_regeneration:
                    break
                
                daily_plan = self.generate_daily_plan(target_calories, allergies)
                attempts += 1
            
            # Track used meals
            for meal_type in ['breakfast', 'lunch', 'dinner', 'snacks']:
                used_meals[meal_type].add(daily_plan[meal_type]['name'])
                # Clear old meals (keep variety window to 3 days)
                if len(used_meals[meal_type]) > 3:
                    used_meals[meal_type].clear()
            
            weekly_plan.append(daily_plan)
        
        return weekly_plan
    
    def generate_motivation_message(self, goal_type: str, timeline: str) -> str:
        """
        Generate motivational message based on user's goal
        """
        messages = {
            "weight_loss": [
                "💪 Remember: Sustainable weight loss is a journey, not a race. Stay consistent!",
                "🌟 Every healthy choice you make brings you closer to your goal!",
                "🎯 Focus on progress, not perfection. You've got this!"
            ],
            "weight_gain": [
                "💪 Building muscle takes time and consistency. Keep up the great work!",
                "🌟 Fuel your body properly and the gains will follow!",
                "🎯 Consistency in nutrition and training is key to your success!"
            ],
            "maintenance": [
                "💪 Maintaining a healthy lifestyle is a victory in itself!",
                "🌟 You're doing great! Keep up these healthy habits!",
                "🎯 Consistency is the foundation of long-term health!"
            ]
        }
        
        return random.choice(messages.get(goal_type, messages["maintenance"]))
    
    def generate_meal_plan(self, user_data: Dict, meal_analysis: Dict = None) -> Dict[str, Any]:
        """
        Main function to generate complete personalized meal plan
        
        Args:
            user_data: User's personal data (weight, height, age, gender, goal, allergies)
            meal_analysis: Optional current meal analysis from image
        
        Returns:
            Complete personalized dietary plan
        """
        # Extract user data
        weight = user_data.get('weight', 70)  # default 70kg
        height = user_data.get('height', 170)  # default 170cm
        age = user_data.get('age', 30)  # default 30 years
        gender = user_data.get('gender', 'male')
        goal = user_data.get('goal', 'maintain weight')
        allergies = user_data.get('allergies', 'none')
        activity_level = user_data.get('activity_level', 'moderately_active')
        
        # Calculate BMR and TDEE
        bmr = self.calculate_bmr(weight, height, age, gender)
        tdee = self.calculate_tdee(bmr, activity_level)
        
        # Determine calorie target based on goal
        calorie_info = self.determine_calorie_target(tdee, goal)
        target_calories = calorie_info['target_calories']
        
        # Calculate macro targets
        macro_targets = self.calculate_macro_targets(target_calories, calorie_info['goal_type'])
        
        # Generate 7-day meal plan
        weekly_plan = self.generate_weekly_plan(target_calories, allergies)
        
        # Generate motivation message
        motivation = self.generate_motivation_message(
            calorie_info['goal_type'], 
            calorie_info['timeline']
        )
        
        # Compile complete plan
        complete_plan = {
            "success": True,
            "bmr": bmr,
            "tdee": tdee,
            "recommended_calories": target_calories,
            "macro_targets": macro_targets,
            "weekly_plan": weekly_plan,
            "estimated_timeline": calorie_info['timeline'],
            "weekly_weight_change": f"{calorie_info['weekly_change']:+.1f} kg/week",
            "motivation_message": motivation,
            "generated_at": datetime.now().isoformat()
        }
        
        # Add current meal context if provided
        if meal_analysis:
            complete_plan["current_meal_analysis"] = meal_analysis
        
        return complete_plan


# Flask API wrapper for n8n integration
if __name__ == "__main__":
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    planner = DietaryPlanner()
    
    @app.route('/generate-meal-plan', methods=['POST'])
    def generate_meal_plan():
        """
        API endpoint for meal plan generation
        
        Expected JSON payload:
        {
            "user_data": {
                "weight": 75,
                "height": 175,
                "age": 30,
                "gender": "male",
                "goal": "lose 5kg",
                "allergies": "nuts",
                "activity_level": "moderately_active"
            },
            "meal_analysis": {
                "total_calories": 650,
                "macros": {...}
            }
        }
        """
        data = request.json
        
        user_data = data.get('user_data', {})
        meal_analysis = data.get('meal_analysis', None)
        
        if not user_data:
            return jsonify({
                "success": False,
                "error": "Missing user_data"
            }), 400
        
        results = planner.generate_meal_plan(user_data, meal_analysis)
        
        return jsonify(results)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({"status": "healthy", "service": "dietary_planner"})
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5001, debug=False)

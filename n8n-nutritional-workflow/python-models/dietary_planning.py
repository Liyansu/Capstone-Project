"""
Advanced Dietary Planning and Nutritional Analysis Module
This module provides comprehensive dietary planning algorithms including BMR/TDEE calculations,
meal plan generation, and nutritional optimization.
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ActivityLevel(Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

@dataclass
class UserProfile:
    """User profile containing all dietary and health information."""
    weight: float  # kg
    height: float  # cm
    age: int
    gender: Gender
    activity_level: ActivityLevel
    allergies: List[str]
    goals: str
    medical_conditions: List[str] = None
    dietary_restrictions: List[str] = None
    target_weight: Optional[float] = None
    timeline_weeks: Optional[int] = None

@dataclass
class NutritionalGoals:
    """Daily nutritional targets for the user."""
    calories: int
    protein: float  # grams
    carbs: float    # grams
    fat: float      # grams
    fiber: float    # grams
    sugar: float    # grams
    sodium: float   # mg

@dataclass
class Meal:
    """Individual meal with nutritional breakdown."""
    name: str
    calories: int
    protein: float
    carbs: float
    fat: float
    fiber: float
    foods: List[str]
    preparation_time: int = 15  # minutes
    difficulty: str = "easy"    # easy, medium, hard

class DietaryPlanner:
    """
    Advanced dietary planning system with comprehensive nutritional analysis.
    """
    
    def __init__(self):
        self.activity_multipliers = {
            ActivityLevel.SEDENTARY: 1.2,
            ActivityLevel.LIGHT: 1.375,
            ActivityLevel.MODERATE: 1.55,
            ActivityLevel.ACTIVE: 1.725,
            ActivityLevel.VERY_ACTIVE: 1.9
        }
        
        # Comprehensive food database with nutritional information
        self.food_database = self._initialize_food_database()
        
        # Meal templates for different meal types
        self.meal_templates = self._initialize_meal_templates()
    
    def calculate_bmr(self, profile: UserProfile) -> float:
        """
        Calculate Basal Metabolic Rate using Mifflin-St Jeor equation.
        
        Args:
            profile: User profile with weight, height, age, gender
            
        Returns:
            BMR in calories per day
        """
        if profile.gender == Gender.MALE:
            bmr = 10 * profile.weight + 6.25 * profile.height - 5 * profile.age + 5
        elif profile.gender == Gender.FEMALE:
            bmr = 10 * profile.weight + 6.25 * profile.height - 5 * profile.age - 161
        else:
            # Average of male and female formulas for non-binary individuals
            male_bmr = 10 * profile.weight + 6.25 * profile.height - 5 * profile.age + 5
            female_bmr = 10 * profile.weight + 6.25 * profile.height - 5 * profile.age - 161
            bmr = (male_bmr + female_bmr) / 2
        
        return round(bmr, 1)
    
    def calculate_tdee(self, profile: UserProfile) -> float:
        """
        Calculate Total Daily Energy Expenditure.
        
        Args:
            profile: User profile with BMR and activity level
            
        Returns:
            TDEE in calories per day
        """
        bmr = self.calculate_bmr(profile)
        multiplier = self.activity_multipliers[profile.activity_level]
        tdee = bmr * multiplier
        return round(tdee, 1)
    
    def determine_caloric_goal(self, profile: UserProfile) -> int:
        """
        Determine daily caloric goal based on user's weight goals.
        
        Args:
            profile: User profile with goals and current weight
            
        Returns:
            Target daily calories
        """
        tdee = self.calculate_tdee(profile)
        
        # Analyze goals to determine caloric adjustment
        goals_lower = profile.goals.lower()
        
        if any(keyword in goals_lower for keyword in ['lose', 'weight loss', 'reduce']):
            # Weight loss: 500-1000 calorie deficit
            if 'aggressive' in goals_lower or 'fast' in goals_lower:
                deficit = 1000
            else:
                deficit = 500
            return max(int(tdee - deficit), 1200)  # Minimum 1200 calories
        
        elif any(keyword in goals_lower for keyword in ['gain', 'weight gain', 'bulk', 'muscle']):
            # Weight gain: 300-500 calorie surplus
            if 'aggressive' in goals_lower or 'fast' in goals_lower:
                surplus = 500
            else:
                surplus = 300
            return int(tdee + surplus)
        
        elif any(keyword in goals_lower for keyword in ['maintain', 'maintenance']):
            # Weight maintenance
            return int(tdee)
        
        else:
            # Default to maintenance
            return int(tdee)
    
    def calculate_macronutrient_goals(self, caloric_goal: int, profile: UserProfile) -> NutritionalGoals:
        """
        Calculate optimal macronutrient distribution based on goals and profile.
        
        Args:
            caloric_goal: Daily caloric target
            profile: User profile
            
        Returns:
            Nutritional goals object
        """
        goals_lower = profile.goals.lower()
        
        # Adjust macronutrient ratios based on goals
        if any(keyword in goals_lower for keyword in ['muscle', 'strength', 'bulk']):
            # Higher protein for muscle building
            protein_ratio = 0.35
            carb_ratio = 0.40
            fat_ratio = 0.25
        elif any(keyword in goals_lower for keyword in ['lose', 'weight loss', 'cut']):
            # Higher protein for satiety and muscle preservation
            protein_ratio = 0.30
            carb_ratio = 0.35
            fat_ratio = 0.35
        elif any(keyword in goals_lower for keyword in ['endurance', 'cardio', 'running']):
            # Higher carbs for endurance
            protein_ratio = 0.25
            carb_ratio = 0.50
            fat_ratio = 0.25
        else:
            # Balanced macronutrients
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
        
        # Calculate other nutrients
        fiber_grams = max(25, profile.weight * 0.4)  # 0.4g per kg body weight
        sugar_grams = min(50, caloric_goal * 0.10 / 4)  # Max 10% of calories from sugar
        sodium_mg = 2300  # Recommended daily limit
        
        return NutritionalGoals(
            calories=caloric_goal,
            protein=round(protein_grams, 1),
            carbs=round(carb_grams, 1),
            fat=round(fat_grams, 1),
            fiber=round(fiber_grams, 1),
            sugar=round(sugar_grams, 1),
            sodium=sodium_mg
        )
    
    def generate_meal_plan(self, profile: UserProfile, nutritional_goals: NutritionalGoals) -> Dict[str, Dict[str, Meal]]:
        """
        Generate a comprehensive 7-day meal plan.
        
        Args:
            profile: User profile
            nutritional_goals: Daily nutritional targets
            
        Returns:
            7-day meal plan with breakfast, lunch, dinner, snacks
        """
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        meal_plan = {}
        
        for day in days:
            meal_plan[day] = {
                'breakfast': self._generate_breakfast(profile, nutritional_goals),
                'lunch': self._generate_lunch(profile, nutritional_goals),
                'dinner': self._generate_dinner(profile, nutritional_goals),
                'snacks': self._generate_snacks(profile, nutritional_goals)
            }
        
        return meal_plan
    
    def _generate_breakfast(self, profile: UserProfile, goals: NutritionalGoals) -> Meal:
        """Generate breakfast meal."""
        breakfast_options = [
            {
                'name': 'Protein Oatmeal Bowl',
                'foods': ['Oatmeal', 'Greek yogurt', 'Berries', 'Almonds', 'Honey'],
                'calories': int(goals.calories * 0.25),
                'protein': goals.protein * 0.25,
                'carbs': goals.carbs * 0.25,
                'fat': goals.fat * 0.25,
                'fiber': goals.fiber * 0.30
            },
            {
                'name': 'Avocado Toast with Eggs',
                'foods': ['Whole grain bread', 'Avocado', 'Eggs', 'Tomato', 'Spinach'],
                'calories': int(goals.calories * 0.25),
                'protein': goals.protein * 0.30,
                'carbs': goals.carbs * 0.20,
                'fat': goals.fat * 0.35,
                'fiber': goals.fiber * 0.25
            },
            {
                'name': 'Smoothie Bowl',
                'foods': ['Banana', 'Greek yogurt', 'Protein powder', 'Granola', 'Chia seeds'],
                'calories': int(goals.calories * 0.25),
                'protein': goals.protein * 0.35,
                'carbs': goals.carbs * 0.30,
                'fat': goals.fat * 0.20,
                'fiber': goals.fiber * 0.25
            }
        ]
        
        # Select breakfast based on user preferences and restrictions
        selected = self._select_meal_option(breakfast_options, profile)
        return Meal(**selected)
    
    def _generate_lunch(self, profile: UserProfile, goals: NutritionalGoals) -> Meal:
        """Generate lunch meal."""
        lunch_options = [
            {
                'name': 'Grilled Chicken Salad',
                'foods': ['Chicken breast', 'Mixed greens', 'Cherry tomatoes', 'Cucumber', 'Olive oil dressing'],
                'calories': int(goals.calories * 0.35),
                'protein': goals.protein * 0.40,
                'carbs': goals.carbs * 0.20,
                'fat': goals.fat * 0.30,
                'fiber': goals.fiber * 0.35
            },
            {
                'name': 'Quinoa Buddha Bowl',
                'foods': ['Quinoa', 'Roasted vegetables', 'Chickpeas', 'Tahini dressing', 'Hemp seeds'],
                'calories': int(goals.calories * 0.35),
                'protein': goals.protein * 0.25,
                'carbs': goals.carbs * 0.45,
                'fat': goals.fat * 0.30,
                'fiber': goals.fiber * 0.40
            },
            {
                'name': 'Salmon with Sweet Potato',
                'foods': ['Salmon fillet', 'Sweet potato', 'Broccoli', 'Lemon', 'Herbs'],
                'calories': int(goals.calories * 0.35),
                'protein': goals.protein * 0.35,
                'carbs': goals.carbs * 0.35,
                'fat': goals.fat * 0.30,
                'fiber': goals.fiber * 0.30
            }
        ]
        
        selected = self._select_meal_option(lunch_options, profile)
        return Meal(**selected)
    
    def _generate_dinner(self, profile: UserProfile, goals: NutritionalGoals) -> Meal:
        """Generate dinner meal."""
        dinner_options = [
            {
                'name': 'Turkey Meatballs with Pasta',
                'foods': ['Ground turkey', 'Whole wheat pasta', 'Marinara sauce', 'Parmesan cheese', 'Basil'],
                'calories': int(goals.calories * 0.30),
                'protein': goals.protein * 0.35,
                'carbs': goals.carbs * 0.40,
                'fat': goals.fat * 0.25,
                'fiber': goals.fiber * 0.30
            },
            {
                'name': 'Baked Cod with Vegetables',
                'foods': ['Cod fillet', 'Roasted vegetables', 'Brown rice', 'Lemon butter', 'Dill'],
                'calories': int(goals.calories * 0.30),
                'protein': goals.protein * 0.40,
                'carbs': goals.carbs * 0.35,
                'fat': goals.fat * 0.25,
                'fiber': goals.fiber * 0.35
            },
            {
                'name': 'Vegetarian Stir-fry',
                'foods': ['Tofu', 'Mixed vegetables', 'Brown rice', 'Soy sauce', 'Sesame oil'],
                'calories': int(goals.calories * 0.30),
                'protein': goals.protein * 0.30,
                'carbs': goals.carbs * 0.45,
                'fat': goals.fat * 0.25,
                'fiber': goals.fiber * 0.40
            }
        ]
        
        selected = self._select_meal_option(dinner_options, profile)
        return Meal(**selected)
    
    def _generate_snacks(self, profile: UserProfile, goals: NutritionalGoals) -> Meal:
        """Generate snack options."""
        snack_options = [
            {
                'name': 'Apple with Almond Butter',
                'foods': ['Apple', 'Almond butter', 'Cinnamon'],
                'calories': int(goals.calories * 0.10),
                'protein': goals.protein * 0.10,
                'carbs': goals.carbs * 0.15,
                'fat': goals.fat * 0.15,
                'fiber': goals.fiber * 0.20
            },
            {
                'name': 'Greek Yogurt Parfait',
                'foods': ['Greek yogurt', 'Berries', 'Granola', 'Honey'],
                'calories': int(goals.calories * 0.10),
                'protein': goals.protein * 0.20,
                'carbs': goals.carbs * 0.10,
                'fat': goals.fat * 0.10,
                'fiber': goals.fiber * 0.15
            },
            {
                'name': 'Protein Smoothie',
                'foods': ['Protein powder', 'Banana', 'Milk', 'Spinach', 'Peanut butter'],
                'calories': int(goals.calories * 0.10),
                'protein': goals.protein * 0.25,
                'carbs': goals.carbs * 0.10,
                'fat': goals.fat * 0.10,
                'fiber': goals.fiber * 0.15
            }
        ]
        
        selected = self._select_meal_option(snack_options, profile)
        return Meal(**selected)
    
    def _select_meal_option(self, options: List[Dict], profile: UserProfile) -> Dict:
        """Select the best meal option based on user profile and restrictions."""
        # Filter options based on allergies and dietary restrictions
        filtered_options = []
        
        for option in options:
            is_suitable = True
            
            # Check for allergens
            for food in option['foods']:
                for allergy in profile.allergies:
                    if allergy.lower() in food.lower():
                        is_suitable = False
                        break
                if not is_suitable:
                    break
            
            # Check for dietary restrictions
            if profile.dietary_restrictions:
                for restriction in profile.dietary_restrictions:
                    if restriction.lower() == 'vegetarian':
                        meat_keywords = ['chicken', 'beef', 'pork', 'turkey', 'fish', 'salmon', 'cod']
                        if any(meat in ' '.join(option['foods']).lower() for meat in meat_keywords):
                            is_suitable = False
                            break
                    elif restriction.lower() == 'vegan':
                        animal_keywords = ['milk', 'cheese', 'yogurt', 'eggs', 'honey', 'butter']
                        if any(animal in ' '.join(option['foods']).lower() for animal in animal_keywords):
                            is_suitable = False
                            break
            
            if is_suitable:
                filtered_options.append(option)
        
        # If no suitable options found, return the first option with a warning
        if not filtered_options:
            return options[0]
        
        # Select based on user goals
        goals_lower = profile.goals.lower()
        
        if any(keyword in goals_lower for keyword in ['muscle', 'protein']):
            # Prefer higher protein options
            return max(filtered_options, key=lambda x: x['protein'])
        elif any(keyword in goals_lower for keyword in ['weight loss', 'low carb']):
            # Prefer lower carb options
            return min(filtered_options, key=lambda x: x['carbs'])
        else:
            # Return first suitable option
            return filtered_options[0]
    
    def generate_safety_warnings(self, profile: UserProfile, meal_plan: Dict) -> List[Dict]:
        """Generate safety warnings based on allergies and dietary restrictions."""
        warnings = []
        
        if not profile.allergies:
            return warnings
        
        # Comprehensive allergen database
        allergen_keywords = {
            'nuts': ['almond', 'walnut', 'peanut', 'cashew', 'pistachio', 'hazelnut', 'pecan'],
            'dairy': ['milk', 'cheese', 'yogurt', 'butter', 'cream', 'whey', 'casein'],
            'gluten': ['wheat', 'bread', 'pasta', 'flour', 'oats', 'barley', 'rye'],
            'eggs': ['egg', 'mayonnaise', 'custard', 'meringue', 'albumin'],
            'soy': ['soy', 'tofu', 'tempeh', 'soy sauce', 'miso', 'edamame'],
            'fish': ['salmon', 'tuna', 'cod', 'fish', 'anchovy', 'sardine'],
            'shellfish': ['shrimp', 'crab', 'lobster', 'shellfish', 'mussel', 'clam'],
            'sesame': ['sesame', 'tahini', 'sesame oil'],
            'sulfites': ['wine', 'dried fruit', 'processed foods']
        }
        
        for allergy in profile.allergies:
            allergy_lower = allergy.lower()
            keywords = allergen_keywords.get(allergy_lower, [allergy_lower])
            found_allergens = []
            
            # Check all meals in the plan
            for day, meals in meal_plan.items():
                for meal_type, meal in meals.items():
                    for food in meal.foods:
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
    
    def calculate_progress_metrics(self, current_meal: Dict, nutritional_goals: NutritionalGoals) -> Dict:
        """Calculate progress metrics for the current meal."""
        current_calories = current_meal.get('totalCalories', 0)
        current_protein = current_meal.get('totalProtein', 0)
        current_carbs = current_meal.get('totalCarbs', 0)
        current_fat = current_meal.get('totalFat', 0)
        
        return {
            'currentMealCalories': current_calories,
            'dailyCalorieGoal': nutritional_goals.calories,
            'remainingCalories': nutritional_goals.calories - current_calories,
            'proteinProgress': (current_protein / nutritional_goals.protein) * 100,
            'carbProgress': (current_carbs / nutritional_goals.carbs) * 100,
            'fatProgress': (current_fat / nutritional_goals.fat) * 100,
            'calorieProgress': (current_calories / nutritional_goals.calories) * 100
        }
    
    def _initialize_food_database(self) -> Dict:
        """Initialize comprehensive food database."""
        # This would typically load from a comprehensive database like USDA FoodData Central
        return {
            # Protein sources
            'chicken_breast': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0},
            'salmon': {'calories': 208, 'protein': 25, 'carbs': 0, 'fat': 12, 'fiber': 0},
            'eggs': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11, 'fiber': 0},
            'greek_yogurt': {'calories': 59, 'protein': 10, 'carbs': 3.6, 'fat': 0.4, 'fiber': 0},
            'tofu': {'calories': 76, 'protein': 8, 'carbs': 1.9, 'fat': 4.8, 'fiber': 0.3},
            
            # Carbohydrate sources
            'brown_rice': {'calories': 111, 'protein': 2.3, 'carbs': 23, 'fat': 0.9, 'fiber': 1.8},
            'quinoa': {'calories': 120, 'protein': 4.4, 'carbs': 22, 'fat': 1.9, 'fiber': 2.8},
            'sweet_potato': {'calories': 86, 'protein': 1.6, 'carbs': 20, 'fat': 0.1, 'fiber': 3},
            'oats': {'calories': 68, 'protein': 2.4, 'carbs': 12, 'fat': 1.4, 'fiber': 1.7},
            
            # Vegetables
            'broccoli': {'calories': 34, 'protein': 2.8, 'carbs': 6.6, 'fat': 0.4, 'fiber': 2.6},
            'spinach': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4, 'fiber': 2.2},
            'carrots': {'calories': 41, 'protein': 0.9, 'carbs': 10, 'fat': 0.2, 'fiber': 2.8},
            
            # Fruits
            'apple': {'calories': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2, 'fiber': 2.4},
            'banana': {'calories': 89, 'protein': 1.1, 'carbs': 23, 'fat': 0.3, 'fiber': 2.6},
            'berries': {'calories': 57, 'protein': 0.7, 'carbs': 14, 'fat': 0.3, 'fiber': 2.4},
            
            # Fats
            'avocado': {'calories': 160, 'protein': 2, 'carbs': 9, 'fat': 15, 'fiber': 7},
            'almonds': {'calories': 579, 'protein': 21, 'carbs': 22, 'fat': 50, 'fiber': 12},
            'olive_oil': {'calories': 884, 'protein': 0, 'carbs': 0, 'fat': 100, 'fiber': 0}
        }
    
    def _initialize_meal_templates(self) -> Dict:
        """Initialize meal templates for different dietary preferences."""
        return {
            'breakfast': [
                'Protein Oatmeal Bowl',
                'Avocado Toast with Eggs',
                'Smoothie Bowl',
                'Greek Yogurt Parfait',
                'Chia Pudding'
            ],
            'lunch': [
                'Grilled Chicken Salad',
                'Quinoa Buddha Bowl',
                'Salmon with Sweet Potato',
                'Turkey Wrap',
                'Vegetable Soup'
            ],
            'dinner': [
                'Turkey Meatballs with Pasta',
                'Baked Cod with Vegetables',
                'Vegetarian Stir-fry',
                'Grilled Steak with Roasted Vegetables',
                'Lentil Curry'
            ],
            'snacks': [
                'Apple with Almond Butter',
                'Greek Yogurt Parfait',
                'Protein Smoothie',
                'Hummus with Vegetables',
                'Mixed Nuts'
            ]
        }


# Example usage and testing
if __name__ == "__main__":
    # Create a sample user profile
    profile = UserProfile(
        weight=70.0,
        height=175.0,
        age=30,
        gender=Gender.FEMALE,
        activity_level=ActivityLevel.MODERATE,
        allergies=['nuts', 'dairy'],
        goals='lose 5kg in 8 weeks',
        dietary_restrictions=['vegetarian']
    )
    
    # Initialize dietary planner
    planner = DietaryPlanner()
    
    # Calculate BMR and TDEE
    bmr = planner.calculate_bmr(profile)
    tdee = planner.calculate_tdee(profile)
    caloric_goal = planner.determine_caloric_goal(profile)
    
    print(f"BMR: {bmr} calories/day")
    print(f"TDEE: {tdee} calories/day")
    print(f"Caloric Goal: {caloric_goal} calories/day")
    
    # Calculate nutritional goals
    nutritional_goals = planner.calculate_macronutrient_goals(caloric_goal, profile)
    print(f"\\nNutritional Goals:")
    print(f"Protein: {nutritional_goals.protein}g")
    print(f"Carbs: {nutritional_goals.carbs}g")
    print(f"Fat: {nutritional_goals.fat}g")
    print(f"Fiber: {nutritional_goals.fiber}g")
    
    # Generate meal plan
    meal_plan = planner.generate_meal_plan(profile, nutritional_goals)
    
    # Generate safety warnings
    warnings = planner.generate_safety_warnings(profile, meal_plan)
    if warnings:
        print("\\nSafety Warnings:")
        for warning in warnings:
            print(f"- {warning['allergen']}: {warning['recommendation']}")
    
    # Example current meal analysis
    current_meal = {
        'totalCalories': 400,
        'totalProtein': 25,
        'totalCarbs': 30,
        'totalFat': 15
    }
    
    progress = planner.calculate_progress_metrics(current_meal, nutritional_goals)
    print(f"\\nProgress Metrics:")
    print(f"Calorie Progress: {progress['calorieProgress']:.1f}%")
    print(f"Protein Progress: {progress['proteinProgress']:.1f}%")
    print(f"Carb Progress: {progress['carbProgress']:.1f}%")
    print(f"Fat Progress: {progress['fatProgress']:.1f}%")
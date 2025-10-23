"""
Unit tests for Dietary Planner
"""

import pytest
from dietary_planner import DietaryPlanner


class TestDietaryPlanner:
    """Test suite for DietaryPlanner class"""
    
    @pytest.fixture
    def planner(self):
        """Create DietaryPlanner instance for testing"""
        return DietaryPlanner()
    
    def test_initialization(self, planner):
        """Test that planner initializes correctly"""
        assert planner is not None
        assert planner.meal_database is not None
        assert planner.activity_levels is not None
        assert len(planner.meal_database) == 4  # breakfast, lunch, dinner, snacks
    
    def test_calculate_bmr_male(self, planner):
        """Test BMR calculation for male"""
        # Male: 30 years, 75kg, 175cm
        bmr = planner.calculate_bmr(75, 175, 30, 'male')
        
        # Expected: (10 * 75) + (6.25 * 175) - (5 * 30) + 5 = 1,698.75
        assert 1690 <= bmr <= 1710
        assert isinstance(bmr, float)
    
    def test_calculate_bmr_female(self, planner):
        """Test BMR calculation for female"""
        # Female: 30 years, 65kg, 165cm
        bmr = planner.calculate_bmr(65, 165, 30, 'female')
        
        # Expected: (10 * 65) + (6.25 * 165) - (5 * 30) - 161 = 1,370.25
        assert 1360 <= bmr <= 1380
        assert isinstance(bmr, float)
    
    def test_calculate_tdee(self, planner):
        """Test TDEE calculation"""
        bmr = 1700
        
        # Test different activity levels
        tdee_sedentary = planner.calculate_tdee(bmr, 'sedentary')
        tdee_moderate = planner.calculate_tdee(bmr, 'moderately_active')
        tdee_very_active = planner.calculate_tdee(bmr, 'very_active')
        
        assert tdee_sedentary == 1700 * 1.2
        assert tdee_moderate == 1700 * 1.55
        assert tdee_very_active == 1700 * 1.725
        
        # Verify TDEE increases with activity
        assert tdee_sedentary < tdee_moderate < tdee_very_active
    
    def test_determine_calorie_target_weight_loss(self, planner):
        """Test calorie target for weight loss goal"""
        tdee = 2500
        goal = "lose 5kg"
        
        result = planner.determine_calorie_target(tdee, goal)
        
        assert result['target_calories'] == 2000  # 500 cal deficit
        assert result['weekly_change'] == -0.5
        assert result['goal_type'] == 'weight_loss'
        assert 'timeline' in result
    
    def test_determine_calorie_target_weight_gain(self, planner):
        """Test calorie target for weight gain goal"""
        tdee = 2500
        goal = "gain 8kg"
        
        result = planner.determine_calorie_target(tdee, goal)
        
        assert result['target_calories'] == 3000  # 500 cal surplus
        assert result['weekly_change'] == 0.5
        assert result['goal_type'] == 'weight_gain'
    
    def test_determine_calorie_target_maintenance(self, planner):
        """Test calorie target for maintenance"""
        tdee = 2500
        goal = "maintain weight"
        
        result = planner.determine_calorie_target(tdee, goal)
        
        assert result['target_calories'] == 2500
        assert result['weekly_change'] == 0
        assert result['goal_type'] == 'maintenance'
    
    def test_calculate_macro_targets_weight_loss(self, planner):
        """Test macro calculation for weight loss"""
        target_calories = 2000
        
        macros = planner.calculate_macro_targets(target_calories, 'weight_loss')
        
        # Weight loss: 40% protein, 30% carbs, 30% fats
        expected_protein = (2000 * 0.40) / 4  # 200g
        expected_carbs = (2000 * 0.30) / 4    # 150g
        expected_fats = (2000 * 0.30) / 9     # ~66.7g
        
        assert abs(macros['protein'] - expected_protein) < 1
        assert abs(macros['carbs'] - expected_carbs) < 1
        assert abs(macros['fats'] - expected_fats) < 1
    
    def test_calculate_macro_targets_weight_gain(self, planner):
        """Test macro calculation for weight gain"""
        target_calories = 3000
        
        macros = planner.calculate_macro_targets(target_calories, 'weight_gain')
        
        # Weight gain: 30% protein, 40% carbs, 30% fats
        expected_protein = (3000 * 0.30) / 4  # 225g
        expected_carbs = (3000 * 0.40) / 4    # 300g
        expected_fats = (3000 * 0.30) / 9     # 100g
        
        assert abs(macros['protein'] - expected_protein) < 1
        assert abs(macros['carbs'] - expected_carbs) < 1
        assert abs(macros['fats'] - expected_fats) < 1
    
    def test_filter_meals_by_allergies_none(self, planner):
        """Test meal filtering with no allergies"""
        meals = planner.filter_meals_by_allergies('breakfast', 'none')
        
        # Should return all breakfast meals
        assert len(meals) == len(planner.meal_database['breakfast'])
    
    def test_filter_meals_by_allergies_nuts(self, planner):
        """Test meal filtering with nut allergy"""
        all_breakfasts = planner.meal_database['breakfast']
        safe_breakfasts = planner.filter_meals_by_allergies('breakfast', 'nuts')
        
        # Should have fewer meals (filtering out those with nuts)
        # Or same if no meals contain nuts
        assert len(safe_breakfasts) <= len(all_breakfasts)
        
        # Verify no nuts in filtered meals
        for meal in safe_breakfasts:
            allergens = [a.lower() for a in meal.get('allergens', [])]
            assert 'nuts' not in allergens
    
    def test_filter_meals_by_allergies_multiple(self, planner):
        """Test meal filtering with multiple allergies"""
        safe_meals = planner.filter_meals_by_allergies('lunch', 'dairy, seafood')
        
        for meal in safe_meals:
            allergens = [a.lower() for a in meal.get('allergens', [])]
            assert 'dairy' not in allergens
            assert 'seafood' not in allergens
    
    def test_generate_daily_plan(self, planner):
        """Test daily meal plan generation"""
        target_calories = 2000
        
        daily_plan = planner.generate_daily_plan(target_calories, 'none')
        
        # Check structure
        assert 'breakfast' in daily_plan
        assert 'lunch' in daily_plan
        assert 'dinner' in daily_plan
        assert 'snacks' in daily_plan
        assert 'total_calories' in daily_plan
        assert 'macros' in daily_plan
        
        # Check each meal has required fields
        for meal_type in ['breakfast', 'lunch', 'dinner', 'snacks']:
            meal = daily_plan[meal_type]
            assert 'name' in meal
            assert 'calories' in meal
            assert 'protein' in meal
            assert 'carbs' in meal
            assert 'fats' in meal
        
        # Check total calories is close to target (within 20%)
        assert 0.8 * target_calories <= daily_plan['total_calories'] <= 1.2 * target_calories
    
    def test_generate_daily_plan_respects_allergies(self, planner):
        """Test that daily plan respects allergies"""
        daily_plan = planner.generate_daily_plan(2000, 'seafood')
        
        # Check no seafood in any meal
        for meal_type in ['breakfast', 'lunch', 'dinner', 'snacks']:
            meal = daily_plan[meal_type]
            # Get the full meal data from database to check allergens
            found = False
            for db_meal in planner.meal_database[meal_type]:
                if db_meal['name'] == meal['name']:
                    allergens = [a.lower() for a in db_meal.get('allergens', [])]
                    assert 'seafood' not in allergens
                    found = True
                    break
    
    def test_generate_weekly_plan(self, planner):
        """Test weekly meal plan generation"""
        target_calories = 2200
        
        weekly_plan = planner.generate_weekly_plan(target_calories, 'none')
        
        # Should have 7 days
        assert len(weekly_plan) == 7
        
        # Each day should have complete structure
        for day in weekly_plan:
            assert 'breakfast' in day
            assert 'lunch' in day
            assert 'dinner' in day
            assert 'snacks' in day
            assert 'total_calories' in day
            assert 'macros' in day
    
    def test_generate_weekly_plan_variety(self, planner):
        """Test that weekly plan has variety"""
        weekly_plan = planner.generate_weekly_plan(2000, 'none')
        
        # Collect all breakfast names
        breakfast_names = [day['breakfast']['name'] for day in weekly_plan]
        
        # Should have some variety (not all the same)
        unique_breakfasts = len(set(breakfast_names))
        assert unique_breakfasts > 1  # At least 2 different breakfasts
    
    def test_generate_motivation_message(self, planner):
        """Test motivation message generation"""
        msg_loss = planner.generate_motivation_message('weight_loss', '10 weeks')
        msg_gain = planner.generate_motivation_message('weight_gain', '8 weeks')
        msg_maint = planner.generate_motivation_message('maintenance', 'Ongoing')
        
        assert isinstance(msg_loss, str)
        assert isinstance(msg_gain, str)
        assert isinstance(msg_maint, str)
        assert len(msg_loss) > 0
        assert len(msg_gain) > 0
        assert len(msg_maint) > 0
    
    def test_generate_meal_plan_complete(self, planner):
        """Test complete meal plan generation"""
        user_data = {
            'weight': 75,
            'height': 175,
            'age': 30,
            'gender': 'male',
            'goal': 'lose 5kg',
            'allergies': 'none',
            'activity_level': 'moderately_active'
        }
        
        plan = planner.generate_meal_plan(user_data)
        
        # Check all required fields
        assert plan['success'] is True
        assert 'bmr' in plan
        assert 'tdee' in plan
        assert 'recommended_calories' in plan
        assert 'macro_targets' in plan
        assert 'weekly_plan' in plan
        assert 'estimated_timeline' in plan
        assert 'weekly_weight_change' in plan
        assert 'motivation_message' in plan
        
        # Verify calculations
        assert plan['bmr'] > 0
        assert plan['tdee'] > plan['bmr']
        assert len(plan['weekly_plan']) == 7
    
    def test_generate_meal_plan_with_defaults(self, planner):
        """Test meal plan generation with missing data (uses defaults)"""
        user_data = {}  # Empty data
        
        plan = planner.generate_meal_plan(user_data)
        
        # Should still generate plan with defaults
        assert plan['success'] is True
        assert plan['bmr'] > 0
        assert len(plan['weekly_plan']) == 7


class TestMealDatabase:
    """Test meal database content"""
    
    @pytest.fixture
    def planner(self):
        return DietaryPlanner()
    
    def test_all_meal_types_present(self, planner):
        """Test all meal types are in database"""
        required_types = ['breakfast', 'lunch', 'dinner', 'snacks']
        
        for meal_type in required_types:
            assert meal_type in planner.meal_database
            assert len(planner.meal_database[meal_type]) > 0
    
    def test_meals_have_required_fields(self, planner):
        """Test all meals have required fields"""
        required_fields = ['name', 'calories', 'protein', 'carbs', 'fats', 'allergens']
        
        for meal_type, meals in planner.meal_database.items():
            for meal in meals:
                for field in required_fields:
                    assert field in meal, f"{meal['name']} missing {field}"
    
    def test_nutrition_values_valid(self, planner):
        """Test all nutrition values are valid"""
        for meal_type, meals in planner.meal_database.items():
            for meal in meals:
                assert meal['calories'] > 0
                assert meal['protein'] >= 0
                assert meal['carbs'] >= 0
                assert meal['fats'] >= 0
                
                # Test macro calories sum approximately equals total calories
                macro_calories = (meal['protein'] * 4) + (meal['carbs'] * 4) + (meal['fats'] * 9)
                # Allow 10% variance
                assert 0.9 * meal['calories'] <= macro_calories <= 1.1 * meal['calories'], \
                    f"{meal['name']} macro calories don't match total"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

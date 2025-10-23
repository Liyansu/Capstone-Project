# Quick Start Guide

Get up and running with the N8N Nutritional Planning Workflow in 5 minutes!

## ⚡ Prerequisites

- Python 3.8+ installed
- n8n installed (or access to n8n cloud)
- Telegram account
- 10 minutes of your time

## 🚀 5-Minute Setup

### Step 1: Create Telegram Bot (2 minutes)

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow prompts to name your bot
4. Copy the bot token (looks like: `1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ`)
5. Save this token - you'll need it!

### Step 2: Setup Python Services (2 minutes)

```bash
# Clone or navigate to the workflow directory
cd n8n-nutritional-workflow

# Run setup script
chmod +x setup.sh
./setup.sh

# Edit .env file with your bot token
cd python-services
nano .env  # or use your favorite editor

# Add your token:
# TELEGRAM_BOT_TOKEN=your_token_here

# Start services
source venv/bin/activate
python service_launcher.py
```

### Step 3: Import n8n Workflow (1 minute)

1. Open your n8n instance
2. Click **Workflows** → **Import from File**
3. Select `nutritional-planning-workflow.json`
4. In the Telegram nodes, add your credentials:
   - Name: `Telegram Account`
   - Access Token: `your_bot_token_here`
5. Click **Save** and **Activate** the workflow

## ✅ Test It!

1. Open Telegram and find your bot
2. Send a photo of a meal with this text:

```
weight: 75kg, height: 175cm, age: 30, gender: male, allergies: none, goal: lose 5kg
```

3. Wait ~10 seconds for your personalized nutrition plan!

## 🎯 Example Input

**Photo:** [Any food photo - chicken, rice, vegetables, etc.]

**Text:**
```
weight: 80kg, height: 180cm, age: 28, gender: male, allergies: nuts, goal: lose 10kg
```

## 📱 Expected Output

You'll receive a message like:

```
🍽️ **NUTRITIONAL ANALYSIS COMPLETE** 🍽️

📸 **Current Meal Analysis:**
- Detected Foods: Chicken Breast, White Rice, Broccoli
- Estimated Calories: 650 kcal
- Protein: 55g, Carbs: 70g, Fats: 12g

📊 **Your Metabolic Profile:**
- BMR: 1,850 kcal/day
- TDEE: 2,867 kcal/day
- Recommended Daily Intake: 2,367 kcal/day

📅 **Your 7-Day Personalized Meal Plan:**

**Day 1 (2,350 kcal)**
🌅 Breakfast: Oatmeal with Berries (350 kcal)
🌞 Lunch: Grilled Chicken Salad with Quinoa (450 kcal)
🌙 Dinner: Lean Beef with Roasted Vegetables (510 kcal)
🍎 Snacks: Greek Yogurt with Honey (150 kcal)
📈 Macros - P: 180g, C: 240g, F: 65g

[Days 2-7...]

💪 **Progress Tracking Tips:**
- Goal: lose 10kg
- Estimated Timeline: 20 weeks (5 months)
- Weekly Weight Change: -0.5 kg/week

✨ **Motivation:**
Remember: Sustainable weight loss is a journey, not a race!
```

## 🐛 Troubleshooting

### Bot doesn't respond?
- Check that Python services are running (`python service_launcher.py`)
- Verify n8n workflow is **activated**
- Check that TELEGRAM_BOT_TOKEN is set correctly

### "Can't download photo" error?
- Ensure photo is attached
- Check bot token is valid
- Try a smaller photo (< 5MB)

### Services won't start?
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt

# Check for port conflicts
lsof -i :5000
lsof -i :5001
```

## 🎓 Next Steps

1. **Read the full documentation:** `README.md`
2. **Understand the workflow:** `WORKFLOW_GUIDE.md`
3. **Explore the architecture:** `ARCHITECTURE.md`
4. **Customize meals:** Edit `dietary_planner.py` meal database
5. **Add your own ML models:** Replace placeholder models in `food_image_analyzer.py`

## 💡 Tips for Best Results

1. **Take clear photos** - well-lit, focused on the food
2. **Use the exact format** for your measurements
3. **Be honest** about your activity level
4. **Set realistic goals** - 0.5-1kg per week is sustainable
5. **Update your info** regularly as you progress

## 📊 Understanding Your Results

### BMR (Basal Metabolic Rate)
- Calories you burn at rest
- Based on age, weight, height, gender

### TDEE (Total Daily Energy Expenditure)
- Total calories you burn daily
- BMR × activity multiplier

### Calorie Target
- **Weight Loss:** TDEE - 500 (lose ~0.5kg/week)
- **Weight Gain:** TDEE + 500 (gain ~0.5kg/week)
- **Maintenance:** TDEE

### Macros
- **Protein:** Building & repairing muscles
- **Carbs:** Primary energy source
- **Fats:** Hormones, vitamins, energy

## 🎯 Input Format Reference

```
weight: [number]kg, 
height: [number]cm, 
age: [number], 
gender: male/female, 
allergies: [list or 'none'], 
goal: [your goal]
```

**Examples:**
```
weight: 65kg, height: 165cm, age: 25, gender: female, allergies: dairy, goal: maintain weight
```

```
weight: 90kg, height: 185cm, age: 35, gender: male, allergies: none, goal: lose 15kg
```

```
weight: 60kg, height: 170cm, age: 22, gender: female, allergies: gluten, seafood, goal: gain 5kg
```

## 🌟 Pro Tips

1. **Meal Timing:** The plan doesn't specify timing - adjust to your schedule
2. **Flexibility:** Swap similar meals if you don't like an option
3. **Hydration:** Drink 2-3L water daily (not in the plan, but crucial!)
4. **Activity:** Plans assume moderate activity - adjust if you're more/less active
5. **Consistency:** Follow the plan for at least 2-3 weeks to see results

## 📞 Need Help?

- Check `README.md` for detailed documentation
- Review `WORKFLOW_GUIDE.md` for technical details
- See `ARCHITECTURE.md` for system architecture

## 🎉 You're All Set!

Start your nutritional journey today! Send a photo and your details to your Telegram bot.

**Remember:** This tool is for educational and informational purposes. Consult with a healthcare professional before making significant dietary changes.

Happy tracking! 🍽️💪

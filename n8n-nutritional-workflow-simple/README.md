# N8N Nutritional Planning Workflow - Simple Version

This is a simplified version of the n8n nutritional planning workflow that can be directly imported and used.

## Files Included

1. **`workflow.json`** - Complete n8n workflow that can be imported directly
2. **`main.py`** - Python FastAPI service for food recognition and dietary planning
3. **`requirements.txt`** - Python dependencies

## Quick Setup

### 1. Import n8n Workflow
1. Open your n8n instance
2. Go to Workflows → Import from File
3. Select the `workflow.json` file
4. Click Import

### 2. Set Up Python Service
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Python service:
   ```bash
   python main.py
   ```

3. The service will be available at `http://localhost:8000`

### 3. Configure Environment Variables
Set these environment variables in n8n:
- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token

### 4. Set Up Telegram Bot
1. Create a bot via @BotFather on Telegram
2. Set the webhook URL: `https://your-n8n-instance.com/webhook/nutritional-planning`

## Usage

Send a message to your Telegram bot with:
1. A photo of your meal
2. Text with your dietary information in this format:
   ```
   Weight: 70kg, Height: 175cm, Age: 30, Gender: female, Activity: moderate, Allergies: nuts, Goals: lose 5kg
   ```

## Features

- **Food Recognition**: Identifies foods in photos (mock implementation)
- **Dietary Planning**: Generates personalized 7-day meal plans
- **BMR/TDEE Calculation**: Calculates metabolic rates
- **Safety Warnings**: Checks for allergens
- **Progress Tracking**: Monitors nutritional goals

## API Endpoints

- `POST /recognize-foods` - Analyze food photos
- `POST /generate-meal-plan` - Generate meal plans
- `POST /analyze-meal` - Analyze specific meals
- `GET /food-database` - Get food database
- `GET /health` - Health check

## Customization

You can customize the food database in `main.py` by modifying the `FOOD_DATABASE` dictionary.

For production use, replace the mock food recognition with actual computer vision APIs like Hugging Face, AWS SageMaker, or Google Vision API.
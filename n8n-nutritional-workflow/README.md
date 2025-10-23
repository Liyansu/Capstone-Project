# N8N Nutritional Planning Workflow

A comprehensive n8n automation workflow for personalized nutritional planning that integrates Telegram API, computer vision for food recognition, and advanced dietary planning algorithms.

## 🚀 Features

- **Telegram Integration**: Receive food photos and dietary information via Telegram
- **AI-Powered Food Recognition**: Computer vision analysis for food identification and calorie estimation
- **Personalized Meal Planning**: 7-day customized dietary plans based on user metrics
- **Metabolic Calculations**: BMR and TDEE calculations for accurate caloric needs
- **Safety Features**: Allergy detection and dietary warnings
- **Progress Tracking**: Real-time nutritional progress monitoring

## 📋 Workflow Components

### 1. Telegram Webhook Node
- Receives photos and text messages from users
- Extracts dietary measurements (weight, height, age, allergies, goals)
- Validates input data format

### 2. Food Recognition & Calorie Estimation
- Processes uploaded food images
- Identifies food items using computer vision
- Estimates portion sizes and nutritional content
- Calculates macronutrient breakdown

### 3. Dietary Planning Algorithm
- Calculates BMR using Mifflin-St Jeor equation
- Determines TDEE based on activity level
- Generates personalized 7-day meal plans
- Provides macronutrient distribution (40% carbs, 30% protein, 30% fat)

### 4. Output Generation
- Structured 7-day meal plans (Breakfast, Lunch, Dinner, Snacks)
- Current meal nutritional analysis
- BMR and TDEE calculations
- Safety warnings for allergies
- Progress tracking metrics

### 5. Telegram Response
- Sends formatted nutritional plan back to user
- Includes motivational tips and success strategies

## 🛠️ Setup Instructions

### Prerequisites
- n8n instance (self-hosted or cloud)
- Telegram Bot Token
- Computer Vision API access (Hugging Face, AWS SageMaker, or Google Vision)

### Environment Variables
Create a `.env` file with the following variables:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
HUGGING_FACE_API_KEY=your_hugging_face_api_key_here
# OR
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
# OR
GOOGLE_APPLICATION_CREDENTIALS=path_to_google_credentials.json
```

### Installation Steps

1. **Import the Workflow**
   - Open your n8n instance
   - Go to Workflows → Import from File
   - Select the `workflow.json` file

2. **Configure Telegram Bot**
   - Create a bot via @BotFather on Telegram
   - Set the webhook URL: `https://your-n8n-instance.com/webhook/nutritional-planning`
   - Copy the bot token to your environment variables

3. **Set up Computer Vision API**
   - Choose one of the supported APIs:
     - **Hugging Face**: Sign up at huggingface.co and get API key
     - **AWS SageMaker**: Set up AWS account and SageMaker endpoint
     - **Google Vision**: Enable Vision API in Google Cloud Console

4. **Update API Integration**
   - Modify the "Food Recognition & Calorie Estimation" node
   - Replace mock data with actual API calls
   - Update authentication headers and endpoints

5. **Test the Workflow**
   - Send a photo with dietary info to your Telegram bot
   - Format: "Weight: 70kg, Height: 175cm, Age: 30, Allergies: nuts, Goals: lose 5kg"

## 📊 Data Flow

```
Telegram Message → Parse Data → Download Photo → Food Recognition → Dietary Planning → Format Response → Send to User
```

### Input Format
Users should send messages in this format:
```
[Photo of meal]

Weight: 70kg, Height: 175cm, Age: 30, Gender: female, Activity: moderate, Allergies: nuts, dairy, Goals: lose 5kg
```

### Output Format
The workflow generates:
- **7-Day Meal Plan**: Detailed daily meal breakdown
- **Current Meal Analysis**: Nutritional content of photographed meal
- **Metabolic Profile**: BMR and TDEE calculations
- **Safety Warnings**: Allergy alerts and dietary recommendations
- **Progress Tracking**: Daily nutritional goals and current progress

## 🔧 Customization

### Adding New Food Recognition Models
1. Update the "Food Recognition & Calorie Estimation" node
2. Add API calls to your preferred model
3. Map model outputs to standardized nutritional data

### Modifying Meal Plans
1. Edit the `generateMealPlan()` function in the "Dietary Planning Algorithm" node
2. Add new food databases or meal templates
3. Adjust macronutrient ratios as needed

### Adding New Safety Features
1. Extend the `generateSafetyWarnings()` function
2. Add new allergen detection patterns
3. Include dietary restriction checks

## 📈 Advanced Features

### Machine Learning Integration
- **Food Recognition**: Use fine-tuned ResNet, YOLO, or Vision Transformers
- **Portion Estimation**: Computer vision for accurate serving sizes
- **Nutritional Analysis**: Deep learning models for macro/micronutrient prediction

### Database Integration
- Store user profiles and meal history
- Track progress over time
- Generate personalized recommendations

### Multi-language Support
- Add translation nodes for international users
- Localize food databases and meal plans
- Support regional dietary preferences

## 🚨 Safety Considerations

- **Allergy Detection**: Comprehensive allergen checking
- **Medical Disclaimer**: Include appropriate disclaimers
- **Data Privacy**: Secure handling of personal health data
- **Accuracy Warnings**: Note limitations of AI estimations

## 📝 API Specifications

### Food Recognition API
```javascript
// Input: Base64 encoded image
// Output: Array of identified foods with nutritional data
{
  "identifiedFoods": [
    {
      "name": "grilled chicken breast",
      "confidence": 0.92,
      "estimatedWeight": 150,
      "calories": 231,
      "protein": 43.5,
      "carbs": 0,
      "fat": 5.0,
      "fiber": 0
    }
  ],
  "totalCalories": 376,
  "totalProtein": 48.6,
  "totalCarbs": 29.6,
  "totalFat": 6.3,
  "totalFiber": 4.4
}
```

### Dietary Planning Output
```javascript
{
  "bmr": 1650,
  "tdee": 2558,
  "caloricGoal": 2058,
  "macronutrientGoals": {
    "protein": 154.4,
    "carbs": 205.8,
    "fat": 68.6
  },
  "mealPlan": { /* 7-day meal plan */ },
  "safetyWarnings": [ /* allergy warnings */ ],
  "progressMetrics": { /* current progress */ }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the n8n documentation

## 🔄 Version History

- **v1.0.0**: Initial release with basic food recognition and meal planning
- **v1.1.0**: Added allergy detection and safety warnings
- **v1.2.0**: Enhanced progress tracking and user metrics
- **v1.3.0**: Improved meal plan generation and customization options
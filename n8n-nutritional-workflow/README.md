# N8N Nutritional Planning Workflow

A comprehensive automation workflow for personalized nutritional planning using n8n, Telegram, and AI-powered food recognition.

## 📋 Overview

This workflow provides:
- **Telegram-based interface** for user interaction
- **AI-powered food recognition** from meal photos
- **Calorie and macro estimation** using computer vision
- **Personalized 7-day meal plans** based on user goals
- **BMR and TDEE calculations** for accurate nutritional planning
- **Allergy detection and warnings** for food safety
- **Progress tracking and motivation** features

## 🏗️ Architecture

### Workflow Components

```
┌─────────────────┐
│  Telegram Bot   │
│  (User Input)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Parse User Data │
│  (Photo + Text) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Download Photo │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Food Image Analysis     │
│ (Python/CV Service)     │
│ - Food Recognition      │
│ - Calorie Estimation    │
│ - Allergen Detection    │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Dietary Plan Generator  │
│ (Python Service)        │
│ - BMR/TDEE Calculation  │
│ - 7-Day Meal Planning   │
│ - Macro Distribution    │
└────────┬────────────────┘
         │
         ▼
┌─────────────────┐
│ Format Response │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Send to Telegram│
└─────────────────┘
```

## 🚀 Getting Started

### Prerequisites

1. **n8n instance** (self-hosted or cloud)
2. **Telegram Bot Token** (from @BotFather)
3. **Python 3.8+** environment for services
4. **GPU-enabled machine** (recommended for CV models)

### Installation

#### 1. Setup Python Services

```bash
# Navigate to python services directory
cd n8n-nutritional-workflow/python-services

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Configure Environment Variables

Create `.env` file in the python-services directory:

```bash
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Service Configuration
PYTHON_SERVICE_URL=http://localhost:5000
DIETARY_SERVICE_URL=http://localhost:5001

# Model Configuration (Optional - for production)
FOOD_MODEL_PATH=/path/to/food_recognition_model.pth
PORTION_MODEL_PATH=/path/to/portion_estimation_model.pth

# Database Configuration (Optional)
NUTRITION_DB_URL=postgresql://user:pass@localhost/nutrition_db
```

#### 3. Import n8n Workflow

1. Open your n8n instance
2. Go to **Workflows** → **Import from File**
3. Select `nutritional-planning-workflow.json`
4. Configure Telegram credentials:
   - Add your Telegram Bot Token in the Telegram Trigger node
   - Add your Telegram Bot Token in the Telegram nodes

#### 4. Start Python Services

```bash
# Terminal 1: Start Food Image Analyzer
python food_image_analyzer.py

# Terminal 2: Start Dietary Planner
python dietary_planner.py
```

Or use the combined launcher:

```bash
python service_launcher.py
```

## 📱 Usage

### User Input Format

Send a message to your Telegram bot with:

1. **A photo** of your meal
2. **Text with your details** in the following format:

```
weight: 75kg, height: 175cm, age: 30, gender: male, allergies: nuts, goal: lose 5kg
```

**Example:**
```
Attached: [Photo of chicken with rice and broccoli]
Caption: weight: 80kg, height: 180cm, age: 28, gender: male, allergies: none, goal: lose 10kg
```

### Expected Response

The bot will reply with:

```
🍽️ **NUTRITIONAL ANALYSIS COMPLETE** 🍽️

📸 **Current Meal Analysis:**
- Detected Foods: Chicken Breast, White Rice, Broccoli
- Estimated Calories: 650 kcal
- Protein: 55g
- Carbs: 70g
- Fats: 12g

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

[... Days 2-7 ...]

💪 **Progress Tracking Tips:**
- Goal: lose 10kg
- Estimated Timeline: 20 weeks (5 months)
- Weekly Weight Change: -0.5 kg/week

✨ **Motivation:**
Remember: Sustainable weight loss is a journey, not a race. Stay consistent!
```

## 🔧 Technical Details

### Data Flow Between Nodes

#### 1. Telegram Trigger → Parse User Input
```json
{
  "message": {
    "chat": {"id": 123456789},
    "from": {"id": 123456789},
    "photo": [{"file_id": "AgACAgIAAx..."}],
    "caption": "weight: 75kg, height: 175cm, age: 30, gender: male, allergies: nuts, goal: lose 5kg"
  }
}
```

#### 2. Parse User Input → Download Photo
```json
{
  "chatId": 123456789,
  "userId": 123456789,
  "photoFileId": "AgACAgIAAx...",
  "weight": 75,
  "height": 175,
  "age": 30,
  "gender": "male",
  "allergies": "nuts",
  "goal": "lose 5kg"
}
```

#### 3. Food Image Analysis Output
```json
{
  "success": true,
  "detected_foods": ["Chicken Breast", "White Rice", "Broccoli"],
  "total_calories": 650,
  "macros": {
    "protein": 55,
    "carbs": 70,
    "fats": 12
  },
  "food_details": [...],
  "allergy_warnings": ["⚠️ Chicken may contain traces of..."],
  "confidence_scores": {...}
}
```

#### 4. Dietary Plan Output
```json
{
  "success": true,
  "bmr": 1850,
  "tdee": 2867,
  "recommended_calories": 2367,
  "macro_targets": {
    "protein": 177,
    "carbs": 237,
    "fats": 66
  },
  "weekly_plan": [
    {
      "breakfast": {...},
      "lunch": {...},
      "dinner": {...},
      "snacks": {...},
      "total_calories": 2350,
      "macros": {...}
    }
  ],
  "estimated_timeline": "20 weeks (5 months)",
  "weekly_weight_change": "-0.5 kg/week",
  "motivation_message": "..."
}
```

## 🤖 Computer Vision Models

### Recommended Models for Production

#### Food Recognition
- **YOLOv8** fine-tuned on Food-101 dataset
- **EfficientNet-B4** for food classification
- **ResNet50** for multi-food detection

#### Calorie Estimation
- **Nutrition5k** dataset models
- **Food2k** for portion estimation
- **Depth estimation models** (MiDaS, DPT)

### Model Training Pipeline

```python
# Pseudo-code for training food recognition model
from torchvision import models, datasets, transforms

# Load pre-trained model
model = models.efficientnet_b4(pretrained=True)

# Fine-tune on Food-101 dataset
dataset = datasets.Food101(root='./data', download=True, transform=transform)

# Training loop
for epoch in range(num_epochs):
    train(model, dataset)
    evaluate(model, test_dataset)
    
# Save model
torch.save(model.state_dict(), 'food_classifier.pth')
```

### Integration with Hugging Face

For easier deployment, use Hugging Face Inference API:

```python
import requests

API_URL = "https://api-inference.huggingface.co/models/nateraw/food"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def query(image_bytes):
    response = requests.post(API_URL, headers=headers, data=image_bytes)
    return response.json()
```

## 🔬 BMR & TDEE Calculations

### Basal Metabolic Rate (BMR)
Uses **Mifflin-St Jeor Equation**:

**For Men:**
```
BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age) + 5
```

**For Women:**
```
BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age) - 161
```

### Total Daily Energy Expenditure (TDEE)
```
TDEE = BMR × Activity Factor
```

**Activity Factors:**
- Sedentary (little/no exercise): 1.2
- Lightly active (1-3 days/week): 1.375
- Moderately active (3-5 days/week): 1.55
- Very active (6-7 days/week): 1.725
- Extremely active (athlete): 1.9

### Calorie Targets

**Weight Loss:**
- Deficit: 500 kcal/day = ~0.5 kg/week loss
- Target: TDEE - 500

**Weight Gain:**
- Surplus: 500 kcal/day = ~0.5 kg/week gain
- Target: TDEE + 500

**Maintenance:**
- Target: TDEE

## 📊 Macronutrient Distribution

### Weight Loss (40/30/30)
- Protein: 40% of calories
- Carbs: 30% of calories
- Fats: 30% of calories

### Weight Gain (30/40/30)
- Protein: 30% of calories
- Carbs: 40% of calories
- Fats: 30% of calories

### Maintenance (30/40/30)
- Protein: 30% of calories
- Carbs: 40% of calories
- Fats: 30% of calories

## 🛡️ Allergen Detection

The system checks for common allergens:
- Nuts (peanuts, almonds, cashews, walnuts)
- Dairy (milk, cheese, yogurt, butter)
- Gluten (wheat, bread, pasta)
- Seafood (fish, shellfish)
- Eggs
- Soy

Warnings are displayed when detected foods contain user's allergens.

## 🔒 Security Considerations

1. **API Keys**: Store in environment variables, never in code
2. **User Data**: Implement GDPR-compliant data handling
3. **Rate Limiting**: Add rate limits to prevent abuse
4. **Input Validation**: Sanitize all user inputs
5. **Image Processing**: Limit file sizes and formats

## 📈 Scaling to Production

### Deployment Options

#### Option 1: Docker Deployment
```bash
docker-compose up -d
```

#### Option 2: Kubernetes
```bash
kubectl apply -f k8s/deployment.yaml
```

#### Option 3: Cloud Functions
- Deploy services as AWS Lambda / Google Cloud Functions
- Use serverless architecture for cost efficiency

### Performance Optimization

1. **Model Optimization**
   - Use ONNX for faster inference
   - Quantize models to reduce size
   - Use TensorRT for GPU acceleration

2. **Caching**
   - Cache nutrition database queries
   - Implement Redis for session management

3. **Load Balancing**
   - Deploy multiple service instances
   - Use NGINX for load balancing

## 🧪 Testing

Run unit tests:
```bash
pytest tests/
```

Run integration tests:
```bash
pytest tests/integration/
```

## 📝 API Documentation

### Food Image Analyzer API

**Endpoint:** `POST /analyze-food-image`

**Request:**
```json
{
  "image_url": "telegram_file_path",
  "telegram_file_id": "AgACAgIAAx...",
  "user_allergies": "nuts, dairy"
}
```

**Response:**
```json
{
  "success": true,
  "detected_foods": ["Chicken Breast", "Rice"],
  "total_calories": 650,
  "macros": {
    "protein": 55,
    "carbs": 70,
    "fats": 12
  },
  "allergy_warnings": []
}
```

### Dietary Planner API

**Endpoint:** `POST /generate-meal-plan`

**Request:**
```json
{
  "user_data": {
    "weight": 75,
    "height": 175,
    "age": 30,
    "gender": "male",
    "goal": "lose 5kg",
    "allergies": "nuts"
  },
  "meal_analysis": {
    "total_calories": 650,
    "macros": {...}
  }
}
```

**Response:**
```json
{
  "success": true,
  "bmr": 1850,
  "tdee": 2867,
  "recommended_calories": 2367,
  "weekly_plan": [...]
}
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Food-101 Dataset** for food recognition training
- **USDA FoodData Central** for nutrition data
- **n8n Community** for automation platform
- **PyTorch** and **Hugging Face** for ML infrastructure

## 📞 Support

For issues and questions:
- GitHub Issues: [link]
- Email: support@example.com
- Documentation: [link]

## 🗺️ Roadmap

- [ ] Add support for meal prep recommendations
- [ ] Integrate with fitness trackers (Fitbit, Apple Health)
- [ ] Multi-language support
- [ ] Restaurant menu analysis
- [ ] Grocery list generation
- [ ] Recipe suggestions
- [ ] Social features (meal sharing)
- [ ] Progress visualization dashboard

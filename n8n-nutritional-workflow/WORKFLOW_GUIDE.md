# N8N Nutritional Workflow - Complete Guide

## 🎯 Workflow Node Breakdown

### Node 1: Telegram Trigger
**Type:** `n8n-nodes-base.telegramTrigger`

**Purpose:** Listens for incoming messages from Telegram users

**Configuration:**
- Updates: `message`
- Webhook ID: `nutritional-bot`

**Output Data Structure:**
```javascript
{
  message: {
    chat: { id: number },
    from: { id: number },
    photo: [{ file_id: string }],
    caption: string,
    text: string
  }
}
```

---

### Node 2: Parse User Input
**Type:** `n8n-nodes-base.code`

**Purpose:** Extract and structure user data from message

**Function Code:**
- Extracts photo file ID (largest version)
- Parses text for dietary measurements
- Uses regex to extract: weight, height, age, gender, allergies, goal

**Input:** Telegram message object

**Output Data Structure:**
```javascript
{
  chatId: number,
  userId: number,
  photoFileId: string,
  messageText: string,
  weight: number,        // in kg
  height: number,        // in cm
  age: number,
  gender: string,        // 'male' or 'female'
  allergies: string,     // comma-separated
  goal: string,          // e.g., 'lose 5kg'
  timestamp: string      // ISO format
}
```

**Regex Patterns:**
- Weight: `/weight[:\s]+(\d+\.?\d*)\s*kg/i`
- Height: `/height[:\s]+(\d+\.?\d*)\s*cm/i`
- Age: `/age[:\s]+(\d+)/i`
- Gender: `/gender[:\s]+(male|female)/i`
- Allergies: `/allergies[:\s]+([^,]+)/i`
- Goal: `/goal[:\s]+(.+?)(?:,|$)/i`

---

### Node 3: Download Food Photo
**Type:** `n8n-nodes-base.telegram`

**Purpose:** Download the meal photo from Telegram servers

**Configuration:**
- Operation: `getFile`
- File ID: `={{ $json.photoFileId }}`

**Output Data Structure:**
```javascript
{
  file_id: string,
  file_unique_id: string,
  file_size: number,
  file_path: string  // Path on Telegram servers
}
```

---

### Node 4: Analyze Food Image (Python)
**Type:** `n8n-nodes-base.httpRequest`

**Purpose:** Call Python service for food recognition and calorie estimation

**Configuration:**
- URL: `={{ $env.PYTHON_SERVICE_URL }}/analyze-food-image`
- Method: `POST`
- Timeout: `60000ms` (60 seconds)

**Request Body:**
```javascript
{
  image_url: string,           // Telegram file path
  telegram_file_id: string,    // File ID
  user_allergies: string       // Optional
}
```

**Response Structure:**
```javascript
{
  success: boolean,
  detected_foods: string[],
  total_calories: number,
  macros: {
    protein: number,
    carbs: number,
    fats: number
  },
  food_details: [
    {
      name: string,
      portion_grams: number,
      calories: number,
      protein: number,
      carbs: number,
      fats: number
    }
  ],
  allergy_warnings: string[],
  confidence_scores: object
}
```

**Computer Vision Pipeline:**
1. Download image from Telegram
2. Preprocess image (resize, normalize)
3. Run through food classification model
4. Detect multiple food items
5. Estimate portion sizes
6. Calculate nutrition from database
7. Check for allergens
8. Return structured results

---

### Node 5: Generate Dietary Plan (Python)
**Type:** `n8n-nodes-base.httpRequest`

**Purpose:** Generate personalized 7-day meal plan

**Configuration:**
- URL: `={{ $env.PYTHON_SERVICE_URL }}/generate-meal-plan`
- Method: `POST`
- Content Type: `application/json`
- Timeout: `60000ms`

**Request Body:**
```javascript
{
  user_data: {
    weight: number,
    height: number,
    age: number,
    gender: string,
    goal: string,
    allergies: string,
    activity_level: string
  },
  meal_analysis: {
    total_calories: number,
    macros: object
  }
}
```

**Response Structure:**
```javascript
{
  success: boolean,
  bmr: number,                    // Basal Metabolic Rate
  tdee: number,                   // Total Daily Energy Expenditure
  recommended_calories: number,   // Daily target
  macro_targets: {
    protein: number,
    carbs: number,
    fats: number
  },
  weekly_plan: [
    {
      breakfast: { name, calories, protein, carbs, fats },
      lunch: { name, calories, protein, carbs, fats },
      dinner: { name, calories, protein, carbs, fats },
      snacks: { name, calories, protein, carbs, fats },
      total_calories: number,
      macros: { protein, carbs, fats }
    }
  ],
  estimated_timeline: string,
  weekly_weight_change: string,
  motivation_message: string
}
```

**Algorithm Steps:**
1. Calculate BMR using Mifflin-St Jeor equation
2. Calculate TDEE based on activity level
3. Determine calorie target from goal
4. Calculate macro distribution
5. Generate 7-day meal plan
6. Filter meals by allergies
7. Ensure variety across days
8. Calculate timeline to goal
9. Generate motivation message

---

### Node 6: Format Response
**Type:** `n8n-nodes-base.code`

**Purpose:** Format complete response for Telegram

**Function Code:**
Builds markdown-formatted message containing:
- Current meal analysis
- BMR and TDEE
- Allergy warnings (if any)
- 7-day meal plan
- Progress tracking tips
- Motivation message

**Input:** Results from both Python services

**Output Data Structure:**
```javascript
{
  chatId: number,
  message: string,      // Markdown-formatted
  parse_mode: 'Markdown'
}
```

**Message Template:**
```
🍽️ **NUTRITIONAL ANALYSIS COMPLETE** 🍽️

📸 **Current Meal Analysis:**
- Detected Foods: [list]
- Estimated Calories: [number] kcal
- Macros: P:[g], C:[g], F:[g]

📊 **Your Metabolic Profile:**
- BMR: [number] kcal/day
- TDEE: [number] kcal/day
- Recommended: [number] kcal/day

⚠️ **ALLERGY WARNING:** (if applicable)
- [warnings]

📅 **Your 7-Day Meal Plan:**
[Daily breakdowns]

💪 **Progress Tracking:**
- Goal: [user goal]
- Timeline: [estimated]
- Weekly Change: [±kg/week]

✨ **Motivation:**
[message]
```

---

### Node 7: Send Telegram Response
**Type:** `n8n-nodes-base.telegram`

**Purpose:** Send formatted response back to user

**Configuration:**
- Operation: `sendMessage`
- Chat ID: `={{ $json.chatId }}`
- Text: `={{ $json.message }}`
- Parse Mode: `Markdown`

---

### Node 8: Send Error Message
**Type:** `n8n-nodes-base.telegram`

**Purpose:** Handle errors and guide users on correct input format

**Configuration:**
- Operation: `sendMessage`
- Triggered on workflow errors

**Message:**
```
❌ An error occurred while processing your request.

Please make sure to:
1. Include a photo of your meal
2. Provide details in this format:
   weight: XXkg, height: XXcm, age: XX, 
   gender: male/female, allergies: none, 
   goal: your fitness goal

Example:
weight: 75kg, height: 175cm, age: 30, 
gender: male, allergies: nuts, goal: lose 5kg
```

---

## 🔄 Data Flow Diagram

```
User Message
    ↓
[Photo] + [Text Data]
    ↓
Parse & Extract
    ↓
┌─────────────┐
│  Photo      │
└──────┬──────┘
       ↓
Download from Telegram
       ↓
┌──────────────────────┐
│ Food Image Analysis  │
│ • Food Recognition   │
│ • Portion Estimation │
│ • Calorie Calculation│
│ • Allergen Check     │
└──────┬───────────────┘
       │
       ├─────────────────┐
       ↓                 ↓
[Meal Analysis]  [User Data]
       │                 │
       └────────┬────────┘
                ↓
┌──────────────────────────┐
│ Dietary Plan Generator   │
│ • BMR Calculation        │
│ • TDEE Calculation       │
│ • Calorie Target         │
│ • Macro Distribution     │
│ • 7-Day Meal Planning    │
│ • Timeline Estimation    │
└──────┬───────────────────┘
       ↓
[Complete Plan]
       ↓
Format as Markdown
       ↓
Send to User via Telegram
```

---

## 📝 Environment Variables

### Required
```bash
TELEGRAM_BOT_TOKEN=your_bot_token
```

### Optional (for Python services)
```bash
PYTHON_SERVICE_URL=http://localhost:5000
FOOD_MODEL_PATH=/path/to/model.pth
USE_GPU=true
HUGGINGFACE_API_KEY=your_key
```

---

## 🧪 Testing the Workflow

### Test Case 1: Weight Loss Goal
**Input:**
```
Photo: [Chicken salad]
Text: weight: 80kg, height: 175cm, age: 28, gender: male, allergies: none, goal: lose 10kg
```

**Expected Output:**
- BMR: ~1,850 kcal
- TDEE: ~2,867 kcal (moderate activity)
- Target: ~2,367 kcal (500 deficit)
- Timeline: ~20 weeks
- Weekly change: -0.5 kg

### Test Case 2: Weight Gain Goal
**Input:**
```
Photo: [Rice and beef]
Text: weight: 65kg, height: 180cm, age: 25, gender: male, allergies: dairy, goal: gain 8kg
```

**Expected Output:**
- BMR: ~1,765 kcal
- TDEE: ~2,736 kcal
- Target: ~3,236 kcal (500 surplus)
- Timeline: ~16 weeks
- Weekly change: +0.5 kg
- No dairy in meal plan

### Test Case 3: Maintenance
**Input:**
```
Photo: [Balanced meal]
Text: weight: 70kg, height: 165cm, age: 35, gender: female, allergies: nuts, goal: maintain weight
```

**Expected Output:**
- BMR: ~1,420 kcal
- TDEE: ~2,201 kcal
- Target: ~2,201 kcal (maintenance)
- Weekly change: 0 kg
- No nuts in meal plan

---

## 🐛 Troubleshooting

### Error: "Cannot download photo"
**Solution:** Check Telegram bot token and file ID

### Error: "Python service not responding"
**Solution:** 
1. Verify Python services are running
2. Check PYTHON_SERVICE_URL environment variable
3. Test endpoint: `curl http://localhost:5000/health`

### Error: "No food detected"
**Solution:**
1. Ensure photo shows food clearly
2. Check model is loaded correctly
3. Verify image preprocessing

### Error: "Missing user data"
**Solution:** Ensure input text matches expected format

---

## 🎯 Best Practices

1. **Image Quality:** Use clear, well-lit photos
2. **Input Format:** Follow the exact format for measurements
3. **Realistic Goals:** Set achievable weight change targets
4. **Activity Level:** Provide accurate activity information
5. **Allergies:** List all allergies clearly

---

## 📊 Performance Metrics

### Expected Processing Times
- Image download: ~1-2 seconds
- Food analysis: ~3-5 seconds (CPU), ~1-2 seconds (GPU)
- Meal plan generation: ~1-2 seconds
- Total workflow: ~5-10 seconds

### Accuracy Targets
- Food recognition: >85% accuracy
- Calorie estimation: ±15% variance
- Portion estimation: ±20% variance

---

## 🚀 Optimization Tips

1. **Caching:** Cache nutrition database queries
2. **Model Optimization:** Use ONNX or TensorRT
3. **Batch Processing:** Process multiple images together
4. **Load Balancing:** Deploy multiple service instances
5. **CDN:** Use CDN for static nutrition data

---

## 📚 Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Food-101 Dataset](https://www.vision.ee.ethz.ch/datasets_extra/food-101/)
- [USDA FoodData Central](https://fdc.nal.usda.gov/)
- [PyTorch Documentation](https://pytorch.org/docs/)

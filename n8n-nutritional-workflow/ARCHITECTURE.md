# N8N Nutritional Planning Workflow - System Architecture

## 📐 System Overview

The N8N Nutritional Planning Workflow is a comprehensive automation system that combines:
- **User Interface Layer:** Telegram Bot
- **Orchestration Layer:** n8n Workflow Engine
- **Processing Layer:** Python Microservices
- **AI/ML Layer:** Computer Vision Models
- **Data Layer:** Nutrition Database

## 🏛️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER LAYER                              │
│                                                                 │
│                   ┌───────────────────┐                        │
│                   │  Telegram User    │                        │
│                   │  [Photo + Text]   │                        │
│                   └─────────┬─────────┘                        │
│                             │                                   │
└─────────────────────────────┼───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TELEGRAM API LAYER                           │
│                                                                 │
│             ┌──────────────────────────────┐                   │
│             │   Telegram Bot API           │                   │
│             │   - Receive Messages         │                   │
│             │   - Download Photos          │                   │
│             │   - Send Responses           │                   │
│             └──────────────┬───────────────┘                   │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  N8N ORCHESTRATION LAYER                        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Trigger    │→ │   Parser     │→ │  Download    │         │
│  └──────────────┘  └──────────────┘  └──────┬───────┘         │
│                                              │                  │
│                    ┌─────────────────────────┘                  │
│                    ▼                                            │
│  ┌──────────────────────────────────────────────────┐          │
│  │          HTTP Request Nodes                      │          │
│  │  ┌────────────────┐   ┌────────────────┐        │          │
│  │  │ Food Analysis  │   │ Meal Planning  │        │          │
│  │  │   Request      │   │    Request     │        │          │
│  │  └────────┬───────┘   └────────┬───────┘        │          │
│  └───────────┼──────────────────────┼───────────────┘          │
│              │                      │                           │
└──────────────┼──────────────────────┼───────────────────────────┘
               │                      │
               ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                  PYTHON MICROSERVICES LAYER                     │
│                                                                 │
│  ┌─────────────────────────┐   ┌──────────────────────────┐   │
│  │  Food Image Analyzer    │   │  Dietary Planner         │   │
│  │  Port: 5000             │   │  Port: 5001              │   │
│  │                         │   │                          │   │
│  │  Flask REST API         │   │  Flask REST API          │   │
│  │  ┌──────────────────┐   │   │  ┌───────────────────┐  │   │
│  │  │ /analyze-food    │   │   │  │ /generate-plan    │  │   │
│  │  │ /health          │   │   │  │ /health           │  │   │
│  │  └──────────────────┘   │   │  └───────────────────┘  │   │
│  │                         │   │                          │   │
│  └────────────┬────────────┘   └─────────────┬────────────┘   │
│               │                              │                 │
└───────────────┼──────────────────────────────┼─────────────────┘
                │                              │
                ▼                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI/ML LAYER                                │
│                                                                 │
│  ┌──────────────────────┐        ┌──────────────────────────┐  │
│  │  Computer Vision     │        │  Algorithmic Processing   │  │
│  │                      │        │                           │  │
│  │  - Food Detection    │        │  - BMR Calculation        │  │
│  │  - Classification    │        │  - TDEE Calculation       │  │
│  │  - Portion Estimation│        │  - Macro Distribution     │  │
│  │                      │        │  - Meal Optimization      │  │
│  │  Models:             │        │  - Timeline Estimation    │  │
│  │  • YOLOv8            │        │                           │  │
│  │  • ResNet50          │        │  Algorithms:              │  │
│  │  • EfficientNet      │        │  • Mifflin-St Jeor       │  │
│  │                      │        │  • Activity Multipliers   │  │
│  └──────────────────────┘        │  • Goal-based Planning    │  │
│                                  └──────────────────────────┘  │
└───────────────┬──────────────────────────────┬──────────────────┘
                │                              │
                ▼                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
│                                                                 │
│  ┌──────────────────────┐        ┌──────────────────────────┐  │
│  │  Nutrition Database  │        │  Meal Database           │  │
│  │                      │        │                           │  │
│  │  - Food nutritional  │        │  - Breakfast options      │  │
│  │    values (per 100g) │        │  - Lunch options          │  │
│  │  - Allergen info     │        │  - Dinner options         │  │
│  │  - Portion sizes     │        │  - Snack options          │  │
│  │                      │        │  - Nutritional data       │  │
│  │  Source:             │        │  - Allergen markers       │  │
│  │  • USDA FoodData     │        │                           │  │
│  │  • Food-101          │        │  ~100+ meal options       │  │
│  │  • Custom DB         │        │                           │  │
│  └──────────────────────┘        └──────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### 1. User Input Flow

```
User
  │
  ├─ Photo (Telegram API)
  │   └─> JPEG/PNG image
  │       └─> file_id: "AgACAgIAAx..."
  │
  └─ Text Data (Message Caption/Text)
      └─> "weight: 75kg, height: 175cm, age: 30, gender: male, 
           allergies: nuts, goal: lose 5kg"
```

### 2. Processing Pipeline

```
Input Reception (n8n Telegram Trigger)
  ↓
Parse & Extract (n8n Code Node)
  ├─> Extract photo file_id
  ├─> Parse user measurements (regex)
  └─> Structure data object
  ↓
Download Photo (n8n Telegram Node)
  └─> Get file_path from Telegram
  ↓
┌──────────────────────────────────────┐
│ Computer Vision Processing           │
│ (Python Service 1: Food Analyzer)    │
├──────────────────────────────────────┤
│ 1. Download image from Telegram      │
│ 2. Preprocess (resize, normalize)    │
│ 3. Run food detection model          │
│    └─> Detect: ["Chicken", "Rice"]   │
│ 4. Estimate portion sizes            │
│    └─> Portions: ["medium", "large"] │
│ 5. Query nutrition database          │
│    └─> Get calories & macros         │
│ 6. Check allergens                   │
│    └─> Match against user allergies  │
│ 7. Aggregate results                 │
│    └─> Total: 650 kcal               │
└──────────────────────────────────────┘
  ↓
┌──────────────────────────────────────┐
│ Dietary Planning Algorithm           │
│ (Python Service 2: Planner)          │
├──────────────────────────────────────┤
│ 1. Calculate BMR (Mifflin-St Jeor)   │
│    └─> BMR = 1,850 kcal              │
│ 2. Calculate TDEE (BMR × activity)   │
│    └─> TDEE = 2,867 kcal             │
│ 3. Set calorie target (goal-based)   │
│    └─> Target = 2,367 kcal (-500)    │
│ 4. Calculate macro distribution      │
│    └─> P: 237g, C: 177g, F: 79g      │
│ 5. Generate 7-day meal plan          │
│    ├─> Filter by allergies           │
│    ├─> Match calorie targets         │
│    ├─> Ensure variety                │
│    └─> Balance macros                │
│ 6. Calculate timeline                │
│    └─> 10 weeks to goal              │
│ 7. Generate motivation               │
└──────────────────────────────────────┘
  ↓
Format Response (n8n Code Node)
  └─> Convert to Markdown
      └─> Add emojis & formatting
  ↓
Send to User (n8n Telegram Node)
  └─> Telegram message with full plan
```

### 3. Response Flow

```
Complete Nutritional Plan
  │
  ├─ Current Meal Analysis
  │   ├─ Detected foods
  │   ├─ Calories & macros
  │   └─ Allergy warnings
  │
  ├─ Metabolic Profile
  │   ├─ BMR
  │   ├─ TDEE
  │   └─ Recommended intake
  │
  ├─ 7-Day Meal Plan
  │   └─ Each day:
  │       ├─ Breakfast (name, calories, macros)
  │       ├─ Lunch (name, calories, macros)
  │       ├─ Dinner (name, calories, macros)
  │       └─ Snacks (name, calories, macros)
  │
  └─ Progress Tracking
      ├─ Timeline to goal
      ├─ Weekly weight change
      └─ Motivation message
```

## 🧩 Component Details

### N8N Workflow Components

| Node Name | Type | Purpose | Dependencies |
|-----------|------|---------|--------------|
| Telegram Trigger | Trigger | Receive user messages | Telegram Bot Token |
| Parse User Input | Code | Extract data from message | None |
| Download Food Photo | Telegram | Get photo from Telegram | Telegram API |
| Analyze Food Image | HTTP Request | Call CV service | Python Service 1 |
| Generate Dietary Plan | HTTP Request | Call planning service | Python Service 2 |
| Format Response | Code | Create markdown message | None |
| Send Telegram Response | Telegram | Send to user | Telegram API |
| Send Error Message | Telegram | Handle errors | Telegram API |

### Python Microservices

#### Service 1: Food Image Analyzer

**Technology Stack:**
- Flask (REST API)
- PyTorch (Deep Learning)
- Pillow (Image Processing)
- NumPy (Numerical Computing)

**Key Functions:**
- `download_telegram_image()` - Fetch image from Telegram
- `detect_foods()` - Run CV model for detection
- `estimate_portion_size()` - Calculate portion sizes
- `calculate_nutrition()` - Aggregate nutritional data
- `check_allergens()` - Match against user allergies

**Endpoints:**
- `POST /analyze-food-image` - Main analysis endpoint
- `GET /health` - Health check

#### Service 2: Dietary Planner

**Technology Stack:**
- Flask (REST API)
- NumPy (Calculations)
- Python Standard Library

**Key Functions:**
- `calculate_bmr()` - Basal Metabolic Rate
- `calculate_tdee()` - Total Daily Energy Expenditure
- `determine_calorie_target()` - Goal-based targeting
- `calculate_macro_targets()` - Macro distribution
- `generate_daily_plan()` - Single day planning
- `generate_weekly_plan()` - 7-day planning
- `filter_meals_by_allergies()` - Safety filtering

**Endpoints:**
- `POST /generate-meal-plan` - Main planning endpoint
- `GET /health` - Health check

## 🔐 Security Architecture

### Authentication & Authorization

```
User → Telegram API
       ├─> Telegram handles user auth
       └─> Bot token validates n8n

n8n → Python Services
       ├─> Internal network only
       └─> Optional: API key validation

Python Services → External APIs
       └─> Encrypted credentials in .env
```

### Data Privacy

1. **No Persistent Storage:** User data not stored long-term
2. **Encrypted Transport:** HTTPS for all external calls
3. **Minimal Data Collection:** Only necessary inputs
4. **GDPR Compliance:** User can request data deletion

### Rate Limiting

- Telegram: Natural rate limiting (user input)
- Python Services: Configurable rate limits
- n8n: Workflow execution limits

## 📊 Scalability Considerations

### Horizontal Scaling

```
┌────────────────────────┐
│   Load Balancer        │
│   (NGINX/HAProxy)      │
└───────────┬────────────┘
            │
     ┌──────┴──────┬──────────┬──────────┐
     ↓             ↓          ↓          ↓
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ Service │  │ Service │  │ Service │  │ Service │
│ Instance│  │ Instance│  │ Instance│  │ Instance│
│    1    │  │    2    │  │    3    │  │    4    │
└─────────┘  └─────────┘  └─────────┘  └─────────┘
```

### Caching Strategy

```
User Request
    ↓
┌───────────────┐
│ Redis Cache   │
│               │
│ - Nutrition   │
│   Database    │
│ - Model       │
│   Results     │
│ - User        │
│   Preferences │
└───────────────┘
```

### Database Sharding

```
Users 1-1000      → Shard 1
Users 1001-2000   → Shard 2
Users 2001-3000   → Shard 3
...
```

## 🚀 Deployment Options

### Option 1: Docker Compose (Single Server)

```yaml
services:
  - n8n
  - python-services
  - redis (optional)
  - postgres (optional)
```

### Option 2: Kubernetes (Multi-Server)

```yaml
Deployments:
  - n8n (1 pod)
  - food-analyzer (3 pods)
  - dietary-planner (3 pods)
  
Services:
  - Load balancing
  - Service discovery
  
Ingress:
  - SSL termination
  - Routing
```

### Option 3: Serverless (AWS Lambda)

```
API Gateway
  ├─> Lambda: Food Analyzer
  └─> Lambda: Dietary Planner
  
Triggers:
  - n8n webhook calls
  
Storage:
  - S3 for models
  - DynamoDB for nutrition DB
```

## 📈 Performance Metrics

### Target Performance

| Metric | Target | Current |
|--------|--------|---------|
| Image Analysis | < 5s | ~3s |
| Meal Planning | < 2s | ~1s |
| Total Workflow | < 10s | ~7s |
| Uptime | > 99.5% | - |
| Error Rate | < 1% | - |

### Optimization Strategies

1. **Model Optimization**
   - ONNX conversion
   - Quantization
   - Pruning

2. **Code Optimization**
   - Async processing
   - Parallel requests
   - Connection pooling

3. **Infrastructure**
   - CDN for static assets
   - Edge computing
   - Auto-scaling

## 🔧 Monitoring & Logging

### Logging Strategy

```
Application Logs
  ├─> n8n execution logs
  ├─> Python service logs
  │   ├─> Request/Response
  │   ├─> Errors
  │   └─> Performance metrics
  └─> System logs

Storage:
  ├─> Local files (development)
  └─> Centralized (production)
      ├─> ELK Stack
      └─> CloudWatch
```

### Monitoring Metrics

```
System Metrics:
  - CPU usage
  - Memory usage
  - Disk I/O
  - Network traffic

Application Metrics:
  - Request rate
  - Response time
  - Error rate
  - Success rate

Business Metrics:
  - Users served
  - Meals analyzed
  - Plans generated
  - User satisfaction
```

## 🧪 Testing Strategy

### Unit Tests
- Individual function testing
- Mock external dependencies
- Cover edge cases

### Integration Tests
- Service-to-service communication
- API endpoint testing
- Database interactions

### End-to-End Tests
- Complete workflow execution
- User journey simulation
- Error handling

## 🗺️ Future Enhancements

1. **ML Model Improvements**
   - Real-time training pipeline
   - User feedback incorporation
   - Multi-cuisine support

2. **Feature Additions**
   - Meal prep recommendations
   - Shopping list generation
   - Recipe suggestions
   - Progress dashboards

3. **Integration Expansions**
   - Fitness trackers (Fitbit, Apple Health)
   - Grocery delivery APIs
   - Restaurant menu analysis

4. **Platform Support**
   - WhatsApp bot
   - Slack integration
   - Mobile app
   - Web dashboard

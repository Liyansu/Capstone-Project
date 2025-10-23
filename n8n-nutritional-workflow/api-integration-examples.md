# API Integration Examples for N8N Nutritional Workflow

This document provides detailed examples for integrating various computer vision APIs with the n8n nutritional planning workflow.

## 🤖 Hugging Face Transformers Integration

### Setup
1. Get API key from [Hugging Face](https://huggingface.co/settings/tokens)
2. Choose a food recognition model (recommended: `microsoft/food-101`)

### n8n Code Node Implementation

```javascript
// Food Recognition using Hugging Face Transformers
const imageData = $input.first().json;
const dietaryData = $input.first().json.dietaryData;

// Prepare image for API
const imageBase64 = imageData.imageBase64;
if (imageBase64.startsWith('data:image')) {
  imageBase64 = imageBase64.split(',')[1];
}

// Call Hugging Face API
const response = await fetch('https://api-inference.huggingface.co/models/microsoft/food-101', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${$env.HUGGING_FACE_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    inputs: imageBase64,
    parameters: {
      top_k: 10,
      threshold: 0.1
    }
  })
});

if (!response.ok) {
  throw new Error(`Hugging Face API error: ${response.status}`);
}

const results = await response.json();

// Process results
const identifiedFoods = [];
let totalCalories = 0;
let totalProtein = 0;
let totalCarbs = 0;
let totalFat = 0;
let totalFiber = 0;

// Food database for nutritional information
const foodDatabase = {
  'apple_pie': { calories: 237, protein: 2.4, carbs: 34, fat: 11, fiber: 1.6 },
  'baby_back_ribs': { calories: 355, protein: 32, carbs: 0, fat: 25, fiber: 0 },
  'baklava': { calories: 334, protein: 6, carbs: 35, fat: 20, fiber: 1.8 },
  'beef_carpaccio': { calories: 250, protein: 25, carbs: 0, fat: 17, fiber: 0 },
  'beef_tartare': { calories: 200, protein: 20, carbs: 2, fat: 13, fiber: 0 },
  'beet_salad': { calories: 43, protein: 1.6, carbs: 10, fat: 0.2, fiber: 2.8 },
  'beignets': { calories: 310, protein: 6, carbs: 35, fat: 17, fiber: 1.2 },
  'bibimbap': { calories: 350, protein: 15, carbs: 45, fat: 12, fiber: 4 },
  'bread_pudding': { calories: 320, protein: 8, carbs: 45, fat: 12, fiber: 2 },
  'breakfast_burrito': { calories: 400, protein: 20, carbs: 35, fat: 20, fiber: 3 },
  'bruschetta': { calories: 180, protein: 6, carbs: 20, fat: 8, fiber: 2 },
  'caesar_salad': { calories: 150, protein: 8, carbs: 8, fat: 10, fiber: 2 },
  'cannoli': { calories: 200, protein: 6, carbs: 25, fat: 9, fiber: 1 },
  'caprese_salad': { calories: 120, protein: 8, carbs: 6, fat: 8, fiber: 1 },
  'carrot_cake': { calories: 350, protein: 5, carbs: 45, fat: 17, fiber: 2 },
  'ceviche': { calories: 150, protein: 25, carbs: 8, fat: 3, fiber: 1 },
  'cheesecake': { calories: 320, protein: 6, carbs: 30, fat: 20, fiber: 1 },
  'cheese_plate': { calories: 250, protein: 15, carbs: 2, fat: 20, fiber: 0 },
  'chicken_curry': { calories: 300, protein: 25, carbs: 15, fat: 18, fiber: 3 },
  'chicken_quesadilla': { calories: 450, protein: 25, carbs: 35, fat: 25, fiber: 2 },
  'chicken_wings': { calories: 320, protein: 30, carbs: 2, fat: 22, fiber: 0 },
  'chocolate_cake': { calories: 400, protein: 6, carbs: 50, fat: 20, fiber: 3 },
  'chocolate_mousse': { calories: 280, protein: 6, carbs: 25, fat: 18, fiber: 2 },
  'churros': { calories: 300, protein: 4, carbs: 35, fat: 16, fiber: 1 },
  'clam_chowder': { calories: 200, protein: 15, carbs: 20, fat: 8, fiber: 2 },
  'club_sandwich': { calories: 500, protein: 30, carbs: 35, fat: 25, fiber: 3 },
  'crab_cakes': { calories: 250, protein: 20, carbs: 8, fat: 15, fiber: 1 },
  'creme_brulee': { calories: 300, protein: 6, carbs: 25, fat: 20, fiber: 0 },
  'croque_madame': { calories: 450, protein: 25, carbs: 20, fat: 30, fiber: 1 },
  'cup_cakes': { calories: 250, protein: 3, carbs: 35, fat: 12, fiber: 1 },
  'deviled_eggs': { calories: 150, protein: 12, carbs: 2, fat: 10, fiber: 0 },
  'donuts': { calories: 300, protein: 4, carbs: 35, fat: 16, fiber: 1 },
  'dumplings': { calories: 200, protein: 8, carbs: 25, fat: 8, fiber: 2 },
  'eggs_benedict': { calories: 400, protein: 20, carbs: 15, fat: 30, fiber: 1 },
  'escargots': { calories: 150, protein: 15, carbs: 5, fat: 8, fiber: 1 },
  'falafel': { calories: 200, protein: 8, carbs: 25, fat: 8, fiber: 4 },
  'filet_mignon': { calories: 300, protein: 30, carbs: 0, fat: 20, fiber: 0 },
  'fish_and_chips': { calories: 600, protein: 25, carbs: 50, fat: 35, fiber: 3 },
  'foie_gras': { calories: 400, protein: 8, carbs: 2, fat: 40, fiber: 0 },
  'french_fries': { calories: 320, protein: 4, carbs: 40, fat: 16, fiber: 3 },
  'french_onion_soup': { calories: 250, protein: 12, carbs: 20, fat: 12, fiber: 2 },
  'french_toast': { calories: 300, protein: 12, carbs: 35, fat: 12, fiber: 2 },
  'fried_calamari': { calories: 250, protein: 20, carbs: 15, fat: 12, fiber: 1 },
  'fried_rice': { calories: 300, protein: 10, carbs: 45, fat: 8, fiber: 2 },
  'frozen_yogurt': { calories: 150, protein: 4, carbs: 25, fat: 4, fiber: 0 },
  'garlic_bread': { calories: 200, protein: 6, carbs: 25, fat: 8, fiber: 1 },
  'gnocchi': { calories: 250, protein: 8, carbs: 45, fat: 6, fiber: 2 },
  'greek_salad': { calories: 180, protein: 8, carbs: 12, fat: 12, fiber: 3 },
  'grilled_cheese_sandwich': { calories: 400, protein: 15, carbs: 30, fat: 25, fiber: 2 },
  'grilled_salmon': { calories: 250, protein: 30, carbs: 0, fat: 15, fiber: 0 },
  'guacamole': { calories: 150, protein: 2, carbs: 8, fat: 14, fiber: 6 },
  'gyro': { calories: 350, protein: 20, carbs: 25, fat: 20, fiber: 2 },
  'hamburger': { calories: 500, protein: 25, carbs: 35, fat: 30, fiber: 2 },
  'hot_and_sour_soup': { calories: 100, protein: 8, carbs: 10, fat: 3, fiber: 1 },
  'hot_dog': { calories: 300, protein: 12, carbs: 20, fat: 20, fiber: 1 },
  'huevos_rancheros': { calories: 400, protein: 20, carbs: 30, fat: 25, fiber: 4 },
  'hummus': { calories: 200, protein: 8, carbs: 20, fat: 10, fiber: 6 },
  'ice_cream': { calories: 200, protein: 3, carbs: 25, fat: 10, fiber: 0 },
  'lasagna': { calories: 400, protein: 20, carbs: 35, fat: 20, fiber: 3 },
  'lobster_bisque': { calories: 300, protein: 15, carbs: 15, fat: 20, fiber: 1 },
  'lobster_roll_sandwich': { calories: 450, protein: 25, carbs: 30, fat: 25, fiber: 2 },
  'macaroni_and_cheese': { calories: 350, protein: 15, carbs: 35, fat: 18, fiber: 2 },
  'macarons': { calories: 150, protein: 3, carbs: 25, fat: 5, fiber: 1 },
  'miso_soup': { calories: 50, protein: 3, carbs: 6, fat: 2, fiber: 1 },
  'mussels': { calories: 150, protein: 20, carbs: 5, fat: 6, fiber: 0 },
  'nachos': { calories: 400, protein: 15, carbs: 35, fat: 25, fiber: 3 },
  'omelette': { calories: 250, protein: 18, carbs: 2, fat: 18, fiber: 0 },
  'onion_rings': { calories: 300, protein: 4, carbs: 35, fat: 16, fiber: 3 },
  'oysters': { calories: 100, protein: 12, carbs: 4, fat: 4, fiber: 0 },
  'pad_thai': { calories: 400, protein: 15, carbs: 50, fat: 15, fiber: 3 },
  'paella': { calories: 350, protein: 20, carbs: 40, fat: 12, fiber: 2 },
  'pancakes': { calories: 300, protein: 8, carbs: 40, fat: 12, fiber: 2 },
  'panna_cotta': { calories: 200, protein: 4, carbs: 20, fat: 12, fiber: 0 },
  'peking_duck': { calories: 400, protein: 30, carbs: 5, fat: 30, fiber: 0 },
  'pho': { calories: 300, protein: 20, carbs: 30, fat: 8, fiber: 2 },
  'pizza': { calories: 400, protein: 18, carbs: 45, fat: 18, fiber: 2 },
  'pork_chop': { calories: 300, protein: 30, carbs: 0, fat: 20, fiber: 0 },
  'poutine': { calories: 500, protein: 15, carbs: 40, fat: 30, fiber: 2 },
  'prime_rib': { calories: 400, protein: 35, carbs: 0, fat: 28, fiber: 0 },
  'pulled_pork_sandwich': { calories: 450, protein: 25, carbs: 35, fat: 25, fiber: 2 },
  'ramen': { calories: 400, protein: 20, carbs: 45, fat: 15, fiber: 3 },
  'ravioli': { calories: 300, protein: 15, carbs: 35, fat: 12, fiber: 2 },
  'red_velvet_cake': { calories: 350, protein: 5, carbs: 45, fat: 16, fiber: 2 },
  'risotto': { calories: 300, protein: 10, carbs: 45, fat: 10, fiber: 2 },
  'samosa': { calories: 200, protein: 6, carbs: 25, fat: 8, fiber: 2 },
  'sashimi': { calories: 150, protein: 25, carbs: 0, fat: 5, fiber: 0 },
  'scallops': { calories: 100, protein: 20, carbs: 2, fat: 1, fiber: 0 },
  'seaweed_salad': { calories: 50, protein: 2, carbs: 8, fat: 1, fiber: 2 },
  'shrimp_and_grits': { calories: 400, protein: 25, carbs: 35, fat: 20, fiber: 2 },
  'spaghetti_bolognese': { calories: 450, protein: 20, carbs: 50, fat: 18, fiber: 3 },
  'spaghetti_carbonara': { calories: 500, protein: 20, carbs: 45, fat: 25, fiber: 2 },
  'spring_rolls': { calories: 150, protein: 6, carbs: 20, fat: 5, fiber: 2 },
  'steak': { calories: 300, protein: 30, carbs: 0, fat: 20, fiber: 0 },
  'strawberry_shortcake': { calories: 300, protein: 5, carbs: 45, fat: 12, fiber: 2 },
  'sushi': { calories: 200, protein: 15, carbs: 25, fat: 5, fiber: 1 },
  'tacos': { calories: 250, protein: 15, carbs: 20, fat: 12, fiber: 3 },
  'takoyaki': { calories: 200, protein: 8, carbs: 25, fat: 8, fiber: 1 },
  'tiramisu': { calories: 300, protein: 6, carbs: 35, fat: 15, fiber: 1 },
  'tuna_tartare': { calories: 200, protein: 25, carbs: 2, fat: 10, fiber: 0 },
  'waffles': { calories: 300, protein: 8, carbs: 40, fat: 12, fiber: 2 }
};

// Process each identified food
for (const result of results) {
  if (result.score > 0.1) { // Confidence threshold
    const foodName = result.label;
    const confidence = result.score;
    
    // Get nutritional data from database
    const nutrition = foodDatabase[foodName] || {
      calories: 200, protein: 10, carbs: 20, fat: 8, fiber: 2
    };
    
    // Estimate portion size (simplified - in production, use computer vision)
    const estimatedWeight = 150; // grams
    const scaleFactor = estimatedWeight / 100;
    
    const foodData = {
      name: foodName.replace(/_/g, ' '),
      confidence: confidence,
      estimatedWeight: estimatedWeight,
      calories: Math.round(nutrition.calories * scaleFactor),
      protein: Math.round(nutrition.protein * scaleFactor * 10) / 10,
      carbs: Math.round(nutrition.carbs * scaleFactor * 10) / 10,
      fat: Math.round(nutrition.fat * scaleFactor * 10) / 10,
      fiber: Math.round(nutrition.fiber * scaleFactor * 10) / 10
    };
    
    identifiedFoods.push(foodData);
    totalCalories += foodData.calories;
    totalProtein += foodData.protein;
    totalCarbs += foodData.carbs;
    totalFat += foodData.fat;
    totalFiber += foodData.fiber;
  }
}

return {
  json: {
    identifiedFoods: identifiedFoods,
    totalCalories: totalCalories,
    totalProtein: Math.round(totalProtein * 10) / 10,
    totalCarbs: Math.round(totalCarbs * 10) / 10,
    totalFat: Math.round(totalFat * 10) / 10,
    totalFiber: Math.round(totalFiber * 10) / 10,
    dietaryData: dietaryData,
    imageProcessed: true
  }
};
```

## ☁️ AWS SageMaker Integration

### Setup
1. Deploy a food recognition model on SageMaker
2. Create an endpoint for inference
3. Set up IAM permissions

### n8n Code Node Implementation

```javascript
// Food Recognition using AWS SageMaker
const AWS = require('aws-sdk');
const imageData = $input.first().json;
const dietaryData = $input.first().json.dietaryData;

// Configure AWS SDK
const sagemaker = new AWS.SageMakerRuntime({
  accessKeyId: $env.AWS_ACCESS_KEY_ID,
  secretAccessKey: $env.AWS_SECRET_ACCESS_KEY,
  region: $env.AWS_REGION
});

// Prepare image data
const imageBase64 = imageData.imageBase64;
if (imageBase64.startsWith('data:image')) {
  imageBase64 = imageBase64.split(',')[1];
}

// Prepare payload for SageMaker endpoint
const payload = {
  image: imageBase64,
  model_type: "food_recognition",
  confidence_threshold: 0.1,
  max_predictions: 10
};

try {
  // Call SageMaker endpoint
  const params = {
    EndpointName: $env.SAGEMAKER_ENDPOINT_NAME,
    ContentType: 'application/json',
    Body: JSON.stringify(payload)
  };
  
  const response = await sagemaker.invokeEndpoint(params).promise();
  const results = JSON.parse(response.Body.toString());
  
  // Process SageMaker results
  const identifiedFoods = [];
  let totalCalories = 0;
  let totalProtein = 0;
  let totalCarbs = 0;
  let totalFat = 0;
  let totalFiber = 0;
  
  // Process predictions from SageMaker
  if (results.predictions && Array.isArray(results.predictions)) {
    for (const prediction of results.predictions) {
      const foodName = prediction.food_name || prediction.label;
      const confidence = prediction.confidence || prediction.score;
      const portionSize = prediction.portion_size || 150; // grams
      
      if (confidence > 0.1) {
        // Get nutritional data (same database as above)
        const nutrition = getNutritionalData(foodName, portionSize);
        
        const foodData = {
          name: foodName,
          confidence: confidence,
          estimatedWeight: portionSize,
          calories: nutrition.calories,
          protein: nutrition.protein,
          carbs: nutrition.carbs,
          fat: nutrition.fat,
          fiber: nutrition.fiber
        };
        
        identifiedFoods.push(foodData);
        totalCalories += foodData.calories;
        totalProtein += foodData.protein;
        totalCarbs += foodData.carbs;
        totalFat += foodData.fat;
        totalFiber += foodData.fiber;
      }
    }
  }
  
  return {
    json: {
      identifiedFoods: identifiedFoods,
      totalCalories: totalCalories,
      totalProtein: Math.round(totalProtein * 10) / 10,
      totalCarbs: Math.round(totalCarbs * 10) / 10,
      totalFat: Math.round(totalFat * 10) / 10,
      totalFiber: Math.round(totalFiber * 10) / 10,
      dietaryData: dietaryData,
      imageProcessed: true
    }
  };
  
} catch (error) {
  throw new Error(`AWS SageMaker error: ${error.message}`);
}

// Helper function to get nutritional data
function getNutritionalData(foodName, portionSize) {
  // Use the same food database as above
  const foodDatabase = { /* ... same as above ... */ };
  
  const nutrition = foodDatabase[foodName] || {
    calories: 200, protein: 10, carbs: 20, fat: 8, fiber: 2
  };
  
  const scaleFactor = portionSize / 100;
  return {
    calories: Math.round(nutrition.calories * scaleFactor),
    protein: Math.round(nutrition.protein * scaleFactor * 10) / 10,
    carbs: Math.round(nutrition.carbs * scaleFactor * 10) / 10,
    fat: Math.round(nutrition.fat * scaleFactor * 10) / 10,
    fiber: Math.round(nutrition.fiber * scaleFactor * 10) / 10
  };
}
```

## 🔍 Google Vision API Integration

### Setup
1. Enable Vision API in Google Cloud Console
2. Create service account credentials
3. Download JSON credentials file

### n8n Code Node Implementation

```javascript
// Food Recognition using Google Vision API
const { ImageAnnotatorClient } = require('@google-cloud/vision');
const imageData = $input.first().json;
const dietaryData = $input.first().json.dietaryData;

// Initialize Google Vision client
const client = new ImageAnnotatorClient({
  keyFilename: $env.GOOGLE_APPLICATION_CREDENTIALS,
  projectId: $env.GOOGLE_CLOUD_PROJECT_ID
});

// Prepare image data
const imageBase64 = imageData.imageBase64;
if (imageBase64.startsWith('data:image')) {
  imageBase64 = imageBase64.split(',')[1];
}

const imageBuffer = Buffer.from(imageBase64, 'base64');

try {
  // Perform food detection
  const [result] = await client.labelDetection({
    image: { content: imageBuffer },
    imageContext: {
      labelDetectionParams: {
        model: 'builtin/latest'
      }
    }
  });
  
  const labels = result.labelAnnotations || [];
  
  // Filter food-related labels
  const foodLabels = labels.filter(label => 
    isFoodRelated(label.description) && label.score > 0.1
  );
  
  // Process food labels
  const identifiedFoods = [];
  let totalCalories = 0;
  let totalProtein = 0;
  let totalCarbs = 0;
  let totalFat = 0;
  let totalFiber = 0;
  
  for (const label of foodLabels) {
    const foodName = label.description;
    const confidence = label.score;
    const portionSize = estimatePortionSize(foodName); // Custom function
    
    const nutrition = getNutritionalData(foodName, portionSize);
    
    const foodData = {
      name: foodName,
      confidence: confidence,
      estimatedWeight: portionSize,
      calories: nutrition.calories,
      protein: nutrition.protein,
      carbs: nutrition.carbs,
      fat: nutrition.fat,
      fiber: nutrition.fiber
    };
    
    identifiedFoods.push(foodData);
    totalCalories += foodData.calories;
    totalProtein += foodData.protein;
    totalCarbs += foodData.carbs;
    totalFat += foodData.fat;
    totalFiber += foodData.fiber;
  }
  
  return {
    json: {
      identifiedFoods: identifiedFoods,
      totalCalories: totalCalories,
      totalProtein: Math.round(totalProtein * 10) / 10,
      totalCarbs: Math.round(totalCarbs * 10) / 10,
      totalFat: Math.round(totalFat * 10) / 10,
      totalFiber: Math.round(totalFiber * 10) / 10,
      dietaryData: dietaryData,
      imageProcessed: true
    }
  };
  
} catch (error) {
  throw new Error(`Google Vision API error: ${error.message}`);
}

// Helper function to check if label is food-related
function isFoodRelated(description) {
  const foodKeywords = [
    'food', 'meal', 'dish', 'cuisine', 'ingredient', 'vegetable',
    'fruit', 'meat', 'chicken', 'beef', 'fish', 'pasta', 'rice',
    'bread', 'salad', 'soup', 'pizza', 'burger', 'sandwich',
    'dessert', 'cake', 'pie', 'cookie', 'candy', 'chocolate'
  ];
  
  return foodKeywords.some(keyword => 
    description.toLowerCase().includes(keyword)
  );
}

// Helper function to estimate portion size
function estimatePortionSize(foodName) {
  // Simplified portion size estimation
  // In production, use computer vision for accurate portion sizing
  const portionSizes = {
    'pizza': 200,
    'burger': 150,
    'salad': 100,
    'soup': 250,
    'pasta': 150,
    'rice': 100,
    'chicken': 150,
    'fish': 120,
    'vegetables': 80,
    'fruit': 100
  };
  
  for (const [key, size] of Object.entries(portionSizes)) {
    if (foodName.toLowerCase().includes(key)) {
      return size;
    }
  }
  
  return 100; // Default portion size
}

// Helper function to get nutritional data
function getNutritionalData(foodName, portionSize) {
  // Use the same food database as above
  const foodDatabase = { /* ... same as above ... */ };
  
  const nutrition = foodDatabase[foodName] || {
    calories: 200, protein: 10, carbs: 20, fat: 8, fiber: 2
  };
  
  const scaleFactor = portionSize / 100;
  return {
    calories: Math.round(nutrition.calories * scaleFactor),
    protein: Math.round(nutrition.protein * scaleFactor * 10) / 10,
    carbs: Math.round(nutrition.carbs * scaleFactor * 10) / 10,
    fat: Math.round(nutrition.fat * scaleFactor * 10) / 10,
    fiber: Math.round(nutrition.fiber * scaleFactor * 10) / 10
  };
}
```

## 🔧 Custom API Integration

### Setup
1. Deploy your own food recognition API
2. Set up authentication (API key, JWT, etc.)
3. Define API endpoints and data format

### n8n Code Node Implementation

```javascript
// Food Recognition using Custom API
const imageData = $input.first().json;
const dietaryData = $input.first().json.dietaryData;

// Prepare image data
const imageBase64 = imageData.imageBase64;
if (imageBase64.startsWith('data:image')) {
  imageBase64 = imageBase64.split(',')[1];
}

// Prepare API request
const apiUrl = $env.CUSTOM_API_URL || 'https://your-api.com/food-recognition';
const apiKey = $env.CUSTOM_API_KEY;

const requestBody = {
  image: imageBase64,
  options: {
    confidence_threshold: 0.1,
    max_predictions: 10,
    include_nutrition: true,
    portion_estimation: true
  }
};

try {
  // Call custom API
  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'X-API-Version': '1.0'
    },
    body: JSON.stringify(requestBody)
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
  
  const results = await response.json();
  
  // Process API response
  const identifiedFoods = results.foods || [];
  const totals = results.totals || {};
  
  return {
    json: {
      identifiedFoods: identifiedFoods,
      totalCalories: totals.calories || 0,
      totalProtein: totals.protein || 0,
      totalCarbs: totals.carbs || 0,
      totalFat: totals.fat || 0,
      totalFiber: totals.fiber || 0,
      dietaryData: dietaryData,
      imageProcessed: true,
      apiResponse: results
    }
  };
  
} catch (error) {
  throw new Error(`Custom API error: ${error.message}`);
}
```

## 📊 Performance Optimization

### Caching Strategy

```javascript
// Add caching to reduce API calls
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 3600 }); // 1 hour cache

// Check cache first
const imageHash = createImageHash(imageBase64);
const cachedResult = cache.get(imageHash);

if (cachedResult) {
  return { json: cachedResult };
}

// Call API and cache result
const result = await callFoodRecognitionAPI(imageBase64);
cache.set(imageHash, result);

return { json: result };
```

### Error Handling

```javascript
// Comprehensive error handling
try {
  const result = await callFoodRecognitionAPI(imageBase64);
  return { json: result };
} catch (error) {
  // Log error for debugging
  console.error('Food recognition error:', error);
  
  // Return fallback result
  return {
    json: {
      identifiedFoods: [],
      totalCalories: 0,
      totalProtein: 0,
      totalCarbs: 0,
      totalFat: 0,
      totalFiber: 0,
      dietaryData: dietaryData,
      imageProcessed: false,
      error: error.message
    }
  };
}
```

## 🔒 Security Considerations

### API Key Management

```javascript
// Secure API key handling
const apiKey = $env.API_KEY;
if (!apiKey) {
  throw new Error('API key not configured');
}

// Use environment variables for sensitive data
const headers = {
  'Authorization': `Bearer ${apiKey}`,
  'Content-Type': 'application/json'
};
```

### Input Validation

```javascript
// Validate input data
function validateImageData(imageData) {
  if (!imageData || !imageData.imageBase64) {
    throw new Error('No image data provided');
  }
  
  // Check image format
  if (!imageData.imageBase64.startsWith('data:image/')) {
    throw new Error('Invalid image format');
  }
  
  // Check image size (optional)
  const imageSize = (imageData.imageBase64.length * 3) / 4;
  if (imageSize > 10 * 1024 * 1024) { // 10MB limit
    throw new Error('Image too large');
  }
}
```

## 📈 Monitoring and Analytics

### API Usage Tracking

```javascript
// Track API usage for monitoring
const usageData = {
  timestamp: new Date().toISOString(),
  api_type: 'hugging_face',
  image_size: imageBase64.length,
  processing_time: Date.now() - startTime,
  success: true
};

// Send to analytics service
await sendAnalytics(usageData);
```

### Performance Metrics

```javascript
// Track performance metrics
const startTime = Date.now();
const result = await callFoodRecognitionAPI(imageBase64);
const processingTime = Date.now() - startTime;

// Log performance data
console.log(`Food recognition completed in ${processingTime}ms`);
```

This comprehensive guide provides all the necessary code examples and configurations for integrating various computer vision APIs with your n8n nutritional planning workflow. Choose the API that best fits your needs and budget, and follow the setup instructions to get started.
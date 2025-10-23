# N8N Nutritional Planning Workflow - Setup Instructions

## 🚀 Quick Start Guide

This guide will help you set up the comprehensive n8n nutritional planning workflow step by step.

## 📋 Prerequisites

### Required Accounts & Services
1. **n8n Instance** (self-hosted or cloud)
2. **Telegram Bot** (via @BotFather)
3. **Computer Vision API** (choose one):
   - Hugging Face Transformers
   - AWS SageMaker
   - Google Vision API
   - Custom API endpoint

### System Requirements
- Node.js 16+ (for n8n)
- Python 3.8+ (for custom models)
- 2GB+ RAM
- 10GB+ storage

## 🔧 Step-by-Step Setup

### 1. Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Choose a name for your bot (e.g., "Nutritional Planner Bot")
4. Choose a username (e.g., "nutritional_planner_bot")
5. Save the bot token provided by BotFather
6. Set bot commands:
   ```
   /start - Start nutritional planning
   /help - Get help with the bot
   /plan - Generate meal plan
   ```

### 2. Set Up Computer Vision API

#### Option A: Hugging Face (Recommended for beginners)

1. Go to [huggingface.co](https://huggingface.co)
2. Create an account and verify email
3. Go to Settings → Access Tokens
4. Create a new token with "Read" permissions
5. Save the token for later use

#### Option B: AWS SageMaker (For advanced users)

1. Create AWS account
2. Set up SageMaker service
3. Deploy a food recognition model endpoint
4. Note down:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Region
   - Endpoint name

#### Option C: Google Vision API

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable Vision API
4. Create service account credentials
5. Download JSON credentials file

### 3. Deploy n8n Instance

#### Option A: n8n Cloud (Easiest)

1. Go to [n8n.cloud](https://n8n.cloud)
2. Sign up for an account
3. Create a new workflow
4. Skip to step 4

#### Option B: Self-hosted n8n

1. Install n8n globally:
   ```bash
   npm install n8n -g
   ```

2. Start n8n:
   ```bash
   n8n start
   ```

3. Access n8n at `http://localhost:5678`

#### Option C: Docker (Recommended for production)

1. Create `docker-compose.yml`:
   ```yaml
   version: '3.8'
   services:
     n8n:
       image: n8nio/n8n
       ports:
         - "5678:5678"
       environment:
         - N8N_BASIC_AUTH_ACTIVE=true
         - N8N_BASIC_AUTH_USER=admin
         - N8N_BASIC_AUTH_PASSWORD=your_password
         - WEBHOOK_URL=https://your-domain.com
       volumes:
         - n8n_data:/home/node/.n8n
   
   volumes:
     n8n_data:
   ```

2. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

### 4. Import Workflow

1. Open your n8n instance
2. Click "Workflows" in the sidebar
3. Click "Import from File"
4. Select the `workflow.json` file from this repository
5. Click "Import"

### 5. Configure Environment Variables

1. In n8n, go to Settings → Credentials
2. Create new credentials for each service:

#### Telegram Bot Credentials
- **Name**: `Telegram Bot`
- **Type**: `Generic Credential Type`
- **Fields**:
  - `bot_token`: Your Telegram bot token

#### Computer Vision API Credentials
Choose based on your selected API:

**Hugging Face:**
- **Name**: `Hugging Face API`
- **Fields**:
  - `api_key`: Your Hugging Face API key
  - `model_name`: `microsoft/food-101`

**AWS SageMaker:**
- **Name**: `AWS SageMaker`
- **Fields**:
  - `aws_access_key_id`: Your AWS access key
  - `aws_secret_access_key`: Your AWS secret key
  - `aws_region`: Your AWS region
  - `endpoint_name`: Your SageMaker endpoint name

**Google Vision:**
- **Name**: `Google Vision API`
- **Fields**:
  - `project_id`: Your Google Cloud project ID
  - `credentials_path`: Path to your credentials JSON file

### 6. Update Workflow Nodes

#### Update Telegram Webhook
1. Click on "Telegram Webhook" node
2. Set the webhook URL to your n8n instance URL
3. Test the webhook connection

#### Update Food Recognition Node
1. Click on "Food Recognition & Calorie Estimation" node
2. Replace the mock code with actual API calls:

**For Hugging Face:**
```javascript
// Replace the mock code with this:
const imageData = $input.first().json;
const dietaryData = $input.first().json.dietaryData;

// Call Hugging Face API
const response = await fetch('https://api-inference.huggingface.co/models/microsoft/food-101', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${$env.HUGGING_FACE_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    inputs: imageData.imageBase64
  })
});

const results = await response.json();
// Process results and return nutritional data
```

**For AWS SageMaker:**
```javascript
// Replace with AWS SageMaker API call
const AWS = require('aws-sdk');
const sagemaker = new AWS.SageMakerRuntime({
  accessKeyId: $env.AWS_ACCESS_KEY_ID,
  secretAccessKey: $env.AWS_SECRET_ACCESS_KEY,
  region: $env.AWS_REGION
});

const params = {
  EndpointName: $env.SAGEMAKER_ENDPOINT_NAME,
  ContentType: 'application/json',
  Body: JSON.stringify({
    image: imageData.imageBase64
  })
};

const response = await sagemaker.invokeEndpoint(params).promise();
const results = JSON.parse(response.Body);
```

### 7. Set Up Webhook URL

1. Get your n8n webhook URL:
   - Format: `https://your-n8n-instance.com/webhook/nutritional-planning`
   - Or: `https://your-domain.com/webhook/nutritional-planning`

2. Set the webhook in Telegram:
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
        -H "Content-Type: application/json" \
        -d '{"url": "https://your-n8n-instance.com/webhook/nutritional-planning"}'
   ```

### 8. Test the Workflow

1. Send a test message to your Telegram bot:
   ```
   [Send a photo of food]
   
   Weight: 70kg, Height: 175cm, Age: 30, Gender: female, Activity: moderate, Allergies: nuts, Goals: lose 5kg
   ```

2. Check n8n execution logs for any errors
3. Verify the bot responds with a nutritional plan

## 🔧 Advanced Configuration

### Custom Food Database

To add custom foods to the recognition system:

1. Edit the `food_database` in `dietary_planning.py`
2. Add new food entries with nutritional data
3. Update the food recognition logic

### Meal Plan Customization

1. Modify the `meal_templates` in `dietary_planning.py`
2. Add new meal options for different dietary preferences
3. Update the meal selection logic

### API Rate Limiting

For production use, implement rate limiting:

1. Add rate limiting to the webhook endpoint
2. Implement user session management
3. Add request throttling

## 🚨 Troubleshooting

### Common Issues

#### 1. Webhook Not Receiving Messages
- Check webhook URL is correct
- Verify bot token is valid
- Check n8n logs for errors

#### 2. Food Recognition Not Working
- Verify API credentials are correct
- Check API rate limits
- Ensure image format is supported

#### 3. Meal Plan Generation Errors
- Check user input parsing
- Verify nutritional calculations
- Review error logs

#### 4. Telegram Response Issues
- Check message formatting
- Verify chat ID is correct
- Review Telegram API limits

### Debug Mode

Enable debug mode in n8n:

1. Go to Settings → General
2. Set "Log Level" to "debug"
3. Check execution logs for detailed information

### Testing Individual Nodes

1. Click on any node
2. Click "Execute Node"
3. Review the output data
4. Fix any issues before testing the full workflow

## 📊 Monitoring & Analytics

### Set Up Monitoring

1. **n8n Execution Logs**: Monitor workflow executions
2. **API Usage**: Track API calls and costs
3. **User Analytics**: Monitor bot usage patterns

### Performance Optimization

1. **Caching**: Implement caching for frequent requests
2. **Async Processing**: Use async operations for better performance
3. **Database**: Store user profiles and meal history

## 🔒 Security Considerations

### Data Protection

1. **Encrypt Sensitive Data**: Use encryption for user data
2. **Secure API Keys**: Store credentials securely
3. **User Privacy**: Implement data retention policies

### Access Control

1. **Bot Permissions**: Limit bot access to necessary functions
2. **Rate Limiting**: Prevent abuse and spam
3. **User Authentication**: Implement user verification

## 📈 Scaling Considerations

### High Volume Usage

1. **Load Balancing**: Distribute load across multiple instances
2. **Database Scaling**: Use scalable database solutions
3. **API Optimization**: Optimize API calls and caching

### Cost Management

1. **API Usage**: Monitor and optimize API costs
2. **Resource Usage**: Optimize server resources
3. **Caching**: Reduce redundant API calls

## 🆘 Support

### Getting Help

1. **Documentation**: Check this README and code comments
2. **Community**: Join n8n community forums
3. **Issues**: Create GitHub issues for bugs

### Common Solutions

1. **Restart n8n**: Often fixes temporary issues
2. **Check Logs**: Review execution logs for errors
3. **Update Dependencies**: Keep n8n and APIs updated

## 🔄 Updates & Maintenance

### Regular Maintenance

1. **Update n8n**: Keep n8n instance updated
2. **API Updates**: Monitor API changes and updates
3. **Security Patches**: Apply security updates regularly

### Backup Strategy

1. **Workflow Backup**: Export workflows regularly
2. **Data Backup**: Backup user data and configurations
3. **Disaster Recovery**: Plan for system failures

---

## 📞 Contact

For additional support or questions:
- Create an issue in this repository
- Contact the development team
- Check n8n documentation at [docs.n8n.io](https://docs.n8n.io)
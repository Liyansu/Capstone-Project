#!/bin/bash

# N8N Nutritional Planning Workflow Setup Script
# This script automates the setup process for the nutritional planning workflow

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Docker
    if ! command_exists docker; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command_exists docker-compose; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    log_success "All prerequisites are met!"
}

# Create necessary directories
create_directories() {
    log_info "Creating necessary directories..."
    
    mkdir -p credentials
    mkdir -p workflows
    mkdir -p monitoring/grafana/dashboards
    mkdir -p monitoring/grafana/datasources
    mkdir -p monitoring/rules
    mkdir -p nginx/ssl
    mkdir -p logs
    mkdir -p backups
    
    log_success "Directories created successfully!"
}

# Generate SSL certificates (self-signed for development)
generate_ssl_certificates() {
    log_info "Generating SSL certificates..."
    
    if [ ! -f "nginx/ssl/cert.pem" ] || [ ! -f "nginx/ssl/key.pem" ]; then
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout nginx/ssl/key.pem \
            -out nginx/ssl/cert.pem \
            -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
        
        log_success "SSL certificates generated!"
    else
        log_info "SSL certificates already exist, skipping..."
    fi
}

# Create environment file
create_env_file() {
    log_info "Creating environment file..."
    
    if [ ! -f ".env" ]; then
        cp .env.example .env
        log_warning "Please edit .env file with your actual configuration values!"
        log_info "Generated .env file from template"
    else
        log_info "Environment file already exists, skipping..."
    fi
}

# Setup Telegram bot
setup_telegram_bot() {
    log_info "Setting up Telegram bot..."
    
    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        log_warning "TELEGRAM_BOT_TOKEN not set in environment"
        log_info "Please follow these steps to create a Telegram bot:"
        echo "1. Open Telegram and search for @BotFather"
        echo "2. Send /newbot command"
        echo "3. Choose a name for your bot"
        echo "4. Choose a username for your bot"
        echo "5. Copy the bot token and add it to your .env file"
        echo "6. Set the webhook URL: https://your-domain.com/webhook/nutritional-planning"
    else
        log_success "Telegram bot token is configured!"
    fi
}

# Setup computer vision API
setup_vision_api() {
    log_info "Setting up computer vision API..."
    
    log_info "Choose your preferred computer vision API:"
    echo "1. Hugging Face (Recommended for beginners)"
    echo "2. AWS SageMaker (For advanced users)"
    echo "3. Google Vision API"
    echo "4. Custom API"
    
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            log_info "Setting up Hugging Face API..."
            log_info "Please get your API key from https://huggingface.co/settings/tokens"
            log_info "Add HUGGING_FACE_API_KEY to your .env file"
            ;;
        2)
            log_info "Setting up AWS SageMaker..."
            log_info "Please configure AWS credentials and SageMaker endpoint"
            log_info "Add AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, and SAGEMAKER_ENDPOINT_NAME to your .env file"
            ;;
        3)
            log_info "Setting up Google Vision API..."
            log_info "Please enable Vision API in Google Cloud Console"
            log_info "Create service account credentials and add GOOGLE_APPLICATION_CREDENTIALS to your .env file"
            ;;
        4)
            log_info "Setting up Custom API..."
            log_info "Please configure your custom API endpoint and add CUSTOM_API_URL and CUSTOM_API_KEY to your .env file"
            ;;
        *)
            log_warning "Invalid choice, skipping API setup..."
            ;;
    esac
}

# Build and start services
start_services() {
    log_info "Building and starting services..."
    
    # Build custom images
    docker-compose build
    
    # Start services
    docker-compose up -d
    
    log_success "Services started successfully!"
}

# Wait for services to be ready
wait_for_services() {
    log_info "Waiting for services to be ready..."
    
    # Wait for n8n
    log_info "Waiting for n8n to be ready..."
    timeout=300
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:5678/healthz >/dev/null 2>&1; then
            log_success "n8n is ready!"
            break
        fi
        sleep 5
        timeout=$((timeout - 5))
    done
    
    if [ $timeout -le 0 ]; then
        log_error "n8n failed to start within 5 minutes"
        exit 1
    fi
    
    # Wait for Python service
    log_info "Waiting for Python service to be ready..."
    timeout=300
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:8000/health >/dev/null 2>&1; then
            log_success "Python service is ready!"
            break
        fi
        sleep 5
        timeout=$((timeout - 5))
    done
    
    if [ $timeout -le 0 ]; then
        log_warning "Python service failed to start within 5 minutes"
    fi
}

# Import workflow
import_workflow() {
    log_info "Importing n8n workflow..."
    
    # Wait a bit for n8n to fully initialize
    sleep 10
    
    # Check if workflow file exists
    if [ -f "workflow.json" ]; then
        log_info "Workflow file found. Please import it manually in n8n:"
        echo "1. Open http://localhost:5678 in your browser"
        echo "2. Login with admin credentials"
        echo "3. Go to Workflows → Import from File"
        echo "4. Select the workflow.json file"
        echo "5. Click Import"
    else
        log_warning "Workflow file not found. Please ensure workflow.json exists."
    fi
}

# Display final instructions
display_final_instructions() {
    log_success "Setup completed successfully!"
    echo ""
    echo "=========================================="
    echo "N8N Nutritional Planning Workflow Setup"
    echo "=========================================="
    echo ""
    echo "Services are now running:"
    echo "• N8N: http://localhost:5678"
    echo "• Python API: http://localhost:8000"
    echo "• Grafana: http://localhost:3000 (admin/nutritional_grafana_2024)"
    echo "• Prometheus: http://localhost:9090"
    echo ""
    echo "Next steps:"
    echo "1. Configure your .env file with actual API keys"
    echo "2. Import the workflow in n8n"
    echo "3. Set up your Telegram bot webhook"
    echo "4. Test the workflow with a sample message"
    echo ""
    echo "For more information, see the README.md file"
    echo ""
}

# Main setup function
main() {
    echo "=========================================="
    echo "N8N Nutritional Planning Workflow Setup"
    echo "=========================================="
    echo ""
    
    check_prerequisites
    create_directories
    generate_ssl_certificates
    create_env_file
    setup_telegram_bot
    setup_vision_api
    start_services
    wait_for_services
    import_workflow
    display_final_instructions
}

# Run main function
main "$@"
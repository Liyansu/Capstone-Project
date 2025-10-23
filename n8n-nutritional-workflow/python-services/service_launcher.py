"""
Service Launcher - Start all Python microservices
"""

import os
import sys
import time
import subprocess
from multiprocessing import Process
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def start_food_analyzer():
    """Start the Food Image Analyzer service"""
    print("🚀 Starting Food Image Analyzer on port 5000...")
    subprocess.run([sys.executable, "food_image_analyzer.py"])


def start_dietary_planner():
    """Start the Dietary Planner service"""
    print("🚀 Starting Dietary Planner on port 5001...")
    subprocess.run([sys.executable, "dietary_planner.py"])


def main():
    """Launch all services"""
    print("=" * 60)
    print("🍽️  N8N Nutritional Planning Workflow Services")
    print("=" * 60)
    print()
    
    # Check for required environment variables
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not telegram_token:
        print("⚠️  WARNING: TELEGRAM_BOT_TOKEN not set in .env file")
        print("Please create a .env file based on .env.example")
        print()
    
    # Start services in separate processes
    services = [
        Process(target=start_food_analyzer, name="FoodAnalyzer"),
        Process(target=start_dietary_planner, name="DietaryPlanner")
    ]
    
    try:
        # Start all services
        for service in services:
            service.start()
            time.sleep(2)  # Give each service time to start
        
        print()
        print("✅ All services started successfully!")
        print()
        print("📊 Service Status:")
        print("  - Food Image Analyzer: http://localhost:5000")
        print("  - Dietary Planner: http://localhost:5001")
        print()
        print("🛑 Press Ctrl+C to stop all services")
        print()
        
        # Wait for all services
        for service in services:
            service.join()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping all services...")
        
        # Terminate all services
        for service in services:
            if service.is_alive():
                service.terminate()
                service.join(timeout=5)
        
        print("✅ All services stopped")
        sys.exit(0)


if __name__ == "__main__":
    main()

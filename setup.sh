#!/bin/bash

# Disaster Response Map - Complete Setup Script
# This script sets up both frontend and backend for the disaster response application

echo "🚀 Disaster Response Map - Complete Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_info "Setting up Disaster Response Map application..."

# Backend Setup
echo ""
echo "🔧 Backend Setup"
echo "================"

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_warning "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_info "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_warning "Creating .env file from template..."
    cp env.example .env
    print_warning "Please update .env file with your MongoDB Atlas connection string"
fi

# Run Django migrations
print_info "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo ""
read -p "Do you want to create a superuser account? (y/N): " create_superuser
if [[ $create_superuser =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Seed sample data
echo ""
read -p "Do you want to seed the database with sample data? (y/N): " seed_data
if [[ $seed_data =~ ^[Yy]$ ]]; then
    python manage.py seed_reports --count 20
fi

print_status "Backend setup completed!"

# Frontend Setup
echo ""
echo "🎨 Frontend Setup"
echo "================="

cd ../frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    print_info "Installing Node.js dependencies..."
    npm install
else
    print_status "Node.js dependencies already installed"
fi

# Create .env file for frontend if it doesn't exist
if [ ! -f ".env" ]; then
    print_info "Creating frontend .env file..."
    echo "VITE_API_BASE_URL=http://localhost:8000/api" > .env
    echo "VITE_USE_MOCK_DATA=false" >> .env
fi

print_status "Frontend setup completed!"

# Final Instructions
echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
print_info "To start the application:"
echo ""
echo "1. Start the backend server:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "2. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Access the application:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000/api/"
echo "   API Documentation: http://localhost:8000/api/docs/"
echo "   Admin Panel: http://localhost:8000/admin/"
echo ""
print_warning "Important Notes:"
echo "- Update backend/.env with your MongoDB Atlas connection string"
echo "- The frontend is configured to use the backend API by default"
echo "- Mock data is disabled, so you need the backend running"
echo ""
print_info "For MongoDB Atlas setup:"
echo "1. Create a free cluster at https://cloud.mongodb.com"
echo "2. Create a database user"
echo "3. Whitelist your IP address"
echo "4. Get the connection string and update backend/.env"
echo "5. Uncomment the MongoDB configuration in backend/disaster_response/settings.py"
echo ""
print_status "Happy coding! 🚀"

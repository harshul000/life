#!/bin/bash

# Deployment Script for India Travel Guide Website on Linux VM
# This script automates the deployment process

set -e  # Exit on error

echo "🇮🇳 India Travel Guide - Deployment Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    print_error "This script is designed for Linux systems"
    exit 1
fi

print_info "Checking system requirements..."

# Update system packages
print_info "Updating system packages..."
sudo apt update && sudo apt upgrade -y
print_success "System packages updated"

# Install Python and dependencies
print_info "Installing Python and dependencies..."
sudo apt install -y python3 python3-pip python3-venv
print_success "Python installed"

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

print_info "Project directory: $PROJECT_DIR"

# Create virtual environment
print_info "Creating virtual environment..."
python3 -m venv venv
print_success "Virtual environment created"

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Install Python packages
print_info "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
print_success "Python packages installed"

# Test the application
print_info "Testing application..."
timeout 5 python app.py &
sleep 3
if curl -s http://localhost:5000 > /dev/null; then
    print_success "Application test successful"
    pkill -f "python app.py"
else
    print_error "Application test failed"
    pkill -f "python app.py"
    exit 1
fi

# Ask user for deployment method
echo ""
echo "Select deployment method:"
echo "1) Development server (simple, for testing)"
echo "2) Production server with Gunicorn and Nginx"
echo "3) Exit"
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        print_info "Starting development server..."
        echo ""
        echo "=========================================="
        echo "Server will start on http://0.0.0.0:5000"
        echo "Press Ctrl+C to stop the server"
        echo "=========================================="
        echo ""
        python app.py
        ;;
    2)
        print_info "Setting up production deployment..."
        
        # Install Nginx
        print_info "Installing Nginx..."
        sudo apt install -y nginx
        print_success "Nginx installed"
        
        # Get username
        USERNAME=$(whoami)
        
        # Create systemd service file
        print_info "Creating systemd service..."
        sudo tee /etc/systemd/system/india-travel.service > /dev/null <<EOF
[Unit]
Description=India Travel Guide Web Application
After=network.target

[Service]
User=$USERNAME
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
EOF
        print_success "Systemd service created"
        
        # Start and enable service
        print_info "Starting service..."
        sudo systemctl daemon-reload
        sudo systemctl start india-travel
        sudo systemctl enable india-travel
        print_success "Service started and enabled"
        
        # Get server IP
        SERVER_IP=$(hostname -I | awk '{print $1}')
        
        # Create Nginx configuration
        print_info "Configuring Nginx..."
        sudo tee /etc/nginx/sites-available/india-travel > /dev/null <<EOF
server {
    listen 80;
    server_name $SERVER_IP;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias $PROJECT_DIR/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF
        
        # Enable site
        sudo ln -sf /etc/nginx/sites-available/india-travel /etc/nginx/sites-enabled/
        sudo rm -f /etc/nginx/sites-enabled/default
        
        # Test Nginx configuration
        sudo nginx -t
        
        # Restart Nginx
        sudo systemctl restart nginx
        print_success "Nginx configured and restarted"
        
        # Configure firewall
        print_info "Configuring firewall..."
        sudo ufw allow 'Nginx Full' 2>/dev/null || true
        sudo ufw --force enable 2>/dev/null || true
        print_success "Firewall configured"
        
        # Check service status
        if sudo systemctl is-active --quiet india-travel; then
            print_success "Deployment successful!"
            echo ""
            echo "=========================================="
            echo "🎉 Your website is now live!"
            echo "=========================================="
            echo ""
            echo "Access your website at:"
            echo "  → http://$SERVER_IP"
            echo ""
            echo "Useful commands:"
            echo "  Check status:  sudo systemctl status india-travel"
            echo "  View logs:     sudo journalctl -u india-travel -f"
            echo "  Restart:       sudo systemctl restart india-travel"
            echo "  Stop:          sudo systemctl stop india-travel"
            echo ""
        else
            print_error "Service failed to start"
            echo "Check logs with: sudo journalctl -u india-travel -n 50"
            exit 1
        fi
        ;;
    3)
        print_info "Exiting..."
        exit 0
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

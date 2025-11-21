# 🇮🇳 Explore India - Travel Guide Website

A beautiful, interactive travel guide website showcasing India's top 10 tourist destinations with detailed information, interactive maps, and stunning visuals.

## ✨ Features

- **Interactive Map**: Click on map markers to explore destinations
- **Search Functionality**: Real-time search across all destinations
- **Detailed Guides**: Comprehensive information for each destination including:
  - Top highlights and attractions
  - Activities to do
  - Best time to visit
  - How to reach
  - Travel tips
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Modern UI**: Vibrant colors, smooth animations, and glassmorphism effects
- **RESTful API**: Backend API for destination data

## 🎯 Destinations Covered

1. **Ladakh** - Land of High Passes
2. **Spiti Valley** - The Middle Land
3. **Munnar** - Kashmir of South India
4. **Ooty** - Queen of Hill Stations
5. **Gokarna** - Peaceful Beach Paradise
6. **Goa** - India's Beach Capital
7. **Alleppey** - Venice of the East
8. **Hampi** - City of Ruins
9. **Manali** - Valley of the Gods
10. **Shimla** - Queen of Hills

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **Python 3.8+** - Programming language

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with modern features (gradients, animations, flexbox, grid)
- **Vanilla JavaScript** - Interactive functionality
- **Google Fonts (Inter)** - Typography

## 📁 Project Structure

```
india-travel-guide/
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   └── main.js            # Interactive JavaScript
│   └── images/
│       └── destinations/       # Destination images
├── templates/
│   ├── index.html             # Homepage
│   └── destination.html       # Destination detail page
└── README.md                  # This file
```

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd india-travel-guide
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # OR
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to: `http://localhost:5000`

## 🐧 Deployment on Linux VM

### Method 1: Simple Development Server

1. **SSH into your Linux VM**
   ```bash
   ssh username@your-vm-ip
   ```

2. **Update system packages**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

3. **Install Python and pip**
   ```bash
   sudo apt install python3 python3-pip python3-venv -y
   ```

4. **Upload project files to VM**
   ```bash
   # From your local machine
   scp -r india-travel-guide username@your-vm-ip:~/
   ```

5. **Navigate to project directory**
   ```bash
   cd ~/india-travel-guide
   ```

6. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

7. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

8. **Run the application**
   ```bash
   python app.py
   ```

9. **Access the website**
   Open browser and navigate to: `http://your-vm-ip:5000`

### Method 2: Production Deployment with Gunicorn and Nginx

#### Step 1: Install Required Packages

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx -y
```

#### Step 2: Set Up Application

```bash
cd ~/india-travel-guide
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### Step 3: Test Gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

#### Step 4: Create Systemd Service

Create a service file:
```bash
sudo nano /etc/systemd/system/india-travel.service
```

Add the following content:
```ini
[Unit]
Description=India Travel Guide Web Application
After=network.target

[Service]
User=your-username
WorkingDirectory=/home/your-username/india-travel-guide
Environment="PATH=/home/your-username/india-travel-guide/venv/bin"
ExecStart=/home/your-username/india-travel-guide/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

Replace `your-username` with your actual username.

#### Step 5: Start and Enable Service

```bash
sudo systemctl start india-travel
sudo systemctl enable india-travel
sudo systemctl status india-travel
```

#### Step 6: Configure Nginx

Create Nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/india-travel
```

Add the following:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Or your VM IP

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /home/your-username/india-travel-guide/static;
    }
}
```

#### Step 7: Enable Nginx Site

```bash
sudo ln -s /etc/nginx/sites-available/india-travel /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 8: Configure Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

Now access your website at: `http://your-vm-ip` or `http://your-domain.com`

### Method 3: Using Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t india-travel-guide .
docker run -d -p 5000:5000 india-travel-guide
```

## 🔧 Configuration

### Changing Port
Edit `app.py` and modify the last line:
```python
app.run(debug=True, host='0.0.0.0', port=YOUR_PORT)
```

### Adding More Destinations
1. Add destination data to `DESTINATIONS` dictionary in `app.py`
2. Add corresponding image to `static/images/destinations/`
3. Update map marker position in `main.js`

## 📡 API Endpoints

- `GET /` - Homepage
- `GET /destination/<id>` - Destination detail page
- `GET /api/destinations` - Get all destinations (JSON)
- `GET /api/destination/<id>` - Get specific destination (JSON)
- `GET /api/search?q=<query>` - Search destinations (JSON)

## 🎨 Customization

### Colors
Edit CSS variables in `static/css/style.css`:
```css
:root {
    --primary: hsl(200, 95%, 45%);
    --secondary: hsl(280, 70%, 55%);
    /* ... more colors */
}
```

### Images
Replace images in `static/images/destinations/` with your own. Recommended size: 800x600px or higher.

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
sudo lsof -i :5000
# Kill the process
sudo kill -9 <PID>
```

### Permission Denied
```bash
sudo chown -R $USER:$USER ~/india-travel-guide
chmod -R 755 ~/india-travel-guide
```

### Service Not Starting
```bash
# Check logs
sudo journalctl -u india-travel -n 50
# Check service status
sudo systemctl status india-travel
```

### Nginx 502 Bad Gateway
```bash
# Check if Gunicorn is running
sudo systemctl status india-travel
# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

## 📝 Development Notes

- The application runs in debug mode by default. For production, set `debug=False` in `app.py`
- Images are served from the `static/images` directory
- The interactive map uses percentage-based positioning for responsiveness
- Search functionality uses real-time API calls with debouncing

## 🚀 Performance Tips

1. **Enable Gzip Compression** in Nginx
2. **Use CDN** for static assets
3. **Optimize Images** - Use WebP format and compress images
4. **Enable Caching** - Add cache headers in Nginx
5. **Use Production WSGI Server** - Gunicorn with multiple workers

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and enhance this project!

## 📧 Support

For issues or questions, please check the troubleshooting section above.

---

**Made with ❤️ for travelers exploring Incredible India**

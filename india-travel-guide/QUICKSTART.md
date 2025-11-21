# 🚀 Quick Start Guide - India Travel Guide Website

## For Your Linux VM

### Step 1: Transfer Files to Your Linux VM

From your local machine, transfer the entire project folder to your Linux VM:

```bash
# Option 1: Using SCP
scp -r india-travel-guide username@your-vm-ip:~/

# Option 2: Using rsync (if available)
rsync -avz india-travel-guide username@your-vm-ip:~/

# Option 3: Use SFTP or any file transfer tool you prefer
```

### Step 2: SSH into Your Linux VM

```bash
ssh username@your-vm-ip
```

### Step 3: Navigate to Project Directory

```bash
cd ~/india-travel-guide
```

### Step 4: Run the Automated Deployment Script

```bash
chmod +x deploy.sh
./deploy.sh
```

The script will:
- ✓ Update system packages
- ✓ Install Python and dependencies
- ✓ Create virtual environment
- ✓ Install required packages
- ✓ Give you options for deployment

**Choose Option 1** for quick testing (development server)
**Choose Option 2** for production deployment (with Nginx)

---

## Manual Installation (Alternative Method)

If you prefer manual installation:

### 1. Install Python

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

### 2. Create Virtual Environment

```bash
cd ~/india-travel-guide
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

### 5. Access the Website

Open your browser and go to:
```
http://your-vm-ip:5000
```

---

## 🎯 Quick Commands Reference

### Start the Server
```bash
cd ~/india-travel-guide
source venv/bin/activate
python app.py
```

### Stop the Server
Press `Ctrl + C` in the terminal

### Check if Server is Running
```bash
curl http://localhost:5000
```

### View Application Logs (if using systemd service)
```bash
sudo journalctl -u india-travel -f
```

### Restart Service (if using systemd)
```bash
sudo systemctl restart india-travel
```

---

## 🔧 Troubleshooting

### Port 5000 Already in Use?
```bash
# Find what's using port 5000
sudo lsof -i :5000

# Kill the process (replace PID with actual process ID)
sudo kill -9 PID

# Or change the port in app.py (line at the bottom)
```

### Can't Access from Browser?
```bash
# Check if firewall is blocking
sudo ufw status

# Allow port 5000
sudo ufw allow 5000

# Or if using Nginx
sudo ufw allow 'Nginx Full'
```

### Python Module Not Found?
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📱 Testing the Website

Once running, you should see:
- ✓ Homepage with hero section
- ✓ Interactive map with clickable markers
- ✓ Search functionality
- ✓ 10 destination cards
- ✓ Detailed pages for each destination

---

## 🎨 Customization Tips

### Change Images
Replace files in `static/images/destinations/` with your own images:
- ladakh.jpg
- spiti.jpg
- munnar.jpg
- ooty.jpg
- gokarna.jpg
- goa.jpg
- alleppey.jpg
- hampi.jpg
- manali.jpg
- shimla.jpg

### Modify Destination Data
Edit `app.py` and update the `DESTINATIONS` dictionary

### Change Colors
Edit `static/css/style.css` and modify the `:root` variables

---

## 📞 Need Help?

1. Check the main [README.md](README.md) for detailed documentation
2. Review error logs: `sudo journalctl -u india-travel -n 50`
3. Ensure all files are uploaded correctly
4. Verify Python version: `python3 --version` (should be 3.8+)

---

**Happy Traveling! 🇮🇳**

# Odoo 19 Installation Guideline

## 1) Overview
This guide explains a production-oriented installation of **Odoo 19** on Ubuntu Server (22.04/24.04), including PostgreSQL, Python virtual environment, systemd service setup, and Nginx reverse proxy.

> **Audience:** Linux administrators and developers who want a maintainable Odoo deployment.

---

## 2) Prerequisites
- Ubuntu Server 22.04 LTS or 24.04 LTS
- A user with `sudo` privileges
- At least:
  - 2 vCPU
  - 4 GB RAM (8 GB recommended)
  - 20+ GB free disk
- Domain name (optional but recommended for SSL)

---

## 3) Update System Packages
```bash
sudo apt update && sudo apt -y upgrade
sudo reboot
```

---

## 4) Install Required Dependencies
```bash
sudo apt install -y git python3-pip python3-venv python3-dev \
  libxml2-dev libxslt1-dev zlib1g-dev libsasl2-dev libldap2-dev \
  libjpeg-dev libpq-dev libffi-dev libssl-dev build-essential \
  libblas-dev libatlas-base-dev liblcms2-dev libwebp-dev \
  node-less npm wkhtmltopdf
```

> If your distribution package for `wkhtmltopdf` is outdated or has missing patches, install the official patched build.

---

## 5) Install and Configure PostgreSQL
```bash
sudo apt install -y postgresql
sudo -u postgres createuser -s odoo19
```

Optional: set a password for the PostgreSQL role.
```bash
sudo -u postgres psql
ALTER USER odoo19 WITH PASSWORD 'strong_password_here';
\q
```

---

## 6) Create Odoo System User
```bash
sudo useradd -m -d /opt/odoo19 -U -r -s /bin/bash odoo19
```

---

## 7) Download Odoo 19 Source Code
```bash
sudo su - odoo19
git clone https://www.github.com/odoo/odoo --depth 1 --branch 19.0 /opt/odoo19/odoo
exit
```

---

## 8) Create Python Virtual Environment and Install Requirements
```bash
sudo su - odoo19
python3 -m venv /opt/odoo19/venv
source /opt/odoo19/venv/bin/activate
pip install --upgrade pip wheel
pip install -r /opt/odoo19/odoo/requirements.txt
deactivate
exit
```

---

## 9) Create Custom Addons and Log Directories
```bash
sudo mkdir -p /opt/odoo19/custom-addons
sudo mkdir -p /var/log/odoo19
sudo chown -R odoo19:odoo19 /opt/odoo19 /var/log/odoo19
```

---

## 10) Create Odoo Configuration File
Create `/etc/odoo19.conf`:

```ini
[options]
admin_passwd = change_this_master_password
db_host = False
db_port = False
db_user = odoo19
db_password = False
addons_path = /opt/odoo19/odoo/addons,/opt/odoo19/custom-addons
logfile = /var/log/odoo19/odoo.log
xmlrpc_port = 8069
proxy_mode = True
```

Set secure permissions:
```bash
sudo chown odoo19: /etc/odoo19.conf
sudo chmod 640 /etc/odoo19.conf
```

---

## 11) Create systemd Service
Create `/etc/systemd/system/odoo19.service`:

```ini
[Unit]
Description=Odoo19
Requires=postgresql.service
After=network.target postgresql.service

[Service]
Type=simple
User=odoo19
Group=odoo19
ExecStart=/opt/odoo19/venv/bin/python3 /opt/odoo19/odoo/odoo-bin -c /etc/odoo19.conf
StandardOutput=journal+console

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now odoo19
sudo systemctl status odoo19
```

---

## 12) Configure Nginx Reverse Proxy (Recommended)
Install Nginx:
```bash
sudo apt install -y nginx
```

Create `/etc/nginx/sites-available/odoo19`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    proxy_read_timeout 720s;
    proxy_connect_timeout 720s;
    proxy_send_timeout 720s;

    client_max_body_size 200m;

    location / {
        proxy_pass http://127.0.0.1:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/odoo19 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 13) Enable SSL with Let's Encrypt (Optional, Recommended)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 14) Access Odoo
- URL: `http://your-server-ip:8069` (direct) or `https://your-domain.com` (via Nginx + SSL)
- Create database from the setup page.
- Set strong admin credentials.

---

## 15) Basic Troubleshooting
### Check service logs
```bash
sudo journalctl -u odoo19 -f
```

### Check Odoo log file
```bash
sudo tail -f /var/log/odoo19/odoo.log
```

### Common issues
- **Port 8069 in use**: change `xmlrpc_port` in config.
- **Permission denied**: verify ownership of `/opt/odoo19` and `/var/log/odoo19`.
- **502 Bad Gateway**: verify Odoo service is running and Nginx proxy target is `127.0.0.1:8069`.

---

## 16) Post-Installation Hardening Checklist
- Change `admin_passwd` in `/etc/odoo19.conf`.
- Use a strong PostgreSQL password and restrict DB access.
- Enable firewall (`ufw`) and allow only required ports.
- Keep packages and Odoo code updated.
- Back up PostgreSQL databases and filestore regularly.

---

## 17) Maintenance Commands
Restart Odoo:
```bash
sudo systemctl restart odoo19
```

Update Odoo code (manual example):
```bash
sudo su - odoo19
cd /opt/odoo19/odoo
git pull
source /opt/odoo19/venv/bin/activate
pip install -r requirements.txt
deactivate
exit
sudo systemctl restart odoo19
```

---

## Notes
- This is a generic guideline and may need adaptation for your hosting provider and security policy.
- For enterprise deployments, consider staging, monitoring, backups, and CI/CD-based update flows.

# Odoo 18 Installation Process

## 1) Overview
This guide explains a production-oriented installation of **Odoo 18** on Ubuntu Server (22.04/24.04), including PostgreSQL, Python virtual environment, systemd service setup, and Nginx reverse proxy.

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
sudo -u postgres createuser -s odoo18
```

Optional: set a password for the PostgreSQL role.
```bash
sudo -u postgres psql
ALTER USER odoo18 WITH PASSWORD 'strong_password_here';
\q
```

---

## 6) Create Odoo System User
```bash
sudo useradd -m -d /opt/odoo18 -U -r -s /bin/bash odoo18
```

---

## 7) Download Odoo 18 Source Code
```bash
sudo su - odoo18
git clone https://www.github.com/odoo/odoo --depth 1 --branch 18.0 /opt/odoo18/odoo
exit
```

---

## 8) Create Python Virtual Environment and Install Requirements
```bash
sudo su - odoo18
python3 -m venv /opt/odoo18/venv
source /opt/odoo18/venv/bin/activate
pip install --upgrade pip wheel
pip install -r /opt/odoo18/odoo/requirements.txt
deactivate
exit
```

---

## 9) Create Custom Addons and Log Directories
```bash
sudo mkdir -p /opt/odoo18/custom-addons
sudo mkdir -p /var/log/odoo18
sudo chown -R odoo18:odoo18 /opt/odoo18 /var/log/odoo18
```

---

## 10) Create Odoo Configuration File
Create `/etc/odoo18.conf`:

```ini
[options]
admin_passwd = change_this_master_password
db_host = False
db_port = False
db_user = odoo18
db_password = False
addons_path = /opt/odoo18/odoo/addons,/opt/odoo18/custom-addons
logfile = /var/log/odoo18/odoo.log
xmlrpc_port = 8069
proxy_mode = True
```

Set secure permissions:
```bash
sudo chown odoo18: /etc/odoo18.conf
sudo chmod 640 /etc/odoo18.conf
```

---

## 11) Create systemd Service
Create `/etc/systemd/system/odoo18.service`:

```ini
[Unit]
Description=Odoo18
Requires=postgresql.service
After=network.target postgresql.service

[Service]
Type=simple
User=odoo18
Group=odoo18
ExecStart=/opt/odoo18/venv/bin/python3 /opt/odoo18/odoo/odoo-bin -c /etc/odoo18.conf
StandardOutput=journal+console

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now odoo18
sudo systemctl status odoo18
```

---

## 12) Configure Nginx Reverse Proxy (Recommended)
Install Nginx:
```bash
sudo apt install -y nginx
```

Create `/etc/nginx/sites-available/odoo18`:

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
sudo ln -s /etc/nginx/sites-available/odoo18 /etc/nginx/sites-enabled/
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
sudo journalctl -u odoo18 -f
```

### Check Odoo log file
```bash
sudo tail -f /var/log/odoo18/odoo.log
```

### Common issues
- **Port 8069 in use**: change `xmlrpc_port` in config.
- **Permission denied**: verify ownership of `/opt/odoo18` and `/var/log/odoo18`.
- **502 Bad Gateway**: verify Odoo service is running and Nginx proxy target is `127.0.0.1:8069`.

---

## 16) Post-Installation Hardening Checklist
- Change `admin_passwd` in `/etc/odoo18.conf`.
- Use a strong PostgreSQL password and restrict DB access.
- Enable firewall (`ufw`) and allow only required ports.
- Keep packages and Odoo code updated.
- Back up PostgreSQL databases and filestore regularly.

---

## 17) Maintenance Commands
Restart Odoo:
```bash
sudo systemctl restart odoo18
```

Update Odoo code (manual example):
```bash
sudo su - odoo18
cd /opt/odoo18/odoo
git pull
source /opt/odoo18/venv/bin/activate
pip install -r requirements.txt
deactivate
exit
sudo systemctl restart odoo18
```

---

## Notes
- This is a generic guideline and may need adaptation for your hosting provider and security policy.
- For enterprise deployments, consider staging, monitoring, backups, and CI/CD-based update flows.

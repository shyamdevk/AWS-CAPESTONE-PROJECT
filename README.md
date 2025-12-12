# **Production-Grade Django Deployment on AWS**

This project demonstrates how to deploy a **production-ready Django web application** on **Amazon Web Services (AWS)** using best practices for scalability, security, high availability, monitoring, and performance.
The goal is to build a **real-world cloud infrastructure**, not just a simple app deployment.

---

## 🚀 **Project Overview**

The Django application is deployed on EC2 instances with **Gunicorn** as the WSGI server and **Nginx** as the reverse proxy.
Instances run inside **private subnets**, while an **Application Load Balancer (ALB)** in public subnets routes all external traffic securely.

A **Launch Template**, combined with an **Auto Scaling Group (ASG)**, ensures the app scales automatically based on demand.

Logs are centrally stored in **Amazon S3**, and network traffic to S3 remains private using a **VPC Gateway Endpoint**.

A **custom domain** is managed via **Route 53**, secured using **ACM SSL certificates**, and accelerated globally using **CloudFront CDN**.

**CloudWatch + SNS** provide real-time monitoring and alerting for system health.

---

## 🏗️ **Architecture Summary**

The infrastructure includes:

* **VPC with 2 public + 4 private subnets**
* **EC2 (Ubuntu) with Django, Gunicorn, and Nginx**
* **Auto Scaling Group (ASG) & Launch Template**
* **Application Load Balancer (ALB)**
* **Amazon RDS (MySQL)**
* **S3 bucket for logs**
* **VPC Gateway Endpoint for secure S3 access**
* **Route 53 for DNS**
* **ACM for HTTPS certificates**
* **CloudFront for global caching and security**
* **CloudWatch + SNS for alarms and notifications**

This architecture ensures:

✔ High availability
✔ Zero hardcoded credentials (IAM roles used)
✔ Secure private networking
✔ Automatic scaling
✔ Centralized logging & monitoring
✔ Low-latency global delivery

---

## 🔧 **Key Features**

### **1. EC2 Hosting with Django**

* Django app running on Ubuntu EC2
* Gunicorn as WSGI server
* Nginx as reverse proxy & static file server
* Unix socket configuration for fast and secure inter-process communication

### **2. Managed MySQL Database (RDS)**

* Secure private subnet placement
* Multi-AZ support
* Automated backups
* Connectivity restricted only to EC2 SG

### **3. Auto Scaling & Load Balancing**

* Launch Template created from custom AMI
* ASG deployed in private subnets
* ALB handles public traffic and health checks

### **4. Secure Logging with S3**

* Application & access logs stored in Amazon S3
* VPC Endpoint ensures logs never travel over the public internet

### **5. Custom Domain + HTTPS**

* DNS migrated from GoDaddy to Route 53
* Free SSL certificate issued using AWS ACM
* ALB configured with HTTPS listener (443)
* CloudFront distribution added for global performance

### **6. Monitoring & Alerts**

* CloudWatch metrics for EC2, RDS, ALB
* Alarms trigger when thresholds exceed (e.g., high CPU)
* SNS sends instant notifications (Email/SMS)

---

## 📦 **Technologies Used**

| Component      | Service                                       |
| -------------- | --------------------------------------------- |
| Compute        | EC2, Auto Scaling, Launch Templates           |
| Networking     | VPC, Subnets, IGW, NAT Gateway, VPC Endpoints |
| Load Balancing | Application Load Balancer (ALB)               |
| Database       | Amazon RDS (MySQL)                            |
| Storage        | Amazon S3                                     |
| DNS & CDN      | Route 53, CloudFront                          |
| Security       | IAM Roles, Security Groups, ACM SSL           |
| Monitoring     | CloudWatch, SNS                               |

---

## 📁 **Project Goal**

To simulate a **real production deployment**, covering:

* End-to-end AWS infrastructure setup
* Fully automated scaling
* Secure private networking
* HTTPS configuration
* Logging, monitoring, and alerting
* Best practices for cloud application hosting

---

# 🚀 **AWS Service Configuration**

## 🟦 **Step 1: VPC and Subnet Configuration**

We start by creating a **Virtual Private Cloud (VPC)**.
A VPC is like your **own private network inside AWS** where all your cloud resources live.

### 🔹 **What we created inside the VPC?**

We created a total of **6 subnets**:

### 🌐 **1. Public Subnets (2)**

These subnets are **open to the internet** and are used for the:

* **Application Load Balancer (ALB)**
  The ALB is the **entry point** to your application.
  When a user opens your website, their request first reaches the ALB.

### 🔐 **2. Private Subnets (4)**

These subnets are **not directly exposed to the internet**, providing higher security.

They are used for:

* **Auto Scaling Group (ASG)** → runs multiple EC2 instances that host the Django application
* **Amazon RDS (MySQL)** → stores your application's data securely

---

## 🔒 **Why Private Subnets?**

EC2 instances inside private subnets:

* ❌ Cannot be accessed directly from the internet
* ✔ Can be accessed only through the **Load Balancer**
* ✔ Are much more secure because they stay hidden

This is how most **production systems** are deployed.

---

## 🌍 **NAT Gateway (For Outbound Access)**

Even though our EC2 instances are in private subnets, they still need internet access for:

* Installing software updates
* Downloading packages
* Connecting to external services

To allow *secure outbound* access, we use a:

### 🔸 **NAT Gateway** (in a public subnet)

This works like a **one-way door**:

* EC2 → Internet (allowed)
* Internet → EC2 (blocked)

This keeps the servers safe while still letting them update software.

---

## 📦 **S3 Gateway VPC Endpoint**

To enhance security even more, we add a:

### 🔸 **VPC Endpoint for Amazon S3**

This allows EC2 instances to connect to S3 **privately**, without using the public internet.

This helps when:

* Storing logs
* Uploading files
* Sending backups

### 💡 **Why use a VPC Endpoint?**

* More secure
* Faster
* No public traffic involved
* Reduced AWS data transfer cost

---
![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/vpc.png)
The above diagram illustrates the architectural layout of the VPC and its associated
resources.

# 🟦 **Step 2: RDS Configuration for MySQL**

In this step, we create a **managed MySQL database** using **Amazon RDS**.
RDS takes care of backups, updates, security, and high availability — perfect for production use.

---

## 🗄️ **Why use RDS instead of installing MySQL on EC2?**

* ✔ Automatically managed by AWS
* ✔ Built-in backups
* ✔ High availability (Multi-AZ)
* ✔ Better performance
* ✔ More secure

---

## 🛠️ **How to Create the RDS MySQL Database (Simple Steps)**

### **1️⃣ Open RDS**

* Go to the AWS Console
* Search **RDS**
* Click **Create Database**

---

### **2️⃣ Choose the Engine**

* Select **MySQL**
* Choose the **latest version** (example: MySQL 8.0)

---

### **3️⃣ Choose Creation Method**

* Choose **Standard Create**
* Select **Production Template**

  * This provides better performance & reliability

---

### **4️⃣ Basic Settings**

Fill in:

| Setting                | Example                        |
| ---------------------- | ------------------------------ |
| DB Instance Identifier | `sample-prod-db`               |
| Master Username        | `admin`                        |
| Password               | Strong password (store safely) |

---

### **5️⃣ Instance Size**

Choose an instance type based on your needs:

* Recommended: **db.t3.medium**

This offers a balance of performance and cost.

---

### **6️⃣ Storage**

* Start with **20 GB**
* Enable **Storage Autoscaling** (grows automatically when needed)

---

### **7️⃣ High Availability (Important for Production)**

* Enable **Multi-AZ Deployment** → RDS will create a standby replica
* Turn on **Automatic Backups** → e.g., 7-day retention

---

## 🔐 **8️⃣ Connectivity (Very Important)**

### **✔ Choose the same VPC as your EC2 servers**

This ensures your app and database are on the same network.

### **✔ Use a *Private Subnet Group***
![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/sub1.png)
![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/sub2.png)
This keeps your database **not exposed to the internet**.

### **✔ Configure Security Group**

Allow **port 3306** (MySQL) only from your **EC2's security group**.

This prevents unknown IPs from accessing your DB.

---

## 🔑 **9️⃣ Authentication Options**

* Use **Password Authentication**
* (Optional) You can use **IAM authentication** later

---

## 🚀 **🔟 Launch the Database**

* Click **Create Database**
* Wait until status becomes **Available**

### 📌 Copy the **Endpoint URL**

Example:

```
sample-prod-db.cwfcqugwafxx.us-east-1.rds.amazonaws.com
```

You will paste this inside your Django `settings.py` under:

```python
DATABASES = { ... }
```

---

# 🟦 **Step 3: Configuring Auto Scaling Group (ASG)**

To make our Django application **highly available and scalable**, we use an **Auto Scaling Group (ASG)**.
ASG automatically **adds more EC2 instances** when traffic increases and **removes them** when traffic is low — saving cost and improving performance.

Before creating the ASG, we must first **set up the application on a temporary EC2 instance**.
This EC2 instance will later be used to create an AMI (image), which the ASG will use to launch identical servers.

---

# 🟩 **Step 3.1 — Application Setup on EC2 Instance**

We begin by launching an **Ubuntu EC2 instance** and install everything needed to run Django.

---

## 🛠️ **1️⃣ Update the Server**

Always update the packages first:

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 🧬 **2️⃣ Clone Your Django Project**

Download your project from GitHub:

```bash
git clone https://github.com/shyamdevk/art.git
```

---

## 📦 **3️⃣ Install Python, Nginx, and Required Dependencies**

Run:

```bash
sudo apt install python3-pip python3-dev nginx default-libmysqlclient-dev pkg-config build-essential mysql-server -y
```

This installs:

* Python
* pip
* MySQL client libraries
* Nginx (web server)
* Build tools

---

## 🗄️ **4️⃣ Connect EC2 to Your RDS MySQL Database**

Before connecting:

✔ Ensure EC2 and RDS are in the **same VPC**
✔ Ensure RDS security group allows **port 3306** from your EC2 SG

### 👉 Test database connection:

```bash
mysql -h <rds-endpoint> -u <username> -p
```

### Create the database for Django:

```sql
CREATE DATABASE art;
```

(Here, **art** is the database name used in the project)

Then exit:

```sql
exit;
```

---

## 🧪 **5️⃣ Create and Activate Python Virtual Environment**

### Install venv:

```bash
sudo apt install python3-venv -y
```

### Create environment:

```bash
python3 -m venv env
```

### Activate it:

```bash
source env/bin/activate
```

### Install requirements:

```bash
pip install -r requirements.txt
```

---

## 🔗 **6️⃣ Connect Django to RDS**

Open your project’s `settings.py` file:

```bash
nano art/settings.py
```

Update the `DATABASES` section:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'art',
        'USER': '<your-db-username>',
        'PASSWORD': '<your-db-password>',
        'HOST': '<your-rds-endpoint>',
        'PORT': '3306',
    }
}
```

---

## 🧱 **7️⃣ Apply Migrations**

Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the required database tables inside RDS.

---

## 🟩 **Collecting Static Files (collectstatic)**

```bash
python3 manage.py collectstatic
```
* Searches all Django apps for static files
* Copies them into the folder defined in `STATIC_ROOT`
* Prepares them to be served by **Nginx** (since Gunicorn cannot serve static files)

### Example output:

```
176 static files copied to '/home/ubuntu/art/staticfiles'
```

# 🟦 **Step 3.1 (Continued) — Install & Test Gunicorn**

After running Django migrations, we now install **Gunicorn**, which is the production-grade WSGI server used to run Django behind Nginx.

---

## 🧱 **Why Gunicorn?**

Gunicorn is a lightweight and fast server that runs your Django application.
It acts as a **bridge between Django and Nginx**.

### ✔ Benefits of Gunicorn

* Easy to configure
* Supports multiple workers (better performance)
* Works perfectly behind Nginx
* Stable and commonly used in production

⚠️ Note:
Gunicorn **cannot serve static files** (CSS, JS, images).
Nginx will handle those later.

---

## 🛠️ **1️⃣ Install Gunicorn**

Activate your virtual environment first:

```bash
source env/bin/activate
```

Then install Gunicorn:

```bash
pip install gunicorn django
```

Now Gunicorn and Django are installed on your EC2 instance.

---

## 🧪 **2️⃣ Test Gunicorn With Your Django App**

Navigate to your Django project folder (where `manage.py` exists):

```bash
cd ~/art
```

Run Gunicorn:

```bash
gunicorn --bind 0.0.0.0:8000 art.wsgi:application
```

### What this means:

* **0.0.0.0:8000** → Gunicorn listens on port 8000
* **art.wsgi:application** → loads your Django project’s WSGI file

---

## 🌐 **3️⃣ Access the Website via Public IP**

Open this in your browser:

```
http://<your-ec2-public-ip>:8000
```

### Make sure:

✔ Port **8000** is allowed in your EC2 Security Group
✔ Gunicorn is running in the terminal

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/signin.png)
Now if you access the website you cant see the static files like images, this is because the
gunicorn server is cant serve the static files .

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/interface.png)
For that we will be using nginx also we will configure nginx as a proxy server



## 🟦 **Setting Up Nginx With Gunicorn (Using Unix Socket)**

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/nginx.png)

To run Django in production, we use **Gunicorn** as the app server and **Nginx** as the web server.

* **Gunicorn** runs your Django code
* **Nginx** receives incoming HTTP requests and forwards them to Gunicorn
* Nginx also serves **static files** (CSS, JS, images), which Gunicorn cannot do

---

## 🧩 **Why Use a Unix Socket Instead of Port 8000?**

Gunicorn and Nginx can communicate in two ways:

✔ Using a port (like `127.0.0.1:8000`)
✔ Using a **Unix socket file** (example: `/home/ubuntu/art/art.sock`)

We choose **Unix socket** because it is:

### 🚀 1. **Faster**

* No networking involved
* Lower latency
* More efficient communication

### 🔐 2. **More Secure**

* Socket file exists only on the server
* Cannot be accessed from the internet
* Reduces attack surface

### 🔧 3. **Simpler**

* No IP or port configuration needed
* Perfect when Gunicorn and Nginx run on the same EC2 instance

### 💾 4. **Uses Fewer Resources**

* Less load on the system
* Better performance

### ⚙️ 5. **Works Well With systemd**

* Easy to manage
* Auto restarts on failure
* Automatically recreates the socket

---

## ⚠️ When NOT to Use a Socket

Use **TCP/IP ports** instead if:

* Gunicorn and Nginx run on **different servers**
* You plan to **load balance Gunicorn** across multiple machines

---

## 🛠️ **Create Gunicorn Systemd Service (Using Socket)**

This allows Gunicorn to run continuously in the background and start automatically on reboot.

### ✏️ Create service file:

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

### 🔧 Add this configuration:

```ini
[Unit]
Description=Gunicorn daemon for Django project
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/yourproject
ExecStart=/home/ubuntu/yourproject/env/bin/gunicorn \
--workers 3 \
--bind unix:/home/ubuntu/yourproject/yourproject.sock \
yourproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

```
WorkingDirectory=/home/ubuntu/yourproject
```

This tells systemd **where your Django project is located**.

👉 It must be the folder where your **manage.py** file exists.

---

### 🔹 **ExecStart**

```
ExecStart=/home/ubuntu/yourproject/env/bin/gunicorn --workers 3 ...
```

This command:

* Starts Gunicorn
* Uses **3 worker processes** (good for handling multiple users)
* Runs your Django application in production mode

Think of this as the command that launches your Django server.

---

### 🔹 **--bind unix:/path/to/project.sock**

```
--bind unix:/home/ubuntu/yourproject/yourproject.sock
```

This tells Gunicorn:

> “Instead of running on a port like 8000, create a **Unix socket file**.”

The socket file acts like a **private communication channel** between Nginx and Gunicorn.

---

## 🟦 **Start Gunicorn Service & Configure Nginx**

After creating the `gunicorn.service` file, we need to **reload systemd** and start Gunicorn.

---

## 🟩 **1️⃣ Reload and Start Gunicorn**

Run these commands:

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### ✔ What these commands do?

* **daemon-reload** → Tells systemd about the new service file
* **start gunicorn** → Starts Gunicorn immediately
* **enable gunicorn** → Starts Gunicorn automatically on system reboot

---

## 🧪 **2️⃣ Check if Gunicorn is Running**

```bash
sudo systemctl status gunicorn
```

You should see it **active (running)** and your socket file created.

---

## 🟦 **3️⃣ Configure Nginx to Use the Gunicorn Socket**

Open the Nginx site configuration:

```bash
sudo nano /etc/nginx/sites-available/art
```

Add your server block (example):

```nginx
server {
    listen 80;
    server_name 54.90.204.232;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/ubuntu/art/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/art/art.sock;
    }
}
```

### ✔ What this does?

* Serves **static files** directly from the `staticfiles` folder
* Sends all other web requests to **Gunicorn via the socket file**

---

## 🔗 **4️⃣ Enable the Nginx Site & Reload Nginx**

Run:

```bash
sudo ln -s /etc/nginx/sites-available/art /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### ✔ Explanation:

* Creates a symlink to enable your config
* Tests if the Nginx config is valid
* Restarts Nginx to apply changes

---

## ⚠️ **Fixing 502 Bad Gateway (If You See It)**

A 502 error usually means **Nginx can't talk to Gunicorn**.

Fix permissions on the socket:

```bash
sudo chown ubuntu:www-data /home/ubuntu/art/art.sock
sudo chmod 770 /home/ubuntu/art/art.sock
```

Also make sure directories are accessible:

```bash
sudo chmod o+x /home
sudo chmod o+x /home/ubuntu
sudo chmod o+x /home/ubuntu/art
```

---

## 🔁 **Restart Gunicorn and Nginx Again**

```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## 🎉 **5️⃣ Access Your Website**

Now open your **EC2 public IP** in the browser:

```
http://<your-public-ip>
```

You should see your Django website fully working with:

* Static files (images, CSS)
* Faster performance
* Nginx + Gunicorn handling all traffic

---

---

# 🟦 **Using Custom Domain + Auto Scaling Setup**

## 🟩 **1️⃣ Use a Custom Domain Instead of EC2 Public IP**

Instead of accessing your website using:

```
http://<ec2-public-ip>
```

You can use a **custom domain** (example: `mysite.com`) by moving DNS from GoDaddy to **AWS Route 53**.

### ✏️ Update Nginx to Use Your Domain

Open the Nginx config:

```bash
sudo nano /etc/nginx/sites-available/art
```

Update this line:

```nginx
server_name mysite.com www.mysite.com;
```
![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/domain.png)

Save the file and restart services:

```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

Your website will now load using your **domain name**.

---

# 🟦 **2️⃣ Create AMI for Auto Scaling**

To prepare for auto scaling, AWS requires a **Launch Template**, which is created using an **AMI (Amazon Machine Image)** of your configured EC2 instance.

This ensures every new EC2 instance:

* Has Django installed
* Has Nginx + Gunicorn configured
* Is connected to RDS
* Has static files collected
* Is production-ready

### ✔ Steps:

1. Go to EC2 → Instances
2. Select your fully working instance
3. Click **Actions → Image and Templates → Create Image (AMI)**
4. Give it a name and save

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/ami.png)

This AMI is now used to launch identical servers automatically.

---

# 🟦 **Step 3.2 — Create Launch Template with IAM Role (For S3 Logs)**

Now create a **Launch Template** using the AMI you created.

### While creating the Launch Template:

### ✔ 1. Select Your AMI

Choose the image you created earlier.

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/lt.png)

### ✔ 2. Attach an IAM Role

The role should allow EC2 to write logs to S3 using the **VPC Endpoint**.

This makes log upload:

* Secure (no public internet)
* Faster
* Cheaper

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/lt2.png)

### ✔ 3. Configure Security Groups

Allow only required communication:

* ALB → EC2 (HTTP 80)
* EC2 → RDS (3306)
* EC2 → S3 (via VPC endpoint)

The launch template ensures **every EC2 instance launched by the ASG is identical and secure**.

---

# 🟦 **Step 3.3 — Create Auto Scaling Group (ASG) with Load Balancer**

Auto Scaling ensures your application is:

✔ Highly available
✔ Automatically scalable
✔ Self-healing (replaces failed instances)

---

## 🔧 Steps to Create ASG

### **1️⃣ Choose the Launch Template**

Select the template created in the previous step.

### **2️⃣ Select VPC & Subnets**

* Choose your VPC
* Select **private subnets** (for security)

Your app servers should *never* be directly exposed to the internet.

---

## 🟦 **3️⃣ Attach Application Load Balancer (ALB)**

The ALB will:

* Receive all incoming traffic
* Distribute it to multiple EC2 instances
* Perform health checks
* Improve reliability

### Steps:

* Select an existing ALB (or create a new one)
* ALB must be placed in **public subnets**
* Register ASG with the **target group** of the ALB

This ensures:

* Traffic → ALB (public) → EC2 (private)
* Only ALB communicates with EC2
* EC2 remains protected

---

# 🔐 **Security & High Availability Notes**

* ALB ensures outside traffic never reaches EC2 directly
* EC2 in private subnets increases security
* IAM role ensures EC2 logs are stored in S3 privately
* ASG ensures the app scales automatically during high traffic
* If an instance fails, ASG launches a new one automatically

---

# 🟦 **Step 4: Store Logs Securely Using S3 Gateway VPC Endpoint**

We want ALB (Application Load Balancer) logs to be stored in an **S3 bucket** without using the public internet.
To do this, we use an **S3 Gateway VPC Endpoint**.

### ✔ Why use an S3 VPC Endpoint?

* Logs are transferred **privately**
* More secure
* Faster
* Reduces cost (no NAT traffic)

### 🛠️ Steps:

1. Create an **S3 bucket** (example: `myapp-alb-logs`)
2. Go to **EC2 → Load Balancers → Select your ALB**
3. Open the **Attributes** tab

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/lb.png)

5. Turn ON **Access Logs**

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/lb1.png)

7. Choose your S3 bucket
8. (Optional) Add a prefix like:

   ```
   alb/logs/
   ```

Now all ALB logs are stored safely in your S3 bucket.

---

# 🟦 **Step 5: Migrate DNS From GoDaddy to AWS Route 53**

To use your custom domain (example: `mysample.xyz`) with your AWS website, we move DNS control to **Route 53**.

---

## 🛠️ Create a Hosted Zone in Route 53

1. Go to **Route 53 console**
2. Click **Hosted Zones → Create Hosted Zone**
3. Enter:

   * **Domain Name:** `mysample.xyz`
   * **Type:** Public Hosted Zone
  
![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/hz.png)

4. Click **Create**

Route 53 will now show **4 Name Servers (NS records)**.

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/hz1.png)

Copy them.

---

## 🔄 Update GoDaddy DNS to Use Route 53

1. Open **GoDaddy Domain Manager**
2. Select your domain
3. Go to **DNS → Nameservers**

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/gd.png)
   
5. Click **Change**
6. Select **Enter my own nameservers (Advanced)**
7. Paste the **4 NS values** from Route 53

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/gd1.png)

9. Click **Save**

Your domain is now fully managed by AWS Route 53.

---

# 🟦 **Step 6: Issue SSL Certificate Using AWS ACM (HTTPS)**

To secure your website with **HTTPS**, we use **AWS Certificate Manager (ACM)**, which provides **free SSL certificates**.

> ⚠️ Important: ACM certificate for CloudFront must be created in **us-east-1 (N. Virginia)**.

---

## 🛠️ Request an ACM Certificate

1. Open **ACM console**
2. Switch region to **N. Virginia (us-east-1)**
3. Click **Request a Certificate**
4. Choose **Public Certificate**
5. Add your domain:

   ```
   mysample.xyz
   ```
![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/acm.png)

6. Choose **DNS Validation**

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/acm1.png)

8. Click **Request**

---

## 🔐 Validate the Certificate

ACM shows a **CNAME record** that must be added to Route 53.

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/acm2.png)

If hosted in Route 53:

* Click **Create record in Route 53**
  ACM will add it automatically.

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/acm3.png)

After a few minutes, the certificate status becomes **Issued**.

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/acm4.png)

---

# 🟦 **Enable HTTPS on Application Load Balancer (Port 443)**

Now we attach the SSL certificate to the ALB.

### 🛠️ Steps:

1. Go to **EC2 → Load Balancers**
2. Select your ALB
3. Open the **Listeners** tab
4. Click **Add Listener**
5. Choose:

   * **Protocol:** HTTPS
   * **Port:** 443

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/acm5.png)

6. Select the **ACM certificate** you created
7. Save

Now your ALB has:

* HTTP listener → Port 80
* HTTPS listener → Port 443

![Proj-img](https://github.com/shyamdevk/AWS-CAPESTONE-PROJECT/blob/images/acm6.png)

Your website can now be accessed securely with **HTTPS**.

---



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



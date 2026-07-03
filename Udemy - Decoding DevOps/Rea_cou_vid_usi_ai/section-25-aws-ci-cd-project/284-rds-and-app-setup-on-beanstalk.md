# 🎓 Deep Learning Material: RDS Database Setup & Initialization for Beanstalk Application

*Reconstructed from video lecture captions (284-rds-and-app-setup-on-beanstalk.txt)*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Why the Application Needs a Separate Database Service

The lecture picks up from a point where an **Elastic Beanstalk application environment** has already been created. Beanstalk has provisioned the compute layer — two EC2 instances behind a load balancer — but the vprofile application requires a **relational database** to store its application tables. The instructor's decision is to create this database as a **separate Amazon RDS instance** rather than running a database directly on the EC2 instances. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

This architectural separation is fundamental. The application runs on Beanstalk (compute), and the data lives in RDS (database). They are independent AWS services that communicate over the network. The Beanstalk environment can be torn down and recreated without losing data. The RDS instance can be scaled, backed up, or migrated independently of the application servers. This is the standard pattern for production applications on AWS: **decouple compute from data**. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

***

## 1.2 Amazon RDS: Managed Database as a Service

Amazon RDS (Relational Database Service) provides managed database instances. The instructor creates a **MySQL** instance (engine version **8.0.35**). The key RDS configuration decisions made in the lecture: [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

* **Template:** Free Tier — constrains instance type and storage to free-tier-eligible options, preventing accidental cost
* **DB Instance Identifier:** `vprords` — the name that identifies this database instance in the AWS console
* **Master Username:** `admin` — the superuser account for database administration
* **Password:** Auto-generated — AWS creates a strong random password
* **Instance Type:** t3.micro or t2.micro — automatically selected by free tier template
* **Storage:** 20 GB General Purpose (minimum for free tier)
* **Public Access:** No — the database is not accessible from the internet, only from within the VPC
* **Security Group:** Create new — named `vprords-sg`
* **Port:** 3306 (MySQL default)
* **Initial Database Name:** `accounts` — this creates an empty database named "accounts" during RDS provisioning

The **initial database name** (`accounts`) is particularly important. The instructor explains: *"Our vprofile application needs the DB name as accounts, so we need to create that."*   Without specifying this during creation, you'd have to manually connect and create the database later. Providing it upfront means RDS creates the empty `accounts` database as part of the provisioning process. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

***

## 1.3 Credential Management: The Auto-Generate Pattern and Its Critical Warning

The instructor chooses **auto-generate password** for the RDS master credentials. This produces a strong random password, but it introduces a critical operational risk that the instructor warns about emphatically: [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

*"Here you will see 'view credential details.' Make sure you do that and you copy this password and store it somewhere... The problem is if you do not save this now and if you close this, then there is no way of retrieving the credentials back. You have to reset the credentials."* [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

The auto-generated password is shown **exactly once** — in a popup/banner immediately after database creation. If you close that banner without copying the password, it's gone forever. Your only recovery option is to wait for the instance to become available and then **reset the master credentials** through the RDS settings. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

The instructor stores the password in **Sticky Notes** temporarily. He also later demonstrates a second critical security lesson: he shows the password in the command line and immediately acknowledges this is bad practice — *"Giving password like that in the command line is a very bad idea."* He explains the correct approach: use `-p` without the password value, and MySQL will prompt you to enter it invisibly. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

⚠️ **Expert Note:**
In production, database credentials should never be in sticky notes, command-line history, or scripts. They belong in a secrets manager (AWS Secrets Manager, SSM Parameter Store, HashiCorp Vault). The auto-generate feature is good for creating strong passwords, but the credential lifecycle must be managed properly — store in secrets manager immediately, rotate periodically, and never expose in logs or CLI history.

***

## 1.4 Security Group Inter-Linking: How Beanstalk Instances Connect to RDS

This is the most architecturally important concept in the lecture. The Beanstalk EC2 instances need to connect to the RDS instance on port 3306 (MySQL). By default, the RDS security group **blocks all inbound traffic** — no one can connect. You must explicitly create a rule that allows the right source to connect. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

The instructor's approach is **security-group-to-security-group referencing** — instead of allowing a specific IP address, you allow an entire security group as the source. The logic: [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

1. Beanstalk created its own security groups — one for the **load balancer** and one for the **EC2 instances**
2. The RDS instance has its own security group (`vprords-sg`)
3. The instructor copies the **security group ID** of the Beanstalk instance security group
4. He then edits the **RDS security group's inbound rules** to add: port 3306, source = Beanstalk instance security group ID

The result: *"Our Beanstalk instance can connect to RDS instance on port 3306."* [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

This approach is superior to using IP addresses because:

* Beanstalk instances can be terminated and replaced (auto-scaling, deployments) — their IP addresses change, but they always belong to the same security group
* Any instance launched by Beanstalk automatically inherits the Beanstalk security group, so it automatically gets database access without any rule changes

The instructor also highlights that Beanstalk creates **two security groups** and you must identify the correct one: *"One is for the load balancer and this one, this is for the instance."*  The load balancer doesn't need database access — only the EC2 instances do. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

🔍 **Deep Dive:**
Security group referencing creates a **dynamic trust relationship**. The RDS rule doesn't say "allow 10.0.1.15" — it says "allow any instance that belongs to security group sg-xxxx." This is declarative security: you define *who* can connect by identity (group membership), not by address. When Beanstalk scales out and adds a third instance, that instance automatically gets database access because it inherits the same security group. When an instance is terminated, its access is automatically revoked. No rule changes needed at any point. This is the standard AWS pattern for inter-service network authorization.

***

## 1.5 Database Initialization: Schema Before Application

The RDS instance was created with an empty `accounts` database. But the vprofile application expects **tables** (schemas) to exist in that database. Without tables, the application would start but fail when trying to query or write data. The database must be **initialized** with the correct schema before the application is deployed. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

The schema is stored as a SQL file (`db_backup.sql`) in the application's **source code repository** — specifically at `src/main/resources/db_backup.sql` in the `aws-ci` branch of the vprofile project on GitHub. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

The initialization process is: download the SQL file onto one of the EC2 instances → connect to the RDS instance → execute the SQL file against the `accounts` database → tables are created. This is a **one-time setup operation** — you do it once before deploying the application, not on every deployment. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

The instructor demonstrates two methods for getting the SQL file onto the instance:

1. **Direct download via wget** — Click "Raw" on the GitHub file page to get a direct URL, then `wget` that URL on the instance
2. **Copy-paste fallback** — Copy the file content and paste it into a file on the instance

Both achieve the same result: the SQL file is present on the EC2 instance and can be piped into the MySQL client. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

***

## 1.6 The Complete System Relationship

The instructor closes by describing the full architecture that emerges across this lecture and the next: [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

*"Our source code will be automatically fetched, built, and deployed to the Beanstalk instance. Our application will be running on Beanstalk instance, and application will be accessing this RDS database."*

The system is:

* **Beanstalk** = Application compute layer (EC2 instances + load balancer)
* **RDS** = Database layer (MySQL, accounts database with tables)
* **CI/CD Pipeline** (next lecture) = Automated deployment from source code to Beanstalk
* **Security Groups** = Network-level trust linking Beanstalk instances to RDS

Each component is an independent AWS service, connected through network rules (security groups) and application configuration (database endpoint, username, password).

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating an **Amazon RDS MySQL database**, connecting it to an existing **Elastic Beanstalk application environment**, and initializing the database with tables from the application's source code. The final outcome: Beanstalk EC2 instances can connect to the RDS database on port 3306, and the `accounts` database contains all required tables for the vprofile application. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

***

## Phase 1: Create the RDS Instance

### Step 1: Navigate to RDS and Start Creation

Search for **RDS** in the AWS console → click **Create database**. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

### Step 2: Configure the Database

| Setting                | Value                               | Reasoning                                  |
| ---------------------- | ----------------------------------- | ------------------------------------------ |
| Creation method        | Standard create                     | Full control over settings                 |
| Engine                 | MySQL                               | vprofile application uses MySQL            |
| Engine version         | 8.0.35                              | Specific version the instructor selects    |
| Template               | **Free Tier**                       | Prevents accidental paid service selection |
| DB instance identifier | `vprords`                           | Descriptive name                           |
| Master username        | `admin`                             | Default superuser                          |
| Credentials            | **Auto generate password**          | Strong random password                     |
| Instance type          | t3.micro or t2.micro                | Auto-selected by free tier template        |
| Storage                | 20 GB General Purpose               | Minimum for free tier                      |
| Connectivity           | Default                             | Will configure security groups manually    |
| Public access          | **No**                              | Database stays private within VPC          |
| Security group         | **Create new** → name: `vprords-sg` | Dedicated security group for RDS           |
| AZ                     | No preference                       | Let AWS choose                             |
| Port                   | 3306                                | MySQL default                              |
| DB authentication      | Password authentication             | Standard auth                              |
| Initial database name  | **`accounts`**                      | The database name the vprofile app expects |

 [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

Click **Create database**.

### Step 3: IMMEDIATELY Save the Credentials

**This is critical and time-sensitive.** [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

After clicking create, look for **"View credential details"** — click it immediately. Copy the **auto-generated password** and the **username** (`admin`). Store them somewhere safe (the instructor uses Sticky Notes temporarily).

**If you miss this:** The password is shown only once. If you close the banner without copying, you must wait for the instance to become available, then go to settings and **reset the master credentials**. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

### Step 4: Wait for RDS to Become Available

The RDS instance takes **5-10 minutes** to provision. Wait until the status shows **"Available"**. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

**Connection to flow:** While waiting, confirm that the Beanstalk environment is also available and has created its two EC2 instances.

***

## Phase 2: Configure Security Group Access

### Step 5: Identify the Security Groups

Navigate to **EC2 → Security Groups**. You should see: [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

1. **RDS security group** (`vprords-sg`) — attached to the RDS instance
2. **Beanstalk load balancer security group** — for the load balancer (we don't need this one)
3. **Beanstalk instance security group** — for the EC2 instances (this is what we need)

**How to distinguish the Beanstalk security groups:** The instructor identifies them by context — the instance security group is the one associated with the EC2 instances, not the load balancer. Check the security group descriptions or the associated resources to confirm. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

### Step 6: Copy the Beanstalk Instance Security Group ID

Select the **Beanstalk instance security group** → copy its **Security Group ID** (format: `sg-xxxxxxxxxxxxxxxxx`). [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

### Step 7: Add Inbound Rule to RDS Security Group

Select the **RDS security group** (`vprords-sg`) → **Inbound rules** → **Edit inbound rules** → **Add rule**: [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

| Field  | Value                                          |
| ------ | ---------------------------------------------- |
| Type   | MySQL/Aurora (or Custom TCP)                   |
| Port   | 3306                                           |
| Source | Paste the Beanstalk instance security group ID |

Click **Save rules**. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

**What this achieves:** Any EC2 instance that belongs to the Beanstalk instance security group can now connect to the RDS instance on port 3306. New instances added by auto-scaling automatically get access.

**Common mistake:** Adding the load balancer security group instead of the instance security group. The load balancer doesn't connect to the database — the EC2 instances do.

***

## Phase 3: SSH into a Beanstalk EC2 Instance

### Step 8: Get the Instance's Public IP

Navigate to **EC2 → Instances** (ensure you're in the correct region). You'll see two instances created by Beanstalk. Select either one and copy its **Public IP address**. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

### Step 9: Set Key Permissions

Open **Git Bash** (Windows) or **Terminal** (macOS). [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

```bash
chmod 400 downloads/vprobeankey
```

**Breakdown:**

* `chmod 400` — Sets the key file to read-only for the owner, no permissions for anyone else
* `downloads/vprobeankey` — Path to the key pair file created when setting up Beanstalk

**Why:** SSH refuses to use a key file with overly permissive permissions. Without this, you get "permission denied" errors. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

### Step 10: SSH into the Instance

```bash
ssh -i downloads/vprobeankey ec2-user@<PUBLIC_IP>
```

 [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

**Breakdown:**

* `ssh` — SSH client
* `-i downloads/vprobeankey` — Specifies the private key file for authentication
* `ec2-user` — The default username for **Amazon Linux** instances (Beanstalk uses Amazon Linux)
* `@<PUBLIC_IP>` — The instance's public IP address

Type `yes` when prompted for host key verification. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

Switch to root:

```bash
sudo -i
```

 [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

***

## Phase 4: Test Database Connectivity

### Step 11: Install MySQL Client

```bash
dnf search mysql
```

**What this does:** Searches available packages for MySQL-related software. On Amazon Linux, the MySQL client package is named `mariadb105` (MariaDB is a MySQL-compatible client). [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

```bash
dnf install mariadb105 -y
```

 [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

**Breakdown:**

* `dnf install` — Package manager install command (Amazon Linux uses DNF)
* `mariadb105` — The MySQL-compatible client package
* `-y` — Auto-confirm installation

### Step 12: Get the RDS Endpoint

Navigate to the RDS console → select your RDS instance → copy the **Endpoint** (a long hostname like `vprords.xxxxxxxxxxxx.us-east-1.rds.amazonaws.com`). [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

### Step 13: Test the Connection

```bash
mysql -h <RDS_ENDPOINT> -u admin -p accounts
```

 [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

**Breakdown:**

* `mysql` — MySQL client command
* `-h <RDS_ENDPOINT>` — The host to connect to (the RDS endpoint copied above)
* `-u admin` — Username
* `-p` — Prompt for password (enter it when prompted — it won't be visible)
* `accounts` — The database name to connect to

**What the instructor actually shows (but warns against):**

```bash
mysql -h <RDS_ENDPOINT> -u admin -p<PASSWORD> accounts
```

The password is directly in the command line. The instructor explicitly says: *"Giving password like that in the command line is a very bad idea."* Use `-p` alone and enter the password at the prompt instead. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

**Expected result:** A MySQL prompt appears, confirming successful connection. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

### Step 14: Verify the Database Exists

```sql
show databases;
```

 [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

**Expected output:** A list including `accounts` and system databases.

Type `exit` to leave the MySQL client. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

**Troubleshooting if connection fails:** [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

* **Timeout error** → Security group rule is missing or incorrect. Verify the inbound rule on the RDS security group allows port 3306 from the Beanstalk instance security group.
* **Invalid credentials** → Check username and password. If password was lost, reset master credentials in RDS settings.
* **Unknown database** → Check the database name (`accounts`). If it wasn't specified during RDS creation, you'll need to create it manually with `CREATE DATABASE accounts;`.

***

## Phase 5: Initialize the Database with Schema

### Step 15: Download the SQL File

Navigate in the browser to the vprofile project source code on GitHub: [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

```
https://github.com/hkhcoder/vprofile-project
```

Switch to the **`aws-ci`** branch → navigate to `src/main/resources/` → open `db_backup.sql` → click **Raw**. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

Copy the **Raw URL** from the browser's address bar.

On the EC2 instance:

```bash
wget <RAW_URL_OF_db_backup.sql>
```

 [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

**Breakdown:**

* `wget` — Downloads a file from a URL
* `<RAW_URL>` — The direct URL to the raw SQL file content from GitHub

**Fallback:** If `wget` fails for any reason, copy the file content from GitHub and paste it into a file on the instance using `vim` or `cat >`. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

**Verification:**

```bash
ls
```

The `db_backup.sql` file should appear in the current directory.

### Step 16: Execute the SQL File Against the Database

```bash
mysql -h <RDS_ENDPOINT> -u admin -p accounts < db_backup.sql
```

 [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

**Breakdown:**

* Same MySQL connection command as Step 13
* `< db_backup.sql` — **Input redirection**: feeds the contents of the SQL file into the MySQL client as commands

**What happens internally:** The MySQL client connects to the RDS instance, enters the `accounts` database, and executes every SQL statement in the file — creating tables, inserting data, setting up schemas. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

### Step 17: Verify Tables Were Created

```bash
mysql -h <RDS_ENDPOINT> -u admin -p accounts
```

At the MySQL prompt:

```sql
show tables;
```

 [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

**Expected result:** A list of tables that the vprofile application needs. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

**If tables don't appear:** [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

* Verify the downloaded file content is correct (not an HTML page or error)
* Re-download the file and re-execute
* Check for SQL errors during execution

Type `exit` to leave the MySQL client.

**Connection to flow:** The database is now fully initialized. The next step (next lecture) is building the CI/CD pipeline that deploys the application to Beanstalk, where it will connect to this RDS instance. [\[284-rds-an...-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/284-rds-and-app-setup-on-beanstalk.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Architecture

```
[Beanstalk Environment]
  ├── Load Balancer (SG: beanstalk-lb-sg)
  ├── EC2 Instance 1 (SG: beanstalk-instance-sg)  ──port 3306──→  [RDS MySQL]
  └── EC2 Instance 2 (SG: beanstalk-instance-sg)  ──port 3306──→  (SG: vprords-sg)
                                                                     │
                                                                     └── Database: accounts
                                                                           └── Tables (from db_backup.sql)
```

***

## Security Group Linking

```
RDS Security Group (vprords-sg):
  Inbound Rule:
    Port: 3306
    Source: beanstalk-instance-sg  (NOT lb-sg, NOT IP address)

Why SG-to-SG (not IP):
  ├── Instances get replaced (auto-scaling, deployments) → IPs change
  ├── New instances auto-inherit SG → auto-get DB access
  └── Terminated instances auto-lose access

CRITICAL: Use INSTANCE SG, not LOAD BALANCER SG
  LB doesn't connect to DB → instances do
```

***

## RDS Creation Config

```
Engine: MySQL 8.0.35 | Template: Free Tier
Instance: vprords | Type: t3/t2.micro | Storage: 20GB GP
Username: admin | Password: AUTO-GENERATED
Public access: NO | Port: 3306
Security group: vprords-sg (new)
Initial DB name: accounts ← APP REQUIRES THIS NAME

Provisioning time: 5-10 minutes → status: "Available"
```

***

## Credential Management

```
Auto-generated password shown ONCE → "View credential details" banner
  ├── Copy immediately → store securely
  ├── Close without copying → password LOST forever
  └── Recovery: Wait for "Available" → Settings → Reset master credentials

NEVER: Put password in command line (visible in history)
DO:    Use -p alone → MySQL prompts invisibly
```

***

## Database Initialization Flow

```
Source code repo (GitHub, aws-ci branch)
  └── src/main/resources/db_backup.sql

Get file onto EC2:
  Browser: File → Raw → copy URL
  Instance: wget <RAW_URL>
  Fallback: copy-paste content into file

Execute:
  mysql -h <ENDPOINT> -u admin -p accounts < db_backup.sql
  (input redirection feeds SQL file into MySQL client)

Verify:
  mysql -h <ENDPOINT> -u admin -p accounts
  > show tables;
  → Tables should appear
```

***

## SSH into Beanstalk Instance

```
chmod 400 downloads/vprobeankey        ← set key permissions (required)
ssh -i downloads/vprobeankey ec2-user@<IP>
  ec2-user = Amazon Linux default username
sudo -i                                ← switch to root
```

***

## MySQL Client on Amazon Linux

```
dnf search mysql → find: mariadb105
dnf install mariadb105 -y
mysql -h <ENDPOINT> -u admin -p accounts
```

***

## Troubleshooting Decision Tree

```
CONNECTION FAILS:
  ├── Timeout?
  │     └── Security group rule missing/wrong
  │           Check: RDS SG → inbound → 3306 → source = beanstalk-instance-sg
  ├── Invalid credentials?
  │     └── Check username (admin) + password
  │           If lost: Reset master credentials in RDS settings
  └── Unknown database?
        └── DB name "accounts" not created during RDS setup
              Fix: CREATE DATABASE accounts;

TABLES NOT CREATED:
  ├── Downloaded file correct? (not HTML error page)
  ├── SQL errors during execution? (re-run, check output)
  └── Correct database specified in command?
```

***

## Complete Operational Sequence

```
── CREATE RDS ──
RDS → Create database → MySQL 8.0.35 → Free Tier
  → vprords, admin, auto-generate password
  → No public access → new SG: vprords-sg
  → Initial DB name: accounts → Create
  → IMMEDIATELY copy credentials from banner

── WAIT ──
5-10 min → RDS status: Available
Verify: Beanstalk also available, 2 EC2 instances exist

── SECURITY GROUP ──
EC2 → Security Groups → identify 3 SGs (RDS, BS-LB, BS-instance)
  → Copy BS-instance SG ID
  → Edit RDS SG inbound → Add: 3306, source = BS-instance SG ID → Save

── SSH + TEST ──
chmod 400 key → ssh ec2-user@<IP>
sudo -i → dnf install mariadb105 -y
mysql -h <RDS_ENDPOINT> -u admin -p accounts
  → show databases; → verify "accounts" exists → exit

── INITIALIZE DB ──
wget <raw_github_url_of_db_backup.sql>
mysql -h <ENDPOINT> -u admin -p accounts < db_backup.sql
mysql -h <ENDPOINT> -u admin -p accounts → show tables; → verify → exit

── NEXT: CI/CD pipeline deploys app → app connects to this RDS
```

***

## Beanstalk Security Groups (Disambiguation)

```
Beanstalk creates TWO security groups:
  1. Load Balancer SG  → controls traffic TO the LB (HTTP/HTTPS from internet)
  2. Instance SG       → controls traffic TO the EC2 instances (from LB + outbound)

For RDS access: Use INSTANCE SG (not LB SG)
  Instances talk to database, load balancer does not
```

***

## Reusable Engineering Patterns

| Pattern                            | Manifestation                                                                 |
| ---------------------------------- | ----------------------------------------------------------------------------- |
| **Compute-data separation**        | Beanstalk (app) + RDS (database) = independent lifecycle, independent scaling |
| **Security group referencing**     | SG-to-SG rules → dynamic trust, survives IP changes and auto-scaling          |
| **Schema-before-app**              | Database initialized with tables BEFORE application deployed                  |
| **One-time credential capture**    | Auto-generated secrets shown once → must capture immediately                  |
| **Input redirection for bulk ops** | `mysql ... < file.sql` → batch execution without interactive session          |
| **Source-code-contains-schema**    | SQL schema lives in app repo → versioned with code, accessible via wget       |
| **Correct-identity selection**     | 3 security groups exist → must identify the RIGHT one (instance, not LB)      |

***

## Core Mental Model

```
RDS + Beanstalk = Separated layers connected by security groups

Trust chain:
  Beanstalk EC2 instance ∈ beanstalk-instance-sg
    → RDS SG allows 3306 from beanstalk-instance-sg
      → Instance can reach RDS on MySQL port
        → App connects using endpoint + credentials + DB name

Initialization chain:
  Source code repo → SQL file → wget to instance → pipe into mysql client → tables created

Three things the app needs from RDS:
  1. Endpoint (hostname)
  2. Credentials (username + password)  
  3. Database name (accounts) with tables initialized
```

***

This material captures every configuration decision, security group interaction, credential warning, troubleshooting path, and architectural relationship from the lecture — structured for deep understanding (Theory), confident execution (Practical), and rapid future recall (Compression Map). 🚀

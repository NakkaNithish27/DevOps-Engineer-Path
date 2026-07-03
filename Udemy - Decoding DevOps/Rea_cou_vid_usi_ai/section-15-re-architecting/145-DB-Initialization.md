# 🎓 Deep Learning Material: RDS Database Initialization via Temporary EC2 Client

**Source:** [145-db-initialization.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt?EntityRepresentationId=db5378bf-ca1a-47b9-8441-f995062d4fa7) — Video caption reconstruction covering the initialization of a private AWS RDS MySQL database by deploying the vProfile application schema through a temporary EC2 instance acting as a MySQL client within the same VPC. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Problem: A Private Database That Cannot Be Reached Directly

The RDS instance hosting the vProfile application's database is a **private instance**. This is a deliberate architectural decision — the database is not exposed to the public internet. It exists only inside the VPC (Virtual Private Cloud) and can only be communicated with by other resources that also reside within that same VPC. You cannot open a browser, paste the RDS endpoint, and connect. You cannot run a `mysql` command from your local laptop and reach it. The RDS instance has an endpoint (a hostname ending in `.com`) and a port (3306, the standard MySQL port), but these are only resolvable and reachable from within the VPC's private network. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

This creates an operational problem: the database exists but is empty. It has no tables, no schema, no application data. The vProfile application expects a specific schema with specific tables in a database called `accounts`. Before the application can function, someone must connect to this RDS instance and deploy that schema. But you can't connect directly. So how do you get inside? [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

***

## 1.2 The Solution: A Temporary EC2 Instance as a Network Bridge

The solution is to launch an EC2 instance in the **same region** (North Virginia) and the **same VPC** as the RDS instance. AWS regions have a default VPC, and when you launch an EC2 instance without specifying a custom VPC, it automatically lands in this default VPC — the same network where the RDS instance lives. Once inside the same VPC, the EC2 instance can reach the RDS endpoint over the private network, provided the security groups allow it. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

This EC2 instance is not a permanent part of the architecture. It is a **temporary operational tool** — created solely to perform the database initialization, and terminated immediately afterward. It serves as a bridge between the operator (you, sitting outside the VPC) and the private database (inside the VPC). You SSH into the EC2 instance from your local machine (which is allowed because SSH port 22 is opened from "My IP" in the instance's security group), and from within that instance, you run MySQL commands against the RDS endpoint. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

🔍 **Deep Dive**
This is an instance of the **bastion host / jump box pattern** — using a publicly accessible instance as a stepping stone to reach private resources. In production environments, bastion hosts are hardened, audited, and often permanent. Here, because the task is one-time and low-risk, the instance is intentionally disposable. The engineering reasoning is: minimize the attack surface by keeping the database private, and use short-lived infrastructure only when direct access is needed. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

***

## 1.3 Security Group Chaining: Granting EC2 Access to RDS

Placing the EC2 instance in the same VPC is necessary but **not sufficient**. AWS security groups act as virtual firewalls around each resource. Even though the EC2 instance and the RDS instance share a network, the RDS instance's security group (the "backend security group") must explicitly allow inbound traffic on port 3306 from the EC2 instance. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

The way this is done is by **referencing the EC2 instance's security group ID** as the source in the RDS security group's inbound rule. You do not use an IP address — you use the security group ID of the MySQL client instance (`vpro-mysql-client-sg`). This means: "allow any resource that belongs to this security group to connect on port 3306." This is a cleaner and more flexible approach than hardcoding IPs, because if the instance is replaced or its IP changes, the rule still works as long as the new instance uses the same security group. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

The video specifically warns: edit **inbound** rules, not outbound. This is a common mistake. Inbound rules control what traffic is allowed **into** the RDS instance. Outbound rules control what traffic the RDS instance can initiate. The EC2 instance is initiating the connection, so the RDS instance needs an **inbound** rule permitting it. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

⚠️ **Expert Note**
The security group for the EC2 instance itself (`vpro-mysql-client-sg`) only has one rule: SSH (port 22) from "My IP." This means the instance is reachable only by you, only via SSH. It does not need any inbound rule for MySQL because it is the *client* initiating the connection to RDS — outbound traffic is allowed by default in AWS security groups. The rule-of-thumb: the **server** (RDS) needs the inbound rule; the **client** (EC2) does not. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

***

## 1.4 What "Initializing the Database" Actually Means

The RDS instance already has MySQL running. It already has a database called `accounts` (created during RDS setup or as part of the configuration). But the database is empty — it has no tables, no structure, no data. "Initializing" means taking the **schema file** (`db_backup.sql`) from the vProfile application's source code and executing it against the `accounts` database. This SQL file contains `CREATE TABLE` statements (and possibly `INSERT` statements for seed data) that build the table structure the application expects. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

The schema file lives inside the application's Git repository at the path `src/main/resources/db_backup.sql`. This is why Git must be installed on the EC2 instance — to clone the repository and access this file. The source code repository is hosted at `github.com/hkhcoder/vprofile-project`, and the schema file is on a specific branch called `awsrefactor`. You must switch to this branch after cloning to find the correct version of the schema. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

🔍 **Deep Dive**
The deployment mechanism uses **MySQL input redirection**. Instead of logging into the MySQL shell and manually pasting SQL commands, you pipe the entire SQL file into the `mysql` command using `<`. The MySQL client reads the file as if you typed every line into the shell. This is the standard way to deploy schemas, import backups, or seed databases in automated and semi-automated workflows. The command connects to the RDS endpoint, authenticates, selects the `accounts` database, and then executes every statement in the SQL file sequentially. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

***

## 1.5 The Ephemeral Infrastructure Pattern

The EC2 instance created here has one job: initialize the database. Once that job is complete, the instance is **terminated**. It is not kept running. It is not repurposed. This is an explicit architectural choice — the video calls it a "temporary instance" and instructs to delete it immediately after the schema is deployed. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

This reflects a broader engineering principle: **infrastructure should exist only as long as it serves a purpose.** Keeping unnecessary instances running wastes cost, increases attack surface, and adds operational complexity. In cloud environments, you can create and destroy resources in minutes, so there is no reason to keep a tool alive after the task is done. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

***

## 1.6 Where This Fits in the Larger System

The video states that after this step, the **backend is ready**. This means all backend services — the RDS database (now initialized with the vProfile schema), along with any other services set up in prior lectures — are operational. The next step in the project is creating the **Elastic Beanstalk instance**, which will host the vProfile application itself. Beanstalk will connect to this initialized RDS database to read user data, session data, and application state. Without the schema deployed, the application would fail on startup or throw errors when trying to query non-existent tables. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are deploying the vProfile application's database schema into a private AWS RDS MySQL instance. Since the RDS instance cannot be accessed from the internet, we will launch a temporary EC2 instance inside the same VPC, SSH into it, install the necessary tools, clone the application source code, and use the MySQL client to push the schema into the database. Once verified, we terminate the temporary instance. The final outcome: the `accounts` database on RDS contains all required tables and is ready for the vProfile application. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

***

## Step 1: Gather RDS Connection Details

Before launching anything, collect the information you will need to connect to the database.

Navigate to the **RDS console** and open your RDS instance.

**1a. Find the endpoint:**

The RDS endpoint is the hostname you will use to connect. It is a long string ending in `.com` (e.g., `vprofile-xxxxxxx.xxxxxxxxx.us-east-1.rds.amazonaws.com`). You can find it on the instance detail page — either read the full endpoint string or click on the "Endpoints" link. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**1b. Note the port:**

The port is **3306** — the default MySQL port. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**1c. Note the credentials:**

The username and password were set during RDS instance creation. In this video, the username is `admin` and the password was previously saved. Keep these accessible (the instructor uses a sticky note — in real work, use a secure method). [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**Connection to larger flow:** These three pieces — endpoint, username, password — are everything needed to authenticate to the database from within the VPC.

***

## Step 2: Launch a Temporary EC2 Instance

Navigate to **EC2 → Launch Instance**.

**2a. Configure the instance:**

| Setting       | Value                                           |
| ------------- | ----------------------------------------------- |
| Name          | `mysql-client`                                  |
| AMI           | Ubuntu Server 24.04                             |
| Instance type | `t2.micro`                                      |
| Key pair      | Select an existing key pair or create a new one |

 [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**2b. Configure the security group:**

Click **Edit** under Network settings. Create a **new** security group:

| Setting             | Value                        |
| ------------------- | ---------------------------- |
| Security group name | `vpro-mysql-client-sg`       |
| Inbound rule        | SSH (port 22) from **My IP** |

No other rules are needed. This instance only needs to be reachable via SSH by you. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**2c. Launch the instance.**

Wait for it to reach the "Running" state and note its **public IP address**. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**Connection to larger flow:** This instance is your bridge into the VPC. It exists solely to run the MySQL client against the private RDS endpoint.

***

## Step 3: Allow the EC2 Instance to Talk to RDS (Security Group Rule)

The EC2 instance is in the same VPC as RDS, but the RDS security group does not yet allow connections from this instance.

**3a. Copy the EC2 security group ID:**

Navigate to **EC2 → Security Groups**. Find `vpro-mysql-client-sg`. Copy its **Security Group ID**. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**3b. Edit the RDS (backend) security group:**

Find the **backend security group** (the one attached to the RDS instance). Click on it. Go to **Inbound rules** → **Edit inbound rules**.

⚠️ Make sure you are editing **inbound**, not outbound. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**3c. Add a rule:**

| Type  | Port | Source                                     |
| ----- | ---- | ------------------------------------------ |
| MySQL | 3306 | `vpro-mysql-client-sg` (security group ID) |

Click **Save rules**. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**What this does:** Any instance belonging to `vpro-mysql-client-sg` can now connect to the RDS instance on port 3306. The EC2 instance we just launched belongs to this security group, so it now has network access to the database.

**Connection to larger flow:** Without this rule, the `mysql` command from EC2 would time out — the packets would be blocked at the RDS security group boundary.

***

## Step 4: SSH into the EC2 Instance and Install Tools

**4a. SSH into the instance:**

```bash
ssh -i <path-to-your-key.pem> ubuntu@<ec2-public-ip>
```

| Part                        | Meaning                                           |
| --------------------------- | ------------------------------------------------- |
| `ssh`                       | Secure Shell — remote login protocol              |
| `-i <path-to-your-key.pem>` | Specifies the private key file for authentication |
| `ubuntu`                    | Default username for Ubuntu AMIs                  |
| `@<ec2-public-ip>`          | The public IP of the EC2 instance                 |

When prompted, type `yes` to accept the host fingerprint. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**4b. Become root:**

```bash
sudo -i
```

(Implied by "let's become the root user." This gives you administrative privileges for installing packages.) [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**4c. Install MySQL client and Git:**

```bash
apt update && apt install mysql-client git -y
```

| Part                              | Meaning                                                                                                     |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `apt update`                      | Refreshes the package index so the system knows what's available                                            |
| `&&`                              | Run the next command only if the first succeeds                                                             |
| `apt install mysql-client git -y` | Installs two packages: `mysql-client` (to connect to MySQL) and `git` (to clone the source code repository) |
| `-y`                              | Auto-confirm installation prompts                                                                           |

 [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**Why both tools?** The MySQL client is needed to connect to and execute SQL against RDS. Git is needed because the database schema file is stored inside the vProfile application's Git repository — there is no other way to get it onto this instance.

**Connection to larger flow:** The instance is now equipped with everything needed: network access (Step 3), SSH access (Step 4a), and the two tools (MySQL client + Git).

***

## Step 5: Test the Database Connection

Before deploying the schema, verify that you can actually connect to RDS.

```bash
mysql -h <rds-endpoint> -u admin -p<password> accounts
```

| Part                | Meaning                                           |
| ------------------- | ------------------------------------------------- |
| `mysql`             | MySQL client command                              |
| `-h <rds-endpoint>` | Host — the RDS endpoint you copied earlier        |
| `-u admin`          | Username for the database                         |
| `-p<password>`      | Password (no space between `-p` and the password) |
| `accounts`          | The database name to connect to                   |

 [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**Expected result:** You should land inside the MySQL shell, connected to the `accounts` database. This confirms: the endpoint is correct, the credentials are correct, and the security group rule is working.

⚠️ **Expert Note**
The video explicitly warns: **never put the password directly in the command line like this in real environments.** Use just `-p` (without the password), press Enter, and MySQL will prompt you for the password interactively. Putting the password in the command line exposes it in shell history, process listings, and logs. This is done here only for convenience during a tutorial. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

After confirming the connection works, type `exit` to leave the MySQL shell. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**Connection to larger flow:** This is a validation checkpoint. If the connection fails here, you debug it now (wrong endpoint? wrong credentials? missing security group rule?) — before attempting the schema deployment.

***

## Step 6: Clone the Source Code and Switch to the Correct Branch

**6a. Clone the repository:**

```bash
git clone https://github.com/hkhcoder/vprofile-project.git
```

This downloads the entire vProfile source code repository onto the EC2 instance. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**6b. Enter the project directory:**

```bash
cd vprofile-project
```

**6c. Switch to the `awsrefactor` branch:**

```bash
git checkout awsrefactor
```

The database schema file is on this specific branch. If you stay on the default branch, the file may not exist or may be a different version. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**6d. Verify the schema file exists:**

The schema file is located at:

```
src/main/resources/db_backup.sql
```

 [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**Connection to larger flow:** The schema file is now locally available on the EC2 instance, ready to be fed into the MySQL client.

***

## Step 7: Deploy the Schema to RDS

This is the core operational step — pushing the SQL schema into the live database.

```bash
mysql -h <rds-endpoint> -u admin -p<password> accounts < src/main/resources/db_backup.sql
```

| Part                                 | Meaning                                                                                                    |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| `mysql -h ... -u ... -p... accounts` | Same connection command as Step 5                                                                          |
| `<`                                  | **Input redirection** — feeds the contents of the file on the right into the MySQL client's standard input |
| `src/main/resources/db_backup.sql`   | The SQL schema file; all CREATE TABLE and INSERT statements inside it will be executed sequentially        |

 [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**What happens internally:** The MySQL client connects to RDS, selects the `accounts` database, and executes every SQL statement in `db_backup.sql` in order. Tables are created, and any seed data is inserted.

**Important:** You must be inside the `vprofile-project` directory for this relative path to work. If you are in a different directory, provide the absolute path to the file instead. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**Expected result:** The command runs silently (no errors). If there are SQL errors, they will be printed to the terminal.

**Connection to larger flow:** The database is now initialized. The `accounts` database contains all the tables the vProfile application needs.

***

## Step 8: Verify the Schema Deployment

Log back into the database:

```bash
mysql -h <rds-endpoint> -u admin -p<password> accounts
```

Then run:

```sql
show tables;
```

**Expected result:** A list of tables created by the schema file. If you see tables, the initialization was successful. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

Type `exit` to leave the MySQL shell.

***

## Step 9: Terminate the Temporary EC2 Instance

The instance has served its purpose. Navigate to **EC2 → Instances**. Select the `mysql-client` instance. Click **Instance State → Terminate**.

The video explicitly states: *"The whole purpose of using this instance was to just initialize the database. Since the database instance is private, we need to do it through another EC2 instance in the same VPC, the same network."* Once the task is done, delete it. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

⚠️ **Expert Note**
After terminating the instance, the security group rule you added in Step 3 (allowing `vpro-mysql-client-sg` on port 3306) becomes inert — no instances use that security group anymore. For cleanliness, you could remove the rule, but it poses no security risk since no active resource references that security group. [\[145-db-ini...ialization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/145-db-initialization.txt)

**Final state:** The backend is fully ready. The RDS database is initialized with the vProfile schema. The next step in the project is creating the Elastic Beanstalk environment to host the application.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Problem → Solution

```
Private RDS (no internet access)
    + Empty database (no schema)
    = Need a bridge into the VPC to deploy schema
    
Solution: Temporary EC2 instance in same VPC → MySQL client → deploy schema → destroy EC2
```

***

## Architecture

```
 YOU (local machine)
   │
   │ SSH (port 22, "My IP")
   ▼
[ EC2: mysql-client ]  ←── temporary, Ubuntu, t2.micro
   │                        SG: vpro-mysql-client-sg (SSH only)
   │
   │ MySQL (port 3306)
   │ Allowed via: backend SG inbound rule ← vpro-mysql-client-sg
   ▼
[ RDS: vprofile DB ]  ←── private, port 3306
   │
   DB: accounts
   Schema: from db_backup.sql
```

***

## Security Group Chain

```
Your IP ──[22]──→ vpro-mysql-client-sg (EC2)
vpro-mysql-client-sg ──[3306]──→ backend SG (RDS)

⚠️ Edit INBOUND on RDS SG, not outbound
⚠️ Source = SG ID, not IP address
```

***

## Operational Sequence

```
1. Gather: RDS endpoint + port 3306 + username + password
2. Launch: EC2 (Ubuntu, t2.micro, vpro-mysql-client-sg, SSH from My IP)
3. Allow:  Backend SG ← inbound 3306 from vpro-mysql-client-sg
4. SSH:    ssh -i <key> ubuntu@<ip>
5. Root:   sudo -i
6. Install: apt update && apt install mysql-client git -y
7. Test:   mysql -h <endpoint> -u admin -p<pw> accounts → exit
8. Clone:  git clone https://github.com/hkhcoder/vprofile-project.git
9. Branch: cd vprofile-project && git checkout awsrefactor
10. Deploy: mysql -h <endpoint> -u admin -p<pw> accounts < src/main/resources/db_backup.sql
11. Verify: mysql → show tables; → exit
12. Destroy: Terminate EC2 instance
```

***

## Schema Deployment Command (Core)

```
mysql -h <endpoint> -u admin -p<password> accounts < src/main/resources/db_backup.sql
       ▲              ▲          ▲          ▲       ▲            ▲
       host          user     password    database  input       SQL file
                                                   redirect    (from git repo, branch: awsrefactor)
```

***

## Two Prerequisites Before MySQL Connection

```
1. Network path:  EC2 SG ──[3306]──→ RDS SG  (security group rule)
2. Same VPC:      EC2 auto-lands in default VPC = same VPC as RDS
```

Both must be true. Same VPC alone is not enough without the SG rule.

***

## Key Data Locations

```
RDS endpoint      → RDS console → instance details → Endpoints
RDS credentials   → Set during RDS creation (username: admin)
Schema file       → github.com/hkhcoder/vprofile-project
                    Branch: awsrefactor
                    Path: src/main/resources/db_backup.sql
```

***

## Lifecycle of the Temporary Instance

```
Create → SSH → Install tools → Test connection → Clone repo → Deploy schema → Verify → TERMINATE
  │                                                                                        │
  └──────────── exists ONLY for this task ─────────────────────────────────────────────────┘
```

***

## Engineering Patterns

| Pattern                                   | Manifestation                                                                                 |
| ----------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Bastion / Jump Box**                    | EC2 bridges the gap between operator (internet) and private resource (RDS)                    |
| **Ephemeral Infrastructure**              | Instance created for one task, destroyed immediately after — minimize cost and attack surface |
| **Security Group Referencing**            | Source = SG ID (not IP) — decouples access control from instance identity                     |
| **Validate-Before-Execute**               | Test `mysql` login before deploying schema — catch connection issues early                    |
| **Schema-as-Code**                        | DB structure lives in Git alongside application code — versioned, branched, reproducible      |
| **Input Redirection for Bulk Operations** | `< file.sql` feeds entire schema without interactive shell — automatable, repeatable          |
| **Private-by-Default Data Tier**          | Database has no internet exposure — all access mediated through VPC-internal resources        |

***

## Project Context

```
BEFORE this lecture: Backend services installed (RDS created but empty)
THIS lecture:        Database initialized (schema deployed into accounts DB)
AFTER this lecture:  Backend fully ready → Create Elastic Beanstalk (application hosting)
```

***

This completes the full reconstruction of the database initialization video. The three sections work together — **Theory** explains *why* each piece exists, **Practical** gives you the exact execution path to reproduce it, and the **Compression Map** lets you mentally reload the entire workflow in under a minute. Let me know if you'd like Anki flashcards or any section expanded! 🚀

# 🧠 EC2 Instances — vprofile AWS Lift & Shift Infrastructure Provisioning

**Source**: [134. EC2 Instances.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt?EntityRepresentationId=c8022dfd-71cb-478b-a39c-2be8ee5ce956) — Video caption reconstruction [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

# 🧠 SECTION 1: THEORY (DEEP LEARNING MODE)

## 1.1 The Four-Instance Architecture of vprofile on AWS

The vprofile project, when lifted and shifted to AWS, requires four distinct EC2 instances, each running a single service. This is not a monolithic deployment — each service is isolated on its own virtual machine to mirror a production-like multi-tier architecture. The four instances are:

| Instance           | Service         | Role                                         |
| ------------------ | --------------- | -------------------------------------------- |
| **vprofile-db01**  | MySQL (MariaDB) | Database layer — stores application data     |
| **vprofile-mc01**  | Memcache        | Caching layer — reduces DB read pressure     |
| **vprofile-rmq01** | RabbitMQ        | Message broker — handles async communication |
| **vprofile-app01** | Tomcat          | Application server — runs the Java web app   |

The first three (MySQL, Memcache, RabbitMQ) are **backend services**. Tomcat is the **application-tier** service. This distinction directly drives the security group assignment — it is not arbitrary naming, it reflects a network isolation boundary. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

The load balancer (created in a later lecture) sits in front of Tomcat in its own security group, forming a three-zone architecture: **Load Balancer → App (Tomcat) → Backend (DB, Cache, MQ)**. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

🔍 **Deep Dive**: This architecture implements a classic N-tier separation pattern. The reason each service gets its own instance rather than co-locating them is twofold: (1) failure isolation — if RabbitMQ crashes, the database remains unaffected, and (2) independent scaling — in production, you could scale Memcache horizontally without touching the DB tier. Even though in this project all are t2.micro, the architecture preserves the ability to scale each tier independently later.

***

## 1.2 Security Group Placement Strategy

Security groups in this project are not just firewalls — they represent **network trust zones**. The placement decision follows a simple rule:

* **Backend security group** → MySQL, Memcache, RabbitMQ (all three)
* **App security group** → Tomcat only
* **Load balancer security group** → Load balancer (later lecture)

The critical relationship is: Tomcat (in the app security group) connects to the backend instances, and the **backend security group rules allow inbound connections from the app security group**. This means the app SG acts as an identity token — being in the app SG is what grants Tomcat access to the backend. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

⚠️ **Expert Note**: A common real-world mistake is modifying the **outbound rules** of security groups. The instructor explicitly warns that if you change the outbound rules, the instance will lose internet access, and user data scripts will fail because they cannot download packages. The default outbound rule (allow all traffic) must remain intact during provisioning. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## 1.3 User Data Scripts — Automation at Instance Launch

User data is an AWS EC2 mechanism that lets you pass a shell script to an instance at launch time. The instance executes this script **automatically** during its first boot — no manual SSH required. This is how all four services get installed and configured without human intervention. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

The scripts live inside the source code repository under the `user data/` folder. Each instance gets its own script:

| Script             | Target Instance |
| ------------------ | --------------- |
| `mysql.sh`         | vprofile-db01   |
| `memcache.sh`      | vprofile-mc01   |
| `rabbitmq.sh`      | vprofile-rmq01  |
| `tomcat_ubuntu.sh` | vprofile-app01  |

**Critical rule**: The first line of the script (the shebang, `#!/bin/bash`) must be included when pasting into the user data field. Without it, AWS does not recognize the content as an executable script and silently does nothing. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

The scripts are similar to those used in the vprofile local setup project (Vagrant/VirtualBox), but adapted for the AWS AMIs. The core logic is the same — install packages, configure services, deploy schemas/configs — but the package names and repository methods differ because the OS is different. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

🔍 **Deep Dive**: User data runs as `root` during instance initialization. It runs only once (on the first boot by default). If the script fails midway, the instance will still launch — but the service will be broken or absent. There is no built-in retry mechanism. This is why the instructor's troubleshooting philosophy is "delete and recreate" rather than "SSH in and debug."

***

## 1.4 AMI Selection Strategy

The project uses two different AMIs deliberately:

* **Amazon Linux 2023 AMI** → MySQL, Memcache, RabbitMQ (all backend instances)
* **Ubuntu 24 (24.04 LTS)** → Tomcat only

The reason for Ubuntu on Tomcat is explicitly stated: on CentOS (or Amazon Linux), installing the latest Tomcat requires downloading the binary manually, extracting it, creating a dedicated Tomcat user, writing a systemd service file, and several other manual steps. On Ubuntu 24, a single command — `apt install tomcat10` — handles everything because Tomcat 10 is available directly in Ubuntu 24's default repositories. Older Ubuntu versions (before 24) only have Tomcat 9 in the repository. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

For the backend instances, Amazon Linux 2023 is used as the project standard. It is the AWS-native Linux distribution, optimized for EC2, and the package for MariaDB is named `mariadb105-server` on this AMI. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

⚠️ **Expert Note**: AMI selection has a direct impact on user data scripts. A script written for CentOS will not work on Amazon Linux 2023 even though they are "almost the same operating system" — the repositories are different. The RabbitMQ script is the clearest example: the local project's CentOS method does not work on Amazon Linux 2023 because the repository structure differs entirely. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## 1.5 Tagging Strategy — Instances and Volumes

Every instance receives at minimum two tags:

1. **Name** — the instance identifier (e.g., `vprofile-db01`)
2. **Project** — the project name (e.g., `vprofile`)

The instructor emphasizes that in real-world environments, you must follow organizational naming conventions and add additional tags like environment (dev/staging/prod) and owner. Tags should never be decided "on the fly." If no standard exists, you must create one. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

**Critical detail**: Tags must also be applied to **EBS volumes**, not just instances. The instructor explicitly warns about this — untagged volumes become orphaned resources that consume storage cost silently when instances are deleted. By tagging volumes, you can identify and clean up orphaned storage. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## 1.6 Source Code Repository and Branch Strategy

The source code lives at `github.com/hkhcoder/vprofile-project`. The repository must be cloned, and then you must switch from the default `main` branch to the **`aws-lift-and-shift`** branch (all lowercase). This branch contains the AWS-specific user data scripts and configuration files. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

The cloning is done via VSCode's source control feature (Clone Repository → paste URL → select destination). The `user data/` folder within this branch contains all four provisioning scripts. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

One notable file lives outside the user data folder: the RabbitMQ repository configuration file. Rather than embedding complex repository definitions inside the shell script (which would make it "very ugly"), the instructor stored the `.repo` file in the source code repository itself. The RabbitMQ user data script downloads this file from GitHub at runtime using a URL that points to the raw file on the `aws-lift-and-shift` branch. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## 1.7 MySQL (MariaDB) User Data Script — Internal Logic

The `mysql.sh` script performs these operations in sequence:

1. Installs `mariadb105-server` (the Amazon Linux 2023 package name for MariaDB)
2. Starts and enables the MariaDB service
3. Clones the source code repository (to access the DB schema file)
4. Executes SQL queries to secure the installation (equivalent to `mysql_secure_installation`)
5. Creates the `accounts` database
6. Creates the `admin` user and grants privileges on `accounts` — both locally and remotely
7. Deploys the DB schema file

The key insight is step 4: in the manual/local setup, you would run `mysql_secure_installation`, which is an interactive command that asks questions (set root password, remove test databases, remove anonymous users, etc.). Since user data runs non-interactively in the background, the script replaces this with raw SQL queries that achieve the same result — removing test users, test databases, and setting the root password programmatically. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## 1.8 Memcache User Data Script — Internal Logic

The `memcache.sh` script is the simplest of the four:

1. Installs Memcache
2. Starts and enables the service
3. Modifies the configuration file — replaces the local loopback IP (`127.0.0.1`) with `0.0.0.0` so Memcache listens on all network interfaces (accepting remote connections from the Tomcat instance)
4. Restarts Memcache to apply the configuration
5. Executes a command to make Memcache listen on **port 11211**

The configuration change from localhost-only to `0.0.0.0` is essential — without it, Memcache would reject connections from Tomcat because it would only accept local connections. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## 1.9 RabbitMQ User Data Script — Internal Logic and Repository Complexity

This script is the most complex and the most different from its local-setup counterpart. The complexity comes from repository management on Amazon Linux 2023.

The script flow:

1. **Imports signing keys** — for both the RabbitMQ repository and the Erlang repository (Erlang is a dependency of RabbitMQ)
2. **Downloads the repository configuration file** from the project's GitHub repository — this file defines the Yum repository URLs for both Erlang and RabbitMQ. It is placed at `/etc/yum.repos.d/`
3. Runs `dnf update`
4. Installs `socat` and `logrotate` — dependencies required by RabbitMQ
5. Installs **Erlang** and then **RabbitMQ**
6. Starts and enables the RabbitMQ service
7. Configures the application: adds a test user, assigns the `administrator` tag, sets permissions
8. Restarts the RabbitMQ server

The reason for the external repository file approach: the RabbitMQ and Erlang packages are not available in Amazon Linux 2023's default repositories. You must add third-party repository definitions. Writing those multi-line repository definitions inside a shell script using `cat` or `echo` commands would make the script unreadable. Instead, the file is pre-created, stored in the GitHub source code, and downloaded at runtime. This is a clean separation of configuration from script logic. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## 1.10 Tomcat User Data Script — Simplicity Through OS Choice

The `tomcat_ubuntu.sh` script is deliberately simple:

1. `apt install tomcat10`

That is essentially all that's needed to get the Tomcat service running on Ubuntu 24. The package manager handles the binary installation, user creation, systemd service file creation, and service registration automatically. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

Building and deploying the application artifact is intentionally deferred to a later lecture — the source code will be built locally on the developer's machine and uploaded via S3 bucket. This separation keeps the Tomcat provisioning clean and introduces S3-based deployment as a separate learning topic. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## 1.11 Troubleshooting Philosophy — Delete and Recreate

The instructor introduces a deliberate troubleshooting principle: when an instance's service is not running or produces errors, **do not SSH in and debug manually**. Instead:

1. Delete the instance
2. Launch a new instance
3. Verify: correct security group, correct AMI, correct user data script, outbound rules not modified

The reasoning is: since everything is automated through user data, there is nothing manual to preserve. The instance is disposable. The common causes of failure are: (1) wrong script pasted for wrong instance, (2) outbound security group rules modified (blocking internet access), (3) wrong AMI selected, (4) wrong security group assigned. Fixing these and relaunching is faster and more reliable than debugging a half-provisioned instance. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

⚠️ **Expert Note**: This is the **immutable infrastructure** mindset — treat instances as cattle, not pets. If something is wrong, you don't heal it; you replace it. This philosophy scales well in production because it ensures every running instance was provisioned from a known-good automation path.

***

## 1.12 Instance Lifecycle Management

If you are not continuing to the next lecture immediately, **shut down (power off) all instances** to avoid unnecessary AWS charges. When you resume, power them back on. Note that upon restart, the **public IP will change** — you must update the security group inbound rules (port 22 SSH, "My IP") to reflect your current IP address before you can SSH in again. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (GUIDED EXECUTION MODE)

## What We Are Building

We are provisioning four EC2 instances on AWS that together form the infrastructure for the vprofile application. Each instance runs one service (MySQL, Memcache, RabbitMQ, Tomcat), automated via user data scripts. By the end, all four instances are running with their services active, ready for the next phase (DNS configuration and application deployment). [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## Step 1: Clone the Source Code Repository

We need the user data scripts from the project repository before launching any instance.

**Open VSCode** → click the **Source Control** button → **Clone Repository** → paste the URL:

```
https://github.com/hkhcoder/vprofile-project
```

Select your destination directory (e.g., `F:\hkhcoder`). If you cloned this repository previously for the local setup project, delete the old clone first to avoid conflicts. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

After cloning, you will be on the `main` branch by default. **Switch to the `aws-lift-and-shift` branch** (all lowercase): click the branch indicator in VSCode's bottom bar → select `aws-lift-and-shift`. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

Navigate to the `user data/` folder — this contains all four provisioning scripts.

**Connection to system flow**: Every instance launch in the following steps will pull its script from this folder.

***

## Step 2: Verify Prerequisites

Before launching instances, confirm these exist (created in previous lectures):

* **Security groups**: backend SG, app SG, load balancer SG
* **Key pair**: `vprofile-prod-key`
* **Region**: N. Virginia (us-east-1) — same region where security groups were created

Go to **EC2 Console → Security Groups** and verify all three groups are listed. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## Step 3: Launch the MySQL Instance (vprofile-db01)

Go to **EC2 → Instances → Launch Instances**.

**Configuration:**

| Setting            | Value                             | Reasoning                          |
| ------------------ | --------------------------------- | ---------------------------------- |
| **Name**           | `vprofile-db01`                   | Standard naming for DB instance    |
| **Additional Tag** | Key: `project`, Value: `vprofile` | Project identification             |
| **Tag volumes**    | ✅ Checked                         | Prevents orphaned untagged volumes |
| **AMI**            | Amazon Linux 2023 AMI             | Project standard for backend       |
| **Instance Type**  | t2.micro (or t3.micro)            | Free tier eligible                 |
| **Key Pair**       | `vprofile-prod-key`               | SSH access                         |
| **Security Group** | vprofile backend SG               | DB is a backend service            |
| **User Data**      | Contents of `mysql.sh`            | Automates MariaDB setup            |

For user data: go to **Advanced Details** → scroll to the bottom → paste the **entire** contents of `mysql.sh` from VSCode, **including the first line** (`#!/bin/bash`). [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

Click **Launch Instance**.

⚠️ **Expert Note**: Two failure causes to watch for: (1) missing the shebang line — script silently doesn't execute, (2) modified outbound security group rules — instance can't reach the internet to download packages. Both result in a launched instance with no running service. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## Step 4: Launch the Memcache Instance (vprofile-mc01)

Go to **EC2 → Launch Instances**.

| Setting            | Value                             |
| ------------------ | --------------------------------- |
| **Name**           | `vprofile-mc01`                   |
| **Additional Tag** | Key: `project`, Value: `vprofile` |
| **Tag volumes**    | ✅                                 |
| **AMI**            | Amazon Linux 2023 AMI             |
| **Instance Type**  | t2.micro / t3.micro (free tier)   |
| **Key Pair**       | `vprofile-prod-key`               |
| **Security Group** | vprofile backend SG               |
| **User Data**      | Contents of `memcache.sh`         |

Same process: **Advanced Details → User Data → paste full `memcache.sh`** including the shebang line. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

Click **Launch Instance**.

**Connection to system flow**: Memcache joins the same backend security group as MySQL — they share the same network trust zone. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## Step 5: Launch the RabbitMQ Instance (vprofile-rmq01)

Go to **EC2 → Launch Instances**.

| Setting            | Value                             |
| ------------------ | --------------------------------- |
| **Name**           | `vprofile-rmq01`                  |
| **Additional Tag** | Key: `project`, Value: `vprofile` |
| **Tag volumes**    | ✅                                 |
| **AMI**            | Amazon Linux 2023 AMI             |
| **Instance Type**  | t2.micro / t3.micro (free tier)   |
| **Key Pair**       | `vprofile-prod-key`               |
| **Security Group** | vprofile backend SG               |
| **User Data**      | Contents of `rabbitmq.sh`         |

Paste the **complete** `rabbitmq.sh` script. This is the longest script — make sure nothing is truncated during copy-paste. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

Click **Launch Instance**.

🔍 **Deep Dive**: The RabbitMQ script downloads a repository file from GitHub at runtime. This means the instance needs internet access (outbound) to reach both GitHub (for the repo file) and the Erlang/RabbitMQ package repositories. If outbound rules are restricted, this instance is the most likely to fail. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## Step 6: Launch the Tomcat Instance (vprofile-app01)

Go to **EC2 → Launch Instances**.

| Setting            | Value                             | Note                                |
| ------------------ | --------------------------------- | ----------------------------------- |
| **Name**           | `vprofile-app01`                  | App, not backend                    |
| **Additional Tag** | Key: `project`, Value: `vprofile` |                                     |
| **Tag volumes**    | ✅                                 |                                     |
| **AMI**            | **Ubuntu 24.04 LTS** (HVM, SSD)   | ⚠️ Different from backend instances |
| **Instance Type**  | t2.micro / t3.micro (free tier)   |                                     |
| **Key Pair**       | `vprofile-prod-key`               |                                     |
| **Security Group** | **vprofile app SG**               | ⚠️ Different from backend instances |
| **User Data**      | Contents of `tomcat_ubuntu.sh`    |                                     |

**Two critical differences from the backend instances:**

1. AMI is **Ubuntu 24**, not Amazon Linux 2023
2. Security group is the **app SG**, not the backend SG

If Ubuntu 24 is not immediately visible in the AMI picker, click the search/browse option and filter for "Ubuntu 24 LTS" — ensure it shows "free tier eligible." [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

Click **Launch Instance**.

**Connection to system flow**: Tomcat in the app SG will connect to backend services. The backend SG rules permit this connection. This is the inter-tier network trust mechanism. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## Step 7: Verify All Services

After all four instances are running, verify each backend service via SSH. (The app instance is verified in a later lecture.)

### 7a. Verify MySQL (vprofile-db01)

Select `vprofile-db01` in the EC2 console → copy its **Public IP**.

```bash
ssh -i Downloads/vprofile-prod-key.pem ec2-user@<PUBLIC_IP>
```

* **`-i Downloads/vprofile-prod-key.pem`** — path to the private key file
* **`ec2-user`** — default username for Amazon Linux 2023 AMI
* **`@<PUBLIC_IP>`** — the instance's public IP from the console

Check the MariaDB service:

```bash
systemctl status mariadb
```

Expected output: **`active (running)`**. Press `q` to exit the status view. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

Verify the database content:

```bash
mysql -u admin -p admin123 accounts
```

* **`-u admin`** — connect as user `admin` (created by the user data script)
* **`-p admin123`** — password is `admin123` (from the script)
* **`accounts`** — the database name

⚠️ **Expert Note**: The instructor explicitly warns: **never type the password on the command line in real environments**. Use `-p` without a value — MySQL will prompt you to enter it interactively, keeping it out of shell history. The password is typed here only for demonstration clarity. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

Inside the MySQL shell:

```sql
show tables;
```

If tables are listed, the schema was deployed successfully. Type `exit` to leave MySQL, then `exit` to leave the instance. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

### 7b. Verify Memcache (vprofile-mc01)

Select `vprofile-mc01` → copy Public IP.

```bash
ssh -i Downloads/vprofile-prod-key.pem ec2-user@<PUBLIC_IP>
```

Switch to root:

```bash
sudo -i
```

Check the service:

```bash
systemctl status memcached
```

Expected: **`active (running)`**. Exit with `exit`, `exit`. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

### 7c. Verify RabbitMQ (vprofile-rmq01)

Select `vprofile-rmq01` → copy Public IP.

```bash
ssh -i Downloads/vprofile-prod-key.pem ec2-user@<PUBLIC_IP>
```

```bash
sudo -i
systemctl status rabbitmq-server
```

Expected: **`active (running)`**. Exit. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

**Important**: When copying public IPs, always **validate the instance name** before copying. With four instances listed, it is easy to copy the wrong IP. [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

### Troubleshooting Any Failed Service

If any service is not `active (running)`:

1. **Do not debug manually** — delete the instance
2. Launch a new instance with the **correct**: AMI, security group (backend SG for backend, app SG for Tomcat), user data script, and unchanged outbound rules
3. If it still fails after verifying all of the above → contact the instructor via Q\&A [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

## Step 8: Instance Lifecycle — Pause or Continue

* **Continuing to the next lecture** → keep all instances running
* **Taking a break** → **Stop (power off)** all instances to avoid charges
  * When resuming: start the instances; note that **public IPs will change** — update the SSH security group rule (port 22 → My IP) before attempting SSH [\[134. EC2 Instances \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/134.%20EC2%20Instances.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Architecture Map

```
[Internet]
    │
    ▼
[Load Balancer] ── LB Security Group (later lecture)
    │
    ▼
[vprofile-app01: Tomcat 10] ── App Security Group
    │         │          │        AMI: Ubuntu 24
    ▼         ▼          ▼        User Data: tomcat_ubuntu.sh
[db01]    [mc01]     [rmq01]  ── Backend Security Group
MariaDB   Memcache   RabbitMQ    AMI: Amazon Linux 2023
mysql.sh  memcache.sh rabbitmq.sh
```

## Security Group → Instance Mapping

```
Backend SG ← db01, mc01, rmq01
App SG     ← app01
LB SG      ← Load Balancer (future)

Trust flow: LB SG → App SG → Backend SG
```

## AMI Decision Tree

```
Backend service? → Amazon Linux 2023
App service (Tomcat)? → Ubuntu 24 (Tomcat 10 in default repo)
Why not Amazon Linux for Tomcat? → Manual binary install, systemd file, user creation = complex
Why not Ubuntu for backend? → Project standardization on Amazon Linux 2023
```

## User Data Script Complexity Ranking

```
Simplest → tomcat_ubuntu.sh (single apt install)
Simple   → memcache.sh (install + config change for remote listen)
Medium   → mysql.sh (install + non-interactive secure install + schema deploy)
Complex  → rabbitmq.sh (signing keys + external repo file download + dependency chain + config)
```

## Instance Launch Checklist (per instance)

```
Name tag ✓ → Project tag ✓ → Volume tags ✓
→ Correct AMI ✓ → Free tier type ✓ → Key pair ✓
→ Correct SG ✓ → User data (with shebang) ✓
→ Outbound rules untouched ✓
```

## Verification Sequence

```
For each backend instance:
  EC2 Console → Select instance → Copy Public IP (validate name!)
  → ssh -i <key> ec2-user@<IP>
  → sudo -i (if needed)
  → systemctl status <service-name>
  → Expect: active (running)

Service names:
  db01  → mariadb
  mc01  → memcached
  rmq01 → rabbitmq-server
  app01 → (verified later)
```

## Failure → Recovery Decision Chain

```
Service not running?
  → Do NOT debug manually
  → Delete instance
  → Relaunch with checklist:
      ├─ Correct AMI?
      ├─ Correct SG?
      ├─ Correct user data script?
      ├─ Shebang line included?
      └─ Outbound rules = allow all?
  → Still failing? → Instructor Q&A
```

## Key Operational Details to Remember

```
Default SSH user for Amazon Linux 2023 → ec2-user
Default SSH user for Ubuntu            → ubuntu (not used in this lecture's SSH demos)
MariaDB package on Amazon Linux 2023   → mariadb105-server
Memcache remote listen                 → replace 127.0.0.1 with 0.0.0.0
Memcache port                          → 11211
RabbitMQ repo file location            → /etc/yum.repos.d/
RabbitMQ dependencies                  → Erlang, socat, logrotate
MySQL test password                    → admin123 (never expose in production)
Tomcat package on Ubuntu 24            → tomcat10
Public IP changes on stop/start        → must update SG inbound rules
```

## Reusable Engineering Patterns Extracted

```
1. IMMUTABLE INFRASTRUCTURE
   Broken instance → delete → recreate (never patch in-place)

2. CONFIGURATION-AS-CODE
   All provisioning logic in version-controlled shell scripts
   No manual steps → reproducible infrastructure

3. EXTERNAL CONFIG FILE PATTERN
   Complex config (RabbitMQ repo def) stored as a file in repo
   Downloaded at runtime → keeps scripts clean and readable

4. NON-INTERACTIVE AUTOMATION
   Interactive commands (mysql_secure_installation) replaced with
   equivalent non-interactive SQL queries for background execution

5. NETWORK TRUST ZONES
   Security groups = identity-based network segmentation
   Being in a SG = permission to communicate with allowed SGs

6. OS-TOOL AFFINITY
   Choose OS based on package availability for your tool
   Ubuntu for Tomcat = one command vs. multi-step manual on CentOS/AL

7. TAG EVERYTHING
   Instances + Volumes → prevents orphaned resources and cost leaks
```

## Next Phase Connection

```
This lecture → Instances provisioned + services verified
Next lecture → Private DNS entries (so services find each other by name, not IP)
Later        → Build artifact locally → Upload to S3 → Deploy to Tomcat
Later        → Load balancer creation in LB security group
```

***

This completes the full reconstruction of the video content. All four EC2 instances are now provisioned with automated user data, placed in the correct security groups, and verified. The next step in the course is setting up private DNS entries so these services can communicate using hostnames rather than IP addresses. Want me to generate Anki flashcards from this material, or would you like to do a fill-in-the-blank recall test? 🚀

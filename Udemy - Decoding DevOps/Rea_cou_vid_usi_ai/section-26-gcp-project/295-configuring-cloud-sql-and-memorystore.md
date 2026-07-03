# GCP Backend Services — Cloud SQL, Memorystore & VPC Peering Configuration

**Source:** Video caption file — *"Configuring Cloud SQL and Memorystore"* (from a GCP / DevOps course) [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Context: What Exists Before This Lecture

Before this lecture begins, the VPC and bastion host have already been created in the previous lecture. The VPC is the custom network in GCP, and the bastion host is a VM instance in a public subnet that serves as the SSH jump point into the private network. Now, the backend services — **Cloud SQL** (managed MySQL) and **Memorystore** (managed Memcache) — need to be created inside the Google-managed private network and connected to our VPC via peering. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## 1.2 — The Core Problem: Connecting Your VPC to Google-Managed Services

Cloud SQL and Memorystore are **managed services** — Google runs and maintains the actual MySQL and Memcache instances on infrastructure that you don't control. These services live in **Google's own internal network**, not in your VPC. Your application VMs live in **your VPC**. The problem: how do you connect your VPC to Google's internal network so your application can reach these backend services privately, without going over the public internet? [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

The answer is a three-step architecture:

1. **Private Service Access (PSA)** — allocate a range of IP addresses from your VPC's address space for Google to use.
2. **VPC Peering** — establish a network peering connection between your VPC and Google's service network.
3. **Service creation** — launch Cloud SQL and Memorystore, which receive IP addresses from the allocated range and are reachable from your VPC through the peering connection.

This is fundamentally different from AWS's approach (where RDS lives inside your VPC's subnets). In GCP, managed services live in Google's network, and VPC peering bridges the gap. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## 1.3 — Private Service Access (PSA): The IP Address Range

Private Service Access is the mechanism by which you **reserve a range of private IP addresses** from your VPC's address space and hand it to Google. Google's managed services (Cloud SQL, Memorystore) will take their IP addresses from this range. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

The command `gcloud compute addresses create` with `--purpose=VPC_PEERING` creates this reserved range. You're telling Google: "Here is a block of IP addresses from my VPC's space. Use these for the backend services you manage for me." The range is **global** (not tied to a specific region) and is associated with a specific VPC. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

After the range is created, you can verify it in the GCP Console under your VPC's **Private Service Access** section, which shows the range name and the actual CIDR block that Google allocated. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

🔍 **Deep Dive:**
The PSA range is not a subnet you create — it's an IP allocation that Google manages. You specify the prefix length (how large the range should be), and Google allocates a specific CIDR block from your VPC's address space. This ensures there's no IP address overlap between your VPC resources and Google's managed services. The managed services' IPs come from this range, which is why the Cloud SQL instance's private IP falls within this allocated block. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## 1.4 — VPC Peering: Connecting Your Network to Google's Network

Once the IP range is allocated, **VPC peering** creates the actual network connection between your VPC and Google's service producer network. The command `gcloud services vpc-peerings connect` establishes this connection, linking your VPC to `servicenetworking.googleapis.com` (Google's networking services) and specifying which IP range to use. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

After peering is established, traffic between your VPC and Google's managed services flows **privately** — it never traverses the public internet. Your application VMs can reach Cloud SQL and Memorystore using private IP addresses, as if they were on the same network. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

You can verify the peering in the GCP Console: **VPC Network → VPC Network Peering** shows the active peering connection. You can also see it from your VPC's detail page under the VPC Network Peering tab. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

The video explicitly notes: "If we are able to connect to our MySQL instance, VPC peering will also be validated." Successfully connecting to Cloud SQL from the bastion host proves that the peering is working — the traffic flows privately from your VPC through the peering connection to Google's service network. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## 1.5 — Cloud SQL: Google's Managed MySQL (Equivalent to AWS RDS)

Cloud SQL is GCP's managed relational database service. The video draws the direct comparison: "Like in AWS we create RDS." Cloud SQL handles the database engine installation, patching, backups, and high availability — you just specify what you want and use it. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

The instance is created with `gcloud sql instances create` with key parameters: [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

* **Database version:** `MYSQL_8_0` — specifies MySQL 8 as the engine.
* **Tier:** `db-f1-micro` — the smallest instance type, chosen for cost efficiency during learning.
* **Region:** `us-central1` — where the instance runs.
* **`--no-assign-ip`** — this is the critical networking flag. It tells Cloud SQL **not to assign a public IP address**. The instance will only have a private IP, taken from the PSA range created earlier. This ensures the database is only accessible through the private network (via VPC peering), never from the public internet.
* **Network:** Your VPC, specified either as `$VPC` or as the full path `projects/<project-id>/global/networks/<vpc-name>`. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

The Cloud SQL instance takes **a lot of time** to create — the video advises a 10-minute break. Once created, you can find it in the GCP Console under Cloud SQL, showing the instance ID, type, and private IP address (which falls within the PSA range). [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## 1.6 — Cloud SQL Post-Creation Setup: Database and User Configuration

After the Cloud SQL instance exists, two additional configuration steps are needed for the vProfile application: [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

**Create the `accounts` database:** The vProfile application expects a database named `accounts`. The command `gcloud sql databases create accounts --instance=<db-name>` creates this database inside the Cloud SQL instance.

**Set the root user password:** The command `gcloud sql users set-password root --host=% --instance=<db-name> --password=<value>` sets the password for the MySQL root user. The `--host=%` flag is important — the percent sign means "allow this user to connect from any host" (remote access). This is necessary because the vProfile application VMs will connect to the database from a different machine (remote access), not from the database server itself. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

The password must match what's configured in the vProfile application's `application.properties` file. The video shows that this file contains the database hostname, username (`root`), and password. If you change the password, you must also change it in `application.properties` — otherwise the application can't connect. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## 1.7 — Memorystore for Memcached: Google's Managed Caching Service

Memorystore is GCP's managed caching service. The video creates a **Memcached** instance (as opposed to Redis, which Memorystore also supports). This is the equivalent of AWS ElastiCache. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

The instance has minimum resource requirements: **at least 2 CPUs and 2 GB RAM** per node. The video creates the minimum viable configuration: 1 node with 2 CPUs and 2 GB RAM. Like Cloud SQL, Memorystore connects to your VPC through the authorized network configuration, using the full VPC path format: `projects/<project-id>/global/networks/<vpc-name>`. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

Memorystore also takes significant time to create. The video proceeds with other work (database initialization) while waiting for it to provision. Once created, it appears in the GCP Console under **Memorystore for Memcached**, showing the IP address, port number, node count, RAM, and CPU allocation. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## 1.8 — Database Initialization: Schema Setup from the Bastion Host

The database instance exists and is empty (except for the `accounts` database). The vProfile application needs tables and data — this comes from a SQL backup file (`db_backup.sql`) in the project's source code repository. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

The initialization must happen from the **bastion host** because the Cloud SQL instance only has a private IP — it's not accessible from the public internet or from your local machine. The bastion host is in the VPC and can reach the Cloud SQL instance through the VPC peering connection. This is the standard **bastion host access pattern**: you SSH into the bastion host (which has a public IP), and from there you access private resources. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

On the bastion host, you install the MySQL client (`apt install mysql-client`), connect to the Cloud SQL instance using its private IP, and run the SQL file against the `accounts` database. The video downloads the SQL file from GitHub (the GCP branch of the vProfile project) using `wget`. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

⚠️ **Expert Note:**
The video explicitly warns about exposing database passwords on the command line: "Exposing like this DB password is very wrong." Instead of passing the password as a flag value (`-p<password>`), the recommended approach is to use `-p` alone (with a space and then the database name), which causes MySQL to prompt for the password interactively. This prevents the password from appearing in shell history and process listings. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## 1.9 — The Complete Backend Architecture

After this lecture, the backend is fully configured: [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

* **PSA range** allocated → Google has IP addresses to assign to managed services.
* **VPC peering** established → your VPC can communicate with Google's service network privately.
* **Cloud SQL** (MySQL 8) running with private IP → `accounts` database created, root password set, schema initialized with tables.
* **Memorystore** (Memcached) running with private IP → caching layer ready.
* **Bastion host** used to access and initialize private backend services.

The next lectures will work on the **frontend** — application VMs, load balancer, and connecting the application to these backend services. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating the backend services for the vProfile application on GCP: a Cloud SQL MySQL instance and a Memorystore Memcached instance, both connected privately to our VPC via Private Service Access and VPC peering. We then initialize the database with the vProfile schema from the bastion host. The final outcome: a fully functional backend (database + cache) accessible only through the private network, ready for the application VMs to connect to in subsequent lectures. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## Execution Flow Overview

```
Phase 1: Private Service Access (IP range allocation)
Phase 2: VPC Peering (connect VPC to Google services)
Phase 3: Create Cloud SQL instance (MySQL 8)
Phase 4: Create database + set root password
Phase 5: Create Memorystore instance (Memcached)
Phase 6: Initialize database from bastion host
Phase 7: Verify Memorystore creation
```

***

### Step 1: Allocate Private Service Access IP Range

**What we are doing:** Reserving a block of IP addresses from our VPC's space for Google's managed services to use.

```bash
gcloud compute addresses create <range-name> \
  --global \
  --purpose=VPC_PEERING \
  --network=$VPC \
  --prefix-length=<length>
```

**Breakdown:**

* `gcloud compute addresses create <range-name>` — creates a named IP address range.
* `--global` — the range is global (not region-specific).
* `--purpose=VPC_PEERING` — marks this range specifically for VPC peering with Google services.
* `--network=$VPC` — associates the range with your VPC (using the VPC variable set in earlier lectures).
* `--prefix-length=<length>` — defines the size of the range (e.g., `/20` gives 4096 addresses). [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

**Expected output:** Confirmation that the address range was created.

**How to verify:** GCP Console → VPC Network → select your VPC → Private Service Access tab → the range name and CIDR block should appear. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

### Step 2: Establish VPC Peering

**What we are doing:** Creating a network peering connection between our VPC and Google's service producer network.

```bash
gcloud services vpc-peerings connect \
  --network=$VPC \
  --service=servicenetworking.googleapis.com \
  --ranges=<range-name>
```

**Breakdown:**

* `gcloud services vpc-peerings connect` — establishes the peering.
* `--network=$VPC` — your VPC to peer.
* `--service=servicenetworking.googleapis.com` — Google's networking service endpoint.
* `--ranges=<range-name>` — the PSA range created in Step 1, from which managed services will receive IPs. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

**This takes time.** Wait for "Operation finished successfully."

**How to verify:** GCP Console → VPC Network → VPC Network Peering → the peering connection should be visible. Also accessible from your VPC's detail page under the VPC Network Peering tab. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

### Step 3: Create Cloud SQL Instance

**What we are doing:** Launching a managed MySQL 8 instance with a private IP only (no public access).

```bash
gcloud sql instances create $db \
  --database-version=MYSQL_8_0 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --no-assign-ip \
  --network=projects/$PROJECT_ID/global/networks/$VPC
```

**Breakdown:**

* `gcloud sql instances create $db` — creates a Cloud SQL instance with the name stored in `$db` variable.
* `--database-version=MYSQL_8_0` — MySQL 8.0 engine.
* `--tier=db-f1-micro` — smallest available instance type (cost-efficient for learning).
* `--region=us-central1` — deployment region.
* `--no-assign-ip` — **no public IP**. The instance gets only a private IP from the PSA range. This ensures it's only accessible via VPC peering.
* `--network=projects/$PROJECT_ID/global/networks/$VPC` — the full path to your VPC. You can also use just `$VPC` in some contexts. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

**⏱️ This takes a lot of time (10+ minutes).** The video advises taking a break.

**Expected output:** Instance ready confirmation.

**How to verify:** GCP Console → search "Cloud SQL" → the instance ID appears with its type and **private IP address** (which should fall within the PSA range from Step 1). [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

### Step 4: Create Database and Set Root Password

**What we are doing:** Creating the `accounts` database and configuring root user access for the vProfile application.

**Create the database:**

```bash
gcloud sql databases create accounts --instance=$db
```

**Breakdown:**

* `accounts` — the database name required by the vProfile application.
* `--instance=$db` — the Cloud SQL instance to create the database in. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

**Set the root password:**

```bash
gcloud sql users set-password root \
  --host=% \
  --instance=$db \
  --password=$dbpass
```

**Breakdown:**

* `root` — the MySQL user.
* `--host=%` — the `%` wildcard means this user can connect from **any host** (remote access). Required because the application VMs will access the database from different machines.
* `--instance=$db` — the Cloud SQL instance.
* `--password=$dbpass` — the password value (stored in a variable from earlier setup). Must match the value in `application.properties`. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

**Common mistake:** Changing the password here but not updating `application.properties` — the application won't be able to connect.

***

### Step 5: Create Memorystore Memcached Instance

**What we are doing:** Launching a managed Memcached instance for the vProfile application's caching layer.

```bash
gcloud memcache instances create vprofile-memcache \
  --region=us-central1 \
  --node-count=1 \
  --node-cpu=2 \
  --node-memory=2GB \
  --authorized-network="projects/$PROJECT_ID/global/networks/$VPC"
```

**Breakdown:**

* `vprofile-memcache` — instance name.
* `--region=us-central1` — deployment region.
* `--node-count=1` — one cache node (minimum).
* `--node-cpu=2` — 2 CPUs per node (**minimum required** — cannot go lower).
* `--node-memory=2GB` — 2 GB RAM per node (**minimum required** — cannot go lower).
* `--authorized-network="projects/$PROJECT_ID/global/networks/$VPC"` — full VPC path in double quotes. This authorizes your VPC to access this Memcached instance. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

**⏱️ This also takes a lot of time.** Proceed with database initialization (Step 6) while waiting.

**How to verify:** GCP Console → search "memcache" → Memorystore for Memcached → instance shows IP address, port, node count, RAM, and CPU. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

### Step 6: Initialize Database from Bastion Host

**What we are doing:** SSHing into the bastion host, installing the MySQL client, connecting to the Cloud SQL instance, and running the schema SQL file to create tables.

#### 6a: SSH into the Bastion Host

```bash
ssh -i <key-name> devops@<bastion-public-ip>
```

**Get the bastion host's public IP:** GCP Console → VM Instances → bastion host → copy the **public** (external) IP, not the private (internal) IP. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

#### 6b: Switch to Root and Install MySQL Client

```bash
sudo -i
apt install mysql-client -y
```

 [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

#### 6c: Connect to Cloud SQL

```bash
mysql -h <cloud-sql-private-ip> -u root -p accounts
```

**Breakdown:**

* `-h <cloud-sql-private-ip>` — the private IP of the Cloud SQL instance (found in Cloud SQL console).
* `-u root` — connect as the root user.
* `-p` — prompt for password (do **NOT** put the password on the command line — "exposing like this DB password is very wrong"). Leave a space after `-p`, then specify the database name.
* `accounts` — connect directly to the `accounts` database. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

**When prompted for password:** Paste the password (Shift+Insert in terminal).

**Expected output:** MySQL prompt appears → you're connected to the `accounts` database.

**What this validates:** If the connection succeeds, it proves VPC peering is working — traffic flows from the bastion host (your VPC) through the peering connection to Cloud SQL (Google's network). [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

**Exit MySQL:** `exit`

#### 6d: Download and Run the Schema File

```bash
wget <github-raw-url-to-db_backup.sql>
```

The SQL file is from the **GCP branch** of the vProfile project repository on GitHub. The URL is in the `backend.sh` script at the end. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

```bash
mysql -h <cloud-sql-private-ip> -u root -p accounts < db_backup.sql
```

**Breakdown:**

* Same connection parameters as before.
* `< db_backup.sql` — **input redirection**: feeds the SQL file's contents into the MySQL client, executing all SQL statements (CREATE TABLE, INSERT, etc.) against the `accounts` database. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

**When prompted:** Enter the database password.

#### 6e: Verify Initialization

```bash
mysql -h <cloud-sql-private-ip> -u root -p accounts
```

Enter password when prompted.

```sql
show tables;
```

**Expected output:** List of tables in the `accounts` database — confirming the schema was applied successfully. [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

**Exit:** `exit`

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    GCP Backend Services — Cloud SQL + Memorystore + VPC Peering
PURPOSE:  Create private backend (DB + cache) for vProfile, connected via VPC peering
CONTEXT:  After VPC + bastion host setup; before frontend VM + load balancer
```

 [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## Architecture (Complete After This Lecture)

```
YOUR VPC
  ├── Bastion Host (public IP) ← SSH entry point
  │      │
  │      │ (mysql -h <private-ip>)
  │      ▼
  │   ┌──────── VPC PEERING ────────┐
  │   │                              │
  │   │  GOOGLE SERVICE NETWORK      │
  │   │  ├── Cloud SQL (MySQL 8)     │
  │   │  │   IP from PSA range       │
  │   │  │   Private IP only         │
  │   │  │   DB: accounts            │
  │   │  │                           │
  │   │  └── Memorystore (Memcache)  │
  │   │      IP from Google network  │
  │   │      Port: 11211             │
  │   └──────────────────────────────┘
  │
  └── (Future: App VMs, Load Balancer)
```

 [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## Three-Step Private Connectivity Pattern

```
STEP 1: PSA (Private Service Access)
  gcloud compute addresses create <range> --purpose=VPC_PEERING --network=$VPC
  → Reserve IP range from your VPC for Google services

STEP 2: VPC Peering
  gcloud services vpc-peerings connect --network=$VPC --ranges=<range>
  → Connect your VPC to Google's service network

STEP 3: Create Services with --no-assign-ip + --network=$VPC
  → Services get private IPs from PSA range
  → Accessible only through VPC peering (no public internet)

DEPENDENCY CHAIN:
  PSA range → VPC peering → Cloud SQL / Memorystore
  (each step requires the previous)
```

 [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## GCP vs AWS Comparison

```
CONCEPT          GCP                          AWS
──────           ───                          ───
Managed DB       Cloud SQL                    RDS
Managed Cache    Memorystore                  ElastiCache
Network Model    VPC Peering to Google net    Service lives IN your VPC subnets
IP Allocation    PSA range (you reserve)      Subnet CIDR (automatic)
Private Access   --no-assign-ip + peering     Deploy in private subnet
```

 [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## Cloud SQL Creation Parameters

```
gcloud sql instances create $db
  --database-version=MYSQL_8_0     ← engine
  --tier=db-f1-micro               ← smallest instance (cost)
  --region=us-central1             ← region
  --no-assign-ip                   ← PRIVATE IP ONLY (no public)
  --network=$VPC_PATH              ← your VPC

POST-CREATION:
  1. gcloud sql databases create accounts --instance=$db
  2. gcloud sql users set-password root --host=% --instance=$db --password=$dbpass
     └── --host=% means remote access from any host
```

 [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## Memorystore Creation Parameters

```
gcloud memcache instances create vprofile-memcache
  --region=us-central1
  --node-count=1                   ← minimum nodes
  --node-cpu=2                     ← MINIMUM 2 CPU (can't go lower)
  --node-memory=2GB                ← MINIMUM 2 GB RAM (can't go lower)
  --authorized-network="$VPC_PATH" ← full path in double quotes
```

 [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## Database Initialization Flow

```
LOCAL MACHINE
    │ ssh -i key devops@<bastion-public-ip>
    ▼
BASTION HOST (public subnet)
    │ sudo -i
    │ apt install mysql-client -y
    │ wget <db_backup.sql from GitHub GCP branch>
    │ mysql -h <cloud-sql-private-ip> -u root -p accounts < db_backup.sql
    ▼
CLOUD SQL (private, via VPC peering)
    │ Tables created in accounts DB
    ▼
VERIFIED: show tables; → tables visible

⚠️ PASSWORD SECURITY:
  ❌ mysql -u root -p<password>     ← password in command line (exposed)
  ✅ mysql -u root -p accounts      ← prompts interactively (safe)
```

 [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## VPC Path Formats

```
SHORT:   $VPC
FULL:    projects/$PROJECT_ID/global/networks/$VPC

WHEN TO USE FULL PATH:
  --network=    (Cloud SQL)        → either works
  --authorized-network= (Memcache) → MUST use full path in double quotes
```

 [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## Verification Checklist

```
CHECK                    WHERE                              EXPECTED
─────                    ─────                              ────────
PSA range               VPC → Private Service Access tab    Range name + CIDR
VPC peering             VPC Network Peering page            Active peering
Cloud SQL               Cloud SQL console                   Instance + private IP in PSA range
Database                mysql → show databases;             'accounts' exists
Root password           mysql login succeeds                Connected successfully
Schema                  mysql → show tables;                Tables in accounts DB
Memorystore             Memorystore for Memcached           Instance + IP + port
VPC peering (implicit)  mysql from bastion → Cloud SQL      Connection succeeds = peering works
```

 [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## Timing Awareness

```
RESOURCE             CREATION TIME    STRATEGY
────────             ─────────────    ────────
PSA range            Fast             Proceed immediately
VPC peering          Minutes          Wait for completion
Cloud SQL            10+ minutes      Take a break / proceed to Memorystore
Memorystore          10+ minutes      Proceed to DB initialization while waiting

PATTERN: Start long-running creates → do other work → verify later
```

 [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## application.properties Connection

```
application.properties (in vProfile source):
  db.host = <hostname>     ← will map to Cloud SQL IP via Cloud DNS (later)
  db.user = root           ← must match Cloud SQL user
  db.password = <value>    ← must match gcloud sql users set-password value

RULE: Change password in Cloud SQL → MUST change in application.properties
      Keep them in sync or application can't connect
```

 [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## Reusable Engineering Patterns

| Pattern                                         | Manifestation                                                                        |
| ----------------------------------------------- | ------------------------------------------------------------------------------------ |
| **Private Service Connectivity via Peering**    | PSA range + VPC peering = private access to managed services without public internet |
| **Bastion Host as Private Access Gateway**      | SSH to bastion (public) → access private resources (Cloud SQL) from inside the VPC   |
| **Dependency Chain Creation**                   | PSA range → VPC peering → services (each requires the previous)                      |
| **Parallel Work During Provisioning**           | Start Cloud SQL/Memorystore → do DB init while waiting for Memorystore               |
| **No Public IP for Backend Services**           | `--no-assign-ip` = security by design (no attack surface from internet)              |
| **Schema Initialization via Input Redirection** | `mysql ... < file.sql` = batch-execute SQL from file (same pattern as AWS RDS init)  |
| **Credential Consistency Across Config**        | Password in Cloud SQL must match application.properties — single source of truth     |
| **Implicit Validation Through Usage**           | Successfully connecting to Cloud SQL from bastion validates VPC peering is working   |

 [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

## One-Line System Reconstruction

> **GCP backend setup requires a three-step private connectivity pattern — allocate a PSA IP range (`gcloud compute addresses create --purpose=VPC_PEERING`), establish VPC peering (`gcloud services vpc-peerings connect`), then create Cloud SQL (`--no-assign-ip --network=$VPC`, MySQL 8, `db-f1-micro`) and Memorystore (`--node-cpu=2 --node-memory=2GB`, minimum specs) which receive private IPs from the PSA range — followed by database initialization from the bastion host (`mysql -h <private-ip> -u root -p accounts < db_backup.sql`) that also implicitly validates the VPC peering connection, with passwords matching `application.properties` for application connectivity.** [\[295-config...emorystore \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/295-configuring-cloud-sql-and-memorystore.txt)

***

This completes the full reconstruction of the Configuring Cloud SQL and Memorystore lecture. It builds on the VPC and bastion host setup from the previous lecture and establishes the backend that the frontend application VMs and load balancer (next lectures) will connect to. Let me know if you'd like any section expanded or adjusted! 🚀

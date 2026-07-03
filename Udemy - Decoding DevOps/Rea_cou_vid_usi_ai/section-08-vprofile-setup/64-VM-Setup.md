**Source:** Video lecture caption file — *VM Setup for Vprofile Project* + accompanying PDF document — *Vprofile Project Setup (Windows & Mac Intel)*

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 What Is the Vprofile Project?

The Vprofile project is a **multi-tier web application stack** that mimics a real production environment. It consists of **six services** working together to serve a web application to end users. The entire stack is deployed across **five virtual machines** managed by a single multi-VM Vagrantfile. The purpose is to give you hands-on experience setting up a complete application infrastructure from scratch — the same kind of architecture you'd encounter in enterprise environments.

The six services and their roles are:

| Service             | Role                                   | VM Hostname |
| ------------------- | -------------------------------------- | ----------- |
| **Nginx**           | Web Service (reverse proxy / frontend) | web01       |
| **Tomcat**          | Application Server (runs the Java app) | app01       |
| **RabbitMQ**        | Broker / Queuing Agent (message queue) | rmq01       |
| **Memcache**        | DB Caching (caches database queries)   | mc01        |
| **MySQL (MariaDB)** | SQL Database (persistent data store)   | db01        |
| **ElasticSearch**   | Indexing / Search service              | *Skipped*   |

ElasticSearch is **intentionally skipped** in this setup because it requires a large amount of memory, making it impractical for local VM environments. This is a pragmatic engineering decision — you exclude components that exceed your resource constraints while keeping the core architecture functional.

## 1.2 Multi-Tier Architecture: The Request Flow

Understanding how these services connect is critical. The architecture follows a **layered dependency chain** where each tier serves the tier above it:

**User → Nginx (web01) → Tomcat (app01) → RabbitMQ (rmq01) / Memcache (mc01) → MySQL (db01)**

When a user accesses the application, their HTTP request hits **Nginx** first. Nginx acts as a **reverse proxy** — it doesn't serve the application itself but forwards the request to **Tomcat** on port 8080. Tomcat is the application server running the actual Java web application. When Tomcat needs data, it first checks **Memcache** (the caching layer). If the data isn't cached, Tomcat queries **MySQL** (the database). **RabbitMQ** handles asynchronous message queuing between application components.

This layered architecture means each component **depends on the components below it**. Nginx depends on Tomcat being available. Tomcat depends on Memcache and MySQL being reachable. This dependency chain directly determines the **setup order** and the **shutdown order** (covered in §1.6).

> 🔍 **Deep Dive**
> The Nginx configuration in the PDF reveals the reverse proxy mechanism explicitly. The `upstream vproapp { server app01:8080; }` block defines a backend pool pointing to Tomcat. The `proxy_pass http://vproapp;` directive inside the `location /` block forwards all incoming requests on port 80 to that upstream. This is a standard Nginx reverse proxy pattern — Nginx listens on port 80 (HTTP) and proxies to Tomcat on port 8080. Notice that the upstream uses the **hostname** `app01`, not an IP address. This works because of the hostmanager plugin (§1.5).

## 1.3 The Multi-VM Vagrantfile

Instead of managing five separate Vagrant projects, all five VMs are defined in a **single Vagrantfile**. This is a multi-VM Vagrantfile — one configuration file that declares multiple virtual machines, each with its own settings (hostname, IP address, memory, box image).

The five VMs and their configurations:

| VM       | Hostname | OS       | Memory |
| -------- | -------- | -------- | ------ |
| DB       | db01     | CentOS 9 | 600 MB |
| Memcache | mc01     | CentOS 9 | 600 MB |
| RabbitMQ | rmq01    | CentOS 9 | 600 MB |
| Tomcat   | app01    | CentOS 9 | 800 MB |
| Nginx    | web01    | Ubuntu   | 800 MB |

Several important observations here. The **first four VMs** use CentOS 9, while the **Nginx VM uses Ubuntu**. This is intentional — it mirrors real-world environments where different services may run on different Linux distributions. The memory allocations are set to the **minimum viable values** (600 MB for backend services, 800 MB for Tomcat and Nginx). The instructor notes that if you have 16 GB or more of RAM, you can increase each VM to 1024 MB (1 GB) for better performance.

The **box name differs by platform**: `ubuntu/jammy64` and CentOS boxes for Windows/macOS Intel, and ARM64-specific boxes for macOS M1/M2/M3 chips. The source code repository contains **separate folders** for each platform variant — `Manual_provisioning_WinMacIntel` and a separate folder for M-series Macs.

Each VM definition in the Vagrantfile includes a **hostname** setting. When you log into a VM, you'll see this hostname in the terminal prompt (e.g., `db01`). This isn't cosmetic — hostnames are used for inter-VM communication through the host file entries (§1.5).

## 1.4 Source Code Management: Clone and Branch

The entire project source code lives in a GitHub repository at `github.com/hkhcoders/vprofile-project`. The workflow begins by **cloning** this repository to your local machine.

A critical step that the instructor emphasizes as **"very, very important"** is **switching to the `local` branch** after cloning. The repository contains multiple branches for different sections of the course. If you stay on the `main` branch, you'll be looking at the wrong code. In VS Code, you click the branch indicator (bottom-left, showing "main") and select `origin/local`. After switching, you should see `local` displayed — nothing else.

Within the repository, the relevant path is: `vagrant/Manual_provisioning/` followed by the platform-specific subfolder. Inside that folder, you find the **Vagrantfile** and the **PDF setup document**.

> ⚠️ **Expert Note**
> The branch-switching step is a common failure point for beginners. If commands or file paths don't match what the instructor shows, the most likely cause is being on the wrong branch. Always verify your branch before proceeding.

## 1.5 The Vagrant Hostmanager Plugin: Automatic DNS Resolution

This is one of the most important concepts in this lecture. In a multi-VM environment, VMs need to communicate with each other **by name** (e.g., Tomcat needs to reach the database as `db01`, not as `192.168.56.x`). The mechanism that enables name-to-IP resolution without a DNS server is the **`/etc/hosts` file**.

The `/etc/hosts` file on any Linux (or any OS) works like a **local DNS lookup table**. When a process tries to connect to a hostname (e.g., `app01`), the operating system **first checks `/etc/hosts`** for a matching entry. If found, it uses the mapped IP address. If not found, it queries the DNS server (typically your ISP's DNS).

Manually editing `/etc/hosts` on every VM every time you create or destroy the environment would be tedious and error-prone. The **`vagrant-hostmanager`** plugin solves this by **automatically populating `/etc/hosts`** on all VMs with hostname-to-IP mappings for every VM defined in the Vagrantfile.

The plugin requires:

1. **Installation:** `vagrant plugin install vagrant-hostmanager` (run once on your host machine)
2. **Vagrantfile configuration:** Two global settings:
   * `config.hostmanager.enabled = true` — activates the plugin
   * `config.hostmanager.manage_host = true` — also updates the **host machine's** `/etc/hosts` file

When `vagrant up` runs, the plugin reads all VM definitions (hostnames and IPs), and writes the corresponding entries into `/etc/hosts` on **every VM** and optionally on the host machine. This means after VMs are up, `app01` can reach `db01` by name, `web01` can reach `app01` by name, and so on — without any manual configuration.

> 🔍 **Deep Dive**
> This is the reason the Nginx configuration can use `server app01:8080;` instead of a hardcoded IP. The hostname `app01` resolves through `/etc/hosts` to the Tomcat VM's IP address. If the hostmanager plugin were not installed or configured, this resolution would fail, and Nginx would return a 502 Bad Gateway error — the reverse proxy couldn't find its upstream. The same applies to application configuration files where backend service hostnames are referenced.

## 1.6 Service Setup Order and Shutdown Order

The PDF document specifies a **mandatory setup order**:

```
Startup:  MySQL → Memcache → RabbitMQ → Tomcat → Nginx
Shutdown: Nginx → Tomcat → RabbitMQ → Memcache → MySQL
```

The reasoning is **dependency-driven**. You start from the **bottom of the stack** (the service with no dependencies — MySQL) and work upward. Each service you bring up next depends on the services already running below it. Memcache connects to MySQL, so MySQL must be up first. Tomcat connects to Memcache, RabbitMQ, and MySQL, so all three must be running before Tomcat starts. Nginx proxies to Tomcat, so Tomcat must be ready before Nginx starts serving traffic.

For shutdown, the order **reverses**. You first cut user access by stopping the frontend (Nginx), then work down to the database last. This prevents users from hitting a partially-dismantled stack.

The instructor notes this is a **standard practice, not always mandatory**. Some applications have hard dependencies (the app crashes if the database is down), making the order truly mandatory. Others are more resilient. But following this order is always the safe approach.

## 1.7 The "Manual Provisioning" Approach

This lecture uses **manual provisioning** — meaning the VMs are brought up as bare operating systems, and you **log into each one individually** to install and configure services by executing commands one by one. This is deliberately contrasted with automated provisioning (where Vagrant provisioning scripts do everything automatically).

The value of manual provisioning is **understanding**. By executing each command yourself, you learn what every service needs, how it's configured, and how components connect. This understanding is essential before you can write or review automated scripts.

## 1.8 Global Status and Environment Cleanup

Before creating new VMs, the instructor checks for existing VMs using `vagrant global-status`. This command shows **all Vagrant-managed VMs across your entire system**, regardless of which project folder you're in. If stale VMs exist, they consume resources and may cause IP conflicts.

The cleanup command `vagrant global-status --prune` removes **stale entries** — records of VMs that no longer exist on disk but are still tracked by Vagrant's internal index. This gives you a clean starting state.

## 1.9 Connectivity Validation: The Ping Sanity Test

After all VMs are up, the instructor demonstrates a **sanity test** using the `ping` command from inside a VM. The command `ping app01 -c 4` sends four ICMP packets to `app01`. If replies come back, it confirms two things: (1) hostname resolution is working (the hostmanager plugin did its job), and (2) network connectivity between VMs is functional.

If pings fail (timeouts or "host not found"), the troubleshooting steps are: verify `/etc/hosts` entries exist, reboot the target VM (`vagrant reload <vmname>`), or re-run `vagrant up`.

## 1.10 The Five Service Setups — Conceptual Architecture

Each of the five services follows a **common setup pattern** with service-specific variations. Understanding the pattern first makes the individual setups easier to absorb.

**Common Pattern (repeated for every service):**

1. SSH into the VM
2. Verify `/etc/hosts` entries
3. Update the OS (`dnf update` for CentOS, `apt update/upgrade` for Ubuntu)
4. Install repositories/dependencies
5. Install the service package
6. Configure the service
7. Start and enable the service
8. Configure the firewall to allow the service's port

**Service-specific variations:**

**MySQL (db01):** Requires running `mysql_secure_installation` (an interactive hardening script), creating a database (`accounts`), creating a user (`admin`), importing schema data from the source code's SQL backup file, and opening port **3306**.

**Memcache (mc01):** Requires changing the bind address from `127.0.0.1` (localhost-only) to `0.0.0.0` (all interfaces) using `sed`, so other VMs can connect. Opens port **11211** (TCP) and **11111** (UDP).

**RabbitMQ (rmq01):** Requires modifying the config to allow non-localhost users (`loopback_users` set to empty), creating a test user with administrator tags and full permissions. Opens port **5672**.

**Tomcat (app01):** The most complex setup. Requires Java 17 (OpenJDK), downloading and extracting Tomcat manually (not from a package manager), creating a dedicated `tomcat` system user, writing a custom **systemd service file** for Tomcat, installing **Maven**, cloning the source code, updating `application.properties` with backend server details, building the application with `mvn install`, and deploying the WAR file. Opens port **8080**.

> 🔍 **Deep Dive — Tomcat Systemd Service File**
> Tomcat doesn't ship as a system service on CentOS — it's a standalone Java application. To manage it with `systemctl` (start/stop/enable), you must create a custom service file at `/etc/systemd/system/tomcat.service`. This file defines the `[Unit]` (dependencies — `After=network.target`), `[Service]` (user, working directory, Java and Catalina environment variables, start/stop commands, restart behavior), and `[Install]` (when to activate — `multi-user.target`). After creating this file, `systemctl daemon-reload` is required to make systemd aware of the new service definition.

> 🔍 **Deep Dive — Code Build and Deploy**
> The build process uses Maven (`mvn install`) to compile the Java source code into a **WAR file** (`vprofile-v2.war`). Deployment involves: stopping Tomcat → removing the existing `ROOT` webapp → copying the WAR as `ROOT.war` into Tomcat's `webapps/` directory → restarting Tomcat. Naming it `ROOT.war` makes it the **default application** served at the root URL path (`/`). Tomcat automatically unpacks WAR files on startup.

**Nginx (web01):** Runs on Ubuntu (not CentOS), so uses `apt` instead of `dnf`. Requires creating a custom site configuration in `/etc/nginx/sites-available/`, removing the default site, and creating a **symbolic link** from `sites-available` to `sites-enabled` to activate the configuration. No firewall configuration is shown (Ubuntu's `ufw` is typically inactive by default).

> 🔍 **Deep Dive — Nginx Sites-Available/Sites-Enabled Pattern**
> This is Debian/Ubuntu's standard Nginx configuration management pattern. All site configurations live in `sites-available/`. To activate a site, you create a symlink from `sites-available/` to `sites-enabled/`. To deactivate, you remove the symlink. This allows you to have multiple site configs prepared but only selectively activated. The instructor removes the `default` symlink and creates one for `vproapp`, making the vProfile reverse proxy the only active site.

## 1.11 The `application.properties` Configuration Bridge

A critical but briefly mentioned step is updating `application.properties` inside the cloned source code on the Tomcat VM. This Java configuration file contains the **backend server connection details** — hostnames, ports, and credentials for MySQL, Memcache, and RabbitMQ. This is the **configuration bridge** that tells the application where its backend services live.

This is where the hostmanager plugin's `/etc/hosts` entries become operationally essential — the application.properties file references backends by hostname (e.g., `db01`, `mc01`, `rmq01`), and those hostnames must resolve to the correct IP addresses.

## 1.12 Firewall Configuration Pattern

Every CentOS service setup includes a **firewall configuration block** that follows the same logic: start `firewalld` → enable `firewalld` → add the service's port → make the rule permanent → reload. The specific mechanism varies slightly:

* **MySQL & Tomcat:** `firewall-cmd --zone=public --add-port=PORT/tcp --permanent` followed by `firewall-cmd --reload`
* **Memcache & RabbitMQ:** `firewall-cmd --add-port=PORT/tcp` followed by `firewall-cmd --runtime-to-permanent`

Both approaches achieve the same result (a persistent firewall rule), but use different `firewalld` commands. The `--permanent` flag writes directly to the permanent config (requires `--reload` to take effect). The `--runtime-to-permanent` approach applies the rule immediately to the runtime config, then copies it to the permanent config.

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are deploying a **complete multi-tier Java web application** (vProfile) across five local virtual machines. The final outcome: a user opens a browser, navigates to the Nginx VM's IP address, and sees a fully functional web application backed by Tomcat, RabbitMQ, Memcache, and MySQL — all running on separate VMs communicating by hostname.

## Phase 1: Environment Preparation

### Step 1.1: Clone the Source Code

**What we are doing:** Getting the project source code onto your local machine.

Open VS Code → click **Source Control** (left sidebar) → **Clone Repository** → paste the URL:

```
https://github.com/hkhcoders/vprofile-project.git
```

Select a destination folder (e.g., `F:\hkhcoder\`). When prompted, open in the same window.

### Step 1.2: Switch to the `local` Branch

**What we are doing:** Selecting the correct branch that contains the code for this section.

In VS Code, click the **branch name** at the bottom-left (shows "main") → select **`origin/local`**. Verify that the indicator now shows `local`.

**Common mistake:** Forgetting this step and working on the `main` branch. All file paths, Vagrantfiles, and scripts differ between branches.

### Step 1.3: Install the Hostmanager Plugin

**What we are doing:** Adding the hostname-to-IP auto-resolution capability to Vagrant (as covered in Theory §1.5).

```bash
vagrant plugin install vagrant-hostmanager
```

* **`vagrant plugin install`** — installs a Vagrant plugin globally on your system
* **`vagrant-hostmanager`** — the specific plugin that auto-populates `/etc/hosts` across all VMs

**Run this once.** It persists across all Vagrant projects.

### Step 1.4: Clean Up Existing VMs

**What we are doing:** Ensuring no stale VMs consume resources or cause IP conflicts.

```bash
vagrant global-status
```

* **`vagrant global-status`** — lists all Vagrant VMs across your entire system

If VMs are listed, navigate to each VM's directory and run `vagrant destroy`. Then:

```bash
vagrant global-status --prune
```

* **`--prune`** — removes stale entries from Vagrant's index that no longer correspond to actual VMs

### Step 1.5: Navigate to the Correct Folder

```bash
cd F:/hkhcoder/vprofile-project/vagrant/Manual_provisioning_WinMacIntel
```

Adjust path based on your OS:

* **Windows / macOS Intel / Linux:** `Manual_provisioning_WinMacIntel`
* **macOS M1/M2/M3:** The M-series specific folder

Verify:

```bash
ls
```

**Expected output:** You should see the `Vagrantfile` and the PDF document.

### Step 1.6: Bring Up All VMs

```bash
vagrant up
```

This creates and boots **all five VMs** defined in the multi-VM Vagrantfile. This will take significant time (downloading box images, creating VMs, configuring networks, populating `/etc/hosts` via hostmanager).

**Password prompt:** Some systems may ask for your **computer password** (not a VM password). This is needed for the hostmanager plugin to modify the host machine's `/etc/hosts` file.

**If it stops in the middle:** Re-run `vagrant up` — it will resume where it left off.

**If a VM shows a timeout error:** Run `vagrant reload <vmname>` to reboot that specific VM, then `vagrant up` again.

### Step 1.7: Verify Host Entries and Connectivity

Log into any VM (e.g., web01):

```bash
vagrant ssh web01
sudo -i
cat /etc/hosts
```

**Expected output:** Entries mapping all VM hostnames to their IP addresses (e.g., `app01 192.168.56.x`, `db01 192.168.56.y`, etc.).

Test connectivity:

```bash
ping app01 -c 4
```

* **`ping`** — sends ICMP echo requests
* **`app01`** — resolved via `/etc/hosts`
* **`-c 4`** — send exactly 4 packets

**Expected output:** Four reply lines with round-trip times. If timeouts occur, reboot the target VM (`vagrant reload app01` from the host).

**Exercise:** Log into `app01` and ping `mc01`, `rmq01`, `db01` to verify full mesh connectivity.

## Phase 2: Service Provisioning (Manual)

Setup follows the dependency order: **MySQL → Memcache → RabbitMQ → Tomcat → Nginx**

### Step 2.1: MySQL Setup (db01)

```bash
vagrant ssh db01
sudo -i
```

**Verify hosts, update OS, install repositories:**

```bash
cat /etc/hosts
dnf update -y
dnf install epel-release -y
```

* **`dnf update -y`** — updates all packages to latest versions; `-y` auto-confirms
* **`epel-release`** — Extra Packages for Enterprise Linux; enables additional package repository

**Install and start MariaDB:**

```bash
dnf install git mariadb-server -y
systemctl start mariadb
systemctl enable mariadb
```

* **`mariadb-server`** — the MySQL-compatible database server
* **`git`** — needed later to clone the source code for schema import
* **`enable`** — ensures MariaDB starts on every future boot

**Run the secure installation script:**

```bash
mysql_secure_installation
```

This is an **interactive** script. Respond as follows:

| Prompt                        | Answer                    | Reasoning                                 |
| ----------------------------- | ------------------------- | ----------------------------------------- |
| Set root password?            | **Y** — set to `admin123` | Secures database access                   |
| Remove anonymous users?       | **Y**                     | Removes insecure default users            |
| Disallow root login remotely? | **n**                     | We need remote root access from other VMs |
| Remove test database?         | **Y**                     | Removes unnecessary test data             |
| Reload privilege tables?      | **Y**                     | Applies all changes immediately           |

**Create database and user:**

```bash
mysql -u root -padmin123
```

* **`-u root`** — connect as root user
* **`-padmin123`** — password immediately after `-p` (no space)

Inside the MySQL shell:

```sql
create database accounts;
grant all privileges on accounts.* TO 'admin'@'localhost' identified by 'admin123';
grant all privileges on accounts.* TO 'admin'@'%' identified by 'admin123';
FLUSH PRIVILEGES;
exit;
```

* **`accounts`** — the database the application uses
* **`'admin'@'localhost'`** — grants access from the local machine
* **`'admin'@'%'`** — grants access from **any host** (needed for Tomcat to connect remotely)
* **`FLUSH PRIVILEGES`** — reloads the grant tables to apply changes immediately

**Import the database schema:**

```bash
cd /tmp/
git clone -b local https://github.com/hkhcoder/vprofile-project.git
cd vprofile-project
mysql -u root -padmin123 accounts < src/main/resources/db_backup.sql
```

* **`accounts < db_backup.sql`** — imports the SQL file into the `accounts` database

**Verify the import:**

```bash
mysql -u root -padmin123 accounts
show tables;
exit;
```

**Expected:** A list of tables populated from the backup file.

**Restart and configure firewall:**

```bash
systemctl restart mariadb
systemctl start firewalld
systemctl enable firewalld
firewall-cmd --get-active-zones
firewall-cmd --zone=public --add-port=3306/tcp --permanent
firewall-cmd --reload
systemctl restart mariadb
```

* **`--add-port=3306/tcp --permanent`** — opens MySQL's default port persistently
* **`--reload`** — applies the permanent rule to the running firewall

**Connection to flow:** MySQL is now ready. Memcache (next step) and Tomcat (later) can connect to it.

### Step 2.2: Memcache Setup (mc01)

```bash
vagrant ssh mc01
sudo -i
cat /etc/hosts
dnf update -y
sudo dnf install epel-release -y
sudo dnf install memcached -y
sudo systemctl start memcached
sudo systemctl enable memcached
sudo systemctl status memcached
```

**Critical configuration change — bind to all interfaces:**

```bash
sed -i 's/127.0.0.1/0.0.0.0/g' /etc/sysconfig/memcached
sudo systemctl restart memcached
```

* **`sed -i 's/127.0.0.1/0.0.0.0/g'`** — in-place replacement of localhost-only binding with all-interfaces binding
* Without this, Memcache only accepts connections from itself — other VMs cannot reach it

**Firewall configuration:**

```bash
systemctl start firewalld
systemctl enable firewalld
firewall-cmd --add-port=11211/tcp
firewall-cmd --runtime-to-permanent
firewall-cmd --add-port=11111/udp
firewall-cmd --runtime-to-permanent
sudo memcached -p 11211 -U 11111 -u memcached -d
```

* **Port 11211 (TCP)** — Memcache's default TCP port
* **Port 11111 (UDP)** — Memcache's UDP port
* **`-d`** — runs as daemon (background process)
* **`-u memcached`** — runs as the memcached user

### Step 2.3: RabbitMQ Setup (rmq01)

```bash
vagrant ssh rmq01
sudo -i
cat /etc/hosts
dnf update -y
dnf install epel-release -y
```

**Install RabbitMQ and dependencies:**

```bash
sudo dnf install wget -y
dnf -y install centos-release-rabbitmq-38
dnf --enablerepo=centos-rabbitmq-38 -y install rabbitmq-server
systemctl enable --now rabbitmq-server
```

* **`centos-release-rabbitmq-38`** — adds the CentOS RabbitMQ 3.8 repository
* **`--enablerepo=centos-rabbitmq-38`** — explicitly enables that repo for this install
* **`enable --now`** — enables AND starts the service in one command

**Configure access and create user:**

```bash
sudo sh -c 'echo "[{rabbit, [{loopback_users, []}]}]." > /etc/rabbitmq/rabbitmq.config'
sudo rabbitmqctl add_user test test
sudo rabbitmqctl set_user_tags test administrator
rabbitmqctl set_permissions -p / test ".*" ".*" ".*"
sudo systemctl restart rabbitmq-server
```

* **`loopback_users, []`** — removes the restriction that users can only connect from localhost
* **`add_user test test`** — creates user `test` with password `test`
* **`set_user_tags test administrator`** — grants admin privileges
* **`set_permissions ... ".*" ".*" ".*"`** — grants full permissions (configure, write, read) on all resources in the `/` vhost

**Firewall:**

```bash
sudo systemctl start firewalld
sudo systemctl enable firewalld
firewall-cmd --add-port=5672/tcp
firewall-cmd --runtime-to-permanent
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl status rabbitmq-server
```

* **Port 5672** — RabbitMQ's AMQP protocol port

### Step 2.4: Tomcat Setup (app01)

This is the longest and most complex setup — it combines service installation, code build, and deployment.

```bash
vagrant ssh app01
sudo -i
cat /etc/hosts
dnf update -y
dnf install epel-release -y
```

**Install Java and tools:**

```bash
dnf -y install java-17-openjdk java-17-openjdk-devel
dnf install git wget -y
```

* **`java-17-openjdk`** — Java runtime
* **`java-17-openjdk-devel`** — Java development kit (needed for compilation)

**Download and extract Tomcat:**

```bash
cd /tmp/
wget https://archive.apache.org/dist/tomcat/tomcat-10/v10.1.26/bin/apache-tomcat-10.1.26.tar.gz
tar xzvf apache-tomcat-10.1.26.tar.gz
```

* **`wget`** — downloads the Tomcat archive directly
* **`tar xzvf`** — extracts (`x`), gunzips (`z`), verbose (`v`), from file (`f`)

**Create Tomcat user and install:**

```bash
useradd --home-dir /usr/local/tomcat --shell /sbin/nologin tomcat
cp -r /tmp/apache-tomcat-10.1.26/* /usr/local/tomcat/
chown -R tomcat.tomcat /usr/local/tomcat
```

* **`--shell /sbin/nologin`** — security practice: the tomcat user cannot log in interactively
* **`chown -R tomcat.tomcat`** — gives the tomcat user ownership of all Tomcat files

**Create the systemd service file:**

```bash
vi /etc/systemd/system/tomcat.service
```

Insert the full service unit content (as specified in Theory §1.10 Deep Dive).

**Activate and start:**

```bash
systemctl daemon-reload
systemctl start tomcat
systemctl enable tomcat
```

* **`daemon-reload`** — tells systemd to re-read all service files (required after creating a new one)

**Firewall:**

```bash
systemctl start firewalld
systemctl enable firewalld
firewall-cmd --get-active-zones
firewall-cmd --zone=public --add-port=8080/tcp --permanent
firewall-cmd --reload
```

**Code Build and Deploy (still on app01):**

```bash
cd /tmp/
wget https://archive.apache.org/dist/maven/maven-3/3.9.9/binaries/apache-maven-3.9.9-bin.zip
unzip apache-maven-3.9.9-bin.zip
cp -r apache-maven-3.9.9 /usr/local/maven3.9
export MAVEN_OPTS="-Xmx512m"
```

* **`MAVEN_OPTS="-Xmx512m"`** — allocates 512 MB max heap to Maven (prevents out-of-memory during build)

```bash
git clone -b local https://github.com/hkhcoder/vprofile-project.git
cd vprofile-project
vim src/main/resources/application.properties
```

**Update `application.properties`** with correct backend hostnames, ports, and credentials (db01, mc01, rmq01).

**Build:**

```bash
/usr/local/maven3.9/bin/mvn install
```

**Deploy:**

```bash
systemctl stop tomcat
rm -rf /usr/local/tomcat/webapps/ROOT*
cp target/vprofile-v2.war /usr/local/tomcat/webapps/ROOT.war
systemctl start tomcat
chown tomcat.tomcat /usr/local/tomcat/webapps -R
systemctl restart tomcat
```

* **Remove `ROOT*`** — clears the default Tomcat landing page
* **Copy as `ROOT.war`** — makes vProfile the root application
* **`chown` after copy** — ensures Tomcat user owns the newly deployed files

### Step 2.5: Nginx Setup (web01)

```bash
vagrant ssh web01
sudo -i
cat /etc/hosts
apt update
apt upgrade
apt install nginx -y
```

Note: Ubuntu uses `apt`, not `dnf`.

**Create reverse proxy configuration:**

```bash
vi /etc/nginx/sites-available/vproapp
```

Content:

```nginx
upstream vproapp {
  server app01:8080;
}
server {
  listen 80;
  location / {
    proxy_pass http://vproapp;
  }
}
```

**Activate the configuration:**

```bash
rm -rf /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/vproapp /etc/nginx/sites-enabled/vproapp
systemctl restart nginx
```

* **Remove `default`** — disables the default Nginx welcome page
* **`ln -s`** — creates symbolic link to activate the vproapp site

**Final verification:** Open a browser on your host machine → navigate to `http://<web01-IP>` → the vProfile application should load, served through the entire Nginx → Tomcat → Backend stack.

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Core Identity

```
VPROFILE PROJECT = Multi-tier Java web app deployed across 5 VMs via manual provisioning
PURPOSE          = Learn real-world multi-service infrastructure setup from scratch
```

## Architecture: Service Dependency Chain

```
User → Browser
         │
         ▼
   Nginx (web01:80)        [Ubuntu, reverse proxy]
         │ proxy_pass
         ▼
   Tomcat (app01:8080)     [CentOS, Java app server, WAR deployment]
         │ connects to ↓
         ├──→ Memcache (mc01:11211)   [CentOS, DB cache]
         ├──→ RabbitMQ (rmq01:5672)   [CentOS, message broker]
         └──→ MySQL/MariaDB (db01:3306) [CentOS, SQL database]
                    ▲
                    │
              Memcache also connects here
```

## VM Configuration Matrix

```
VM       Hostname  OS        RAM     Port   Service
─────────────────────────────────────────────────────
db01     db01      CentOS9   600MB   3306   MariaDB
mc01     mc01      CentOS9   600MB   11211  Memcached
rmq01    rmq01     CentOS9   600MB   5672   RabbitMQ
app01    app01     CentOS9   800MB   8080   Tomcat 10
web01    web01     Ubuntu    800MB   80     Nginx
```

## Setup & Shutdown Order

```
STARTUP:  MySQL → Memcache → RabbitMQ → Tomcat → Nginx
          (bottom of stack → top of stack)
          (dependencies first → dependents last)

SHUTDOWN: Nginx → Tomcat → RabbitMQ → Memcache → MySQL
          (reverse: cut user access first → database last)
```

## Hostmanager Plugin Flow

```
vagrant plugin install vagrant-hostmanager  (once, on host)
         │
Vagrantfile:
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
         │
vagrant up
  │
  └──→ Auto-populates /etc/hosts on ALL VMs + host machine
         │
         └──→ Hostnames (app01, db01, mc01...) resolve to IPs
                │
                └──→ Nginx config, application.properties, ping — all work by name
```

## Common Setup Pattern (Per Service)

```
vagrant ssh <hostname>
  └─ sudo -i
     └─ cat /etc/hosts               ← verify hostmanager entries
        └─ dnf update -y             ← (apt update on Ubuntu)
           └─ install epel-release   ← (Ubuntu: skip)
              └─ install packages
                 └─ configure service
                    └─ start + enable
                       └─ firewall: open port + permanent rule
```

## Service-Specific Key Details

```
MySQL:
  mysql_secure_installation → root password admin123
  Disallow remote root? → NO (VMs need remote access)
  create database accounts; grant to 'admin'@'%'
  Import: mysql ... accounts < db_backup.sql
  Firewall: 3306/tcp

Memcache:
  CRITICAL: sed -i 's/127.0.0.1/0.0.0.0/g' /etc/sysconfig/memcached
  (bind all interfaces, not just localhost)
  Firewall: 11211/tcp + 11111/udp

RabbitMQ:
  Config: loopback_users → [] (allow remote connections)
  User: test/test → administrator tag → full permissions
  Firewall: 5672/tcp

Tomcat:
  Manual install (wget tar, not dnf)
  System user: tomcat (nologin shell)
  Custom systemd service file: /etc/systemd/system/tomcat.service
  daemon-reload after creating service file
  Maven build → mvn install → vprofile-v2.war
  Deploy: stop → rm ROOT* → cp as ROOT.war → start → chown → restart
  Firewall: 8080/tcp

Nginx:
  Ubuntu (apt, not dnf)
  sites-available/vproapp → upstream app01:8080 + proxy_pass
  rm default → ln -s to sites-enabled → restart nginx
```

## Configuration Bridge

```
application.properties (on app01)
  ├─ db.host = db01          → resolves via /etc/hosts → MySQL
  ├─ cache.host = mc01       → resolves via /etc/hosts → Memcache
  └─ mq.host = rmq01         → resolves via /etc/hosts → RabbitMQ

Nginx config (on web01)
  └─ upstream: app01:8080    → resolves via /etc/hosts → Tomcat
```

## Operational Commands Quick Reference

```
vagrant global-status          → list all VMs system-wide
vagrant global-status --prune  → clean stale entries
vagrant up                     → create/start all VMs
vagrant reload <vm>            → reboot specific VM
vagrant ssh <hostname>         → SSH into VM
ping <hostname> -c 4           → connectivity sanity test
cat /etc/hosts                 → verify hostname resolution
```

## Reusable Engineering Patterns

| Pattern                              | Manifestation                                                           |
| ------------------------------------ | ----------------------------------------------------------------------- |
| **Dependency-ordered setup**         | Start from database → work up to frontend                               |
| **Reverse-order shutdown**           | Frontend first → database last                                          |
| **Service discovery via hosts file** | Hostmanager plugin auto-populates `/etc/hosts`                          |
| **Bind address exposure**            | `127.0.0.1` → `0.0.0.0` for cross-VM access (Memcache)                  |
| **Loopback restriction removal**     | RabbitMQ `loopback_users: []` for remote access                         |
| **Custom systemd service**           | Manual Tomcat → systemctl managed via unit file                         |
| **WAR-as-ROOT deployment**           | Copy WAR as ROOT.war → becomes default app                              |
| **Reverse proxy frontend**           | Nginx proxies to Tomcat — separates web layer from app layer            |
| **Firewall per-service port**        | Each service explicitly opens only its required port                    |
| **Common setup skeleton**            | SSH → verify hosts → update OS → install → configure → start → firewall |

## Quick Recall Triggers

```
"vprofile"               → multi-tier Java stack on 5 VMs
"hostmanager"            → auto /etc/hosts population across VMs
"manual provisioning"    → log in to each VM, run commands by hand
"origin/local"           → the branch to switch to (critical!)
"admin123"               → DB root password & admin user password
"0.0.0.0"                → bind to all interfaces (Memcache fix)
"ROOT.war"               → deploy as default Tomcat app
"sites-enabled symlink"  → Nginx activation pattern (Ubuntu)
"daemon-reload"          → required after creating new systemd service file
"application.properties" → config bridge connecting Tomcat to all backends
```

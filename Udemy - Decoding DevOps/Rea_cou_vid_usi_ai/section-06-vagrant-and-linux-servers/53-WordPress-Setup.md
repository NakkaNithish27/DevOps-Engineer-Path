**Source:** [53-wordpress-setup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/53-wordpress-setup.txt?EntityRepresentationId=d89f26cf-4e1f-4aff-8f31-836623d2d878) — Video lecture on setting up an Ubuntu VM with the LAMP stack and deploying WordPress.

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 Context & System Overview — What Are We Building and Why

This lecture is part of a series. The previous lecture covered setting up a website on a **CentOS VM** using the `httpd` service and deploying an HTML template from tooplate.com. This lecture shifts the operating system to **Ubuntu** and significantly raises the complexity: instead of serving a static HTML template, we are deploying **WordPress** — a dynamic web application that requires a full **LAMP stack** (Linux, Apache, MySQL, PHP) and a live database connection.

The purpose is not just to "install WordPress." The deeper engineering objective is to understand the **full vertical stack** that makes a dynamic web application work: an OS layer (Ubuntu), a web server (Apache2), a database engine (MySQL), an application runtime (PHP), and finally the application itself (WordPress). Every component must be correctly installed, configured, and wired to its neighbors. If any single connection is broken — Apache doesn't know where the files are, WordPress doesn't know the database credentials, PHP libraries are missing — the application fails. This is the foundational pattern behind virtually every web application deployment.

## 1.2 The LAMP Stack — Architecture of a Dynamic Web Application

The LAMP stack is not a single piece of software. It is a **layered cooperation model** between four independent systems:

**Linux** is the operating system — the foundation that provides process management, file system, networking, and user permissions. In this lecture, it is Ubuntu 20 (codename "focal"). Every other component runs as a process or service on top of Linux.

**Apache2** is the web server. Its job is to listen on port 80 (HTTP) for incoming browser requests and respond with content. Apache does not generate dynamic content itself — it serves files from a designated directory called the **DocumentRoot**. When PHP is involved, Apache hands off `.php` files to the PHP interpreter and returns the result. Apache is the **front door** of the system.

**MySQL** is the relational database engine. WordPress stores all its blog posts, user accounts, settings, and metadata in a MySQL database. MySQL runs as a separate service, listening for connections. Applications connect to it using a username, password, and database name. It is the **persistent memory** of the system.

**PHP** is the application runtime. WordPress is written in PHP. When Apache receives a request for a WordPress page, it passes the request to PHP, which executes the WordPress code, queries MySQL for data, assembles an HTML page, and returns it to Apache, which sends it to the browser. PHP is the **processing engine** between the web server and the database.

The critical insight: these four layers are **independently installed, independently configured, and independently running services**. The deployment task is to install each one, then **wire them together** through configuration files so they cooperate as a single application system.

## 1.3 Vagrant — VM Lifecycle Management

Vagrant is the tool used to create, configure, and manage the Ubuntu virtual machine. The workflow follows a precise lifecycle:

`vagrant init <box-name>` creates a **Vagrantfile** — a configuration file that describes the VM's properties (OS image, RAM, network settings). The box name `ubuntu/focal64` refers to a pre-built Ubuntu 20.04 image hosted on Vagrant Cloud.

The Vagrantfile is then edited to set: a **static IP** on the host-only network (e.g., `192.168.56.26` — the `56` subnet is VirtualBox's default host-only range), optionally a **public/bridge network** (which gets an IP from the WiFi router, making the VM accessible from other devices on the LAN), and **RAM allocation** (1600 MB recommended; 1024 MB minimum). The IP must be unique across all running VMs to avoid conflicts.

`vagrant up` builds and boots the VM. `vagrant ssh` logs in. After work is complete, `vagrant destroy` tears it down. This lifecycle pattern — **create, configure, provision, use, destroy** — is the foundational pattern of disposable infrastructure.

## 1.4 Apache2 Virtual Host Configuration — How Apache Knows What to Serve

By default, Apache serves content from `/var/www/html`. But WordPress is installed to `/srv/www/wordpress`. Apache needs to be explicitly told about this new location. This is done through a **Virtual Host configuration file**.

A file named `wordpress.conf` is created inside Apache's configuration directory. The key directive inside this file is `DocumentRoot /srv/www/wordpress` — this tells Apache: "When a request comes in, serve files from this directory."

🔍 **Deep Dive — Apache's sites-available / sites-enabled Architecture:**

Apache on Ubuntu uses a two-directory pattern for managing websites:

* **`/etc/apache2/sites-available/`** — Contains all configuration files for all websites. A file here is just a definition; it does **not** mean the site is active.
* **`/etc/apache2/sites-enabled/`** — Contains **symbolic links** pointing to files in `sites-available`. Only sites with a link here are actually active.

The commands `a2ensite` (Apache2 Enable Site) and `a2dissite` (Apache2 Disable Site) manage these symlinks. When you run `a2ensite wordpress`, it creates a symlink in `sites-enabled` pointing to `sites-available/wordpress.conf`. When you run `a2dissite 000-default`, it removes the symlink for the default site. This is why after running these commands, `ls -l /etc/apache2/sites-enabled/` shows `wordpress.conf -> ../sites-available/wordpress.conf`.

The command `a2enmod rewrite` enables the Apache **rewrite module**, which allows URL rewriting/redirect rules — WordPress uses this for clean/pretty URLs.

After any configuration change, Apache must be **reloaded or restarted** (`systemctl reload apache2`) for the changes to take effect. This is because Apache reads its configuration at startup and caches it in memory.

⚠️ **Expert Note:** The `sites-available` / `sites-enabled` symlink pattern is Ubuntu/Debian-specific. On CentOS/RHEL (the previous lecture's OS), the equivalent is typically done through `.conf` files in `/etc/httpd/conf.d/`. This is why the same conceptual action (enabling a virtual host) looks different across distributions — the **mechanism** differs, but the **intent** is identical.

## 1.5 The www-data User — Apache's Service Identity

When Apache2 is installed on Ubuntu, it automatically creates a system user called `www-data`. Apache runs its worker processes under this user identity. This means all file read/write operations performed by Apache happen with `www-data`'s permissions.

This is why the WordPress directory `/srv/www/wordpress` must be **owned by `www-data`** — if Apache can't read the files, it can't serve them. And when editing WordPress configuration files, the documentation uses `sudo -u www-data vim <file>` — this opens the editor **as the www-data user**, ensuring that file permissions remain correct and the file is accessible to Apache after editing. <cite>turn1search1</cite>

This is a fundamental Linux security pattern: services run as dedicated low-privilege users, not as root. The service user owns only the files it needs, limiting damage if the service is compromised.

## 1.6 MySQL Database Setup — Creating the Application's Persistent Layer

WordPress cannot function without a database. The MySQL setup involves three distinct operations, each with a specific purpose: <cite>turn1search1</cite>

**Creating the database** (`CREATE DATABASE wordpress;`) — This creates an empty container (a namespace) inside MySQL where WordPress will store its tables. <cite>turn1search1</cite>

**Creating a user** (`CREATE USER wordpress@localhost IDENTIFIED BY '<password>';`) — This creates a MySQL account that WordPress will use to authenticate. The `@localhost` part means this user can only connect from the same machine — not remotely. This is a security restriction: the web application and database are on the same server. <cite>turn1search1</cite>

**Granting privileges** (`GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER ON wordpress.* TO wordpress@localhost;`) — This gives the WordPress user specific permissions on the wordpress database. The `.*` means "all tables in this database." The specific operations granted (SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER) are exactly what WordPress needs to read, write, modify, and manage its tables. <cite>turn1search1</cite>

**FLUSH PRIVILEGES** reloads MySQL's internal privilege cache so the changes take effect immediately. <cite>turn1search1</cite>

🔍 **Deep Dive:** Every SQL command ends with a **semicolon** (`;`). This is the SQL statement terminator. Forgetting it is a common mistake — MySQL will wait for more input instead of executing the command. The video explicitly warns about this. The video also warns about the multi-line arrow syntax (`>`) in the documentation — many people make mistakes trying to use multi-line SQL. The safer approach is to write each command as a **single line**. <cite>turn1search1</cite>

## 1.7 WordPress Configuration — Wiring the Application to the Database

After the database exists and has a user, WordPress must be told how to find and authenticate to it. This happens through a file called `wp-config.php`, located in the WordPress document root (`/srv/www/wordpress/`). <cite>turn1search1</cite>

WordPress ships with a **sample configuration file** (`wp-config-sample.php`). The first step is copying this sample to the actual location (`wp-config.php`). Then three placeholder values inside it are replaced with real values: <cite>turn1search1</cite>

* `database_name_here` → `wordpress` (the database name)
* `username_here` → `wordpress` (the MySQL user)
* `password_here` → `admin123` (the MySQL user's password)

This replacement is done using the `sed` command (stream editor) — a Linux tool for automated search-and-replace in files. <cite>turn1search1</cite>

Additionally, the file contains **SALT keys** — a block of placeholder text that must be replaced with unique cryptographic strings. WordPress provides a link (`api.wordpress.org/secret-key/...`) that generates random SALT values each time you visit it. You copy the generated block and replace the placeholder block in `wp-config.php`. These SALT keys are used to **secure cookies and authentication tokens**. <cite>turn1search1</cite>

⚠️ **Expert Note:** The `wp-config.php` file is the **single most critical configuration file** in a WordPress deployment. If the database name, username, or password is wrong, WordPress will show a "Error establishing a database connection" page. If the SALT keys are missing or malformed, authentication will fail. The video explicitly identifies `wordpress.conf` (Apache config) and `wp-config.php` (WordPress config) as the **two files to check first** when troubleshooting. <cite>turn1search1</cite>

## 1.8 The Multi-Line Command Syntax in Linux

The video explains a useful Linux shell feature: if a command is very long, you can split it across multiple lines using a **backslash (`\`) preceded by a space** at the end of each line. The shell interprets `\` followed by a newline as a continuation — "this command continues on the next line." The dependency installation command uses this to list many packages vertically for readability. <cite>turn1search1</cite>

## 1.9 Troubleshooting Mental Model

The video provides an explicit troubleshooting framework for when the WordPress site doesn't load correctly: <cite>turn1search1</cite>

1. Run `history` to check what commands you may have missed.
2. Verify `wordpress.conf` — is DocumentRoot correct? Is the file properly linked in `sites-enabled`?
3. Verify `wp-config.php` — are database name, username, password, and SALT keys correct?
4. Log into MySQL and run `SHOW DATABASES;` — does the `wordpress` database exist?
5. Re-run the database steps if needed.
6. Restart Apache2 after any configuration change.
7. Retry from the browser.

The instructor's core message: "These steps will definitely work unless you make a typographical mistake." The overwhelmingly common failure mode is **human transcription error** in configuration values. <cite>turn1search1</cite>

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are building a **fully functional WordPress blog** running on an Ubuntu 20 virtual machine. The final outcome: you type the VM's IP address into a browser and see the WordPress setup wizard, then a working WordPress admin dashboard. Behind the scenes, Apache serves PHP-processed pages, WordPress queries a MySQL database, and everything runs inside a Vagrant-managed VM. <cite>turn1search1</cite>

## Step 1: Prepare the Documentation Reference

Before touching the terminal, open a browser and search **"WordPress on Ubuntu"**. Navigate to the **official Ubuntu documentation**. Read through the overview and all nine steps. The instructor specifically recommends reading the full documentation first before executing. <cite>turn1search1</cite>

This documentation will be your reference throughout. Key sections: installing dependencies, installing WordPress, Apache configuration, database setup, WordPress configuration, and browser access. <cite>turn1search1</cite>

## Step 2: Create and Configure the Vagrant VM

Navigate to your Vagrant working directory and create a new project folder:

```bash
mkdir wordpress
cd wordpress
vagrant init ubuntu/focal64
```

* `mkdir wordpress` — Creates a dedicated directory for this project.
* `cd wordpress` — Enters the directory.
* `vagrant init ubuntu/focal64` — Generates a `Vagrantfile` configured to use the Ubuntu 20.04 (Focal Fossa) box from Vagrant Cloud. <cite>turn1search1</cite>

**Edit the Vagrantfile** (using `vim Vagrantfile` or a graphical editor):

1. **Set a static IP:** `config.vm.network "private_network", ip: "192.168.56.26"` — The `.56` subnet is VirtualBox's host-only range. Choose an IP not used by other VMs.
2. **Enable bridge/public network:** `config.vm.network "public_network"` — This gets an IP from your WiFi router, useful for browser access.
3. **Set RAM:** Inside the provider block, set `vb.memory = "1600"` — 1600 MB recommended; 1024 MB minimum. <cite>turn1search1</cite>

Save and quit, then boot the VM:

```bash
vagrant up
```

Once the VM is running:

```bash
vagrant ssh
```

Inside the VM, switch to root and set a hostname:

```bash
sudo -i
hostnamectl set-hostname wordpress
```

Log out and log back in, then switch to root again to see the new hostname in the prompt. This is optional but helps identify which VM you're working in. <cite>turn1search1</cite>

## Step 3: Install Dependencies (LAMP Stack)

First, update the package index:

```bash
apt update
```

Then install all required packages:

```bash
apt install apache2 ghostscript libapache2-mod-php mysql-server php php-bcmath php-curl php-imagick php-intl php-json php-mbstring php-mysql php-xml php-zip -y
```

* `apache2` — The web server.
* `mysql-server` — The database engine.
* `php` and all `php-*` packages — PHP runtime and the specific extensions WordPress requires.
* `ghostscript` — Used by WordPress for PDF rendering.
* `libapache2-mod-php` — The Apache module that enables PHP processing.
* `-y` — Auto-confirm installation (the instructor adds this manually). <cite>turn1search1</cite>

The backslash (`\`) syntax in the documentation is for visual readability — it splits the long command across lines. You can paste it as a single line or use the multi-line format. <cite>turn1search1</cite>

**Verification:** After installation completes, Apache should already be running. You can verify with `systemctl status apache2`.

## Step 4: Download and Install WordPress

```bash
mkdir -p /srv/www
chown www-data: /srv/www
curl https://wordpress.org/latest.tar.gz | sudo -u www-data tar zx -C /srv/www
```

* `mkdir -p /srv/www` — Creates the parent directory. `-p` prevents errors if it already exists.
* `chown www-data: /srv/www` — Changes ownership to the `www-data` user (Apache's service user). The trailing colon sets both user and group.
* `curl ... | sudo -u www-data tar zx -C /srv/www` — Downloads the latest WordPress archive and pipes it directly to `tar`, which extracts it (`zx`) into `/srv/www` as the `www-data` user. This results in `/srv/www/wordpress/`. <cite>turn1search1</cite>

**Verification:**

```bash
ls -ld /srv/www
```

Should show `www-data` as owner.

```bash
ls -l /srv/www/wordpress/
```

Should show WordPress core files (wp-admin, wp-content, wp-includes, etc.). <cite>turn1search1</cite>

**Connection to system flow:** `/srv/www/wordpress` will become the DocumentRoot — the directory Apache serves to browsers. But Apache doesn't know this yet; that happens in the next step.

## Step 5: Configure Apache Virtual Host

Create the Apache configuration file:

```bash
vim /etc/apache2/sites-available/wordpress.conf
```

Enter insert mode (`i`), then paste the following content:

```apache
<VirtualHost *:80>
    DocumentRoot /srv/www/wordpress
    <Directory /srv/www/wordpress>
        Options FollowSymLinks
        AllowOverride Limit Options FileInfo
        DirectoryIndex index.php
        Require all granted
    </Directory>
    <Directory /srv/www/wordpress/wp-content>
        Options FollowSymLinks
        Require all granted
    </Directory>
</VirtualHost>
```

Save and quit (`:wq`). <cite>turn1search1</cite>

⚠️ **Critical:** Make sure you are in **insert mode** (`i`) before pasting. Pasting in normal mode will execute random vim commands and corrupt the file. Use `Shift+Insert` to paste in terminal. <cite>turn1search1</cite>

Now enable the site and disable the default:

```bash
a2ensite wordpress
a2enmod rewrite
a2dissite 000-default
```

* `a2ensite wordpress` — Creates a symlink in `sites-enabled` pointing to `sites-available/wordpress.conf`. This **activates** the WordPress site.
* `a2enmod rewrite` — Enables the Apache rewrite module for URL rewriting.
* `a2dissite 000-default` — Removes the symlink for the default Apache site, **deactivating** it. <cite>turn1search1</cite>

Reload Apache:

```bash
systemctl reload apache2
```

**Verification:**

```bash
ls -l /etc/apache2/sites-enabled/
```

You should see `wordpress.conf` as a symlink pointing to `../sites-available/wordpress.conf`. The default site should **not** appear here. <cite>turn1search1</cite>

## Step 6: Configure MySQL Database

Log into MySQL as root:

```bash
sudo mysql -u root
```

You are now at the MySQL command prompt (`mysql>`). Run each command **one at a time**: <cite>turn1search1</cite>

```sql
CREATE DATABASE wordpress;
```

Creates the database.

```sql
CREATE USER wordpress@localhost IDENTIFIED BY 'admin123';
```

Creates the MySQL user. Replace `admin123` with your chosen password.

```sql
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER ON wordpress.* TO wordpress@localhost;
```

Grants the necessary permissions. **Important:** The instructor explicitly warns to write this as a **single line** rather than using the multi-line arrow format from the documentation, as many people make mistakes with multi-line SQL. <cite>turn1search1</cite>

```sql
FLUSH PRIVILEGES;
```

Reloads the privilege tables.

```sql
quit
```

Exits the MySQL prompt. <cite>turn1search1</cite>

**Verification (inside MySQL before quitting):**

```sql
SHOW DATABASES;
```

Should list `wordpress` among the databases. <cite>turn1search1</cite>

⚠️ **Expert Note:** Every SQL statement **must** end with a semicolon (`;`). Forgetting it is the most common mistake — MySQL will just display `->` waiting for more input. If this happens, type `;` and press Enter to complete the statement. <cite>turn1search1</cite>

## Step 7: Configure WordPress to Connect to the Database

Copy the sample configuration:

```bash
cp /srv/www/wordpress/wp-config-sample.php /srv/www/wordpress/wp-config.php
```

Run the `sed` commands to replace placeholder values:

```bash
sed -i 's/database_name_here/wordpress/' /srv/www/wordpress/wp-config.php
sed -i 's/username_here/wordpress/' /srv/www/wordpress/wp-config.php
sed -i 's/password_here/admin123/' /srv/www/wordpress/wp-config.php
```

* `sed -i` — Edit the file **in-place** (modify the actual file, not just print to screen).
* `s/old/new/` — Substitute (search and replace) pattern.
* Ensure the password matches **exactly** what you set in the MySQL step. <cite>turn1search1</cite>

**Verification:**

```bash
cat /srv/www/wordpress/wp-config.php
```

Check that `DB_NAME` is `wordpress`, `DB_USER` is `wordpress`, `DB_PASSWORD` is `admin123` (or your chosen password). If any value is wrong, edit the file manually with `vim`. <cite>turn1search1</cite>

## Step 8: Replace the SALT Keys

Open the WordPress secret key generator by visiting the URL provided in the documentation (it's a link to `api.wordpress.org/secret-key/1.1/salt/`). This page generates a fresh block of random cryptographic keys every time you load it. <cite>turn1search1</cite>

Open the config file as the www-data user:

```bash
sudo -u www-data vim /srv/www/wordpress/wp-config.php
```

* `sudo -u www-data` — Run the command as the `www-data` user to preserve correct file ownership.

Find the block of placeholder SALT key lines (they say `put your unique phrase here`). Delete all of them using `dd` in vim (press `dd` on each line). Then enter insert mode (`i`), paste the copied keys from the browser (`Shift+Insert`), press `Escape`, and save (`:wq`). <cite>turn1search1</cite>

⚠️ **Critical:** Delete **only** the SALT placeholder lines. Do not accidentally delete surrounding configuration. Verify after saving. <cite>turn1search1</cite>

## Step 9: Access WordPress from the Browser

Find the VM's IP address:

```bash
ip addr show
```

You will see two relevant IPs — the host-only IP (e.g., `192.168.56.26`) and the bridge IP (e.g., `192.168.1.10`). Either works; the instructor uses the bridge IP. <cite>turn1search1</cite>

Enter the IP in your browser. You should see the **WordPress installation wizard**. <cite>turn1search1</cite>

Complete the setup:

* Choose a language
* Set a site title (e.g., "devops")
* Set a username and password
* Provide an email address (can be any for practice)
* Click "Install WordPress" <cite>turn1search1</cite>

Log in with your credentials. You should see the **WordPress admin dashboard** with the message "Welcome to WordPress." <cite>turn1search1</cite>

## Step 10: Troubleshooting (If Something Goes Wrong)

If you see "Error establishing a database connection," a default Apache page, or a blank/broken page: <cite>turn1search1</cite>

1. **`history`** — Review your command history. Identify any missed steps.
2. **Check `wordpress.conf`** — `cat /etc/apache2/sites-available/wordpress.conf`. Is DocumentRoot correct?
3. **Check `wp-config.php`** — `cat /srv/www/wordpress/wp-config.php`. Are DB\_NAME, DB\_USER, DB\_PASSWORD, and SALT keys correct?
4. **Check the database** — `sudo mysql -u root` → `SHOW DATABASES;` → Confirm `wordpress` exists.
5. **Re-run database commands** if needed.
6. **Restart Apache** — `systemctl restart apache2`.
7. **Retry from browser.** <cite>turn1search1</cite>

The instructor's guarantee: "These steps will definitely work unless you make a typographical mistake." <cite>turn1search1</cite>

## Step 11: Cleanup

When finished:

```bash
exit          # exit root
exit          # exit vagrant ssh
vagrant destroy
```

This destroys the VM completely — disposable infrastructure pattern. <cite>turn1search1</cite>

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## System Architecture (Single-Machine LAMP)

```
Browser Request (HTTP:80)
    │
    ▼
┌──────────────────────────────────────┐
│           UBUNTU 20 VM               │
│         (Vagrant / focal64)          │
│                                      │
│  ┌────────────┐                      │
│  │  Apache2    │◄── wordpress.conf   │
│  │  (Port 80)  │    DocumentRoot:    │
│  │             │    /srv/www/wordpress│
│  └──────┬─────┘                      │
│         │ passes .php to             │
│         ▼                            │
│  ┌────────────┐                      │
│  │    PHP      │                     │
│  │ (mod_php)   │                     │
│  └──────┬─────┘                      │
│         │ reads wp-config.php        │
│         │ connects using credentials │
│         ▼                            │
│  ┌────────────┐                      │
│  │   MySQL     │                     │
│  │  DB: wordpress                    │
│  │  User: wordpress@localhost        │
│  └────────────┘                      │
└──────────────────────────────────────┘
```

## Critical File Map

```
/etc/apache2/sites-available/wordpress.conf   ← Apache virtual host definition
/etc/apache2/sites-enabled/wordpress.conf     ← Symlink (active site)
/srv/www/wordpress/                           ← DocumentRoot (WordPress files)
/srv/www/wordpress/wp-config.php              ← DB credentials + SALT keys
```

## Deployment Flow (9-Step Chain)

```
1. apt update + install deps (apache2, mysql-server, php-*)
       │
2. mkdir /srv/www → chown www-data → curl+tar WordPress
       │
3. Create wordpress.conf → set DocumentRoot /srv/www/wordpress
       │
4. a2ensite wordpress → a2enmod rewrite → a2dissite 000-default → reload
       │
5. mysql: CREATE DATABASE → CREATE USER → GRANT → FLUSH → quit
       │
6. cp wp-config-sample.php → wp-config.php → sed replace DB/user/pass
       │
7. Replace SALT keys from api.wordpress.org/secret-key
       │
8. Browser → VM IP → WordPress setup wizard → admin dashboard
       │
9. vagrant destroy (cleanup)
```

## Apache Site Activation Pattern

```
sites-available/  ──[a2ensite]──►  sites-enabled/  (symlink created = site active)
sites-enabled/    ──[a2dissite]──► (symlink removed = site deactivated)
Config change     ──[systemctl reload apache2]──► takes effect
```

## WordPress ↔ Database Wiring

```
wp-config.php
    ├── DB_NAME     →  must match  →  CREATE DATABASE <name>
    ├── DB_USER     →  must match  →  CREATE USER <name>@localhost
    └── DB_PASSWORD →  must match  →  IDENTIFIED BY '<password>'

Mismatch in ANY of these → "Error establishing a database connection"
```

## Ownership & Permission Chain

```
www-data (auto-created by apache2 install)
    ├── Owns /srv/www/  (chown www-data:)
    ├── Owns /srv/www/wordpress/  (extracted as www-data)
    ├── Apache workers run as www-data → can read files
    └── wp-config.php edited with: sudo -u www-data vim → preserves ownership
```

## Troubleshooting Decision Tree

```
Site not loading?
    ├── Default Apache page? → a2dissite 000-default not run / reload missed
    ├── "Error establishing DB connection" → wp-config.php credentials wrong
    │       ├── Check DB_NAME, DB_USER, DB_PASSWORD
    │       └── Log into MySQL → SHOW DATABASES → verify existence
    ├── Weird/broken page → SALT keys missing or malformed
    ├── Blank page → PHP module not loaded or php packages missing
    └── All else → run `history`, re-verify both config files, restart apache2
```

## Reusable Engineering Patterns

| Pattern                       | Instance in This Lecture                                                        |
| ----------------------------- | ------------------------------------------------------------------------------- |
| **Layered cooperation**       | Linux → Apache → PHP → MySQL (each independent, wired by config)                |
| **Symlink activation**        | sites-available / sites-enabled (definition vs. activation)                     |
| **Service identity**          | www-data user — service runs as dedicated low-privilege user                    |
| **Config-driven wiring**      | wp-config.php connects app to DB; wordpress.conf connects Apache to app         |
| **Disposable infrastructure** | vagrant up → use → vagrant destroy                                              |
| **Credential chain**          | DB password set once in MySQL, referenced in wp-config.php — must match exactly |
| **Copy-then-customize**       | wp-config-sample.php → cp → sed replace → production config                     |
| **Reload-after-change**       | Apache caches config at startup; changes require explicit reload                |

## One-Line Recall Triggers

* **"What wires WordPress to MySQL?"** → `wp-config.php` (DB\_NAME, DB\_USER, DB\_PASSWORD)
* **"What wires Apache to WordPress?"** → `wordpress.conf` (DocumentRoot /srv/www/wordpress)
* **"Why www-data?"** → Apache's runtime identity; files must be owned by it
* **"a2ensite does what?"** → Creates symlink in sites-enabled → activates site
* **"FLUSH PRIVILEGES?"** → Reloads MySQL's in-memory privilege cache
* **"SALT keys?"** → Cryptographic strings in wp-config.php for cookie/auth security

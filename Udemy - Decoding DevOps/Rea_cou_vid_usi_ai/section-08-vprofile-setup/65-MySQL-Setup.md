**Source:** [65-mysql-setup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/65-mysql-setup.txt?EntityRepresentationId=6a2f193f-1d4f-46ff-a7ab-e68b8e288468) — Video caption transcript covering the complete database layer setup for the VProfile multi-tier application stack.

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Role of a Database in the VProfile Architecture

The VProfile project is a multi-tier application. In this architecture, each service lives on a separate virtual machine — there is a Tomcat application server (app01), a Memcached server, a RabbitMQ server, and a **database server (db01)**. The database server's job is to persistently store all application data — user accounts, session information, and any structured data the application needs to read and write.

The application server (Tomcat on app01) does not store data itself. It connects **remotely** over the network to the database server. This is the fundamental reason the database must be configured to accept remote connections from specific users — a concept that becomes critical during the privilege-granting phase.

The database engine chosen for VProfile is **MariaDB**, which is a community-maintained fork of MySQL. On CentOS/RHEL-based systems, MariaDB is the standard MySQL-compatible database. The commands, SQL syntax, and client tools (`mysql` CLI) are effectively identical to MySQL. When the video says "MySQL," it means MariaDB in practice.

## 1.2 Operating System Preparation: DNF Update

Every time you bring up a new virtual machine — whether freshly provisioned via Vagrant, launched in the cloud, or installed bare-metal — the first operational discipline is to **update all installed packages** to their latest versions. This is done with `dnf update -y`.

This matters for two reasons. First, **security patches**: between the time the base OS image was built and the time you use it, vulnerabilities may have been discovered and fixed. Second, **dependency compatibility**: packages you install later (like MariaDB) may depend on newer versions of shared libraries. If the base system is stale, installations can fail or behave unpredictably.

`dnf` is the package manager for CentOS/RHEL 8+ (replacing the older `yum`). The `-y` flag auto-confirms all prompts so the command runs non-interactively.

## 1.3 EPEL Release Repository

EPEL stands for **Extra Packages for Enterprise Linux**. The default CentOS/RHEL repositories contain a curated, stability-focused subset of packages. Many tools that engineers routinely need (monitoring utilities, development libraries, additional server software) are not in the default repos. EPEL is a Fedora-maintained repository that provides these additional packages in a way that is compatible with Enterprise Linux.

Installing the `epel-release` package does not install software — it **registers a new package source** with `dnf`. After this, `dnf install <package>` can find and pull packages from EPEL in addition to the base repos. This is a prerequisite step because some packages needed later (or their dependencies) may only exist in EPEL.

## 1.4 Package Name vs. Service Name — A Critical Operational Distinction

When you install MariaDB, the **package name** is `mariadb-server`. But when you start, enable, or check the status of the running daemon, the **service name** is `mariadb` (lowercase, no `-server` suffix).

This is not unique to MariaDB — it is a **general pattern across Linux services**. The package name is what the package manager uses to locate and install the software. The service name is what `systemctl` uses to manage the running process. These names are determined independently: the package maintainer names the RPM/DEB package, while the service unit file (a systemd configuration) defines the service name.

There is no universal rule to predict the mapping. The reliable approaches are: check the official documentation, list the installed service unit files (`systemctl list-unit-files | grep maria`), or simply search online.

> 🔍 **Deep Dive:** After installing a package, you can discover its service name by running `rpm -ql mariadb-server | grep systemd` to find the `.service` unit file it ships. The filename of that unit file (minus the `.service` extension) is the service name.

## 1.5 Starting and Enabling a Service — Two Separate Actions

`systemctl start mariadb` — this **starts the service right now**, in the current boot session. If you reboot the VM without doing anything else, MariaDB will NOT be running after reboot.

`systemctl enable mariadb` — this **configures the service to start automatically on every future boot**. It does NOT start the service right now.

This is why both commands are always issued together. `start` gives you an immediately running service. `enable` gives you persistence across reboots. They are independent operations — forgetting `enable` is one of the most common operational mistakes, leading to services that mysteriously "disappear" after a reboot.

## 1.6 MySQL Secure Installation — Hardening a Fresh Database

A freshly installed MariaDB instance is **intentionally insecure by default**. It ships with: no root password, anonymous user accounts that allow anyone to connect without credentials, a test database accessible to anyone, and remote root login enabled. This is designed for ease of initial setup, not production use.

`mysql_secure_installation` is an interactive script that walks you through locking down all of these default weaknesses. It asks a series of yes/no questions:

**"Enter current password for root"** — This is the **MySQL root user**, not the Linux root user. These are completely separate authentication systems. MySQL has its own internal user table. A freshly installed MariaDB has no root password, so you press Enter (empty).

**"Switch to unix\_socket authentication"** — This controls whether the MySQL root user authenticates via the OS socket (meaning only the Linux root user can connect as MySQL root) or via a traditional password. The default (Y) is generally fine.

**"Change root password"** — Yes. This sets the MySQL root password. In the video, `admin123` is used for simplicity. In production, this must be long and complex.

**"Remove anonymous users"** — Yes. This prevents unauthenticated access.

**"Disallow root login remotely"** — Yes. The MySQL root user should only be accessible locally on the database server itself. Remote administrative access is a significant security risk.

**"Remove test database"** — Yes. The test database is world-accessible and serves no purpose in any real deployment.

**"Reload privilege tables"** — Yes. This applies all the changes immediately without requiring a service restart.

> ⚠️ **Expert Note:** In production environments, `mysql_secure_installation` is often replaced by configuration management (Ansible, Puppet, Chef) that programmatically sets the root password, drops anonymous users, and removes the test database — achieving the same hardening without interactive prompts.

## 1.7 MySQL User and Privilege System

MySQL/MariaDB has its own **internal user management system**, completely independent of the Linux OS user system. A MySQL user is identified by a **combination of username AND host**. This means `'admin'@'localhost'` and `'admin'@'%'` are **two different users** in MySQL's eyes, even though the username string is the same.

**`'admin'@'localhost'`** — This user can only connect when the connection originates from the database server itself (local connections).

**`'admin'@'%'`** — The `%` is a wildcard meaning "any host." This user can connect from any remote machine. In the VProfile architecture, the Tomcat application on app01 needs to reach the database on db01 — that is a remote connection. Without this user, the application would be unable to authenticate.

The `GRANT ALL PRIVILEGES ON accounts.*` statement does two things simultaneously when the user does not yet exist: it **creates the user** and **assigns permissions**. `accounts.*` means "all tables within the `accounts` database." The `IDENTIFIED BY 'admin123'` clause sets the password.

**`FLUSH PRIVILEGES`** tells the MySQL server to **reload the in-memory grant tables** from disk. While modern MySQL versions often auto-reload after GRANT statements, running FLUSH PRIVILEGES is a defensive operational habit that guarantees the changes are active. It is analogous to reloading a firewall rule set after making changes.

> 🔍 **Deep Dive:** MySQL stores user and privilege data in the `mysql` system database, specifically in tables like `mysql.user`, `mysql.db`, and `mysql.tables_priv`. GRANT statements modify these tables. FLUSH PRIVILEGES forces the server to re-read them into memory. If you directly modify these tables with INSERT/UPDATE (not recommended), FLUSH PRIVILEGES is mandatory.

## 1.8 Database Initialization and Schema Deployment

In the VProfile project, the database schema (table structures, initial data) is provided as an **SQL dump file** (`db_backup.sql`) within the application source code repository, at the path `src/main/resources/`.

This file contains raw SQL statements — CREATE TABLE, INSERT, and other DDL/DML commands — that, when executed against the `accounts` database, build the complete data structure the application expects. This process is called **database initialization**.

The video explains that in real-world environments, this initialization can happen in two ways:

1. **Manual deployment** — An operations engineer receives a DB dump file from the development team and manually executes it against the target database. This is what is done in the video.
2. **Automatic initialization** — The application itself (e.g., the Tomcat service) connects to the database on first startup and runs migration scripts automatically (common with frameworks like Hibernate, Flyway, or Liquibase).

The term **"DB dump"** refers to any file containing SQL statements that can recreate a database's structure and/or data. It is the standard mechanism for transporting database state between environments.

## 1.9 Input Redirection for SQL Execution

The command `mysql -u root -padmin123 accounts < src/main/resources/db_backup.sql` uses the shell's **input redirection operator (`<`)**. Instead of typing SQL commands interactively at the MySQL prompt, the shell feeds the contents of `db_backup.sql` directly into the `mysql` client's standard input. The MySQL client processes each statement in the file sequentially, exactly as if you had typed them one by one.

The `accounts` argument at the end of the `mysql` command specifies the **default database** — all SQL statements in the file will execute in the context of the `accounts` database, so the file does not need to include `USE accounts;`.

## 1.10 Password on the Command Line — Security Consideration

The video explicitly calls out that typing the password directly in the command (`mysql -u root -padmin123`) is **not recommended** for real usage. There is no space between `-p` and the password — this is the syntax MySQL expects for inline passwords.

The secure approach is to use `-p` alone (with no password following it). MySQL will then interactively prompt for the password, and the input will not be visible on screen or stored in shell history.

> ⚠️ **Expert Note:** Commands with inline passwords get recorded in `~/.bash_history` and are visible in `ps aux` output to other users on the system while the command is running. In production, use MySQL option files (`~/.my.cnf`), environment variables, or secrets management tools to avoid password exposure.

## 1.11 Firewall Context (Deferred)

The video mentions that there are firewall-related commands in the documentation but **explicitly skips them**, stating that firewall concepts require networking knowledge that will be covered later in the AWS section. The video notes that for this local Vagrant-based project, the setup works identically whether or not firewall commands are executed.

> 🔍 **Deep Dive:** In production, databases listen on specific ports (MariaDB default: 3306). A firewall must be configured to allow inbound connections on that port only from trusted sources (e.g., the app server's IP). In this Vagrant lab, all VMs are on a private network with no firewall restrictions, so this step is safely deferred.

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are setting up the **database layer** of the VProfile multi-tier application. By the end of this process, we will have a running MariaDB instance on the `db01` VM, with a database called `accounts`, populated with the application schema, and accessible both locally and remotely by an `admin` user. This database will be consumed by the Tomcat application server (app01) in a later setup stage.

## Step 1: Access the Database VM

If you took a long break since the last lecture, first reboot all VMs:

```bash
vagrant reload
```

Make sure you are in the correct Vagrant project directory before running this. If you are continuing directly from the previous lecture, skip the reload.

Now SSH into the database VM:

```bash
vagrant ssh db01
```

* `vagrant ssh` — Opens an SSH session into a Vagrant-managed VM.
* `db01` — The name of the database VM as defined in the Vagrantfile.

Once inside, switch to the root user:

```bash
sudo -i
```

* `sudo` — Execute a command with superuser privileges.
* `-i` — Simulate a full root login shell (sets root's environment, home directory, etc.).

All subsequent commands require root privileges. Operating as root eliminates permission issues during package installation and service management.

## Step 2: Update the Operating System

```bash
dnf update -y
```

* `dnf` — The package manager for CentOS/RHEL 8+.
* `update` — Upgrade all installed packages to their latest available versions.
* `-y` — Automatically answer "yes" to all confirmation prompts.

**What happens internally:** `dnf` contacts all configured repositories, downloads updated package metadata, compares installed versions against available versions, downloads and installs all updates.

**Expected result:** A long output stream showing packages being downloaded and upgraded. This takes significant time.

**Verification:** The command exits with no errors. You return to the shell prompt.

## Step 3: Install EPEL Release Repository

```bash
dnf install epel-release -y
```

* `epel-release` — The package that registers the EPEL repository with dnf.

**What happens:** A new `.repo` file is placed in `/etc/yum.repos.d/`, making EPEL packages discoverable by future `dnf install` commands.

**Verification:** Command completes without errors. You can verify with `dnf repolist` — EPEL should appear.

## Step 4: Install Git and MariaDB Server

```bash
dnf install git mariadb-server -y
```

* `git` — Version control tool. Needed to clone the VProfile source code repository which contains the DB schema file.
* `mariadb-server` — The MariaDB database server package. This installs the server daemon, the `mysql` client CLI, and all dependencies.

**Verification:** Command completes without errors. You can verify with `rpm -q mariadb-server` to confirm the installed version.

## Step 5: Start, Enable, and Verify the MariaDB Service

```bash
systemctl start mariadb
systemctl enable mariadb
systemctl status mariadb
```

* `systemctl start mariadb` — Starts the MariaDB daemon immediately.
* `systemctl enable mariadb` — Configures MariaDB to auto-start on every future boot.
* `systemctl status mariadb` — Displays the current state of the service.

**Note on naming:** The package is `mariadb-server`, but the service name is `mariadb`. (See Theory §1.4 for explanation.)

**Expected output from `status`:** You should see **"active (running)"** in green. Press `q` to exit the status view (it uses a pager).

**Common mistake:** Forgetting `enable`. The service will run now but will not survive a reboot.

## Step 6: Run MySQL Secure Installation

```bash
mysql_secure_installation
```

This is an **interactive** command. Answer the prompts as follows:

| Prompt                                | Action                                          | Reasoning                          |
| ------------------------------------- | ----------------------------------------------- | ---------------------------------- |
| Enter current password for root       | Press **Enter** (empty)                         | Fresh install has no root password |
| Switch to unix\_socket authentication | Press **Enter** (default Y)                     | Acceptable default                 |
| Change the root password              | Press **Enter** (Y), then type `admin123` twice | Sets MySQL root password           |
| Remove anonymous users                | Press **Enter** (Y)                             | Prevents unauthenticated access    |
| Disallow root login remotely          | Press **Enter** (Y)                             | Root should only be local          |
| Remove test database                  | Press **Enter** (Y)                             | Removes unnecessary default DB     |
| Reload privilege tables               | Press **Enter** (Y)                             | Applies changes immediately        |

**Critical distinction:** The "root" user here is the **MySQL root user**, not the Linux root user. They are independent.

**Verification:** The script completes with a success message. The database is now hardened.

**Password used:** `admin123` — as documented. In production, use a strong, complex password.

## Step 7: Log into MySQL as Root

```bash
mysql -u root -padmin123
```

* `mysql` — The MySQL/MariaDB command-line client.
* `-u root` — Connect as the MySQL user `root`.
* `-padmin123` — The password, with **no space** between `-p` and the password value.

**Expected result:** You enter the **MySQL prompt** (`MariaDB [(none)]>`). This is NOT a Linux shell — only SQL commands work here.

**Secure alternative (for real usage):**

```bash
mysql -u root -p
```

This will prompt you to type the password interactively (hidden input).

## Step 8: Create the Application Database

At the MySQL prompt:

```sql
CREATE DATABASE accounts;
```

* `CREATE DATABASE` — SQL command to create a new empty database.
* `accounts` — The specific database name required by the VProfile application. This is not arbitrary — the application configuration expects exactly this name.
* `;` — All SQL statements must end with a semicolon.

**Expected output:** `Query OK, 1 row affected`

## Step 9: Grant Privileges — Local Access

```sql
GRANT ALL PRIVILEGES ON accounts.* TO 'admin'@'localhost' IDENTIFIED BY 'admin123';
```

Breaking this down:

* `GRANT ALL PRIVILEGES` — Give every possible permission (SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, etc.).
* `ON accounts.*` — On all tables (`*`) within the `accounts` database.
* `TO 'admin'@'localhost'` — To a user named `admin` connecting from `localhost` (the DB server itself). If this user does not exist, it is **created automatically**.
* `IDENTIFIED BY 'admin123'` — Set the password for this user.
* `;` — Statement terminator.

**What this achieves:** Creates a local `admin` user with full control over the `accounts` database.

## Step 10: Grant Privileges — Remote Access

```sql
GRANT ALL PRIVILEGES ON accounts.* TO 'admin'@'%' IDENTIFIED BY 'admin123';
```

This is **almost identical** to Step 9, with one critical difference:

* `'admin'@'%'` — The `%` wildcard means **any remote host**. This allows the Tomcat application on `app01` to connect to this database over the network.

**Why both are needed:** `'admin'@'localhost'` and `'admin'@'%'` are treated as **separate users** by MySQL. Without the `%` variant, remote application connections would be rejected.

## Step 11: Flush Privileges and Exit

```sql
FLUSH PRIVILEGES;
```

Forces MySQL to reload the grant tables from disk into memory, ensuring all privilege changes are active.

Then exit:

```sql
exit
```

You return to the Linux root shell.

## Step 12: Clone the Source Code

```bash
cd /tmp
git clone -b local <repository-URL>
```

* `cd /tmp` — Navigate to the `/tmp` directory (a temporary working location).
* `git clone` — Download a copy of the remote Git repository.
* `-b local` — Check out the branch named `local` specifically. This branch contains the configuration suitable for the local Vagrant setup.

**Expected result:** A directory named `vprofile-project` is created inside `/tmp`.

Then navigate into it:

```bash
cd vprofile-project
```

## Step 13: Locate and Deploy the SQL Schema File

First, verify the file exists:

```bash
ls src/main/resources/
```

You should see **`db_backup.sql`** among the listed files.

Optionally inspect it:

```bash
cat src/main/resources/db_backup.sql
```

This shows the SQL statements inside — CREATE TABLE, INSERT, etc.

Now deploy the schema:

```bash
mysql -u root -padmin123 accounts < src/main/resources/db_backup.sql
```

Breaking this down:

* `mysql -u root -padmin123` — Connect as root with the password.
* `accounts` — Use the `accounts` database as the default database context.
* `<` — Shell input redirection: feeds the file's contents into `mysql`'s standard input.
* `src/main/resources/db_backup.sql` — The path to the schema file.

**What happens internally:** Every SQL statement in `db_backup.sql` executes sequentially against the `accounts` database. Tables are created, data is inserted, and the schema is fully initialized.

**Expected result:** The command completes silently (no output means success).

**Common mistake:** Running this from the wrong directory. The relative path `src/main/resources/db_backup.sql` only works from inside `vprofile-project/`.

## Step 14: Verify the Database Setup

Log back into MySQL, directly into the accounts database:

```bash
mysql -u root -padmin123 accounts
```

The `accounts` argument at the end opens the MySQL client with `accounts` as the active database.

At the MySQL prompt:

```sql
SHOW TABLES;
```

**Expected result:** You should see the list of tables created by `db_backup.sql` — this confirms the schema was deployed successfully.

Optionally, check all databases:

```sql
SHOW DATABASES;
```

You will see system databases (`mysql`, `information_schema`, `performance_schema`) plus the `accounts` database.

Exit when done:

```sql
exit
```

## Step 15: Firewall Commands (Skipped)

The documentation includes firewall configuration commands, but these are **intentionally skipped** in this stage. The Vagrant private network does not enforce firewall rules, so the project works without them. Firewall concepts will be covered in the AWS section.

## What Comes Next

The database layer is now complete. The next lecture covers setting up the **Memcached server**, which is the next component in the VProfile multi-tier stack.

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## System Architecture Position

```
VProfile Multi-Tier Stack:
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   app01       │────▶│   db01        │     │  memcached   │
│   (Tomcat)    │     │  (MariaDB)    │     │  (next)      │
└──────────────┘     └──────────────┘     └──────────────┘
       │                     ▲
       │   remote connect    │
       │   admin@% :3306     │
       └─────────────────────┘
```

**db01's role:** Persistent data store. Serves the `accounts` database to the Tomcat app via remote MySQL connection.

## Complete Execution Flow

```
vagrant ssh db01 → sudo -i
    │
    ▼
dnf update -y                          ← OS patching
    │
    ▼
dnf install epel-release -y            ← Enable extra repo
    │
    ▼
dnf install git mariadb-server -y      ← Install DB + Git
    │
    ▼
systemctl start mariadb                ← Start NOW
systemctl enable mariadb               ← Start on BOOT
systemctl status mariadb               ← Verify: "active (running)"
    │
    ▼
mysql_secure_installation              ← Harden (interactive)
    │   root pw: admin123
    │   remove anon users: Y
    │   disallow remote root: Y
    │   remove test db: Y
    │   reload privileges: Y
    │
    ▼
mysql -u root -padmin123               ← Enter MySQL prompt
    │
    ├─▶ CREATE DATABASE accounts;
    ├─▶ GRANT ALL ... TO 'admin'@'localhost' IDENTIFIED BY 'admin123';
    ├─▶ GRANT ALL ... TO 'admin'@'%' IDENTIFIED BY 'admin123';
    ├─▶ FLUSH PRIVILEGES;
    └─▶ exit
    │
    ▼
cd /tmp → git clone -b local <repo>   ← Get source code
cd vprofile-project
    │
    ▼
mysql -u root -padmin123 accounts < src/main/resources/db_backup.sql
    │                                   ← Schema deployment via input redirection
    ▼
mysql -u root -padmin123 accounts      ← Verify
    ├─▶ SHOW TABLES;                   ← Confirm schema exists
    ├─▶ SHOW DATABASES;                ← Confirm accounts DB exists
    └─▶ exit
    │
    ▼
✅ DATABASE LAYER COMPLETE → Next: Memcached setup
```

## Key Concept Chains

```
Package name ≠ Service name
  mariadb-server (package) → mariadb (service)
  Discovery: docs / rpm -ql / grep systemd

start ≠ enable
  start  → runs NOW, lost on reboot
  enable → runs on BOOT, not running now
  Always: start + enable together

MySQL root ≠ Linux root
  Separate auth systems. mysql_secure_installation sets MySQL root pw.

MySQL user identity = username + host
  'admin'@'localhost'  → local connections only
  'admin'@'%'          → remote connections (wildcard)
  These are TWO DIFFERENT USERS despite same username.

GRANT (on non-existent user) = CREATE + GRANT combined

FLUSH PRIVILEGES = reload grant tables into memory
  (Defensive habit — ensures changes are active)

-padmin123 (no space) = inline password (insecure, visible in history)
-p (alone)            = interactive prompt (secure)
```

## Schema Deployment Pattern

```
Source code repo
  └─ src/main/resources/
       └─ db_backup.sql          ← "DB dump" provided by developers

Deployment method:
  mysql -u <user> -p<pw> <database> < <file.sql>
       │            │        │            │
       │            │        │            └─ Input redirection: file → stdin
       │            │        └─ Default database context
       │            └─ Auth credentials
       └─ MySQL CLI client

Real-world alternatives:
  Manual:    DBA runs dump file (this video)
  Automatic: App initializes DB on first startup (Hibernate/Flyway/Liquibase)
```

## Reusable Engineering Patterns

| Pattern                              | Instance in This Setup                                     |
| ------------------------------------ | ---------------------------------------------------------- |
| **OS-first, service-second**         | Always `dnf update` before installing anything             |
| **Repo expansion before install**    | EPEL before MariaDB (dependency availability)              |
| **Start + Enable discipline**        | Every daemon: start for now, enable for persistence        |
| **Secure-by-default hardening**      | `mysql_secure_installation` immediately after install      |
| **Least privilege + explicit grant** | Separate local/remote users, grant only needed DB          |
| **Schema-as-code**                   | DB structure lives in version control, deployed from repo  |
| **Input redirection for batch ops**  | `< file.sql` instead of interactive typing                 |
| **Verify after every state change**  | `status`, `SHOW TABLES`, `SHOW DATABASES` after each phase |

## Validation Checkpoints

```
After service start     → systemctl status mariadb → "active (running)"
After secure_install    → Script completes with success message
After CREATE DATABASE   → "Query OK"
After GRANT             → "Query OK"
After schema deploy     → Silent return (no errors)
After final login       → SHOW TABLES returns populated table list
```

## Failure Quick-Reference

| Symptom                          | Likely Cause                                  | Fix                                 |
| -------------------------------- | --------------------------------------------- | ----------------------------------- |
| `mariadb` service not found      | Used package name instead of service name     | Use `mariadb`, not `mariadb-server` |
| Service not running after reboot | Forgot `systemctl enable`                     | Run `enable`                        |
| Can't log in to MySQL            | Wrong password or wrong user (MySQL vs Linux) | Use MySQL root pw, not Linux pw     |
| App can't connect remotely       | Missing `'admin'@'%'` grant                   | Create the `%` user                 |
| Schema deploy fails silently     | Wrong directory (relative path)               | `cd` into `vprofile-project` first  |
| `db_backup.sql` not found        | Cloned wrong branch                           | Use `-b local`                      |

## Mental Reload Sentence

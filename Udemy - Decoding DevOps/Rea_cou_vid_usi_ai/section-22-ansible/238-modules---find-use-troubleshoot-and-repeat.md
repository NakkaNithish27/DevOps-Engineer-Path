# 🎓 Deep Learning Material: Ansible Modules — Find, Use, Troubleshoot, and Repeat

**Source:** Video lecture on Ansible module discovery, usage, and troubleshooting (from [238-modules-find-use-troubleshoot-and-repeat.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt?EntityRepresentationId=a3544461-0821-4129-914b-2c93a9b914ae) caption file) [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Video Context:** This lecture teaches the **core operational workflow** that a DevOps engineer uses daily with Ansible: find a module for a task, use it in a playbook, encounter failures, troubleshoot them, fix the playbook, and reuse the solution. The instructor deliberately walks into two failures — a missing Python dependency and a missing MySQL socket file — to teach the troubleshooting mindset. Three modules are used: **copy** (simple, no dependencies), **mysql\_db** (requires Python MySQL library + socket configuration), and **mysql\_user** (reuses the same dependency and fix). The lecture also introduces **community modules** (`community.mysql`) and the `ansible-galaxy` command to install them. The highest-value content is not any individual module but the **find → use → fail → troubleshoot → fix → reuse** workflow itself.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Module Index: How to Find Modules for Any Task

Ansible's power comes from its **modules** — pre-built units of functionality that handle specific tasks (copying files, managing packages, configuring databases, interacting with cloud services). When you're assigned a task, your first step is always to **find the right module**. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

The instructor directs to the **Ansible module index** (searchable as "ansible module index"). The index organizes modules into categories: **cloud modules**, **database modules**, **files modules**, etc. You can also view "All modules" as a flat list. The instructor emphasizes this is regular work: *"This will be your very regular work as a DevOps engineer. You need to write playbook. There'll be different kinds of tasks. You need to find modules for your task, use it. If it fails, you need to troubleshoot."* [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

***

## 1.2 — The Copy Module: A Simple Module with No Dependencies

The **copy** module copies files from the control machine (where Ansible runs) to remote target machines. It's in the **files** module category. The instructor highlights that files modules are heavily used in DevOps work: *"Being a DevOps, our job will be majorly managing files. Their configuration of files could be an archive, it could be an artifact, a text file, configuration files, scripts. We deal with files a lot."* [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

The copy module internally uses the **SCP command** in Linux — the instructor notes: *"copy is a very simple module. It uses SCP command in the Linux."* This is important because it means the copy module has **no special dependencies** beyond basic SSH connectivity. It works out of the box. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

### Module Parameters: Mandatory vs. Optional

Every module has **parameters** (also called arguments or options). Some are **mandatory** (required), others are **optional**. The instructor examines the copy module's parameters: [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

* **`dest` (destination)** — **Required**. Where to put the file on the remote machine.
* **`src` (source)** — Not mandatory, because there's an alternative: you can use `content` instead, which lets you write text content directly in the playbook rather than referencing a file.
* **`owner`**, **`group`**, **`mode`** — Optional. Set file ownership and permissions. Not needed if you just want to copy.
* **`backup`** — Optional. If set to `yes`, takes a backup of the existing destination file before overwriting it. The backup file gets a timestamp appended to its name. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

The instructor's key advice: *"look at the options, or parameters, and you can find interesting options to use which may enhance your playbook. And look at the examples, of course."* [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

***

## 1.3 — Module Dependencies: Why Some Modules Fail Out of the Box

This is the lecture's most important conceptual lesson. The copy module works immediately because it relies only on SCP — a basic Linux utility. But **many modules require additional dependencies** — typically **Python libraries** — installed on the **target machine** (not the control machine). [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

The instructor explains the mechanism: *"We know Ansible creates Python scripts. It will dump in the destination, which is db01 now, at the remote location and execute those Python scripts. Those Python scripts will need some Python dependency for certain module."* [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

When Ansible executes a task using the `mysql_db` module, it generates a Python script on the control machine, transfers it to the target machine (db01), and executes it there. That Python script needs to **import Python MySQL libraries** to connect to the MySQL/MariaDB database. If those libraries aren't installed on the target, the script fails with an import error. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

The dependencies are documented in the module's **Requirements** section: *"The below requirements are needed on the host that executes this module."* The key phrase is **"on the host that executes"** — this means the **target machine**, not the control machine. For the `mysql_db` module, the requirement is a Python MySQL library (like `PyMySQL`). [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

> 🔍 **Deep Dive**
>
> The dependency chain is: Ansible module → generates Python script → script runs on target → script imports Python library → library connects to service. If any link breaks, the task fails. The most common break is the missing Python library on the target. The fix is always: **(1)** identify the required library from the module documentation or error message, **(2)** find the installable package name on the target OS (using `yum search` or `apt search`), **(3)** add a task in the playbook to install that package **before** the module task that needs it. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

***

## 1.4 — The Socket File Problem: Process-to-Process Communication on Linux

The second failure the instructor encounters is about **connecting to the MySQL server**. Even after installing the Python MySQL library, the `mysql_db` module fails because it doesn't know **how** to connect to the database process. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

On Linux, local processes connect to each other through **socket files**. A socket file is a special file on the filesystem that acts as a communication endpoint. MySQL/MariaDB creates a socket file when it starts, and client processes (including Ansible's Python scripts) use that socket file to establish a connection. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

The problem: the default socket file path assumed by the module doesn't match the actual path on CentOS. On CentOS, the MariaDB socket file is located at `/var/lib/mysql/mysql.sock` (inside the MariaDB default home directory `/var/lib/mysql`). The fix is to explicitly specify the socket path using the `login_unix_socket` parameter. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

The instructor finds this solution through **Stack Overflow**: *"Problem is basically Ansible is not able to connect to MySQL server because it does not know how to connect."* The community MySQL module documentation also mentions this in its **Notes** section under "commonly found errors." [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

***

## 1.5 — Community Modules vs. Built-in Modules

Ansible has two sources of modules: **built-in modules** (maintained by Ansible/Red Hat) and **community modules** (developed by the broader Ansible community). For MySQL operations, there's a **community module collection** called `community.mysql` that is better maintained and more thoroughly documented than the older built-in MySQL modules. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

Community modules must be **explicitly installed** on the control machine using `ansible-galaxy`:

```bash
ansible-galaxy collection install community.mysql
```

Once installed, you reference them with their **fully qualified collection name** (FQCN) in playbooks: `community.mysql.mysql_db` instead of just `mysql_db`. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

The instructor points out that the community module documentation is more helpful — it lists requirements clearly, provides examples with socket file options, and documents commonly found errors. *"We have community MySQL module also where all this is already mentioned."* [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

***

## 1.6 — The Reusability Principle: Solve Once, Reuse Everywhere

When the instructor adds the `mysql_user` task (creating a database user), the **exact same socket file error** occurs. But this time, the fix is already known — just add the `login_unix_socket` parameter. The instructor emphasizes: *"you see you solve once, and then you can use it as many times."* [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

This demonstrates that troubleshooting effort is **an investment, not a cost**. Every problem you solve becomes a reusable solution for all future tasks using the same module or similar patterns. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are executing three Ansible tasks across two exercises: **(1)** copying a file to web servers using the `copy` module, **(2)** creating a MySQL database using `community.mysql.mysql_db`, and **(3)** creating a MySQL user using `community.mysql.mysql_user`. The real goal is not the tasks themselves but learning the **find → use → troubleshoot → fix → reuse** operational workflow. The final outcome: a working playbook that installs dependencies, creates a database, and creates a user — with all troubleshooting steps resolved.

***

## Part A: Copy Module — Exercise 6

### Step 1: Set Up Exercise 6

```bash
cp -r exercise5 exercise6
cd exercise6
```

Rename the playbook to focus only on web servers:

```bash
mv web-db.yaml web.yaml
```

Open `web.yaml` and **remove the db play** — keep only the web play. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

### Step 2: Find the Copy Module and Add the Task

**Finding the module:** Search "ansible module index" → Files modules → **copy** — "Copy files to remote location." [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Go to the Examples section** of the documentation and copy the example for "Copy file with owner and permission." [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Paste into `web.yaml`** under the web play's tasks. Fix indentation first — copy-pasting from documentation often breaks YAML structure. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Modify the task:**

```yaml
- name: index file
  ansible.builtin.copy:
    src: files/index.html
    dest: /var/www/html/index.html
    backup: yes
```

* `name: index file` — descriptive task name [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)
* `src: files/index.html` — source file path relative to the playbook (a `files/` directory next to the playbook)
* `dest: /var/www/html/index.html` — full destination path **including filename** on the remote machine
* `backup: yes` — takes a timestamped backup of the existing file before overwriting [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)
* **Removed:** `owner`, `group`, `mode` — not needed for this simple copy task (optional parameters)

### Step 3: Create the Source File

```bash
mkdir files
vim files/index.html
```

Write any content, e.g.: `learning modules in ansible` [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Important:** The file path in the playbook (`files/index.html`) must match the actual file location relative to the playbook directory. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

### Step 4: Execute and Verify

```bash
ansible-playbook -i inventory web.yaml
```

**Expected result:** Task shows **"changed"** for both web01 and web02. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Verify by SSH into a web server:**

```bash
ssh -i clientkey ec2-user@<web01-ip>
cd /var/www/html
ls
```

**Expected files:** [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

* `index.html` — the file we pushed (check content with `cat index.html`)
* `index.html.<timestamp>~` — the backup of the previous file (created because `backup: yes`)

The backup filename includes a timestamp showing when the backup was taken. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Log out** from the web server: `exit`

### Optional: Set Control Machine Hostname

```bash
sudo hostname control
```

Then log out and log back in. The prompt now shows `control` — helps identify which machine you're on when SSH-ing to multiple servers. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

***

## Part B: MySQL Database Module — Exercise 7

### Step 5: Set Up Exercise 7

```bash
cp -r exercise5 exercise7
cd exercise7
mv web-db.yaml db.yaml
```

Open `db.yaml` and **remove the web play** — keep only the db play (which installs mariadb-server and starts the service). [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

### Step 6: Find the mysql\_db Module and Add the Task

**Finding the module:** Ansible module index → Database modules → MySQL → **mysql\_db** [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Copy the example** for "Create a new database with name 'bobdata'" and paste into `db.yaml` under the existing tasks. Fix indentation. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Modify:**

```yaml
- name: Create a new database
  mysql_db:
    name: accounts
    state: present
```

 [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

### Step 7: Execute — First Failure (Missing Python Dependency)

```bash
ansible-playbook -i inventory db.yaml
```

**Expected result: FAILURE** [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Error:** The module requires a Python MySQL library on the target machine (db01), but it's not installed. The error message references missing Python MySQL dependencies.

**Diagnosis:** The module documentation's Requirements section states: *"The below requirements are needed on the host that executes this module"* — meaning db01, not the control machine. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

### Step 8: Find the Python Package Name

SSH into db01:

```bash
ssh -i clientkey ec2-user@<db01-ip>
```

Search for the package:

```bash
yum search python | grep -i mysql
```

* `yum search python` — lists all Python-related packages
* `| grep -i mysql` — filters for MySQL-related packages (case-insensitive) [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Result:** Find `python3-PyMySQL` — this is the package to install. **Copy the exact package name.** [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Log out** from db01: `exit`

### Step 9: Add Dependency Installation to the Playbook

**Don't install manually on db01** — add it as a playbook task so it's automated. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

Open `db.yaml` and add a yum task **before** the mysql\_db task (copy an existing yum task from the playbook and modify):

```yaml
- name: install pymysql
  yum:
    name: python3-PyMySQL
    state: present
```

 [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

### Step 10: Execute — Second Failure (Socket File)

```bash
ansible-playbook -i inventory db.yaml
```

**Expected result: FAILURE** — dependency installs successfully, but the mysql\_db task fails. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Error:** Access denied / unable to connect to MySQL. The Python script on db01 can't find the MySQL socket file.

**Diagnosis:** The instructor Googles the error with "ansible" added to the search query. Stack Overflow reveals: the module doesn't know the socket file location on CentOS. The default path assumed by the module is wrong for CentOS. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**CentOS socket file path:** `/var/lib/mysql/mysql.sock` (inside MariaDB's default home directory) [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

### Step 11: Add Socket File Path and Succeed

Open `db.yaml` and add the `login_unix_socket` parameter to the mysql\_db task:

```yaml
- name: Create a new database
  community.mysql.mysql_db:
    name: accounts
    state: present
    login_unix_socket: /var/lib/mysql/mysql.sock
```

 [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

### Step 12: Install Community MySQL Module

Before using `community.mysql.*`, install the collection on the control machine:

```bash
ansible-galaxy collection install community.mysql
```

 [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

Update the module name in the playbook from `mysql_db` to `community.mysql.mysql_db`. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

### Step 13: Execute — Success

```bash
ansible-playbook -i inventory db.yaml
```

**Expected result:** All tasks show **"changed"** or **"ok"**. Database `accounts` created. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

***

## Part C: MySQL User Module — Reusing the Fix

### Step 14: Add the mysql\_user Task

**Find the module:** Ansible module index → `mysql_user` — "Add or remove a user from MySQL database." [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Copy the example** for creating a database user and add to `db.yaml`:

```yaml
- name: Create database user
  community.mysql.mysql_user:
    name: vprofile
    password: 'admin943'
    state: present
    login_unix_socket: /var/lib/mysql/mysql.sock
```

 [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Key point:** The `login_unix_socket` parameter is included **immediately** — reusing the fix from the previous troubleshooting. *"You solve once, and then you can use it as many times."* [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

### Step 15: Execute — Success

```bash
ansible-playbook -i inventory db.yaml
```

**Expected result:** All tasks succeed. Database `accounts` exists, user `vprofile` created with the specified password. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 The Core Workflow (This Lecture's Central Teaching)

```
FIND → USE → FAIL → TROUBLESHOOT → FIX → REUSE

1. FIND:  Ansible module index → category → module → examples
2. USE:   Copy example → paste into playbook → fix YAML → customize
3. FAIL:  Run playbook → error (dependency / config)
4. TROUBLESHOOT:
     → Read error message
     → Check module Requirements section
     → Google error + "ansible"
     → Stack Overflow / community docs
5. FIX:   Add dependency task / add missing parameter
6. REUSE: Apply same fix to all tasks using same module

"This will be your very regular work as a DevOps engineer."
```

***

## 🔷 Three Modules Used

```
MODULE              CATEGORY    DEPENDENCIES        DIFFICULTY
─────────────────   ─────────   ──────────────────   ──────────
copy                Files       None (uses SCP)      Simple
mysql_db            Database    Python MySQL lib      Medium
mysql_user          Database    Python MySQL lib      Medium (same fix)

Community versions: community.mysql.mysql_db
                    community.mysql.mysql_user
Install: ansible-galaxy collection install community.mysql
```

***

## 🔷 Copy Module Quick Reference

```yaml
- name: index file
  ansible.builtin.copy:
    src: files/index.html              # relative to playbook
    dest: /var/www/html/index.html     # full path INCLUDING filename
    backup: yes                        # timestamp backup of existing file

Required: dest
Optional: src OR content, owner, group, mode, backup
```

***

## 🔷 MySQL Module Failure → Fix Chain

```
FAILURE 1: Missing Python dependency
  Error: "A MySQL module is required for Python"
  
  FIND PACKAGE:
    ssh into target → yum search python | grep -i mysql
    → python3-PyMySQL
  
  FIX: Add yum task BEFORE mysql_db task:
    - name: install pymysql
      yum:
        name: python3-PyMySQL
        state: present

FAILURE 2: Cannot connect to MySQL
  Error: "Access denied" / can't find socket
  
  CAUSE: Module doesn't know socket file location on CentOS
  
  FIX: Add login_unix_socket parameter:
    login_unix_socket: /var/lib/mysql/mysql.sock
  
  HOW FOUND: Google error + "ansible" → Stack Overflow
```

***

## 🔷 Why Modules Need Dependencies (Execution Model)

```
CONTROL MACHINE                          TARGET MACHINE (db01)
─────────────────                        ─────────────────────
Ansible reads playbook                   
  │                                      
  ├── Generates Python script            
  │   (for mysql_db task)                
  │                                      
  ├── Transfers script via SSH ────────► Python script arrives
  │                                      │
  │                                      ├── Script tries: import pymysql
  │                                      │   → FAILS if not installed
  │                                      │
  │                                      ├── Script tries: connect via socket
  │                                      │   → FAILS if wrong socket path
  │                                      │
  │                                      └── Both fixed → task succeeds

Dependencies must be on TARGET, not control machine.
```

***

## 🔷 Module Parameters: Mandatory vs. Optional

```
MANDATORY (required):
  → Task fails if missing
  → Documented as "required" in parameter list
  → Example: copy.dest, mysql_db.name

OPTIONAL:
  → Task works without them
  → Enhance functionality
  → Example: copy.backup, copy.owner, mysql_db.login_unix_socket
  
"A module may have mandatory option, one or two,
 and most of the options will be optional."
```

***

## 🔷 Community Modules vs. Built-in

```
BUILT-IN:                            COMMUNITY:
─────────                            ──────────
Included with Ansible                Must install separately
mysql_db                             community.mysql.mysql_db
Less documented                      Better docs, examples, error notes

INSTALL:
  ansible-galaxy collection install community.mysql

USE IN PLAYBOOK:
  community.mysql.mysql_db           (fully qualified name)
```

***

## 🔷 Files Module Category (Important for DevOps)

```
FILES MODULES (high-frequency for DevOps):
  ├── copy      → copy files to remote (SCP-based)
  ├── file      → manage file properties (permissions, directories)
  ├── archive   → create archives
  ├── blockinfile → manage blocks of text in files
  └── ... many more

"Being a DevOps, our job will be majorly managing files."
```

***

## 🔷 Exercise File Structure

```
exercise6/                           exercise7/
  ├── inventory                        ├── inventory
  ├── web.yaml                         ├── db.yaml
  └── files/                           └── clientkey
        └── index.html

web.yaml tasks:                      db.yaml tasks:
  1. copy index.html → web servers     1. install mariadb-server
     (with backup: yes)                2. start mariadb service
                                       3. install python3-PyMySQL (dependency)
                                       4. create database 'accounts'
                                       5. create user 'vprofile'
```

***

## 🔷 Troubleshooting Toolkit

```
1. READ THE ERROR MESSAGE (exact text)
2. CHECK MODULE DOCS:
   → Requirements section ("on the host that executes")
   → Notes section ("commonly found errors")
   → Examples section (working examples with all params)
3. GOOGLE: error message + "ansible"
   → Stack Overflow, community forums
4. FIND PACKAGES: yum search <keyword> | grep -i <filter>
5. FIX IN PLAYBOOK (not manually on server)
6. REUSE FIX for all tasks using same module
```

***

## 🔷 Socket File Concept (Quick Reference)

```
SOCKET FILE = filesystem endpoint for inter-process communication
  → MySQL client → reads socket file → connects to MySQL server
  → Path varies by OS:
       CentOS: /var/lib/mysql/mysql.sock
       Ubuntu: /var/run/mysqld/mysqld.sock (typical)
  → Must specify with: login_unix_socket parameter
```

***

## 🔷 Reusable Engineering Pattern: Dependency-Aware Task Ordering

```
PATTERN: Install Dependencies Before Using Dependent Modules

WRONG ORDER:                         CORRECT ORDER:
  1. mysql_db task → FAILS             1. yum: install python3-PyMySQL
     (missing pymysql)                 2. mysql_db task → SUCCEEDS

GENERAL RULE:
  For any module with requirements:
    1. Read Requirements section
    2. Add package installation task BEFORE the module task
    3. Add configuration parameters (socket, connection strings)
    4. Then use the module

This pattern applies to:
  - Database modules (need Python DB drivers)
  - Cloud modules (need boto3, azure-cli, etc.)
  - Network modules (need paramiko, netmiko, etc.)
  - Any module with external library dependencies
```

***

## 🔷 The Instructor's Deliberate Failure Teaching Method

```
"I did this purposefully, actually."

TEACHING SEQUENCE:
  1. Skip reading Requirements → run playbook → FAIL
  2. Diagnose from error message → find package → fix
  3. Run again → FAIL (second issue)
  4. Google error → Stack Overflow → find fix
  5. Run again → SUCCESS
  6. THEN show community module docs where everything was documented

LESSON: "If you read properly, you won't even get into those problems.
         But anyways, you will get into problem. Don't worry, it will happen."

Both paths are valid:
  - Read docs first → fewer failures
  - Fail first → deeper understanding of WHY things break
```

This is the lecture's meta-teaching: the troubleshooting skill is more valuable than any individual module knowledge. Modules change; the find → use → fail → fix workflow is permanent. [\[238-module...and-repeat \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/238-modules-find-use-troubleshoot-and-repeat.txt)

**Source:** [72-automated-code.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/72-automated-code.txt?EntityRepresentationId=df5bce99-3218-46db-93c0-a7925b273f38) — Video lecture walking through the automated provisioning scripts that replace the manual setup of the vprofile-project stack.

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 Context — From Manual Provisioning to Automated Provisioning

In previous lectures, every service in the vprofile-project stack — MySQL (db01), Memcache (mc01), RabbitMQ (rmq01), Tomcat (app01), and Nginx — was set up **manually**: SSH into each VM, run commands one by one, edit configuration files by hand. That worked for learning, but it is slow, error-prone, and non-repeatable. This lecture introduces the **automated provisioning** approach: every command that was previously typed manually is now captured inside **Shell scripts**, and the Vagrant file is configured to execute those scripts automatically when the VMs are created. The result: a single `vagrant up` brings up all VMs and configures all services without any manual intervention.

This is the foundational step from "operations by hand" to "infrastructure as code." The scripts themselves are not complex — they are the **exact same commands** from the manual lectures, pasted into files with minor tweaks. The engineering value is in understanding the **pattern**: take manual operational procedures, encode them as scripts, wire them into the VM provisioning lifecycle, and make the entire stack reproducible.

## 1.2 Repository Structure — Where the Scripts Live

The source code repository contains a **"vagrant" folder** with an **"Automated provisioning"** subfolder. Inside, there are two variants based on the host operating system: one folder for **Windows and MacOS with Intel chip**, and another for **MacOS M1/M2 chip** (ARM architecture). The learner should choose the folder matching their hardware. This repository was already cloned in VSCode in an earlier lecture.

Inside the chosen folder, you find:

* The **Vagrantfile** (the VM definition file)
* **mysql.sh** — Shell script for the database VM (db01)
* **memcache.sh** — Shell script for the Memcache VM (mc01)
* **rabbitmq.sh** — Shell script for the RabbitMQ VM
* **tomcat\_ubuntu.sh** — Shell script for the Tomcat/application VM (Ubuntu-based)
* **nginx.sh** — Shell script for the Nginx VM

Each script corresponds to one VM in the stack. Each script contains the commands to set up that specific service — the same commands from the manual provisioning lectures.

## 1.3 The Vagrantfile Change — Provisioning Integration

The Vagrantfile in the automated provisioning folder is **identical to the manual provisioning Vagrantfile** with one critical addition: for every VM definition, there is now a **provisioning line** that specifies a Shell script to execute. For example, the DB01 VM definition includes a reference to `mysql.sh`.

This is Vagrant's **provisioning mechanism**. When `vagrant up` is run, Vagrant does not just create and boot the VM — after the VM is running, it also executes the specified Shell script inside the VM. This means: VM creation + OS boot + service configuration all happen in one automated step, per VM, for every VM in the stack.

🔍 **Deep Dive — The Provisioning Execution Model:**

Vagrant copies the Shell script from the host machine into the guest VM and executes it as root. The script runs non-interactively — there is no human to type "yes" at prompts or paste text into editors. This is why the scripts use `-y` flags on all install commands and why file creation uses the `cat` command with heredoc syntax instead of `vim` (see §1.6). The script must be fully autonomous.

## 1.4 Shell Script Basics — The Shebang and Structure

Every Shell script in this project begins with `#!/bin/bash` — called the **shebang** (hash-exclamation). The instructor explains: "This is to open the bash Shell interpreter. It's the same black screen where we execute the command. So it's going to open a new Shell and execute all the command."

When Linux encounters this line at the top of a script file, it knows to use `/bin/bash` as the interpreter for all subsequent lines. Without it, the system might try to use a different shell (like `sh` or `dash`), which could behave differently. The shebang is the **contract** between the script and the operating system about which interpreter to use.

After the shebang, the scripts follow a straightforward pattern: **variable assignments** (like setting the database password), then the **exact same commands** from manual provisioning, executed sequentially.

## 1.5 Script-by-Script Walkthrough — What Each Script Automates

### mysql.sh (db01 — Database)

This script automates the entire MySQL/MariaDB setup from the manual lecture. It begins by setting a **variable** for the database password — the instructor notes this is "for convenience purpose only" (so the password can be referenced by variable name throughout the script rather than hardcoded in every command). Then it installs MariaDB, starts and enables the service, clones the source code, and deploys the database schema.

The critical difference from manual provisioning: **SQL queries are executed from the Shell**, not from inside the MySQL command prompt. In manual provisioning, you ran `mysql -u root` to enter the SQL prompt, then typed SQL commands interactively. In a script, there is no interactive prompt. Instead, you use:

```bash
mysql -u username -p password -e "SQL QUERY HERE"
```

The `-e` flag means "execute this query and exit." This allows SQL commands to run non-interactively from within a bash script. The login credentials (`-u` for username, `-p` for password) are passed inline so the script can authenticate without human input.

The script ends with firewall commands, which the instructor says not to worry about — they will be covered later in the context of AWS security groups.

### memcache.sh (mc01 — Cache)

Contains the same commands from the Memcache manual setup lecture: install, start, enable, change the listen address from `127.0.0.1` to `0.0.0.0`, restart. The instructor describes it as "pretty simple, same commands."

### rabbitmq.sh (RabbitMQ — Message Queue)

Same pattern: the manual RabbitMQ setup commands encoded as a script. "Once again, pretty simple, same commands."

### tomcat\_ubuntu.sh (app01 — Application Server)

This is the most complex script because the Tomcat setup on Ubuntu involves more steps: installing dependencies, setting up the Tomcat systemd file, cloning the source code, running `mvn install` to build the application artifact, and deploying it.

The key difference from manual provisioning is **file creation**. In the manual lecture, the systemd service file was created by opening `vim`, entering insert mode, pasting content, and saving. In a script, you **cannot use vim** — there is no interactive editor. Instead, the script uses the **`cat` command with heredoc syntax** to create files with content (see §1.6).

### nginx.sh (Nginx — Reverse Proxy/Load Balancer)

Installs Nginx, creates the configuration file (again using `cat`/heredoc instead of vim), disables the default website, enables the vprofile website, starts and enables the Nginx service.

## 1.6 The cat Heredoc Pattern — Creating Files in Scripts Without an Editor

This is the most important **new technique** introduced in this lecture. In manual provisioning, whenever a configuration file needed to be created with specific content (like the Tomcat systemd file or the Nginx config), the instructor used `vim`: open file → insert mode → paste → save. That workflow requires a human at the keyboard.

In a Shell script, you cannot open vim. The solution is the **cat heredoc** pattern:

```bash
cat > /path/to/file <<EOT
[all the content]
[goes here]
[exactly as needed]
EOT
```

The instructor explains: "With cat command, we create this file and all this content will be injected into this file. This EOT you see, EOT or EOF, something like that, you will see and between that all the content will be there. All the content in between that will be injected into that file."

`EOT` (End Of Text) or `EOF` (End Of File) is a **delimiter** — a marker that tells the shell "everything between the first `EOT` and the closing `EOT` is the file content." The `cat >` redirects that content into the specified file path. This is the standard way to create files with multi-line content inside Shell scripts.

⚠️ **Expert Note:** This pattern — `cat <<EOF > file` — is one of the most frequently used constructs in infrastructure automation scripts. You will see it in Docker entrypoint scripts, Terraform provisioners, cloud-init user data, CI/CD pipelines, and Ansible shell tasks. Mastering it is essential for any DevOps workflow that involves generating configuration files programmatically.

## 1.7 Variables in Shell Scripts — Parameterization

The mysql.sh script demonstrates the use of **Shell variables** — the database password is assigned to a variable at the top of the script, then referenced wherever the password is needed. This is a minor but important tweak from the manual process: instead of hardcoding the password in every SQL command, you define it once and reference it. This makes the script easier to maintain — change the password in one place, it updates everywhere.

## 1.8 The Bigger Picture — Manual to Automated Progression

The instructor frames this entire lecture as a bridge: "same commands... with some tweaks." The tweaks are:

1. **Variables** instead of hardcoded values
2. **`mysql -u -p -e`** instead of interactive SQL prompt
3. **`cat` heredoc** instead of vim for file creation
4. **Vagrantfile provisioning lines** to wire scripts to VMs

These four adaptations are what transform a manual procedure into an automated one. The commands themselves are identical. The engineering lesson: **automation is not about writing new logic — it is about encoding existing manual procedures into a non-interactive, repeatable format.**

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are reviewing the **automated provisioning scripts** that will, in the next lecture, bring up the entire vprofile-project stack — all five VMs with all services configured — using a single `vagrant up` command. This lecture is a **code walkthrough**, not an execution lecture. The actual execution happens next. The goal here is to understand every script so you know exactly what will happen automatically.

## Step 1: Navigate to the Correct Folder

Open VSCode (where the repository was previously cloned). Navigate to:

```
repository → vagrant → Automated provisioning
```

Choose the subfolder based on your hardware:

* **Windows or MacOS with Intel chip** → first folder
* **MacOS M1/M2 chip** → second folder

Inside, you will see the Vagrantfile and all `.sh` script files.

## Step 2: Examine the Vagrantfile

Open the Vagrantfile. It is the **same Vagrantfile from manual provisioning** with one addition per VM: a provisioning path pointing to a Shell script. For the DB01 VM, this path is `mysql.sh`. Each VM has its corresponding `.sh` file.

This means when `vagrant up` runs, after each VM boots, Vagrant will automatically execute the specified script inside that VM. No manual SSH, no manual commands.

## Step 3: Review mysql.sh (Database Script)

Open `mysql.sh`. Observe the structure:

**Line 1:** `#!/bin/bash` — Shebang. Tells the OS to use the bash interpreter.

**Variable assignment:** A variable holds the database password value. Used throughout the script wherever the password is needed.

**Package installation:** Same `dnf install mariadb-server` (or equivalent) command from manual provisioning, with `-y` for non-interactive confirmation.

**Service management:** `systemctl start mariadb`, `systemctl enable mariadb`.

**Source code:** Clone the repository containing the SQL schema.

**SQL execution from Shell:**

```bash
mysql -u username -p password -e "SQL QUERY"
```

* `-u` — MySQL username
* `-p` — MySQL password (immediately follows, no space in some formats)
* `-e` — Execute the following SQL query and exit

This replaces the manual workflow of: `mysql -u root` → type SQL interactively → `quit`. In a script, everything must be non-interactive.

**Firewall commands** at the end — the instructor says to ignore these for now.

## Step 4: Review memcache.sh (Cache Script)

Open `memcache.sh`. Same commands from the Memcache manual lecture: install epel-release, install memcached, start, enable, `sed` to change `127.0.0.1` to `0.0.0.0`, restart, run the memcached daemon command. No new techniques — straightforward command-to-script translation.

## Step 5: Review rabbitmq.sh (Message Queue Script)

Open `rabbitmq.sh`. Same pattern: the manual RabbitMQ setup commands encoded into a script.

## Step 6: Review tomcat\_ubuntu.sh (Application Server Script)

Open the Tomcat Ubuntu script. This is the longest script because Tomcat's manual setup involved the most steps: dependency installation, Tomcat download and extraction, user creation, systemd file creation, source code clone, Maven build, artifact deployment.

**Key technique — creating the systemd file without vim:**

In manual provisioning, you opened `vim /etc/systemd/system/tomcat.service`, entered insert mode, and pasted the `[Unit]`, `[Service]`, `[Install]` content. In the script, this is replaced with:

```bash
cat > /etc/systemd/system/tomcat.service <<EOT
[Unit]
Description=Tomcat
After=network.target

[Service]
...all the content...

[Install]
WantedBy=multi-user.target
EOT
```

Everything between the first `EOT` and the closing `EOT` is written into the file. This is the **heredoc pattern** (see Theory §1.6).

After file creation, the script continues with `systemctl daemon-reload`, `systemctl start tomcat`, `systemctl enable tomcat`, source code clone, `mvn install`, and artifact deployment — same steps as manual.

## Step 7: Review nginx.sh (Reverse Proxy Script)

Open `nginx.sh`. Installs Nginx, creates the configuration file using `cat` heredoc, disables the default site, enables the vprofile site, starts and enables the service.

## Step 8: What Happens Next

In the next lecture, the instructor will run `vagrant up` from this folder. Vagrant will:

1. Create all VMs in sequence
2. Boot each VM
3. Execute the corresponding `.sh` script inside each VM
4. All services get configured automatically
5. The application is tested from the browser

No manual SSH. No manual commands. One command deploys the entire stack.

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Core Transformation

```
MANUAL PROVISIONING                    AUTOMATED PROVISIONING
─────────────────                      ──────────────────────
vagrant up                             vagrant up
vagrant ssh db01                       (scripts execute automatically)
sudo -i                                
type commands one by one...            
repeat for mc01, rmq01, app01, nginx   
                                       
= hours of manual work                = single command, fully automated
```

## Repository Structure

```
repo/vagrant/Automated provisioning/
    ├── [Windows + Intel Mac] /
    │       └── (use this folder)
    ├── [M1/M2 Mac] /
    │       └── (use this folder)
    │
    Inside chosen folder:
    ├── Vagrantfile          ← same as manual + provisioning paths
    ├── mysql.sh             ← db01 setup
    ├── memcache.sh          ← mc01 setup
    ├── rabbitmq.sh          ← rmq01 setup
    ├── tomcat_ubuntu.sh     ← app01 setup (most complex)
    └── nginx.sh             ← nginx setup
```

## Vagrantfile Wiring

```
Vagrantfile
    ├── VM: db01   → provision: mysql.sh
    ├── VM: mc01   → provision: memcache.sh
    ├── VM: rmq01  → provision: rabbitmq.sh
    ├── VM: app01  → provision: tomcat_ubuntu.sh
    └── VM: nginx  → provision: nginx.sh

vagrant up → create VM → boot → execute .sh script → service ready
```

## Manual → Script Adaptation Rules (4 Tweaks)

```
Manual Technique              Script Equivalent
──────────────                ─────────────────
Hardcoded values         →    Variables (define once, reference everywhere)
mysql -u root (interactive) → mysql -u user -p pass -e "QUERY" (non-interactive)
vim → insert → paste → :wq → cat > file <<EOT ... EOT (heredoc)
Human runs vagrant ssh   →    Vagrantfile provisioning path (automatic)
```

## cat Heredoc Pattern (Key New Technique)

```bash
cat > /path/to/file <<EOT
[entire file content here]
[multi-line, exactly as needed]
EOT
```

```
Purpose: Create files with content inside scripts (no vim)
Delimiter: EOT or EOF (arbitrary marker)
Rule: Everything between first EOT and closing EOT → injected into file
Use cases: systemd files, nginx configs, any multi-line config file
```

## mysql -e Pattern (Non-Interactive SQL)

```bash
mysql -u username -p password -e "SQL QUERY HERE"
```

```
-u  = username
-p  = password
-e  = execute query from Shell (no interactive prompt)

Replaces: mysql -u root → type SQL → quit
```

## Script Internal Structure

```
#!/bin/bash                    ← shebang (use bash interpreter)
VARIABLE=value                 ← parameterization
dnf install <package> -y       ← non-interactive install
systemctl start/enable <svc>   ← service management
sed -i 's/old/new/' <file>     ← config changes
cat > <file> <<EOT ... EOT     ← file creation
mysql -u -p -e "..."           ← non-interactive SQL
```

## Per-Script Content Map

```
mysql.sh       : variable → install mariadb → start/enable → clone code → sql via -e → firewall
memcache.sh    : install epel → install memcached → start/enable → sed 127→0.0.0.0 → restart → daemon
rabbitmq.sh    : install → configure → start/enable
tomcat_ubuntu.sh : install deps → download tomcat → user → cp files → cat heredoc systemd file → 
                   daemon-reload → start/enable → clone → mvn install → deploy artifact
nginx.sh       : install → cat heredoc config file → disable default → enable site → start/enable
```

## Reusable Engineering Patterns

| Pattern                       | Instance                                                               |
| ----------------------------- | ---------------------------------------------------------------------- |
| **Manual → Script encoding**  | Same commands, 4 adaptations (vars, -e, heredoc, provisioning path)    |
| **Provisioner wiring**        | Vagrantfile points each VM to its setup script                         |
| **Non-interactive execution** | `-y` flags, `mysql -e`, `cat <<EOT` — no human input needed            |
| **Heredoc file creation**     | `cat > file <<EOF ... EOF` — universal script pattern for config files |
| **One script per service**    | Clean separation: each VM's setup is isolated in its own file          |
| **Parameterization**          | Variables replace hardcoded values for maintainability                 |

## One-Line Recall Triggers

* **"What changed from manual to automated?"** → Same commands + 4 tweaks (variables, mysql -e, cat heredoc, Vagrantfile provisioning)
* **"How to create a file in a script without vim?"** → `cat > /path <<EOT ... content ... EOT`
* **"How to run SQL from a script?"** → `mysql -u user -p pass -e "QUERY"`
* **"What is #!/bin/bash?"** → Shebang — tells OS to use bash as the interpreter
* **"What does EOT/EOF mean?"** → Heredoc delimiter — content between markers gets injected into file
* **"Which folder to use?"** → Windows/Intel Mac = first folder; M1/M2 Mac = second folder

*Reconstructed from video lecture captions — [69-nginx-setup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/69-nginx-setup.txt?EntityRepresentationId=66be21df-e549-4ffd-be5c-d756bdd57d39)*

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 Nginx's Role in the Stack — The Final Service

Nginx is the **last service** to be set up in the V Profile stack (following MySQL → Memcached → RabbitMQ → Tomcat, as established in the introduction lecture). It runs on the VM called `web01` and functions as the **load balancer** — the entry point for all user traffic. Its job is simple in concept: receive HTTP requests from users and **forward them to the Tomcat application server**. The instructor explicitly calls this "pretty simple" because Nginx in this configuration is not serving content itself — it's purely a traffic router.

The VM `web01` runs an **Ubuntu-based OS** (the instructor uses `apt` commands — the package manager for Debian/Ubuntu systems). This is the only service in the stack exposed directly to the user's browser.

## 1.2 `apt update` vs. `apt upgrade` — A Critical Distinction

The instructor pauses to clarify a distinction that many beginners confuse:

**`apt update`** does **not** install or change anything on the system. It contacts the configured package repositories and **downloads the latest package index** — essentially a catalog of what packages are available and what versions exist. Think of it as checking a menu without ordering anything.

**`apt upgrade`** takes the updated package index from `apt update` and **actually applies the updates** — downloading and installing newer versions of packages that are already installed on the system. This is the command that makes real changes.

The two are always run together (`apt update && apt upgrade`) because upgrading without updating first means you're upgrading against a stale package index — you might miss the latest versions.

## 1.3 Nginx Configuration Architecture — `sites-available` vs. `sites-enabled`

This is the most important conceptual section of the lecture. Nginx uses a **two-directory configuration pattern** that separates configuration *definition* from configuration *activation*:

```
/etc/nginx/
├── sites-available/    ← configuration files DEFINED here
│   ├── default         ← Nginx's built-in default site
│   └── vproapp         ← our custom configuration
│
└── sites-enabled/      ← ACTIVE configurations (symlinks only)
    └── vproapp → ../sites-available/vproapp   ← symlink
```

**`/etc/nginx/sites-available/`** is where you **create** configuration files. Placing a file here does NOT activate it. It's a storage location — a library of available site configurations.

**`/etc/nginx/sites-enabled/`** is what Nginx **actually reads** when it starts or restarts. Only configurations linked here are active. The mechanism for activation is creating a **symbolic link** (`ln -s`) from `sites-enabled/` pointing to the configuration file in `sites-available/`.

**Why this two-directory pattern?** It allows you to have multiple site configurations prepared in `sites-available` but selectively activate only the ones you want by creating or removing symlinks in `sites-enabled`. To deactivate a site, you delete the symlink — the configuration file itself remains intact in `sites-available` for future reactivation. You never lose configuration; you just toggle activation.

> 🔍 **Deep Dive**
> This is an instance of a general **definition-activation separation pattern** found across many systems. Apache HTTPD uses the same structure (`sites-available` / `sites-enabled`). Systemd uses a similar approach with unit files and symlinks. The pattern provides a clean separation between "what exists" and "what's currently active," enabling safe configuration management without deleting files.

## 1.4 The Nginx Configuration File — Understanding the Two Blocks

The configuration file (`vproapp`) contains two logical sections that work together:

### The `upstream` Block

```nginx
upstream vproapp {
    server app01:8080;
}
```

This defines a **backend server group** named `vproapp`. It tells Nginx: "when I refer to `vproapp`, I mean the server at hostname `app01` on port `8080`." In this stack, `app01` is the Tomcat VM, and `8080` is Tomcat's default HTTP port.

The name `vproapp` is arbitrary — you could name it anything. But it must match exactly between the `upstream` block and the `proxy_pass` directive that references it.

> 🔍 **Deep Dive**
> In a production load-balancing scenario, the `upstream` block would contain **multiple servers** for redundancy and load distribution:
>
> ```nginx
> upstream vproapp {
>     server app01:8080;
>     server app02:8080;
>     server app03:8080;
> }
> ```
>
> Nginx would then distribute requests across all listed servers. In this local project, there's only one Tomcat instance, but the architecture is load-balancer-ready. The instructor notes that load balancing will be covered in detail in the AWS section.

### The `server` Block

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://vproapp;
    }
}
```

This defines how Nginx handles incoming requests:

* **`listen 80`** — Nginx listens on **port 80** (the standard HTTP port). When a user types an IP address in a browser without specifying a port, the browser defaults to port 80 for HTTP.

* **`location /`** — This matches requests to the **root path** (`/`). The `/` means "any request to just the hostname/IP with no additional URL path." The instructor clarifies: "just the hostname, there is no slash any other extra URL after that."

* **`proxy_pass http://vproapp`** — This is the **forwarding directive**. Instead of serving content from local files, Nginx passes the request to the backend defined in the `upstream` block named `vproapp` — which resolves to `app01:8080` (the Tomcat server).

The complete flow: User hits `http://<web01_IP>:80` → Nginx matches `location /` → `proxy_pass` forwards to `http://vproapp` → resolved via `upstream` to `app01:8080` → Tomcat receives and processes the request.

## 1.5 The Default Nginx Configuration — Why We Remove It

Nginx ships with a **default configuration** file that serves a "Welcome to Nginx" placeholder page. This default site occupies port 80. If we leave it in place, it will conflict with our custom `vproapp` configuration (which also listens on port 80), or it may take priority and serve the default page instead of routing to Tomcat.

The solution: **remove the default configuration** from `sites-enabled` before activating our custom configuration. This ensures Nginx only serves our proxy configuration and nothing else.

## 1.6 Symbolic Links (`ln -s`) — The Activation Mechanism

A **symbolic link** (symlink) is a special file that points to another file — like a shortcut. The command `ln -s` creates one. When Nginx reads `sites-enabled/vproapp`, it follows the symlink to `sites-available/vproapp` and reads the actual configuration content from there.

The symlink is the **activation switch**: create it → site is active. Remove it → site is deactivated. The original file in `sites-available` is never touched.

## 1.7 Restart as Activation — Configuration Reload Behavior

After creating the configuration and the symlink, Nginx must be **restarted** to read the new configuration. Nginx does not watch its configuration files for changes in real time — it reads them at startup. A restart (`systemctl restart nginx`) forces Nginx to re-read everything in `sites-enabled/` and apply the new routing rules.

## 1.8 Error Diagnosis Pattern

The instructor identifies the **most common failure mode**: if Nginx fails to restart or shows errors in its status, the cause is almost always a **configuration syntax error** — typically from copy-paste mistakes. The debugging approach:

1. Check `systemctl status nginx` for error messages
2. Open the configuration file (`/etc/nginx/sites-available/vproapp`)
3. Compare line-by-line against the documentation
4. Fix typos, missing semicolons, mismatched braces
5. Restart again

## 1.9 The "Don't Memorize" Principle

The instructor makes a deliberate operational philosophy point: **do not try to memorize all the commands and steps**. This project will be repeated many times throughout the course (in AWS, Docker, Kubernetes, Ansible contexts). Real-world engineers use documentation, Google, and AI tools — they don't carry every command in memory. The goal is **understanding the flow and architecture**, not rote memorization of syntax. Overloading yourself with memorization leads to burnout, not competence.

> ⚠️ **Expert Note**
> This is genuine professional advice. Senior engineers rarely type long commands from memory. They understand **what** needs to happen and **why**, then look up the exact syntax. The value is in the mental model — knowing that Nginx needs an upstream block pointing to Tomcat on 8080, that the config goes in `sites-available` and gets symlinked to `sites-enabled`. The exact `ln -s` syntax is searchable in 5 seconds.

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are setting up **Nginx as a reverse proxy / load balancer** on the `web01` VM — the final service in the V Profile stack. After this setup, a user can hit `web01`'s IP address in a browser, and Nginx will forward the request to the Tomcat application server (`app01:8080`). This completes the entire stack: the user-facing entry point is now connected to the application layer.

## Step 1: SSH into the `web01` VM

```bash
vagrant ssh web01
```

* `vagrant` — Vagrant CLI
* `ssh` — open an SSH session into the specified VM
* `web01` — the VM name defined in the Vagrantfile (the Nginx VM)

Once inside, switch to root:

```bash
sudo -i
```

Clear the screen for readability:

```bash
clear
```

**Connection:** We must be inside `web01` because Nginx is the service assigned to this VM.

## Step 2: Update and Upgrade System Packages

```bash
apt update && apt upgrade -y
```

**Command breakdown:**

* `apt update` — refreshes the package index (checks what updates exist, changes nothing)
* `&&` — **logical AND** — only runs the next command if the previous one succeeded. If `apt update` fails (e.g., no internet), `apt upgrade` won't run, preventing partial/broken upgrades
* `apt upgrade` — applies available updates to installed packages
* `-y` — automatically answers "yes" to all confirmation prompts (non-interactive execution)

**Expected behavior:** The system downloads package lists, then begins upgrading packages. You may encounter **interactive prompts** (the instructor hits these):

* A screen asking about package configuration → **press Spacebar** to select "OK"
* A second prompt → **use Tab** to navigate to "OK", then **press Spacebar**

These prompts appear when upgraded packages need configuration decisions. In manual setup, you handle them interactively. In automated provisioning, they'd need to be pre-answered with flags or configuration.

**How to verify:** Command completes without errors. No "Failed" messages in the output.

**Common mistake:** Forgetting `-y` on `apt upgrade` — the command will hang waiting for confirmation.

## Step 3: Install Nginx

```bash
apt install nginx -y
```

* `apt install` — install a package
* `nginx` — the Nginx web server package
* `-y` — auto-confirm

**Expected output:** Package downloads, installs, and Nginx service starts automatically.

**How to verify:** The command completes with no errors. You can also check:

```bash
systemctl status nginx
```

Should show Nginx as "active (running)."

**Connection:** Nginx is now installed but serving its default "Welcome" page. We need to replace this with our custom proxy configuration.

## Step 4: Explore the Nginx Directory Structure

```bash
ls /etc/nginx
```

**Expected output:** You see multiple files and directories, including:

* `sites-available/` — where configuration files are defined
* `sites-enabled/` — where active configurations are symlinked

This confirms the two-directory pattern described in Theory §1.3.

**Connection:** We'll create our file in `sites-available` and symlink it to `sites-enabled`.

## Step 5: Create the Nginx Configuration File

```bash
vi /etc/nginx/sites-available/vproapp
```

* `vi` — the text editor
* `/etc/nginx/sites-available/vproapp` — the file path; `vproapp` is the configuration file name (arbitrary, but meaningful)

Press `i` to enter **insert mode**, then paste the following content:

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

The instructor formats it with clean spacing for readability.

**Save and quit:** Press `Esc`, then type `:wq` and press `Enter`.

**What each part does** (brief — see Theory §1.4 for full explanation):

* `upstream vproapp` → defines Tomcat backend (`app01:8080`)
* `server` → listens on port 80, forwards all `/` requests to the upstream

**Common mistakes:**

* Missing semicolons after `server app01:8080` or `proxy_pass http://vproapp`
* Mismatched braces (opening `{` without closing `}`)
* Typo in `proxy_pass` or `upstream` name (must match exactly)
* Wrong port number (must be `8080` for Tomcat, `80` for listen)

**Connection:** The configuration file is now *defined* in `sites-available` but not yet *activated*.

## Step 6: Remove the Default Nginx Configuration

```bash
rm /etc/nginx/sites-enabled/default
```

* `rm` — remove a file
* `/etc/nginx/sites-enabled/default` — the symlink to Nginx's default "Welcome" page configuration

**Why:** The default configuration listens on port 80 and serves a placeholder page. It would conflict with our `vproapp` configuration which also uses port 80. Removing it ensures only our proxy configuration is active.

**Connection:** The `sites-enabled` directory is now empty — ready for our custom symlink.

## Step 7: Create a Symbolic Link to Activate the Configuration

```bash
ln -s /etc/nginx/sites-available/vproapp /etc/nginx/sites-enabled/vproapp
```

**Command breakdown:**

* `ln` — create a link
* `-s` — make it a **symbolic** link (shortcut), not a hard link
* `/etc/nginx/sites-available/vproapp` — the **source** (the actual file)
* `/etc/nginx/sites-enabled/vproapp` — the **destination** (where the symlink is created)

**What happens:** A symlink file is created in `sites-enabled/` that points to the actual configuration in `sites-available/`. When Nginx reads `sites-enabled/`, it follows this symlink and loads the `vproapp` configuration.

**How to verify:**

```bash
ls -l /etc/nginx/sites-enabled/
```

Should show: `vproapp -> /etc/nginx/sites-available/vproapp`

**Connection:** The configuration is now defined AND activated. One step remains — telling Nginx to read it.

## Step 8: Restart Nginx

```bash
systemctl restart nginx
```

* `systemctl` — systemd service management command
* `restart` — stop and start the service (forces full configuration reload)
* `nginx` — the service name

**What happens internally:** Nginx process stops, re-reads all configuration from `sites-enabled/`, and starts again with the new routing rules active.

**How to verify success:**

```bash
systemctl status nginx
```

Should show **"active (running)"** with no error messages.

**If there are errors:** The instructor identifies the most likely cause — **configuration syntax errors from copy-paste mistakes**. The fix:

1. Read the error message from `systemctl status nginx`
2. Open the config file: `vi /etc/nginx/sites-available/vproapp`
3. Compare against the documentation line by line
4. Fix any typos, missing semicolons, or mismatched braces
5. Save and restart: `systemctl restart nginx`

**Connection:** With this restart, the entire V Profile stack setup is **complete**. Nginx is now actively listening on port 80 and forwarding requests to Tomcat at `app01:8080`. Validation of the full stack happens in the next lecture.

## Post-Setup: Full Stack Completion Status

After this lecture, all five services are running:

| VM      | Service   | Status                     |
| ------- | --------- | -------------------------- |
| `db01`  | MySQL     | ✅ Running                  |
| `mc01`  | Memcached | ✅ Running                  |
| `rmq01` | RabbitMQ  | ✅ Running                  |
| `app01` | Tomcat    | ✅ Running                  |
| `web01` | Nginx     | ✅ Running (just completed) |

The next lecture validates the complete stack by accessing the web application from a browser.

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Nginx's Position in the Stack

```
USER → Browser → http://<web01_IP>:80
                        │
                        ▼
                 ┌─────────────┐
                 │   NGINX      │  web01
                 │  (port 80)   │
                 └──────┬──────┘
                        │ proxy_pass
                        ▼
                 ┌─────────────┐
                 │   TOMCAT     │  app01
                 │  (port 8080) │
                 └─────────────┘
```

## Configuration Architecture

```
/etc/nginx/
├── sites-available/         ← DEFINE configs here
│   ├── default              ← built-in (REMOVE from sites-enabled)
│   └── vproapp              ← our proxy config (CREATE)
│
└── sites-enabled/           ← ACTIVATE via symlinks
    └── vproapp → ../sites-available/vproapp  (ln -s)

RULE: Nginx reads ONLY sites-enabled/ at startup
```

## Configuration File Structure

```
┌─ upstream vproapp ──────────────┐
│   server app01:8080;            │  ← backend definition
└─────────────────────────────────┘
         ▲
         │ referenced by name
         │
┌─ server ────────────────────────┐
│   listen 80;                    │  ← entry port
│   location / {                  │  ← match root path
│     proxy_pass http://vproapp;  │  ← forward to upstream
│   }                             │
└─────────────────────────────────┘
```

## Command Sequence (Operational Flow)

```
vagrant ssh web01
sudo -i
    │
    ├── apt update && apt upgrade -y        ← refresh + apply system updates
    ├── apt install nginx -y                ← install nginx
    │
    ├── vi /etc/nginx/sites-available/vproapp  ← create proxy config
    │       (upstream + server blocks)
    │
    ├── rm /etc/nginx/sites-enabled/default    ← remove default site
    ├── ln -s .../sites-available/vproapp .../sites-enabled/vproapp  ← activate
    │
    └── systemctl restart nginx             ← apply config
         └── systemctl status nginx         ← verify
```

## `apt update` vs. `apt upgrade`

```
apt update   → CHECK for updates (download index, change nothing)
apt upgrade  → APPLY updates (install newer package versions)
&&           → run upgrade ONLY if update succeeded
-y           → auto-confirm (non-interactive)
```

## Activation Pattern

```
DEFINE           ACTIVATE              APPLY
──────           ────────              ─────
sites-available/ ──ln -s──→ sites-enabled/ ──restart──→ nginx reads config
(file exists)    (symlink)                  (service reloads)
```

**Deactivation:** `rm sites-enabled/vproapp` → restart → site disabled, file preserved.

## Failure → Debug Chain

```
nginx won't restart
    │
    ├── systemctl status nginx → read error message
    │
    └── Most likely: config syntax error
          ├── Missing semicolon
          ├── Mismatched braces { }
          ├── Typo in directive name
          ├── upstream name mismatch (proxy_pass ≠ upstream)
          └── Wrong port number
          │
          └── FIX: vi /etc/nginx/sites-available/vproapp
                    → compare with documentation
                    → fix → save → restart
```

## Transferable Engineering Pattern

**Define → Link → Activate Pattern:**

```
DEFINITION STORE     ACTIVATION STORE       TRIGGER
────────────────     ────────────────       ───────
sites-available/  →  sites-enabled/ (symlink) → restart

Same pattern in:
├── Apache HTTPD:  sites-available/ → sites-enabled/
├── Systemd:       /lib/systemd/ → /etc/systemd/ (symlinks)
├── Kubernetes:    ConfigMap (defined) → Pod mount (activated) → restart
└── Feature flags: config exists → flag enabled → deploy

Core idea: Separate WHAT EXISTS from WHAT IS ACTIVE
           Toggle activation without destroying definitions
```

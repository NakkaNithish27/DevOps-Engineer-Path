*Reconstructed from video lecture captions: "Automated Provisioning — Executing and Validating the Full V Profile Stack"*

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Core Problem: Manual Provisioning Is Broken

Throughout the previous lectures, each service in the V Profile stack — MySQL, Memcached, RabbitMQ, Tomcat, Nginx — was set up **manually** by SSH-ing into each VM, running commands one by one, troubleshooting individually, and verifying each service. The instructor now explicitly names the two fatal problems with this approach: it is **time-consuming** and it is **not repeatable**. "Not repeatable" doesn't mean you can't do it again — it means you can't guarantee the same result every time. A missed command, a typo, a different package version, a skipped configuration step — any of these silently produces a different environment. This is the foundational motivation for everything in this lecture.

## 1.2 Automated Provisioning: What It Actually Means

Automated provisioning is the practice of encoding your entire infrastructure setup — every VM, every package installation, every configuration file, every service start — into **scripts and declarative files** that a tool can execute without human intervention. In this project, that tool is **Vagrant**, and the scripts are **shell scripts** (one per service: `mysql.sh`, etc.) referenced from the **Vagrantfile**.

The critical conceptual shift is this: the human's job is no longer to *execute* the setup — it is to *define* the setup. You write the Vagrantfile and the provisioning scripts once. From that point forward, a single command (`vagrant up`) produces the entire multi-service stack from scratch. The human becomes the architect; Vagrant becomes the executor.

## 1.3 How Vagrant Orchestrates Multi-VM Provisioning

When `vagrant up` is issued in a directory containing a Vagrantfile that defines multiple VMs, Vagrant processes them **sequentially** in the order they are defined. For each VM, the lifecycle is:

1. **Create the VM** — Vagrant instructs VirtualBox (or whichever provider) to create and boot the virtual machine.
2. **Wait for stability** — Vagrant waits for the VM to finish booting and become SSH-accessible. The instructor explicitly observes: "db01 vm is up and running, but our vagrant is waiting for it to become stable."
3. **Execute the provisioning script** — Once the VM is stable, Vagrant SSH-es into it and runs the shell script associated with that VM (e.g., `mysql.sh` for db01). This is the exact same script content that was previously run manually.
4. **Move to the next VM** — Only after provisioning completes for the current VM does Vagrant proceed to create the next one.

The order observed in the video is: **db01 → memcache → rabbitmq → app01 → web01**. This order is not arbitrary — it follows a dependency chain. The database must exist before the application can connect to it. The queuing and caching services must be running before the app tries to use them. The web server (Nginx) must come last because it reverse-proxies to Tomcat (app01).

> 🔍 **Deep Dive**
> The sequential processing is defined by the Vagrantfile's VM declaration order. Vagrant doesn't analyze dependencies between VMs — it simply processes them top-to-bottom. The *engineer* encodes the correct order into the Vagrantfile. This is an important distinction: Vagrant provides the orchestration mechanism, but the dependency logic is the engineer's responsibility.

## 1.4 Provisioning Happens Only Once — The Idempotency Boundary

The instructor highlights a crucial Vagrant behavior: **"vagrant will do provisioning only once when the VMs are created."** This means the shell scripts run only during the initial `vagrant up` that creates the VMs. If you later halt the VMs (`vagrant halt`) and bring them back up (`vagrant up`), Vagrant detects that the VMs already exist and simply **powers them on** — it does **not** re-run the provisioning scripts.

This is Vagrant's built-in distinction between **creation** and **resumption**. The first `vagrant up` = create + provision. Every subsequent `vagrant up` (for already-existing VMs) = power on only. This is why `vagrant halt` is safe — your configured stack is preserved on disk inside the VMs. You're just shutting off the power, not destroying the setup.

> ⚠️ **Expert Note**
> If you need to re-run provisioning on an existing VM (e.g., you updated a script), you must explicitly use `vagrant provision` or `vagrant up --provision`. Without the flag, Vagrant skips provisioning for existing VMs. If you want a completely fresh start, `vagrant destroy` followed by `vagrant up` tears everything down and rebuilds from scratch — that's the true "repeatable" guarantee.

## 1.5 The Validation Model: End-to-End Stack Verification

After all five VMs are provisioned, the instructor validates the entire stack by accessing the **web tier entry point** — the Nginx server on `web01` — from a browser. The access method is either the **static IP address** defined in the Vagrantfile or the **hostname** (`http://web01`). The request flows through the full stack: browser → Nginx (web01) → Tomcat (app01) → backend services (db, rmq, memcache).

The validation sequence tests each backend individually:

* **Login with `admin_vp` / `admin_vp`** — This authenticates against MySQL (db01). If login succeeds, the database is operational and the user/schema provisioned by `mysql.sh` is correct.
* **Click on RabbitMQ** — The application sends a test message through RabbitMQ. If "RMQ is Validated" appears, the queuing service, its user, and its permissions are all functional.
* **Select a user (Memcache test)** — The application queries a user, and the result is inserted into the Memcache cache. If "Data is inserted in cache" appears, both the initial database read and the cache write succeeded.

This is not just a smoke test — it's a **full data-path validation** that exercises every layer of the stack through the actual application. Each validation step implicitly confirms that the corresponding provisioning script ran correctly, the service started, the configuration is right, the credentials match, and the network connectivity between VMs works.

## 1.6 Infrastructure as Code (IaC) — The Architectural Achievement

The instructor closes with three properties of the final system: **automated**, **repeatable**, and **infrastructure as code**. These are not just buzzwords — they represent a fundamental shift from the manual approach:

* **Automated** — No human SSH sessions, no manual command entry. One command triggers everything.
* **Repeatable** — Running `vagrant destroy` then `vagrant up` produces an identical stack every time, because the definition hasn't changed.
* **Infrastructure as Code** — The Vagrantfile and shell scripts *are* the infrastructure. They can be version-controlled (Git), reviewed, shared, and diffed just like application code.

> 🔍 **Deep Dive**
> The source code directory structure the instructor navigates — `source code → vagrant dir → automated provisioning` — implies that the infrastructure code lives *alongside* the application code. This is a deliberate organizational pattern: the infrastructure definition is part of the project repository, not a separate manual runbook. Anyone who clones the repo can bring up the entire stack.

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are executing a **single command** that automatically provisions the entire V Profile application stack — five interconnected VMs (database, memcache, rabbitmq, application server, web server) — and then validating that every layer works end-to-end through the browser. The final outcome: a fully functional multi-tier application running locally, built entirely from code, with zero manual intervention.

## Step 1: Navigate to the Automated Provisioning Directory

Open **Git Bash** and navigate into the project's automated provisioning directory:

```bash
cd <source-code-path>/vagrant/automated_provisioning
```

* **Git Bash** — the terminal environment used throughout this course (provides Unix-like commands on Windows).
* **`<source-code-path>`** — the root of the cloned project repository.
* **`vagrant/automated_provisioning`** — the subdirectory containing the Vagrantfile and all provisioning shell scripts for the automated setup.

**Why this directory matters:** Vagrant looks for a `Vagrantfile` in the current working directory. If you're in the wrong folder, `vagrant up` will either fail or bring up the wrong set of VMs (e.g., the manual provisioning Vagrantfile from earlier lectures).

**Verification:** You can `ls` the directory — you should see the `Vagrantfile` and the `.sh` provisioning scripts (mysql.sh, etc.).

## Step 2: Launch the Entire Stack

```bash
vagrant up
```

* **`vagrant`** — the Vagrant CLI.
* **`up`** — instructs Vagrant to create, boot, and provision all VMs defined in the Vagrantfile.

**What happens internally:** Vagrant reads the Vagrantfile, identifies all VM definitions, and begins processing them sequentially. For each VM, it creates the VM in VirtualBox, waits for SSH readiness, then executes the associated shell provisioning script.

**The provisioning order observed:**

| Order | VM       | Provisioning Script | What It Sets Up                        |
| ----- | -------- | ------------------- | -------------------------------------- |
| 1     | db01     | mysql.sh            | MySQL database + schema + user         |
| 2     | memcache | memcache script     | Memcached caching service              |
| 3     | rmq      | rabbitmq script     | RabbitMQ + Erlang + socat + user/perms |
| 4     | app01    | app script          | Tomcat + application build/deploy      |
| 5     | web01    | nginx script        | Nginx reverse proxy                    |

**Time expectation:** The instructor states the entire process takes **15 to 30 minutes** depending on internet speed. The longest individual steps are the database provisioning (full `yum update` + MySQL setup) and RabbitMQ provisioning (Erlang + socat have many dependencies). The instructor fast-forwards the video through these waits.

**What to watch for during execution:**

* After each VM boots, you'll see Vagrant output: "Machine booted and ready!" followed by the provisioning script output.
* The instructor notes: "db01 vm is up and running, but our vagrant is waiting for it to become stable" — there's a brief pause between VM boot and script execution. This is normal.
* You should see each provisioning script's output scroll by (package installations, service starts, etc.).
* If any script fails, Vagrant will report the error and stop. You'd need to debug the specific script.

**Verification during execution:** Open **VirtualBox** to see VMs appearing as they are created. The instructor checks VirtualBox to confirm machines are being brought up.

**Common failure scenarios:**

* **Wrong directory** — Vagrant can't find the Vagrantfile → navigate to the correct folder.
* **Port conflicts** — Another VM or process is using the same ports → halt conflicting VMs first.
* **Network timeout during provisioning** — Package downloads fail due to slow/unstable internet → `vagrant provision <vmname>` to retry just the provisioning on the failed VM.

## Step 3: Validate the Stack via Browser

Once all five VMs show successful provisioning, open your **browser** and navigate to the web tier:

```
http://web01
```

You can also use the **static IP address** from the Vagrantfile instead of the hostname. The instructor notes: "from vagrantfile, you can get the IP address, that's a static IP, or we can even use the hostname."

**What happens:** The browser sends a request to Nginx (web01), which reverse-proxies it to Tomcat (app01), which serves the V Profile application login page.

**If the page doesn't load:**

* Confirm all VMs are running: `vagrant status`
* Confirm web01's IP or hostname resolves correctly
* Check if Nginx is running inside web01: `vagrant ssh web01` → `systemctl status nginx`

## Step 4: Validate the Database Layer

On the application login page, enter:

* **Username:** `admin_vp`
* **Password:** `admin_vp`

**What this validates:** The application authenticates the credentials against the **MySQL database** on db01. A successful login confirms: MySQL is running, the database schema exists, the application user was created correctly by the provisioning script, and the network path from app01 to db01 is functional.

The instructor confirms: "And we are in, so db is validated."

## Step 5: Validate RabbitMQ

Inside the application, click the **RabbitMQ** test option.

**Expected result:** The page displays "RMQ is Validated."

**What this validates:** The application successfully sent and/or received a message through the RabbitMQ service on the rmq VM. This confirms: RabbitMQ is running, the `test` user and permissions are correctly configured, and the app-to-rmq network connectivity works.

## Step 6: Validate Memcache

Inside the application, **select a user** from the list.

**Expected result:** The page displays "Data is inserted in cache."

**What this validates:** The application queried user data from MySQL, then wrote it into **Memcached**. This confirms: Memcached is running, the application can connect to it, and the cache-write operation succeeded. This is a two-layer validation — it re-confirms DB read capability *and* validates the caching layer.

## Step 7: Manage the Stack Lifecycle

### Halt (Power Off) All VMs

```bash
vagrant halt
```

* **`halt`** — sends a graceful shutdown signal to all VMs. They power off but remain on disk with all their provisioned state intact.

**Verification:**

```bash
vagrant status
```

All VMs should show as "poweroff." The instructor confirms: "All the VMs are powered off."

### Resume the Stack Later

```bash
vagrant up
```

When run against already-existing VMs, this **only powers them on** — it does **not** re-run provisioning scripts. The stack comes back exactly as it was when you halted it. The instructor emphasizes this: "since vagrant will do provisioning only once when the VMs are created, if the VMs already exist and you say vagrant up, it will just bring up all these VMs."

**This is the key operational advantage:** You build the stack once (15–30 min), then halt/resume it in seconds whenever you need it.

> ⚠️ **Expert Note**
> If you need a completely clean rebuild (e.g., you changed a provisioning script), use `vagrant destroy -f` followed by `vagrant up`. The `-f` flag skips confirmation prompts. This destroys all VMs and their disks, then recreates everything from scratch — guaranteeing a fresh, consistent environment.

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## 🏗️ Full Stack Architecture

```
Browser
   │
   ▼
┌─────────┐     ┌─────────┐     ┌─────────┐
│  web01   │────▶│  app01   │────▶│  db01   │
│ (Nginx)  │     │(Tomcat)  │     │(MySQL)  │
└─────────┘     └────┬─┬───┘     └─────────┘
                     │ │
              ┌──────┘ └──────┐
              ▼               ▼
        ┌──────────┐   ┌───────────┐
        │ memcache │   │   rmq     │
        │(Memcached)│   │(RabbitMQ) │
        └──────────┘   └───────────┘
```

## ⚡ The One-Command Execution Model

```
Human action:  cd automated_provisioning → vagrant up
                          │
Vagrant reads Vagrantfile │
                          ▼
        ┌─── db01 ──── create VM → wait stable → run mysql.sh ───── ✓
        │
        ├─── memcache ─ create VM → wait stable → run memcache.sh ─ ✓
        │
        ├─── rmq ───── create VM → wait stable → run rabbitmq.sh ── ✓
        │
        ├─── app01 ─── create VM → wait stable → run app.sh ─────── ✓
        │
        └─── web01 ─── create VM → wait stable → run nginx.sh ───── ✓
                                                                     │
                                                            Stack ready
```

**Per-VM lifecycle:** Create → Boot → Wait for SSH → Execute shell script → Done → Next VM

## 🔁 Vagrant State Machine

```
         vagrant up (first time)
[Non-existent] ──────────────────────▶ [Running + Provisioned]
                                              │
                                      vagrant halt
                                              ▼
                                        [Powered Off]
                                         (state preserved)
                                              │
                                      vagrant up (again)
                                              ▼
                                        [Running]
                                    (NO re-provisioning)
                                              │
                                    vagrant destroy
                                              ▼
                                       [Non-existent]
                                      (clean slate)
```

**Critical rule:** Provisioning = **creation-time only**. Resume = power-on only.

**Override:** `vagrant up --provision` or `vagrant provision` to force re-provisioning.

## ✅ Validation Chain

```
Browser → http://web01
   │
   ├── Login (admin_vp/admin_vp) ──▶ DB validated ✓
   │       (auth hits MySQL on db01)
   │
   ├── Click RabbitMQ ─────────────▶ RMQ validated ✓
   │       (message test through rmq VM)
   │
   └── Select user ────────────────▶ Cache validated ✓
           (read from DB → write to Memcache)
```

**Each validation step confirms:** service running + config correct + credentials valid + network path open.

## 🔧 Operational Commands (Complete Set)

| Command                   | What It Does                       |
| ------------------------- | ---------------------------------- |
| `vagrant up` (first)      | Create all VMs + provision         |
| `vagrant up` (subsequent) | Power on only, no provisioning     |
| `vagrant halt`            | Graceful shutdown, state preserved |
| `vagrant status`          | Show power state of all VMs        |
| `vagrant destroy -f`      | Delete all VMs + disks             |
| `vagrant provision`       | Re-run scripts on existing VMs     |
| `vagrant up --provision`  | Power on + force re-provision      |

## 🧩 Key Mental Anchors

* **One command = entire stack** → `vagrant up` from the correct directory
* **Order matters** → db → cache → queue → app → web (dependency chain encoded in Vagrantfile)
* **15–30 min first time** → internet-dependent (package downloads)
* **Seconds to resume** → halt/up cycle skips provisioning
* **Validation = browser-driven** → single entry point (web01) tests all layers
* **IP or hostname** → both work, defined in Vagrantfile

## 🔁 Transferable Mental Model: The IaC Lifecycle

```
MANUAL WORLD                         IaC WORLD
─────────────                        ─────────
SSH into each VM                     vagrant up
Run commands one by one              Shell scripts run automatically
Hope you didn't miss a step          Scripts are deterministic
Can't share your setup               Vagrantfile + scripts = shareable
Can't rebuild reliably               vagrant destroy + vagrant up = identical rebuild
Time-consuming                       Automated (15-30 min, unattended)
Not repeatable                       Fully repeatable
```

**Core engineering principle:**

> **Define once → Execute infinitely → Destroy and rebuild with confidence**

This pattern transfers directly to: Terraform (cloud infra), Ansible (config management), Docker Compose (container stacks), Kubernetes manifests (orchestration). The tool changes; the principle is identical.

## ⚡ Rapid Recall Trigger

> **"Automated provisioning = cd to right dir → `vagrant up` → Vagrant creates VMs sequentially → runs shell scripts per VM → validate via browser → halt/resume without re-provisioning → destroy for clean rebuild. Manual was slow and unrepeatable; this is IaC."**

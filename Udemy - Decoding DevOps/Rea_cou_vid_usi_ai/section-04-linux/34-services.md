# 🎓 Linux Services — Managing Services with `systemctl` — Deep Learning Material

*Reconstructed from the video lecture on Linux service management using systemctl* [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. What Is a Service — The Concept Behind Background Operations

A **service** in Linux is a program that runs in the background, continuously performing a function without requiring a user to manually execute it each time. When the instructor says "a service is running," what that concretely means is: **there are processes running**. A service is not a single monolithic thing — it is one or more **processes** (running instances of a program) that together deliver a capability. The httpd web service, for example, spawns multiple processes (each with a unique **process ID**), and those processes collectively serve web traffic. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

This means that managing a service — starting it, stopping it, restarting it — is fundamentally about **managing the lifecycle of its underlying processes**. You're telling the system: "launch these processes," "terminate these processes," or "kill and relaunch these processes." The tool that abstracts this process management into clean, human-friendly operations is **`systemctl`**. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

***

## 2. The Relationship Between Packages, Services, and `systemctl`

Before a service can exist, its software must be **installed**. The instructor uses **httpd** (the Apache web server) as the running example. `httpd` is both the **package name** (the software you install via `yum install httpd`) and the **service name** (the background process you manage via `systemctl`). This naming alignment is common but not universal — some packages install services with different names. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

When you install a package like httpd through `yum`, two things happen that are relevant to service management: the **binary/executable** files are installed (the actual program that runs), and a **systemctl configuration file** (a `.service` unit file) is automatically created. This configuration file is what tells `systemctl` *how* to manage the service — how to start it, how to stop it, and with what options. Without this file, `systemctl` cannot manage the service. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

> 🔍 **Deep Dive**
> The instructor explicitly distinguishes two software installation methods and their impact on service management. When you install via `yum` (the package manager), the `.service` unit file is created automatically — service management works immediately. But when you install software by downloading a **tar ball** (a compressed archive), extracting it, and running it manually, **no `.service` file is created**. In that case, you must write your own systemctl configuration file if you want to manage the software as a service. The instructor notes this will be covered in a later lecture.

***

## 3. `systemctl` — The Service Management Command

**`systemctl`** is the single command used to manage services in modern Linux systems. It is the interface between the administrator and the service lifecycle. Every service operation — checking status, starting, stopping, restarting, reloading, enabling, disabling — goes through `systemctl`. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

The core operations are:

**`systemctl status <service>`** — Shows the current state of the service: whether it's **active** (running) or **inactive** (stopped), and lists the process IDs of its running processes. This is your primary diagnostic command. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**`systemctl start <service>`** — Starts the service (launches its processes). The service transitions from inactive to active. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**`systemctl stop <service>`** — Stops the service (terminates its processes). The service transitions from active to inactive. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**`systemctl restart <service>`** — Stops and then starts the service. This is used after making **configuration changes** to the service, so the new configuration takes effect. Restart is a full cycle: processes are killed and relaunched. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**`systemctl reload <service>`** — Reloads the service's configuration **without stopping the service**. The processes remain running but re-read their configuration files. This is a less disruptive alternative to restart — the service never goes down. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

> ⚠️ **Expert Note**
> Not all services support `reload`. Whether reload works depends on the service's binary — the program must be designed to re-read its configuration on signal. If a service doesn't support reload, you must use `restart`. The instructor presents both options but doesn't elaborate on which services support which — in practice, always check the service documentation.

***

## 4. Runtime State vs. Boot-Time State — Two Independent Dimensions

This is the most architecturally important concept in the lecture. A service has **two independent states** that must be managed separately: [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**Runtime state** — Is the service running *right now*? Controlled by `start` / `stop`. This is immediate and temporary. Starting a service makes it active now, but this state **does not survive a reboot**. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**Boot-time state** — Will the service start automatically when the system boots? Controlled by `enable` / `disable`. This is persistent but **does not affect the current runtime**. Enabling a service means it will start on the next boot, but it does **not** start it right now. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

The instructor demonstrates this critical distinction by rebooting the VM. Before reboot, httpd is running (started manually). After reboot, httpd is **inactive** — because it was started but never enabled. The service ran during the session but was not configured to survive a reboot. To make a service both run now AND start on boot, you need **both** `systemctl start` (for now) AND `systemctl enable` (for boot). [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

This two-dimensional state model is the source of a common operational mistake: administrators `enable` a service (thinking it's running) but forget to `start` it. The service won't actually run until the next reboot. Conversely, administrators `start` a service in production but forget to `enable` it — everything works until the server reboots, and then the service is mysteriously down. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

***

## 5. Verification Commands — `is-active` and `is-enabled`

Beyond `systemctl status` (which shows comprehensive information), `systemctl` provides two focused query commands: [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**`systemctl is-active <service>`** — Returns a single word: `active` or `inactive`. This is a quick check for runtime state without the full status output. Useful in scripts where you need a simple yes/no answer. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**`systemctl is-enabled <service>`** — Returns whether the service is configured to start at boot time (`enabled` or `disabled`). This checks the boot-time dimension independently of whether the service is currently running. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

These two commands map directly to the two independent state dimensions: `is-active` checks runtime, `is-enabled` checks boot-time. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

***

## 6. The Service Configuration File — How `systemctl` Knows What to Do

When you run `systemctl start httpd`, how does systemctl know what program to execute, with what options? It reads a **configuration file** — a `.service` unit file. For httpd, this file is located at: [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

```
/etc/systemd/system/multi-user.target.wants/httpd.service
```

This file contains directives that define the service's lifecycle behavior. The instructor specifically points out two key directives visible in the file: **`ExecStart`** — the exact binary path and command-line options that systemctl executes to start the service; and an implied **`ExecStop`** (or kill-based stop) — the command used to stop the service (the instructor mentions a "kill command" used for stopping, which will be covered in the processes lecture). [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

The critical architectural insight: **`systemctl` is not the service itself** — it's a **controller** that reads a configuration file to know how to manage the service. The actual work is done by the binary specified in `ExecStart`. Systemctl is an orchestration layer that translates human commands (`start`, `stop`, `restart`) into the correct binary executions and process management operations. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

> 🔍 **Deep Dive**
> The file path `/etc/systemd/system/multi-user.target.wants/httpd.service` reveals the boot-time mechanism. The `multi-user.target.wants` directory represents a boot target (similar to a "run level"). When you `systemctl enable httpd`, a symbolic link to the httpd.service file is created in this `wants` directory. During boot, systemd reads all `.service` files in the `wants` directories of the active target and starts them. When you `systemctl disable httpd`, the symlink is removed — the service file still exists, but it's no longer referenced by the boot target. This is how enable/disable works without modifying the service file itself.

***

## 7. SSH as a Critical Always-Running Service

The instructor briefly connects this to a service the learner has been using all along: **SSH** (the `sshd` service). Every time you run `vagrant ssh` to connect to the VM, you're relying on the SSH service being active inside the VM. If `sshd` were stopped, SSH connections would fail — you would be locked out of the VM. This demonstrates that services are not abstract concepts — they are the **operational backbone** of a system. Critical services like SSH must be both **running** (active) and **enabled** (start on boot) to ensure continuous access. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Building

We are learning to **manage the complete lifecycle of a Linux service** — installing it, starting/stopping it, surviving reboots, and understanding the configuration that drives it all. The working example is **httpd** (Apache web server). By the end, you can manage any service on a Linux system: check its state, control its runtime, configure its boot behavior, and understand the configuration file behind it. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

***

## Step 1: Install the Service Package

**What we're doing:** Installing the httpd web server package, which also creates the systemctl configuration.

```bash
yum install httpd -y
```

* **`yum`** — the package manager (Red Hat/CentOS)
* **`install`** — action: install a package
* **`httpd`** — the package name (Apache web server)
* **`-y`** — auto-confirm the installation prompt [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**What happens:** If httpd is not installed, yum downloads and installs it. If already installed (as in the demo), it reports "already installed." Upon installation, the httpd binary is placed on the system AND a `.service` configuration file is created at `/etc/systemd/system/multi-user.target.wants/httpd.service`. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**Connection to larger flow:** Without installation, there is no service to manage. The yum installation step creates both the executable and the systemctl configuration file that makes management possible.

***

## Step 2: Check Service Status

**What we're doing:** Verifying the current state of the httpd service.

```bash
systemctl status httpd
```

* **`systemctl`** — the service management command
* **`status`** — action: show current state
* **`httpd`** — the service name [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**Expected output:** `inactive (dead)` — the service is installed but not running. Installation does not automatically start a service.

**How to verify success:** Look for the `Active:` line in the output. It will say `active (running)` or `inactive (dead)`.

***

## Step 3: Start the Service

**What we're doing:** Launching the httpd service (bringing its processes up).

```bash
systemctl start httpd
```

* **`start`** — action: launch the service's processes [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**Verify:**

```bash
systemctl status httpd
```

**Expected output:** `active (running)` — the service is now live. You should also see process IDs listed, confirming that actual processes are running behind the service. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**Important:** This start is **temporary** — it only affects the current runtime session. If the machine reboots, this service will NOT come back up automatically (demonstrated in Step 5).

***

## Step 4: Stop and Restart the Service

**Stopping:**

```bash
systemctl stop httpd
```

Terminates the service's processes. Status returns to `inactive`. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**Restarting (after configuration changes):**

```bash
systemctl restart httpd
```

Stops then starts — full process cycle. Use after modifying service configuration. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**Reloading (less disruptive alternative):**

```bash
systemctl reload httpd
```

Re-reads configuration without stopping processes. Service stays running throughout. Use when you want zero downtime. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**When to use which:** If you made a config change → try `reload` first (no downtime). If reload doesn't pick up the change, or the service doesn't support reload → use `restart`.

***

## Step 5: Demonstrate the Reboot Problem

**What we're doing:** Proving that `start` alone does not survive a reboot.

**Before reboot:** httpd is `active (running)`.

```bash
exit
vagrant reload
```

* **`exit`** — leave the SSH session
* **`vagrant reload`** — reboots the VM from the host machine [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

Alternatively, from inside the VM as root:

```bash
reboot
```

 [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**After reboot, log back in:**

```bash
vagrant ssh
sudo -i
systemctl status httpd
```

**Expected output:** `inactive (dead)` — the service did NOT start on boot because it was never **enabled**. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**This is the most common operational mistake:** starting a service in production but forgetting to enable it. Everything works until the next reboot.

***

## Step 6: Enable the Service for Boot Time

**What we're doing:** Configuring httpd to start automatically on system boot.

```bash
systemctl enable httpd
```

* **`enable`** — action: configure service to start at boot [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**Critical understanding:** `enable` does NOT start the service now. It only sets up the boot-time behavior. After running `enable`, the service is still inactive in the current session.

**You still need to start it for the current session:**

```bash
systemctl start httpd
```

 [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**Now httpd is:** running (started) AND configured to start on boot (enabled). Both dimensions are covered.

***

## Step 7: Quick-Check Commands

**Check if currently running:**

```bash
systemctl is-active httpd
```

**Output:** `active` or `inactive` — single-word answer. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**Check if enabled for boot:**

```bash
systemctl is-enabled httpd
```

**Output:** `enabled` or `disabled` — single-word answer. [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**When to use these vs. `status`:** Use `is-active` / `is-enabled` in scripts or when you need a quick binary answer. Use `status` when you need full diagnostic detail (process IDs, logs, etc.).

***

## Step 8: Examine the Service Configuration File

**What we're doing:** Understanding what systemctl reads to manage the service.

```bash
cat /etc/systemd/system/multi-user.target.wants/httpd.service
```

 [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**What you see:**

* **`ExecStart=`** — the exact binary path and arguments that systemctl executes when you run `systemctl start httpd`. This is the actual program that runs.
* **Stop/Kill directives** — how systemctl terminates the service processes (uses a kill command, covered in the processes lecture). [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**Key insight:** `systemctl start httpd` doesn't do anything magical — it reads this file, finds the `ExecStart` line, and runs that exact command. You're looking at the **source of truth** for service behavior.

**How this file got here:** It was automatically created by `yum install httpd`. If you install software via a tar ball (manual download/extract), this file won't exist — you'll need to create it manually (covered in a later lecture). [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

> ⚠️ **Expert Note**
> The path `multi-user.target.wants` tells you this service is associated with the multi-user boot target. The `enable` command creates a symlink here; `disable` removes it. The actual service definition file may live elsewhere (e.g., `/usr/lib/systemd/system/httpd.service`), with the `wants` directory containing a symlink to it.

***

## Step 9: Verify SSH Service (Context Connection)

**What we're doing:** Checking the service you've been relying on all along.

```bash
systemctl status sshd
```

 [\[34-services \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/34-services.txt)

**Expected output:** `active (running)` and `enabled`. If SSH were stopped, `vagrant ssh` would fail — you'd be locked out of the VM. This demonstrates why critical infrastructure services must be both active and enabled.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Service = Running Processes

```
Service ──▶ one or more PROCESSES (each with a PID)
Managing a service = managing process lifecycle
systemctl = the controller interface for this
```

***

## Package → Service → Configuration Chain

```
yum install httpd
    │
    ├──▶ installs binary (the actual program)
    └──▶ creates .service file (systemctl config)
         └── /etc/systemd/system/multi-user.target.wants/httpd.service
               ├── ExecStart = <binary path + args>   ← how to start
               └── ExecStop / Kill                    ← how to stop

tar ball install → NO .service file created → must write manually
```

***

## systemctl Operations Map

```
RUNTIME (now):                     BOOT-TIME (persistent):
  start   → launch processes         enable  → start on boot
  stop    → kill processes            disable → don't start on boot
  restart → stop + start
  reload  → re-read config (no stop)

QUERY:
  status    → full diagnostic (state + PIDs + logs)
  is-active → "active" / "inactive"  (runtime check)
  is-enabled→ "enabled" / "disabled" (boot check)
```

***

## The Two-Dimensional State Model

```
                  ┌──────────────┬───────────────┐
                  │  NOT enabled │   enabled     │
     ┌────────────┼──────────────┼───────────────┤
     │  stopped   │  ❌ down now  │  ❌ down now   │
     │            │  ❌ no boot   │  ✅ boots up   │
     ├────────────┼──────────────┼───────────────┤
     │  started   │  ✅ up now    │  ✅ up now     │
     │            │  ❌ no boot   │  ✅ boots up   │
     └────────────┴──────────────┴───────────────┘

     SAFE STATE = started + enabled (bottom-right)
     
     Common mistakes:
       enable without start → "why isn't it running?"
       start without enable → works until reboot, then gone
```

***

## Config Change → Apply Flow

```
Make config change
    │
    ├──▶ try: systemctl reload <svc>   (zero downtime, if supported)
    │
    └──▶ fallback: systemctl restart <svc>  (brief downtime, always works)
```

***

## Reboot Survival Test

```
start httpd → status: active
reboot
status httpd → inactive  ← NOT enabled, didn't survive

enable httpd → boot config set
start httpd  → now running
reboot
status httpd → active    ← survived (enabled + was started)
```

***

## systemctl Architecture (Controller Pattern)

```
┌──────────────────────┐
│   Admin (you)        │
│   systemctl start X  │
└──────────┬───────────┘
           │ reads
           ▼
┌──────────────────────────────────────────────┐
│  /etc/systemd/system/.../X.service           │
│  ┌─────────────────────────────────────────┐ │
│  │ ExecStart=/usr/sbin/httpd -DFOREGROUND  │ │
│  │ ExecStop=/bin/kill ...                  │ │
│  └─────────────────────────────────────────┘ │
└──────────┬───────────────────────────────────┘
           │ executes
           ▼
┌──────────────────────┐
│  httpd binary        │
│  PID 1234, 1235 ...  │
│  (actual processes)  │
└──────────────────────┘

systemctl = controller/orchestrator
.service file = configuration/instruction set
binary = the actual worker
```

***

## Critical Service Example: SSH

```
vagrant ssh ──▶ requires sshd service ACTIVE inside VM
sshd stopped → SSH connection fails → locked out
sshd must be: active + enabled (always)
```

***

## Reusable Patterns

```
PATTERN 1: Controller / Configuration / Worker
  systemctl (controller) → reads .service file (config) → runs binary (worker)
  Controller never does the work itself — it delegates based on config
  → Same pattern: Kubernetes→pod specs→containers, Terraform→HCL→cloud resources

PATTERN 2: Runtime vs. Persistent State (Two-Axis Management)
  Immediate action (start/stop) ≠ persistent configuration (enable/disable)
  Must manage BOTH axes independently
  → Same pattern: firewall rules (active vs. saved), cron jobs (running vs. installed)

PATTERN 3: Package Manager as Infrastructure Bootstrapper
  yum install → installs binary + creates management config
  Manual install (tar) → binary only, no management config
  → Managed installation provides full lifecycle; manual requires extra work

PATTERN 4: Graceful vs. Hard Reconfiguration
  reload = graceful (re-read config, no process restart)
  restart = hard (kill + relaunch)
  → Same pattern in web servers (graceful reload), databases (online vs. offline config change)
```

***

This lecture is the gateway to understanding how Linux runs and manages background services — the operational backbone of any server. The two-dimensional state model (runtime × boot-time) is the single most important takeaway; internalizing it prevents the most common production mistakes. The next lecture on **processes** will deepen the understanding of what's actually happening beneath `systemctl`. Ready when you are! 🚀

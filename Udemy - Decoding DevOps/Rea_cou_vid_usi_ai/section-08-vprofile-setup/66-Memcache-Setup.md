**Source:** [66-memcache-setup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/66-memcache-setup.txt?EntityRepresentationId=1bf7df17-fa2e-421f-bd82-bd48216b46ed) — Video lecture on setting up Memcache as part of the vprofile-project multi-service stack.

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 Context — Where Memcache Fits in the vprofile-project Stack

This lecture is part of a series where multiple services are being deployed across **separate virtual machines** to form a working application stack called **vprofile-project**. In previous lectures, a database service (db01) was set up. In this lecture, **Memcache** is set up on a VM called **mc01**. In the next lecture, RabbitMQ will be set up. Eventually, Tomcat (the application server) will connect to all of these backend services.

The word "stack" is explicitly defined by the instructor: **a combination of multiple services working together as a single unit.** Each service runs on its own machine but must communicate with the others over the network. This is the fundamental architecture of real-world distributed applications — separate services, separate machines, networked together.

## 1.2 What Memcache Is and Why It Exists

Memcache (specifically `memcached` — the daemon implementation) is a **caching service**. In the vprofile-project, the application running on Tomcat will connect to Memcache for **database caching** — instead of querying the database for every request, frequently accessed data is stored in Memcache's fast in-memory cache. When Tomcat needs data, it checks Memcache first. If the data is there (a "cache hit"), it avoids the slower database query entirely.

Memcache is not a database. It does not persist data to disk. It holds data **in RAM** for fast retrieval. Its role in the stack is to sit between the application layer (Tomcat) and the database layer, reducing database load and improving response times.

## 1.3 The Local Listening Problem — The Most Important Concept in This Lecture

This is the central engineering lesson the instructor wants you to internalize. It applies far beyond Memcache.

**The default behavior of most network services is to listen only on `127.0.0.1` — the local loopback address.** This means the service will only accept connections originating from the same machine. Any connection attempt from a remote machine (like Tomcat running on a different VM) will be refused.

The instructor explains this with emphasis: every machine refers to itself using `127.0.0.1`. When Memcache starts, it reads its configuration file and sees `OPTIONS -l 127.0.0.1`, which tells it to bind only to the local interface. This is a **deliberate security default** — services ship configured for local-only access because exposing a service to the network without explicit intent is a security risk.

The problem arises in a **multi-machine stack**: Tomcat is on a different VM and needs to connect to Memcache over the network. That is a **remote connection**. If Memcache only listens on 127.0.0.1, Tomcat's connection will fail — even if Memcache is running perfectly, the network is fine, and everything else is correct. The service is simply refusing to listen on the network interface.

The instructor frames this as a general diagnostic rule: **"If a service is not able to connect to a remote service, even though the service is running, everything is fine, network is fine, everything is fine — make sure you check whether it is designed to run remote connection or not."** Most services are not, by default.

## 1.4 The Solution: 0.0.0.0 — Listen on All Interfaces

To allow remote connections, the listening address must be changed from `127.0.0.1` to **`0.0.0.0`**. In networking, `0.0.0.0` means **"all IPv4 addresses"** — the equivalent of a wildcard. Just as `*` means "everything" in Linux file globbing, `0.0.0.0` means "every IPv4 interface on this machine." When Memcache binds to `0.0.0.0`, it listens on all network interfaces — local, private network, bridge network — accepting connections from any source.

The alternative is to specify the **exact IP address** of the machine that needs to connect (e.g., the Tomcat VM's IP). Using `0.0.0.0` is simpler but less restrictive. The instructor chooses `0.0.0.0` for this setup.

🔍 **Deep Dive — Where This Setting Lives:**

Every service has a **configuration file** where it reads its startup settings. For Memcache on CentOS, this file is `/etc/sysconfig/memcached`. The file contains variables — one of which is `OPTIONS` with the `-l 127.0.0.1` flag. The `-l` flag specifies the listen address. The `sed` command is used to change this value without manually opening the file.

⚠️ **Expert Note:** This local-only default is a recurring pattern across nearly every network service — MySQL defaults to local-only, Redis defaults to local-only, MongoDB defaults to local-only. In every multi-machine stack setup, you will encounter this. The diagnostic instinct should be automatic: "remote connection failing despite everything looking fine" → check the listen/bind address in the service's configuration.

## 1.5 The Configuration Change → Restart Rule

The instructor reinforces a rule that has appeared in every previous lecture in this series: **whenever you make a configuration change to a service, you must restart (or reload) that service.** Services read their configuration files at startup and cache the settings in memory. Editing the file on disk does not affect the running process — you must restart the service so it re-reads the configuration from disk. For Memcache: `systemctl restart memcached`.

## 1.6 The Memcached Daemon Command — Port and Background Execution

After the service is configured and restarted, an additional `memcached` command is executed directly. This command tells Memcache to listen on **TCP port 11211** and **UDP port 11111**, run as the `memcached` user (`-u memcached`), and run in the background as a daemon (`-d`).

The instructor explicitly clarifies: **this is a memcached command, not a firewall command.** It configures Memcache's runtime listening behavior — the specific ports on which it accepts connections. Port 11211 is Memcache's standard TCP port.

🔍 **Deep Dive:** The `-d` flag means "daemon mode" — the process detaches from the terminal and runs in the background. This is a common Unix pattern: services meant to run continuously are "daemonized" so they don't block the terminal and persist after the user logs out.

## 1.7 EPEL Repository — Accessing Additional Packages

Before installing Memcache, the `epel-release` package is installed. **EPEL** (Extra Packages for Enterprise Linux) is a supplementary package repository that provides software not included in the default CentOS/RHEL repositories. `memcached` is available through EPEL, not the base CentOS repos. Installing `epel-release` registers this additional repository with the package manager (`dnf`), making the `memcached` package discoverable and installable.

## 1.8 dnf update — Optional but Mentioned

The instructor runs `dnf update -y` at the start, which updates all installed packages to their latest versions. He explicitly notes this is **optional for this project setup** — it takes a long time and makes no functional difference to the Memcache configuration. It is a general good practice but not a requirement for this specific task.

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are setting up **Memcache** (the `memcached` service) on a CentOS VM called **mc01**, which is part of the vprofile-project multi-service stack. The final outcome: Memcache is installed, running, enabled at boot, and **configured to accept remote connections** from the Tomcat application server on a separate VM.

## Step 1: Log Into the Memcache VM

Exit from any other VM you are currently connected to (the instructor exits from db01), then SSH into mc01:

```bash
vagrant ssh mc01
```

* `mc01` — The Vagrant VM name designated for Memcache in the vprofile-project.

Switch to root:

```bash
sudo -i
```

## Step 2: Update System Packages (Optional)

```bash
dnf update -y
```

* `dnf update` — Updates all installed packages to their latest versions.
* `-y` — Auto-confirms all prompts.

The instructor explicitly states: **this is optional and can be skipped** — it does not affect the project setup and takes significant time. He runs it anyway but pauses the recording while it completes.

## Step 3: Install EPEL Repository and Memcached

```bash
dnf install epel-release -y
```

* `epel-release` — Registers the EPEL repository, which contains the `memcached` package not available in base CentOS repos (see Theory §1.7).

```bash
dnf install memcached -y
```

* `memcached` — The Memcache daemon package.

**Verification:** The install should complete without errors, showing "Complete!" at the end.

**Connection to flow:** The package is now installed but the service is not yet running or configured.

## Step 4: Start and Enable Memcached Service

```bash
systemctl start memcached
```

Starts the Memcache service immediately.

```bash
systemctl enable memcached
```

Registers Memcache to start automatically at boot.

**Verification:**

```bash
systemctl status memcached
```

Should show "active (running)."

**Connection to flow:** The service is now running, but it is still listening on `127.0.0.1` only — remote connections from Tomcat will not work yet.

## Step 5: Change Listening Address from Local to All Interfaces (CRITICAL STEP)

This is the most important step in this lecture. Memcache's configuration file currently has `127.0.0.1` as the listen address, which blocks all remote connections (see Theory §1.3).

```bash
sed -i 's/127.0.0.1/0.0.0.0/' /etc/sysconfig/memcached
```

Breaking this down:

* `sed` — Stream editor, used for search and replace in files.
* `-i` — Edit the file in-place (modify the actual file on disk).
* `'s/127.0.0.1/0.0.0.0/'` — Substitute pattern: search for `127.0.0.1`, replace with `0.0.0.0`.
* `/etc/sysconfig/memcached` — Memcache's configuration file on CentOS.

**What happens internally:** The `OPTIONS` line in the configuration file changes from `-l 127.0.0.1` to `-l 0.0.0.0`, telling Memcache to listen on all IPv4 interfaces.

**Verification:**

```bash
cat /etc/sysconfig/memcached
```

Look for the `OPTIONS` line — it should now show `0.0.0.0` instead of `127.0.0.1`.

**Alternative approach:** The instructor mentions you can also open the file manually with `vi /etc/sysconfig/memcached` and make the change by hand.

**Common mistake:** If you skip this step, everything will appear to work locally — Memcache runs, systemctl shows active — but Tomcat on the other VM will fail to connect. The symptom will be confusing because "everything is fine" except the connection. This is the diagnostic trap the instructor warns about.

**Connection to flow:** The configuration file is now changed on disk, but the running Memcache process is still using the old cached configuration. A restart is required.

## Step 6: Restart Memcached to Apply Configuration Change

```bash
systemctl restart memcached
```

Forces Memcache to stop and start again, re-reading the configuration file from disk. After this, Memcache is listening on `0.0.0.0` — accepting remote connections.

## Step 7: Run the Memcached Daemon Command

```bash
memcached -p 11211 -U 11111 -u memcached -d
```

Breaking this down:

* `memcached` — The Memcache binary, invoked directly (not through systemctl).
* `-p 11211` — Listen on **TCP port 11211** (Memcache's standard port).
* `-U 11111` — Listen on **UDP port 11111**.
* `-u memcached` — Run as the `memcached` user.
* `-d` — Run as a **daemon** (background process).

The instructor explicitly clarifies: **this is not a firewall command** — it is a Memcache-specific command configuring its port listening behavior.

**Connection to flow:** Memcache is now fully operational — installed, running, enabled at boot, listening on all interfaces, accepting connections on the correct ports. The setup for this service is complete.

## Step 8: Log Out

```bash
exit
```

Log out from the mc01 VM before proceeding to the next service (RabbitMQ) in the next lecture.

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Stack Position

```
vprofile-project Stack:
    ├── db01   ← Database      (previous lecture)
    ├── mc01   ← Memcache      (THIS LECTURE) — database caching layer
    ├── rmq01  ← RabbitMQ      (next lecture)
    └── app01  ← Tomcat        (later) — connects TO all above
```

## Memcache Setup Flow (6 Steps)

```
1. dnf install epel-release → memcached
2. systemctl start memcached → enable memcached
3. sed: 127.0.0.1 → 0.0.0.0 in /etc/sysconfig/memcached
4. systemctl restart memcached (apply config change)
5. memcached -p 11211 -U 11111 -u memcached -d
6. exit
```

## The Core Lesson — Local vs Remote Listening

```
DEFAULT STATE (most services):
    Config file has: 127.0.0.1 (loopback only)
        │
        └── Service accepts: local connections ONLY
                │
                └── Remote VM (Tomcat) → CONNECTION REFUSED

AFTER FIX:
    Config file has: 0.0.0.0 (all interfaces)
        │
        └── Service accepts: ALL IPv4 connections
                │
                └── Remote VM (Tomcat) → CONNECTION SUCCEEDS
```

## The Diagnostic Trap

```
Symptom: Remote service cannot connect
    ├── Service is running           ✓
    ├── Network is fine              ✓
    ├── Firewall is open             ✓
    ├── Everything looks correct     ✓
    └── BUT listen address = 127.0.0.1  ← ROOT CAUSE

Fix: Check service config → change bind/listen address → restart service
```

## Address Meaning Map

```
127.0.0.1  = "myself only" (loopback, local-only)
0.0.0.0    = "all IPv4 interfaces" (wildcard, accept from anywhere)
<specific IP> = "only from this one source" (targeted access)
```

## Configuration Change Rule

```
Edit config file on disk
    │
    └── Running process still uses OLD cached config
            │
            └── systemctl restart <service>
                    │
                    └── Process re-reads config → NEW settings active
```

## Key File

```
/etc/sysconfig/memcached
    └── OPTIONS line: -l <listen_address>
        ├── Default: 127.0.0.1 (local only)
        └── Changed to: 0.0.0.0 (all interfaces)
```

## Memcached Daemon Command Breakdown

```
memcached -p 11211 -U 11111 -u memcached -d
    │        │         │         │          │
    │        │         │         │          └── daemon (background)
    │        │         │         └── run as memcached user
    │        │         └── UDP port 11111
    │        └── TCP port 11211 (standard)
    └── memcache binary (NOT a firewall command)
```

## Reusable Engineering Patterns

| Pattern                                    | Instance                                                                            |
| ------------------------------------------ | ----------------------------------------------------------------------------------- |
| **Local-only default**                     | Services bind to 127.0.0.1 by default for security; must explicitly open for remote |
| **Config-change → restart**                | Disk changes invisible to running process until restart                             |
| **Supplementary repository**               | EPEL extends base CentOS packages (same concept: PPAs on Ubuntu)                    |
| **Stack = multi-service on multi-machine** | Each service separate VM, connected over network                                    |
| **Wildcard binding**                       | `0.0.0.0` = listen on all interfaces (networking equivalent of `*`)                 |
| **sed for config automation**              | `sed -i 's/old/new/' file` — automated config change without opening editor         |

## One-Line Recall Triggers

* **"What does 127.0.0.1 mean for a service?"** → Local-only; refuses all remote connections
* **"What does 0.0.0.0 mean?"** → All IPv4 interfaces; accepts connections from anywhere
* **"Remote connection fails but everything looks fine?"** → Check listen/bind address in service config
* **"Why EPEL?"** → memcached not in base CentOS repos; EPEL adds it
* **"memcached -p -U -u -d?"** → TCP port, UDP port, run-as user, daemon mode (not a firewall command)
* **"Config file for Memcache on CentOS?"** → `/etc/sysconfig/memcached`

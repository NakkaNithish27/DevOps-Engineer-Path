**Source:** Video lecture caption file — *Validate the Vprofile Stack Setup*

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 What Validation Means in a Multi-Tier Stack

After manually setting up five services across five VMs (MySQL, Memcache, RabbitMQ, Tomcat, Nginx — as covered in the previous lecture), you need to **prove that the entire chain works end-to-end**. Validation isn't just "can I open a web page" — it means systematically confirming that **every service in the dependency chain is reachable, functional, and correctly integrated with its neighbors**.

The Vprofile application was specifically designed with built-in validation checkpoints for each backend service. This is a deliberate architectural choice — the application provides UI elements that exercise each tier individually, so you can isolate which layer is working and which is broken.

## 1.2 HTTP Request Flow and Default Port Behavior

When you type an IP address into a browser (e.g., `192.168.56.11`), the browser automatically prepends `http://` — this is the default protocol. The **default port for HTTP is 80**. You don't need to type `:80` explicitly; the browser assumes it. If you were to type `https://`, the default port changes to **443**.

This directly connects to the Nginx configuration from the previous setup. Nginx was configured to `listen 80;` — meaning it accepts HTTP requests on port 80. When a user's browser connects to the web01 IP address, the request arrives at Nginx on port 80, and Nginx's `proxy_pass` forwards it to Tomcat on `app01:8080`. The user never interacts with Tomcat directly.

> 🔍 **Deep Dive**
> You *can* explicitly specify `http://192.168.56.11:80` in the browser and it works identically to just entering the IP address. The instructor demonstrates this explicitly for understanding purposes — making the implicit default visible. This understanding matters when you're debugging: if Nginx were configured on a non-standard port (say 8080), you'd need to explicitly include `:8080` in the URL.

## 1.3 Layered Validation Strategy

The validation follows the same dependency chain as the architecture, but tested **from the top down** (user perspective). Each successful validation step proves that specific tiers are connected:

**Step 1 — Page loads:** Proves Nginx received the request on port 80 and successfully forwarded it to Tomcat. Also proves the Vprofile application is running inside Tomcat. This single page load validates **three things simultaneously**: Nginx is up, Tomcat is up, and the application is deployed.

**Step 2 — Login succeeds:** The login credentials (`admin_vp` / `admin_vp`) are stored in the **MySQL database** — specifically in the schema that was imported from the `db_backup.sql` dump file during setup. A successful login proves that Tomcat can connect to MySQL, execute queries against the `accounts` database, and authenticate the user. This validates **database connectivity**.

**Step 3 — RabbitMQ button:** The application provides a dedicated button (visible only to the `admin_vp` user) that generates a queue connection to RabbitMQ. If the success message appears, **RabbitMQ connectivity is validated**. If the message doesn't appear, the RabbitMQ connection is broken — you'd need to troubleshoot the RabbitMQ service on `rmq01`.

**Step 4 — Memcache (two-click test):** This is the most nuanced validation. The "All Users" button lists all users from the database. Clicking on a specific user (e.g., "Aejaaz Habeeb") retrieves the user data from MySQL and displays the message: **"data is from db, and data is inserted in cache."** This confirms two things: the database query worked, and the result was written into Memcache. When you go **Back** and click the **same user again**, the data loads noticeably faster and the message changes to indicate it came from **cache**, not the database. This proves Memcache is working — it cached the first query result and served it on the second request without hitting MySQL.

> 🔍 **Deep Dive**
> The Memcache two-click test demonstrates the **cache-aside pattern** (also called lazy-loading). The application doesn't pre-populate the cache. Instead: (1) on first request, it queries MySQL, returns the result to the user, and simultaneously writes it to Memcache; (2) on subsequent requests for the same data, it checks Memcache first — if found (cache hit), it returns the cached data without touching MySQL. The speed difference between the two clicks is the observable proof of caching.

## 1.4 The Credential Source: Database Schema

The login credentials `admin_vp` / `admin_vp` are not hardcoded in the application — they exist in the **database schema** that was imported during MySQL setup using the `db_backup.sql` file. This is a critical conceptual link: the SQL dump file contained not just table structures but also **seed data** including user accounts. If the database import step was skipped or failed during setup, the login would fail — not because of a connectivity issue, but because the data simply doesn't exist.

## 1.5 Understanding Flow vs. Memorizing Commands

The instructor makes a deliberate pedagogical point that forms a core engineering philosophy: **you do not need to memorize setup commands**. What matters is understanding the **flow** — why each command was executed, where it was executed, and what it achieved in the larger system.

Commands are readily available through documentation, Google, ChatGPT, or internal project documents. In real-world work, you'll either have existing setup documentation or need to create it. The instructor emphasizes that knowing **how to set up your project locally** (or in any test environment) is a professional skill — and having documentation with all setup steps stored is standard practice.

The deeper purpose of the manual setup exercise was **not** copy-pasting commands. It was to **train your brain for real-time challenges** — understanding your project's stack so you can troubleshoot, modify, and eventually automate it. Once you understand manual setup, you can move to automation (CI/CD, containerization), but without that foundational understanding, you'll struggle.

## 1.6 The Setup → Validate → Destroy → Automate Lifecycle

The lecture concludes by establishing a clear lifecycle:

1. **Manual setup** — understand every component (previous lecture)
2. **Validate** — prove the stack works end-to-end (this lecture)
3. **Destroy** — clean up the environment (`vagrant destroy --force`)
4. **Automate** — recreate everything automatically without executing a single setup command (next lecture)

This lifecycle is a transferable engineering pattern: you always understand a system manually before automating it. Automation built on top of understanding is reliable; automation built without understanding is fragile.

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Doing

We are **validating the entire Vprofile multi-tier stack** that was manually provisioned across five VMs. The validation proves that all five services (Nginx, Tomcat, MySQL, RabbitMQ, Memcache) are correctly installed, configured, interconnected, and serving the application. After validation, we destroy the environment to prepare for automated provisioning in the next lecture.

## Step 1: Get the Web01 IP Address

**What we are doing:** Finding the Nginx VM's IP address to access the application from the host browser.

Open the **Vagrantfile** and locate the `web01` VM definition. The IP address is on the private network line. In this case: `192.168.56.11`.

Copy this IP address — you'll enter it in the browser.

## Step 2: Access the Application via Browser

**What we are doing:** Sending an HTTP request to Nginx to verify the frontend and reverse proxy are working.

Open a browser on your **host machine** and enter:

```
http://192.168.56.11
```

Or simply enter `192.168.56.11` — the browser automatically adds `http://` and uses port `80`.

You can also explicitly enter `http://192.168.56.11:80` — this is functionally identical but makes the port visible for understanding.

**What happens internally:**

1. Browser sends HTTP request to `192.168.56.11` on port 80
2. Nginx on `web01` receives the request
3. Nginx's `proxy_pass` forwards it to `app01:8080` (Tomcat)
4. Tomcat serves the Vprofile application page
5. The response travels back through Nginx to the browser

**Expected result:** The Vprofile login page loads.

**What this validates:** ✅ Nginx is running and accepting requests on port 80. ✅ Nginx can reach Tomcat (`app01:8080`). ✅ The Vprofile application is deployed and running in Tomcat.

**If the page doesn't load:**

* Verify Nginx is running: `vagrant ssh web01` → `sudo systemctl status nginx`
* Verify Tomcat is running: `vagrant ssh app01` → `sudo systemctl status tomcat`
* Verify `/etc/hosts` on web01 contains the `app01` entry
* Try `ping app01 -c 4` from web01 to test network connectivity
* Check Nginx config: `cat /etc/nginx/sites-enabled/vproapp`

## Step 3: Validate Database Connectivity via Login

**What we are doing:** Logging into the application to prove Tomcat can connect to MySQL and authenticate users.

On the login page, enter:

```
Username: admin_vp
Password: admin_vp
```

These credentials come from the database schema imported via `db_backup.sql` during MySQL setup.

**Expected result:** Successful login — you see the application dashboard (a simple blog-style website).

**What this validates:** ✅ Tomcat can connect to MySQL on `db01:3306`. ✅ The `accounts` database exists and contains user data. ✅ The `admin` user grant and the database import were successful.

**If login fails:**

* Verify MariaDB is running: `vagrant ssh db01` → `sudo systemctl status mariadb`
* Verify the `accounts` database has tables: `mysql -u root -padmin123 accounts` → `show tables;`
* Verify `application.properties` on `app01` has correct `db01` hostname and credentials
* Check firewall on db01: `firewall-cmd --list-ports` (should show `3306/tcp`)

## Step 4: Validate RabbitMQ Connectivity

**What we are doing:** Testing the application's connection to the RabbitMQ message broker.

After logging in as `admin_vp`, locate and click the **RabbitMQ** button on the dashboard.

**Expected result:** A success message indicating the queue connection was established.

**What this validates:** ✅ Tomcat can connect to RabbitMQ on `rmq01:5672`. ✅ The RabbitMQ `test` user and permissions are configured correctly.

**If the message doesn't appear:**

* Verify RabbitMQ is running: `vagrant ssh rmq01` → `sudo systemctl status rabbitmq-server`
* Verify the `test` user exists: `sudo rabbitmqctl list_users`
* Verify `loopback_users` config allows remote access
* Check firewall on rmq01: `firewall-cmd --list-ports` (should show `5672/tcp`)
* Verify `application.properties` on `app01` references `rmq01` correctly

## Step 5: Validate Memcache (Two-Click Cache Test)

**What we are doing:** Proving that Memcache is caching database query results.

This is a **two-part test**:

**Part A — First click (data from DB):**

1. Click **"All Users"** — this lists all users from the MySQL database
2. Click on a specific user (e.g., **"Aejaaz Habeeb"**)
3. Observe the message: **"data is from db, and data is inserted in cache"**

This confirms: the application queried MySQL, retrieved the data, displayed it, and simultaneously wrote it into Memcache.

**Part B — Second click (data from cache):**

1. Click **Back**
2. Click the **same user** again (Aejaaz Habeeb)
3. Observe: the page loads **noticeably faster** and the message indicates data came from **cache**

**What this validates:** ✅ Tomcat can connect to Memcache on `mc01:11211`. ✅ Memcache is accepting write operations (caching data). ✅ Memcache is returning cached data on subsequent requests. ✅ The cache-aside pattern is functioning correctly.

**If the first click shows no data:**

* Database issue — revisit MySQL troubleshooting from Step 3

**If the second click still says "data from db" (not cache):**

* Memcache isn't working — verify it's running: `vagrant ssh mc01` → `sudo systemctl status memcached`
* Verify bind address was changed from `127.0.0.1` to `0.0.0.0` in `/etc/sysconfig/memcached`
* Check firewall: `firewall-cmd --list-ports` (should show `11211/tcp`)
* Verify `application.properties` on `app01` references `mc01` correctly

## Step 6: Validation Complete — All Services Confirmed

At this point, all five services are validated:

| Service  | Validation Method       | Status |
| -------- | ----------------------- | ------ |
| Nginx    | Page loads              | ✅      |
| Tomcat   | Application renders     | ✅      |
| MySQL    | Login succeeds          | ✅      |
| RabbitMQ | Queue connection button | ✅      |
| Memcache | Two-click cache test    | ✅      |

## Step 7: Cleanup — Destroy All VMs

**What we are doing:** Removing all five VMs to free resources, preparing for automated provisioning in the next lecture.

```bash
vagrant destroy --force
```

* **`vagrant destroy`** — deletes all VMs defined in the current Vagrantfile
* **`--force`** — skips confirmation prompts for each VM

This takes some time as each VM is shut down and deleted. After this, you're ready for the next lecture where the same stack is set up **automatically** without executing a single manual setup command.

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Core Identity

```
THIS LECTURE = End-to-end validation of the manually provisioned Vprofile stack
THEN        = Destroy environment → next lecture automates everything
```

## Validation Chain (Top-Down from User Perspective)

```
Browser → http://<web01-IP>:80
   │
   ├─ PAGE LOADS?
   │    YES → ✅ Nginx (web01) + ✅ Tomcat (app01) + ✅ App deployed
   │    NO  → check Nginx, Tomcat, /etc/hosts, network
   │
   ├─ LOGIN SUCCEEDS? (admin_vp / admin_vp)
   │    YES → ✅ MySQL (db01) connectivity + schema imported
   │    NO  → check MariaDB, accounts DB, application.properties, firewall 3306
   │
   ├─ RABBITMQ BUTTON → success message?
   │    YES → ✅ RabbitMQ (rmq01) connectivity
   │    NO  → check rabbitmq-server, test user, loopback_users, firewall 5672
   │
   └─ MEMCACHE TWO-CLICK TEST:
        Click user → "data from db, inserted in cache"
        Click SAME user again → fast load, "data from cache"
           YES → ✅ Memcache (mc01) caching works
           NO  → check memcached, bind 0.0.0.0, firewall 11211
```

## HTTP Default Port Behavior

```
Browser input        → Actual request
─────────────────────────────────────
192.168.56.11        → http://192.168.56.11:80
http://x.x.x.x      → http://x.x.x.x:80
https://x.x.x.x     → https://x.x.x.x:443
```

## Credential Source Chain

```
db_backup.sql → imported into MySQL (accounts DB) → contains admin_vp user
                                                         │
                                        Login page → authenticates against DB
```

## Memcache Validation: Cache-Aside Pattern

```
1st click on user:
   App → query MySQL → return data → display "from db"
                     → write to Memcache → "inserted in cache"

2nd click on SAME user:
   App → check Memcache → HIT → return cached data → display "from cache"
                                 (fast, MySQL not touched)
```

## Full Lifecycle Pattern

```
MANUAL SETUP (understand) → VALIDATE (prove) → DESTROY (clean) → AUTOMATE (next lecture)
     │                          │                    │                    │
  Know every                 Test every         vagrant destroy      No manual commands
  command & why              service tier         --force             needed at all
```

## Troubleshooting Decision Tree (Per Service)

```
Service not validating?
  │
  ├─ Is the service running?     → systemctl status <service>
  ├─ Is the port open?           → firewall-cmd --list-ports
  ├─ Is /etc/hosts correct?      → cat /etc/hosts on source VM
  ├─ Is application.properties   → check hostname + port + credentials
  │   pointing correctly?
  └─ Can VMs reach each other?   → ping <hostname> -c 4
```

## Key Credentials

```
Application login:  admin_vp / admin_vp  (from db_backup.sql)
MySQL root:         root / admin123      (set during mysql_secure_installation)
MySQL app user:     admin / admin123     (created via GRANT)
RabbitMQ user:      test / test          (created via rabbitmqctl)
```

## Instructor's Core Message (Compressed)

```
DON'T memorize commands → UNDERSTAND the flow
Commands are findable   → Flow understanding is not
Manual setup purpose    → Train brain for real-time stack challenges
Know manual first       → Then automate (CI/CD, containers, etc.)
Document your setups    → Standard professional practice
```

## Cleanup Command

```
vagrant destroy --force    → deletes all 5 VMs, no confirmation prompts
```

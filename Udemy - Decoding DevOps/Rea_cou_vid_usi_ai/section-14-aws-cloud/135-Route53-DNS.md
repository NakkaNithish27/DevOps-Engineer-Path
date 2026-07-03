# 🧠 DNS & AWS Route 53 — Private Service Discovery for Cloud Applications

**Source:** *135. DNS Route 53* — vProfile Application Cloud Deployment Series (Video Caption Reconstruction)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Fundamental Problem: Application-to-Backend Service Discovery

The vProfile application runs on an instance called `app01`. It is not a standalone system — it depends on three distinct backend services to function: a **Database** (`db01`), **Memcache** (`mc01`), and **RabbitMQ** (`rmq01`). Every time the application performs an operation — querying data, caching a result, publishing a message — it must establish a network connection to the appropriate backend service.

Here is the foundational truth of networking: **all network connectivity happens through IP addresses**. A hostname like `db01` is a human-readable label — the machine's networking stack cannot use it directly. Somewhere in the resolution chain, that name must be translated into an IP address like `172.31.x.x` before any packet can be sent. The entire lesson addresses one central question: **where and how should this name-to-IP translation happen in a cloud environment?**

The answer to this question is not merely technical — it's an **architectural decision** that determines how resilient, maintainable, and operationally manageable your infrastructure becomes over time.

***

## 1.2 The Application Properties File — Where Service Addresses Are Declared

The vProfile application reads its backend connection information from a specific configuration file located at `SRC/main/resources/application.properties`. Inside this file, you find hostnames — `db01`, `mc01`, `rmq01` — that the application uses at runtime to establish connections to the database, cache, and message queue respectively.

This is a deliberate architectural separation: the **application code** does not contain addresses. It reads them from a **configuration file**. This means you can change where services live without touching a single line of application code — only the configuration or the resolution mechanism needs to change. This separation is the foundation of every maintainable deployment system.

***

## 1.3 Why Hardcoding IP Addresses in Configuration Is Dangerous

The simplest approach would be to put the actual IP addresses of each backend instance directly into `application.properties` — something like `db01=172.31.5.10`. This works initially. The application reads the IP, connects, and everything runs.

The problem reveals itself when **something goes wrong with a backend instance**. In cloud environments, instances are treated as disposable. If a database instance becomes corrupted, unresponsive, or needs upgrading, the standard approach is to **delete it and create a new one**. The new instance will almost certainly receive a **different IP address**. Now the application.properties file points to a dead or incorrect IP. To fix this, you would need to update the properties file with the new IP, rebuild or redeploy the application, and restart it. Every single instance replacement triggers this painful manual cycle.

The instructor's rule is explicit: *"Always remember, in configuration files we should have names, not IP addresses."* Names introduce a **stable reference layer** — the name stays constant while the underlying IP can change. Only the mapping between name and IP needs to be updated, and the application never has to be touched.

> 🔍 **Deep Dive:** This is an instance of the **indirection principle** — one of the most powerful patterns in systems engineering. By inserting a naming layer between consumer (application) and provider (backend service), you decouple the application's configuration lifecycle from the infrastructure's lifecycle. The configuration becomes **stable**, while the infrastructure beneath it remains **fluid and replaceable**. This exact pattern appears in load balancer URLs, Kubernetes service names, service discovery registries (Consul, Eureka), and environment variable-based endpoint configuration.

***

## 1.4 The Local Solution: /etc/hosts — And Its Cloud Limitations

In the local project setup (running vProfile on local VMs), name-to-IP translation was handled through the **`/etc/hosts`** file. This is a static text file on every Linux machine that maps hostnames to IP addresses. When the operating system needs to resolve a name, it checks `/etc/hosts` first (by default) before querying any external DNS server.

The instructor acknowledges that this approach *technically works* in the cloud too — you could SSH into `app01` and add lines like `172.31.5.10 db01`. But he immediately flags it as **not a good or standard practice** for cloud environments.

The core weakness is that `/etc/hosts` is a **per-machine, manually-managed, static file**. It has no centralization — if you have multiple application servers, each needs its own copy. It has no API — you can't update it programmatically through infrastructure automation. It has no integration with cloud lifecycle events — when an instance gets replaced, no one automatically updates the hosts file on other machines. It creates a **manual, fragile, unscalable** name resolution system that becomes increasingly burdensome as the infrastructure grows.

What's needed instead is a **centralized DNS service**: a single authoritative source for name-to-IP mappings that every instance in the network queries automatically.

***

## 1.5 AWS Route 53 — Managed DNS as Infrastructure

AWS provides a fully managed DNS service called **Route 53**. It can do many things — domain registration, internet traffic routing, health checks — but for this project, we use only its most fundamental capability: **hosting DNS records that map names to IP addresses**.

Route 53 organizes DNS records into containers called **hosted zones**. A hosted zone holds all the DNS records for a particular domain (e.g., all records under `vprofile.in`). You create individual records inside the hosted zone, each mapping a specific name to a specific IP address (or another name).

The critical capability for this project: Route 53 supports **private hosted zones** — DNS zones that are only resolvable from within a specific VPC. This gives us exactly what we need: internal, private name resolution without any public internet exposure.

***

## 1.6 Private vs. Public Hosted Zones — The Scope Decision

When creating a hosted zone in Route 53, you must choose its **visibility scope**:

A **public hosted zone** makes DNS records available to the entire internet. Anyone, anywhere, can resolve names in this zone. This is what you use when you want the world to find `www.yourcompany.com`.

A **private hosted zone** makes DNS records available **only within the associated VPC(s)**. Only EC2 instances (and other resources) inside that VPC can resolve these names. Nothing outside the VPC — not the internet, not other VPCs (unless explicitly associated) — can see or query these records.

For vProfile, the choice is **private**. The backend services are internal infrastructure — there is zero reason for the outside world to know or resolve `db01.vprofile.in`. The instructor's reasoning is direct: *"We just need internal resolution, that's all."*

When creating a private hosted zone, you must specify a **Region** and associate it with a **VPC**. The instructor uses **US East (N. Virginia / us-east-1)** and the **default VPC**. This association tells Route 53's internal DNS infrastructure: "inject these records into the DNS resolution path for this VPC, so instances inside it can query them."

> 🔍 **Deep Dive:** The domain name chosen for a private hosted zone (e.g., `vprofile.in`) does **not** need to be a registered, real-world domain. Since it exists only within the VPC's private DNS scope, you could name it `vprofile.internal`, `myapp.corp`, or anything else. The only hard requirement is **consistency**: whatever domain name you choose in Route 53, the same fully-qualified hostnames must appear in `application.properties`. The instructor emphasizes: *"make sure you put that same entry in the application properties file."*

***

## 1.7 DNS Record Types: A Record vs. CNAME

Inside a hosted zone, each DNS record has a **type** that defines what kind of mapping it performs:

**A Record (Address Record)** — Maps a name **directly to an IPv4 address**. This is name-to-IP mapping. When something queries `db01.vprofile.in`, Route 53 returns the IP address `172.31.x.x`, and the connection is made to that IP. This is the most direct, most common record type.

**CNAME Record (Canonical Name)** — Maps a name **to another name**. This is name-to-name mapping. For example, `myservice.vprofile.in → my-load-balancer-1234.elb.amazonaws.com`. DNS first resolves the CNAME to get the target name, then resolves *that* name to get the final IP. The instructor mentions this is useful for things like **load balancer URLs**, where the underlying IPs change frequently but the DNS name remains stable.

For this project, every record is an **A record** — we are mapping backend service hostnames directly to the private IP addresses of specific EC2 instances.

***

## 1.8 Why Private IPs, Not Public IPs

Every EC2 instance in a VPC has a **private IP address** (from the VPC's internal CIDR range, typically `172.31.x.x` for default VPCs). Instances may also have a **public IP** (internet-routable). The instructor repeatedly and emphatically states: use **private IPs** for DNS records, never public IPs.

The reasoning is straightforward: all communication between `app01` and its backend services happens **entirely within the same VPC**. Internal VPC traffic routes through the VPC's internal networking fabric using private IPs — it never touches the internet gateway, it's lower latency, it's more secure, and it's the correct networking path for intra-VPC communication. Putting a public IP in a private DNS record would route traffic through the internet gateway unnecessarily, adding latency, potential cost, and security exposure for what should be a purely internal connection.

> ⚠️ **Expert Note:** In properly architected production environments, backend services like databases, caches, and message queues typically live in **private subnets** with no internet gateway route — meaning they don't even *have* public IPs. Using private IPs in DNS is not just best practice; it's often the only option. Design your network so that internal services are unreachable from the internet by default.

***

## 1.9 DNS Validation — Why Verification Is Operationally Critical

After creating DNS records, the instructor insists on **explicit validation**. This is not optional polish — it's operationally essential. A misconfigured DNS record (wrong name, wrong IP, wrong record type) will cause the application to either **fail to connect** or **connect to the wrong service**. Both failure modes produce confusing symptoms: connection timeouts, authentication errors, or bizarre data corruption — all against what *appears* to be the correct hostname.

Validation operates at two levels:

**Console-level check:** In the Route 53 dashboard, visually confirm that every record shows a **private IP** (172.x.x.x range) and that hostnames are correctly spelled. Confirm no public IPs have accidentally been used.

**Live resolution check:** SSH into an instance *inside the VPC* (specifically `app01`) and use the `ping` command to verify that each hostname resolves to the **correct** private IP. The purpose of ping here is not to test ICMP reachability — it's to observe what IP address the DNS resolver returns for the hostname. The resolved IP must match the private IP of the intended backend instance.

***

## 1.10 The app01 Record — Optional Completeness

The instructor creates a fourth DNS record: `app01.vprofile.in` pointing to app01's private IP. He explicitly states this is **not mandatory** for the project — no service connects *to* app01 by hostname. Users access the application server through a **load balancer**, not directly by DNS name. Nobody is looking up `app01.vprofile.in` to reach the app.

He creates it purely for **completeness** — maintaining a full DNS inventory of all instances in the stack. This is an engineering housekeeping decision: having every instance registered in DNS, even if not currently needed, aids debugging, monitoring, and future architectural changes.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are configuring **AWS Route 53 as a private DNS service** so that the vProfile application on `app01` can reach its three backend services — Database, Memcache, and RabbitMQ — using **stable hostnames** instead of fragile IP addresses. The hostnames in `application.properties` will be resolved by Route 53 within the VPC, completely privately.

**Final outcome:** `app01` reads `db01.vprofile.in` from its config → Route 53 resolves it to `172.31.x.x` (db01's private IP) → the connection is established internally within the VPC. If any backend instance is ever replaced, only the Route 53 record needs updating — not the application.

***

## Step 1: Create a Private Hosted Zone in Route 53

Navigate to **Route 53** in the AWS Console. In the left sidebar, click **Hosted zones**, then click **Create hosted zone**.

**Configuration:**

| Field           | Value                     | Reasoning                                                                                                                                      |
| --------------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Domain name** | `vprofile.in`             | This becomes the parent domain for all records. You can choose any name, but it **must exactly match** what you use in application.properties. |
| **Type**        | **Private hosted zone**   | We need internal-only resolution (see Theory §1.6).                                                                                            |
| **Region**      | **US East (N. Virginia)** | Must match the region where your EC2 instances are running.                                                                                    |
| **VPC**         | **Default VPC**           | Associates this zone with your VPC so instances inside it can query the records.                                                               |

Click **Create hosted zone**.

**What happens internally:** Route 53 creates the zone and injects it into the VPC's DNS resolution pipeline. Two default records are auto-created — **NS** (Name Server) and **SOA** (Start of Authority) — which you should leave untouched. From this point, any instance in the associated VPC that queries `*.vprofile.in` will be served by this zone.

**Verification:** The hosted zone list should now show `vprofile.in` with type **Private**.

**Connection to flow:** The zone is the container. Next, we populate it with the actual name-to-IP records.

***

## Step 2: Collect Private IP Addresses from EC2

Navigate to **EC2 → Instances**. For each of the following backend instances, click on the instance and copy its **Private IPv4 address**:

* `db01` (Database)
* `mc01` (Memcache)
* `rmq01` (RabbitMQ)

⚠️ **Critical:** Copy the **private IP** (typically `172.31.x.x`), **not** the public IP. The instructor warns about this multiple times. Using a public IP would break the architectural intent of private DNS resolution.

**Connection to flow:** These IPs become the values in the A records we create next.

***

## Step 3: Create A Records for Each Backend Service

Go to **Route 53 → Hosted zones → click on `vprofile.in`**. For each service, click **Create record**.

***

### 3a: db01 Record

* **Record name:** `db01` → full name becomes `db01.vprofile.in`
* **Record type:** **A — Routes traffic to an IPv4 address**
* **Value:** Paste the private IP of `db01`

Click **Create record**.

***

### 3b: mc01 Record

* **Record name:** `mc01` → full name becomes `mc01.vprofile.in`
* **Record type:** **A**
* **Value:** Private IP of `mc01`

Click **Create record**.

***

### 3c: rmq01 Record

* **Record name:** `rmq01` → full name becomes `rmq01.vprofile.in`
* **Record type:** **A**
* **Value:** Private IP of `rmq01`

Click **Create record**.

***

### 3d: app01 Record (Optional)

* **Record name:** `app01` → full name becomes `app01.vprofile.in`
* **Record type:** **A**
* **Value:** Private IP of `app01`

Click **Create record**.

This record is **not functionally required** — app01 is accessed through a load balancer, not by DNS name. Created here only for inventory completeness (see Theory §1.10).

***

**⚠️ Instructor's Warning (Repeated Emphasis):** *"Be very careful creating this record. Make sure you're giving the right name and right IP address."* A name/IP mismatch (e.g., putting mc01's IP under db01's name) will cause the application to connect to the **wrong backend** — a failure mode that's extremely difficult to diagnose because DNS resolution technically "succeeds."

**Connection to flow:** The DNS resolution layer is now fully configured. Next, we must ensure the application config matches and then validate.

***

## Step 4: Align application.properties with Route 53

Open the application configuration file at `SRC/main/resources/application.properties`. The hostnames used in this file must be the **exact fully qualified domain names** from Route 53:

| Config Entry  | Must Match          |
| ------------- | ------------------- |
| Database host | `db01.vprofile.in`  |
| Memcache host | `mc01.vprofile.in`  |
| RabbitMQ host | `rmq01.vprofile.in` |

If you used a domain name other than `vprofile.in` when creating the hosted zone, update the properties file accordingly. DNS resolution is **exact-match** — a single character difference means resolution failure.

**Connection to flow:** Config and DNS are now aligned. The final step is proving it actually works.

***

## Step 5: Validate DNS Resolution from Inside the VPC

### 5a: SSH into app01

Get the **public IP** of `app01` from the EC2 console. (This time you need the public IP because you're connecting from your local machine over the internet.)

```bash
ssh ubuntu@<app01-public-ip>
```

**Command breakdown:**

* `ssh` — Secure Shell, establishes an encrypted remote session
* `ubuntu` — the SSH username, because app01 runs an **Ubuntu AMI**
* `@<app01-public-ip>` — the target instance's public address

***

### 5b: Test DNS Resolution with Ping

```bash
ping -c 4 db01.vprofile.in
```

**Command breakdown:**

* `ping` — sends ICMP echo requests; critically for our purpose, it **triggers DNS resolution** and displays the resolved IP in the output
* `-c 4` — send exactly 4 packets then stop (without this flag, Linux ping runs indefinitely)
* `db01.vprofile.in` — the fully qualified domain name to resolve and ping

**Expected output pattern:**

```
PING db01.vprofile.in (172.31.x.x) 56(84) bytes of data.
64 bytes from 172.31.x.x: icmp_seq=1 ttl=64 time=0.5 ms
...
```

**What to verify:** The IP address in parentheses `(172.31.x.x)` **must exactly match** the private IP you assigned to `db01` in Route 53. If it shows a different IP → record value is wrong. If it says "Name or service not known" → record name is wrong, or the hosted zone isn't properly associated with the VPC.

**Repeat for all backend services:**

```bash
ping -c 4 mc01.vprofile.in
ping -c 4 rmq01.vprofile.in
```

Verify each resolves to the correct private IP of its respective instance.

***

### 5c: Console-Level Visual Verification

Back in Route 53 → Hosted zones → `vprofile.in`, scan all records and confirm:

* ✅ All values are **private IPs** (172.x.x.x or 10.x.x.x)
* ✅ **No public IPs** present in any record value
* ✅ Hostnames are correctly spelled (`db01`, `mc01`, `rmq01`)
* ✅ All record types are **A**

***

### Failure Diagnosis Table

| Symptom                                    | Probable Cause                                                                            | Recovery                                                                            |
| ------------------------------------------ | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `ping: Name or service not known`          | Typo in record name, or hosted zone not associated with VPC                               | Fix the record name in Route 53, or re-associate the VPC                            |
| Resolves to unexpected IP                  | IPs swapped between records during creation                                               | Compare each record's IP against EC2 console; delete and recreate incorrect records |
| Resolves to a public IP                    | Pasted public IP instead of private IP when creating the record                           | Delete the record, recreate with the correct private IP                             |
| App connects but gets auth/protocol errors | DNS resolves to wrong backend (e.g., db01 name → mc01's IP)                               | Verify each record's IP individually against EC2                                    |
| Ping works but application still fails     | application.properties hostname doesn't exactly match the Route 53 FQDN                   | Ensure config uses `db01.vprofile.in`, not just `db01`                              |
| Created public zone instead of private     | Records resolve from internet but not from within VPC (or resolve incorrectly inside VPC) | Delete the hosted zone, recreate as **Private** with correct VPC                    |

> ⚠️ **Expert Note:** DNS issues are among the most frustrating to debug because the symptom often appears at the application layer (connection refused, auth failed, timeout) rather than at the DNS layer. When any backend connectivity issue arises, **always verify DNS resolution first** — it eliminates the most common misconfiguration before you start debugging the application or the backend service itself.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      VPC (us-east-1)                        │
│                                                             │
│  ┌──────────┐                                               │
│  │  app01   │──reads──→ application.properties              │
│  │ (Ubuntu) │              │                                │
│  └────┬─────┘              ├─ db01.vprofile.in              │
│       │                    ├─ mc01.vprofile.in              │
│       │                    └─ rmq01.vprofile.in             │
│       │                                                     │
│       ▼  DNS query                                          │
│  ┌─────────────────────────────────────────────┐            │
│  │  Route 53 Private Hosted Zone: vprofile.in  │            │
│  │                                             │            │
│  │  db01   ──A──→  172.31.x.a                  │            │
│  │  mc01   ──A──→  172.31.x.b                  │            │
│  │  rmq01  ──A──→  172.31.x.c                  │            │
│  │  app01  ──A──→  172.31.x.d  (optional)      │            │
│  └─────────────────────────────────────────────┘            │
│       │                                                     │
│       ▼  resolved private IPs                               │
│  ┌─────────┐     ┌─────────┐     ┌──────────┐              │
│  │  db01   │     │  mc01   │     │  rmq01   │              │
│  │  (DB)   │     │ (Cache) │     │  (MQ)    │              │
│  └─────────┘     └─────────┘     └──────────┘              │
│                                                             │
│  [Load Balancer] ──→ app01  (users connect via LB, not DNS)│
└─────────────────────────────────────────────────────────────┘
```

***

## Problem → Solution Chain

```
App needs to reach backend services
  → needs IP addresses for network connectivity
    → hardcoding IPs breaks on instance replacement (new IP)
      → need names in config (stable reference)
        → names must resolve to IPs somewhere
          → /etc/hosts: works but manual, per-machine, unscalable
            → need centralized DNS
              → Route 53 Private Hosted Zone
                → A records: name → private IP
                  → internal resolution, no public exposure
```

***

## Decision Map

| Decision           | Choice                          | Reason                                                     |
| ------------------ | ------------------------------- | ---------------------------------------------------------- |
| Config values      | Names, not IPs                  | Instance replacement changes IPs; names stay stable        |
| Resolution method  | Centralized DNS, not /etc/hosts | Scalable, API-managed, cloud-native vs. manual per-machine |
| Zone type          | Private, not Public             | Internal-only resolution needed                            |
| IP type in records | Private IP, not Public          | Intra-VPC traffic; no internet routing                     |
| Record type        | A record, not CNAME             | Direct name→IP for EC2 instances                           |
| app01 record       | Created, but optional           | No service resolves app01 by name (LB used instead)        |
| Domain name        | `vprofile.in`                   | Arbitrary; must match application.properties exactly       |

***

## Execution Sequence (Compressed)

```
1. Route 53 → Create Hosted Zone
     domain: vprofile.in │ type: Private │ region: us-east-1 │ VPC: default

2. EC2 Console → Copy private IPs
     db01, mc01, rmq01 (+ app01 optional)

3. Route 53 → vprofile.in → Create A Records ×4
     db01.vprofile.in  → private IP of db01
     mc01.vprofile.in  → private IP of mc01
     rmq01.vprofile.in → private IP of rmq01
     app01.vprofile.in → private IP of app01  [optional]

4. application.properties → Ensure FQDNs match:
     db01.vprofile.in, mc01.vprofile.in, rmq01.vprofile.in

5. Validate from inside VPC:
     ssh ubuntu@<app01-public-ip>
     ping -c 4 db01.vprofile.in   → verify resolved IP = db01's private IP
     ping -c 4 mc01.vprofile.in   → verify resolved IP = mc01's private IP
     ping -c 4 rmq01.vprofile.in  → verify resolved IP = rmq01's private IP
```

***

## Record Type Quick Reference

```
A Record     :  NAME  →  IP ADDRESS       (direct mapping)
CNAME Record :  NAME  →  ANOTHER NAME     (alias, e.g., to load balancer URL)
```

***

## Failure Signature Index

```
"Name or service not known"       → record missing / typo / zone not linked to VPC
Resolves to wrong IP              → IPs swapped between records
Resolves to public IP             → wrong IP pasted (public instead of private)
App auth/protocol error           → name resolves to wrong backend service
App fails, ping works             → application.properties FQDN mismatch with Route 53
```

***

## Reusable Engineering Pattern: Stable Indirection Layer

```
PROBLEM:
  Consumer (app) depends on Provider (backend)
  Provider's address is UNSTABLE (cloud instance → replaceable → new IP)

PATTERN:
  Insert a NAMING LAYER between Consumer and Provider
  Consumer references a STABLE NAME
  Naming layer maps NAME → CURRENT ADDRESS

EFFECT:
  Consumer config is IMMUTABLE
  Only the naming layer updates when Provider changes

WHERE THIS PATTERN APPEARS:
  • DNS (this lesson)
  • Load Balancers (stable URL → rotating backends)
  • Kubernetes Services (service name → ephemeral pod IPs)
  • Service Discovery (Consul, Eureka)
  • Environment variables → endpoint URLs
  • Config servers (Spring Cloud Config, etc.)

CORE INSIGHT:
  Stability for the consumer.
  Flexibility for the infrastructure.
  Decoupling through indirection.
```

***

## Validation Logic (Compressed)

```
LEVEL 1 — Console visual check:
  All records → private IPs only (172.x.x.x / 10.x.x.x)
  All names → correctly spelled
  Zone type → Private

LEVEL 2 — Live resolution from inside VPC:
  SSH into app01 (Ubuntu AMI → username: ubuntu)
  ping -c 4 <hostname>.vprofile.in
  Check: resolved IP in output == private IP from EC2 console
  Repeat for each backend service
```

***

## One-Line Mental Reload Trigger

> *"Names in config, Route 53 private zone resolves them to private IPs via A records, validate with ping from inside the VPC."*

This single sentence reconstructs the entire architecture, every decision, and the validation strategy. [\[135. DNS Route 53 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/135.%20DNS%20Route%2053.txt)

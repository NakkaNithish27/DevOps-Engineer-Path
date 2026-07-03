# Setting Up Cloud DNS (Private Hosted Zone) — Deep Learning Material

**Source:** [296-setting-up-cloud-dns.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt?EntityRepresentationId=1a2792d6-137a-4745-af68-ef444a11dc43) (VTT Caption File) [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Problem — Why DNS Is Needed Here

The vprofile application has backend services already deployed: a **Cloud SQL** instance (MySQL) and a **Memorystore** instance (Memcached). The application server, which will be placed in a **private subnet**, needs to connect to both of these services. The connection configuration lives in the application's source code at `src/main/resources/application.properties`, where hostnames are used as endpoints — one for MySQL, one for Memcached. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

Here is the core problem: these hostnames in the configuration file need to **resolve to the actual private IP addresses** of the Cloud SQL and Memorystore instances. The application doesn't use raw IP addresses — it uses symbolic names. Something must translate those names into IP addresses. That something is **DNS**. And because all of this traffic is internal (private subnet to private services), we need **internal DNS resolution** — not public DNS that the internet can see. This is why we create a **private hosted zone**. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## 1.2 Private Hosted Zone — Internal DNS Resolution

A **hosted zone** in Google Cloud DNS is a container for DNS records belonging to a single domain. It defines how DNS queries for that domain are answered. Hosted zones come in two visibility types: **public** (resolvable from the internet) and **private** (resolvable only within specified VPC networks). [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

Since our DNS entries are purely for internal service-to-service communication within the VPC — the app server reaching Cloud SQL and Memorystore — we only need **private** visibility. No external user or system needs to resolve these names. The private hosted zone is scoped to a specific **VPC network**, meaning only resources inside that VPC can query and resolve names in this zone. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

In this lecture, two identifiers define the zone:

* **Zone name**: `vprofile-private` — this is the administrative identifier used in `gcloud` commands to reference the zone. It is stored in the variable `private_zone`.
* **Domain name (DNS name)**: `vprofile.internal` — this is the actual DNS domain under which records are created. It is stored in the variable `private_dns`.

These are distinct concepts: the zone name is how **you** (the operator) refer to the zone in commands; the DNS name is how **the system** (DNS resolvers) identifies the domain namespace. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

Under this domain, two DNS records are created:

* `db.vprofile.internal` → private IP of Cloud SQL
* `mc.vprofile.internal` → private IP of Memorystore

When the application's configuration references these hostnames, the private DNS resolver within the VPC translates them into the correct private IPs. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

> 🔍 **Deep Dive**
> The domain `.internal` is a deliberate naming choice. It signals that this domain is not intended for public resolution — it exists only within the private network. This is a common convention in infrastructure design: use non-routable or reserved-style domain suffixes for internal services to clearly separate internal DNS namespaces from public ones. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## 1.3 A Records — Name-to-IP Mapping

The DNS records being created are **A records**. An A record is the most fundamental DNS record type — it maps a **hostname to an IPv4 address**. When you say "db.vprofile.internal is an A record pointing to 10.x.x.x," you are telling the DNS system: whenever anyone asks "what is the IP address of db.vprofile.internal?", respond with that specific IP address. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

The instructor explicitly states: *"It's a record because the name maps to the IP address."* This is the defining characteristic of A records — direct hostname-to-IP translation. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## 1.4 Transaction-Based DNS Record Management

Google Cloud DNS uses a **transaction model** for modifying DNS record sets. You do not directly insert records into the zone. Instead, the process follows a strict three-step sequence: **start → add → execute**. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

**How it works internally:**

1. **Start transaction** — This creates a local file called `transaction.yaml` in your **current working directory**. This file is a local staging area — nothing has changed on Google Cloud yet.

2. **Add record(s)** — This writes the DNS record information (hostname, IP, record type) into the `transaction.yaml` file. Again, nothing has changed on Google Cloud. You are only modifying the local YAML file.

3. **Execute transaction** — This **uploads** the `transaction.yaml` file to Cloud DNS, which processes it and adds the records to the zone. Only at this step do the records actually appear in the hosted zone.

This is a **batch-commit model**: you stage changes locally, then commit them to the remote system in a single operation. The advantage is atomicity — you can add multiple records to a transaction before executing, and they all apply together. In this lecture, each record (DB and MC) is handled in its own separate transaction cycle, but the mechanism supports batching. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

After execution, the status initially shows as **"pending"** — the record has been submitted but DNS propagation within the zone takes a brief moment. Listing the records afterward confirms the entries are active. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

> 🔍 **Deep Dive**
> The transaction model imposes a constraint: you cannot start a new transaction while one is already in progress (the `transaction.yaml` file would conflict). Each transaction must be either executed or aborted before starting the next. This is why the lecture runs a complete start→add→execute cycle for the DB record before beginning a new cycle for the MC record. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## 1.5 Extracting Values from GCP Describe Commands

To create DNS records, you first need the **private IP addresses** of the target services. The lecture demonstrates a powerful GCP pattern for extracting specific values from service descriptions using the `--format` flag. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

When you run `gcloud sql instances describe <instance-name>` without formatting, you get a **large YAML output** containing all metadata about the instance. The IP address is buried inside this output, within a nested structure: `ipAddresses` is a top-level key containing a list, and the first element (index `[0]`) of that list has a key called `ipAddress`. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

The `--format` flag with the `value()` function lets you extract exactly the field you need:

```
--format="value(ipAddresses[0].ipAddress)"
```

This returns **only** the IP address as plain text — no YAML wrapper, no extra metadata. The instructor emphasizes that if you understand JSON/YAML structure, you can extract any value from any describe command using this pattern. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

The extracted IPs are stored in shell variables using **command substitution** (`$(command)`):

* `DB_IP` — stores the Cloud SQL private IP
* `MC_IP` — stores the Memorystore private IP

These variables are then referenced in the transaction add commands, making the workflow dynamic rather than hardcoded. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## 1.6 Architectural Context — Where DNS Fits

The overall system architecture at this point: [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

* **Backend services**: Cloud SQL (MySQL) and Memorystore (Memcached) — already provisioned.
* **Application code**: `application.properties` references hostnames for DB and cache endpoints.
* **Private hosted zone** (this lecture): Creates the DNS layer that translates those hostnames into private IPs.
* **App server** (next lecture): Will be deployed in the private subnet, will use these DNS names to connect to backend services.

DNS is the **glue layer** between the application's hostname-based configuration and the infrastructure's IP-based addressing. Without this DNS setup, the app server would fail to connect to its backends because the hostnames would not resolve. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating a **private hosted zone** in Google Cloud DNS with the domain `vprofile.internal`, and adding two **A records** that map application-level hostnames to the private IP addresses of Cloud SQL and Memorystore. This enables the vprofile application (to be deployed next) to resolve backend service names internally within the VPC. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

**Final outcome:** Two DNS entries — `db.vprofile.internal` → Cloud SQL IP, and `mc.vprofile.internal` → Memorystore IP — resolvable only from within the VPC.

***

## Variables Used Throughout

Before beginning, note the two variables the lecture references:

| Variable       | Value               | Purpose                                              |
| -------------- | ------------------- | ---------------------------------------------------- |
| `private_dns`  | `vprofile.internal` | The domain name of the hosted zone                   |
| `private_zone` | `vprofile-private`  | The administrative zone name used in gcloud commands |

These are referenced in commands below using `$private_dns` and `$private_zone` notation. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## Step 1: Create the Private Hosted Zone

Run the following command:

```bash
gcloud dns managed-zones create vprofile-private \
  --dns-name=vprofile.internal \
  --networks=vpc \
  --visibility=private \
  --description="private DNS for vprofile"
```

**Command breakdown:**

| Part                                       | Meaning                                                                                                    |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| `gcloud dns managed-zones create`          | Creates a new managed DNS zone in Cloud DNS                                                                |
| `vprofile-private`                         | The zone name (administrative identifier, stored as `$private_zone`)                                       |
| `--dns-name=vprofile.internal`             | The actual DNS domain this zone manages (stored as `$private_dns`)                                         |
| `--networks=vpc`                           | The VPC network to which this zone is attached — only resources in this VPC can resolve names in this zone |
| `--visibility=private`                     | Makes this a private hosted zone — not visible on the public internet                                      |
| `--description="private DNS for vprofile"` | Human-readable description                                                                                 |

**Expected result:** The zone is created. No DNS records exist yet (beyond default SOA and NS records). [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

**Verification:** Navigate to **Cloud DNS** in the Google Cloud Console. You should see a zone named `vprofile-private` with DNS name `vprofile.internal`. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

**Key operational detail:** The `--visibility=private` flag is what makes this an internal-only zone. Without it (or with `--visibility=public`), the domain would be resolvable from the internet, which is unnecessary and a security exposure for internal service names. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## Step 2: Retrieve the Private IP Addresses

Before adding DNS records, we need the private IP addresses of both backend services.

### 2a: Get the Cloud SQL Private IP

Run the describe command with formatting:

```bash
gcloud sql instances describe <db-instance-name> \
  --format="value(ipAddresses[0].ipAddress)"
```

**Command breakdown:**

| Part                                         | Meaning                                                       |
| -------------------------------------------- | ------------------------------------------------------------- |
| `gcloud sql instances describe`              | Retrieves full metadata for the specified Cloud SQL instance  |
| `<db-instance-name>`                         | The name of your Cloud SQL instance                           |
| `--format="value(ipAddresses[0].ipAddress)"` | Extracts only the IP address from the nested output structure |

**Without the `--format` flag:** You would see a large YAML output with all instance metadata. The IP address is nested inside the `ipAddresses` list as the first element's `ipAddress` key. The format flag drills into this path and returns only the value. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

**Store it in a variable:**

```bash
DB_IP=$(gcloud sql instances describe <db-instance-name> --format="value(ipAddresses[0].ipAddress)")
```

**Verify:**

```bash
echo $DB_IP
```

This should print the private IP address of your Cloud SQL instance. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

### 2b: Get the Memorystore Private IP

Use a similar command for Memorystore (the exact describe command follows the same pattern for Memorystore/Memcached instances):

```bash
MC_IP=$(gcloud ... describe <memcache-instance-name> --format="value(...)")
```

**Verify:**

```bash
echo $MC_IP
```

This should print the private IP of your Memorystore instance. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

> 🔍 **Deep Dive**
> The `--format="value(...)"` extraction pattern is a general-purpose GCP technique. For any `gcloud ... describe` command, you can navigate the output's JSON/YAML structure using dot notation and array indexing. If you know the structure of the output (visible from running describe without formatting), you can extract any nested value. This is a reusable skill across all GCP services. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## Step 3: Add the Database DNS Record (Transaction Cycle 1)

This follows the three-step transaction model: **start → add → execute**.

### 3a: Start the Transaction

```bash
gcloud dns record-sets transaction start \
  --zone=vprofile-private \
  --project=<project-id>
```

| Part                                       | Meaning                                                          |
| ------------------------------------------ | ---------------------------------------------------------------- |
| `gcloud dns record-sets transaction start` | Initiates a DNS transaction — creates `transaction.yaml` locally |
| `--zone=vprofile-private`                  | Specifies which hosted zone this transaction applies to          |
| `--project=<project-id>`                   | Your GCP project ID                                              |

**Expected result:** A file called `transaction.yaml` appears in your **current working directory**. Nothing has changed on Cloud DNS yet. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

### 3b: Add the DB Record

```bash
gcloud dns record-sets transaction add $DB_IP \
  --name=db.vprofile.internal \
  --type=A \
  --zone=vprofile-private \
  --project=<project-id>
```

| Part                          | Meaning                                                            |
| ----------------------------- | ------------------------------------------------------------------ |
| `transaction add $DB_IP`      | Adds a record mapping to the IP stored in `$DB_IP`                 |
| `--name=db.vprofile.internal` | The fully qualified hostname being created (`db` + `$private_dns`) |
| `--type=A`                    | A record — maps hostname to IPv4 address                           |
| `--zone=vprofile-private`     | The target zone                                                    |
| `--project=<project-id>`      | Your GCP project ID                                                |

**Expected result:** The `transaction.yaml` file is updated with the new record entry. Still, **nothing has changed on Cloud DNS**. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

### 3c: Execute the Transaction

```bash
gcloud dns record-sets transaction execute \
  --zone=vprofile-private \
  --project=<project-id>
```

**Expected result:** The `transaction.yaml` file is uploaded to Cloud DNS. The output shows status: **"pending"** — the record is being propagated within the zone. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

### 3d: Verify

```bash
gcloud dns record-sets list --zone=vprofile-private
```

**Expected output:** You should see the default records (SOA, NS) plus the new entry: `db.vprofile.internal` with its A record pointing to the Cloud SQL private IP. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## Step 4: Add the Memcache DNS Record (Transaction Cycle 2)

Repeat the same three-step cycle with modified values for Memorystore.

### 4a: Start Transaction

```bash
gcloud dns record-sets transaction start \
  --zone=vprofile-private \
  --project=<project-id>
```

### 4b: Add the MC Record

```bash
gcloud dns record-sets transaction add $MC_IP \
  --name=mc.vprofile.internal \
  --type=A \
  --zone=vprofile-private \
  --project=<project-id>
```

The only differences from Step 3b: `$MC_IP` instead of `$DB_IP`, and `mc.vprofile.internal` instead of `db.vprofile.internal`. The instructor notes you can use the **up arrow** to recall the previous command and change just these two values. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

### 4c: Execute Transaction

```bash
gcloud dns record-sets transaction execute \
  --zone=vprofile-private \
  --project=<project-id>
```

**Expected result:** Status "pending" again. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

### 4d: Verify

```bash
gcloud dns record-sets list --zone=vprofile-private
```

**Expected output:** Both entries now visible — `db.vprofile.internal` and `mc.vprofile.internal` — each with their respective A record IPs. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

**GUI Verification:** Navigate to **Cloud DNS → vprofile-private zone** in the Google Cloud Console. Refresh the page. Both A records should be visible with their hostnames and IP addresses. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## What Comes Next

The DNS glue layer is now in place. In the next lecture, the **app server** will be deployed in the private subnet. Its `application.properties` configuration will use `db.vprofile.internal` and `mc.vprofile.internal` as endpoints, and the private DNS zone will resolve them to the correct backend service IPs. [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
Cloud DNS Private Hosted Zone = Internal name resolution layer
  Purpose: Translate application hostnames → backend service private IPs
  Scope: VPC-internal only (visibility=private)
```

 [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## Why It Exists

```
application.properties uses HOSTNAMES (db01, mc01, etc.)
Backend services have PRIVATE IPs (dynamic, infrastructure-assigned)

Gap: hostname ≠ IP → resolution needed
Solution: Private DNS zone → A records → hostname→IP mapping
Scope: Internal only → private visibility → VPC-bound
```

 [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## Zone vs Domain (Two Identifiers)

```
Zone Name (administrative):  vprofile-private   ($private_zone)  ← used in gcloud commands
DNS Name (domain):           vprofile.internal   ($private_dns)   ← used in hostname resolution

Zone name ≠ Domain name — distinct purposes
```

 [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## DNS Records Created

```
db.vprofile.internal  ──A record──►  Cloud SQL private IP    ($DB_IP)
mc.vprofile.internal  ──A record──►  Memorystore private IP  ($MC_IP)

A record = hostname → IPv4 address mapping
```

 [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## Transaction Model (Core Mechanism)

```
START ──► creates transaction.yaml (local file, nothing on cloud)
  │
ADD   ──► updates transaction.yaml with record entry (still local)
  │
EXECUTE ──► uploads transaction.yaml to Cloud DNS (records applied, status: pending)
  │
LIST  ──► verify records are active

Constraint: must complete (execute) one transaction before starting another
```

 [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## IP Extraction Pattern

```
gcloud <service> describe <name>
  └── without --format: huge YAML output
  └── with --format="value(path[index].key)": extracts single value

Cloud SQL IP path: ipAddresses[0].ipAddress

Store: VAR=$(gcloud ... --format="value(...)")
Verify: echo $VAR
```

 [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## Full Command Sequence

```
1. CREATE ZONE
   gcloud dns managed-zones create $private_zone \
     --dns-name=$private_dns --networks=vpc \
     --visibility=private --description="..."

2. GET IPs
   DB_IP=$(gcloud sql instances describe <name> --format="value(ipAddresses[0].ipAddress)")
   MC_IP=$(gcloud ... describe <name> --format="value(...)")

3. DB RECORD (transaction cycle 1)
   start  → transaction.yaml created
   add    → $DB_IP, --name=db.$private_dns, --type=A
   execute → uploaded, status: pending
   list   → verify

4. MC RECORD (transaction cycle 2)
   start  → transaction.yaml created
   add    → $MC_IP, --name=mc.$private_dns, --type=A
   execute → uploaded, status: pending
   list   → verify (both records visible)
```

 [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## Architecture Position

```
Cloud SQL (MySQL)  ◄──private IP──  db.vprofile.internal  ◄──DNS──┐
                                                                   │
Memorystore (MC)   ◄──private IP──  mc.vprofile.internal  ◄──DNS──┤
                                                                   │
                                         Private Hosted Zone       │
                                         (vprofile-private)        │
                                         domain: vprofile.internal │
                                         VPC-scoped                │
                                                                   │
                               App Server (private subnet) ────────┘
                               application.properties uses hostnames
                               [NEXT LECTURE]
```

 [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

## Reusable Engineering Patterns

**DNS as Abstraction Layer (Service Discovery Pattern)**

```
Application code → uses hostnames (stable, human-readable)
Infrastructure   → uses IPs (dynamic, machine-assigned)
DNS              → bridges the gap (hostname→IP translation)

Benefit: Application config never changes when IPs change
         Only DNS records need updating
Recurrence: Service meshes, Kubernetes Services, Route53, internal DNS everywhere
```

**Transaction-Based State Mutation Pattern**

```
Stage locally → commit remotely
  Local file (transaction.yaml) = staging area
  Execute = atomic commit to remote system

Benefit: review before apply, batch changes, atomicity
Recurrence: Terraform plan/apply, git staging/commit, database transactions
```

**Describe-and-Extract Pattern (GCP)**

```
gcloud <service> describe <name> → full metadata (YAML/JSON)
  + --format="value(path)" → extract single value

Reusable across ALL GCP services
Key skill: understand output structure → extract any field
```

 [\[296-settin...-cloud-dns \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/296-setting-up-cloud-dns.txt)

***

This completes the full reconstruction of the Cloud DNS lecture. **Theory** explains the why and how of private DNS, **Practical** walks through every command with full breakdown, and the **Compression Map** enables rapid future recall of the architecture, flow, and patterns. Let me know if you'd like any adjustments! 🚀

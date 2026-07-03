# 🧠 Amazon ElastiCache (Memcached) — Managed Caching Layer for Cloud Applications

**Source:** *143. ElastiCache* — vProfile Application Cloud Refactoring Series (Video Caption Reconstruction)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Why the Application Needs a Caching Layer

The vProfile application connects to a MySQL database for persistent data. But hitting the database for every single query — especially repeated, identical queries — is inefficient. A **cache** sits between the application and the database, storing the results of frequently executed queries in memory. When the same query comes again, the application retrieves the result from the fast in-memory cache instead of making a round trip to the database. This dramatically reduces database load and improves response times.

The caching technology chosen for vProfile is **Memcached** — a simple, high-performance, distributed in-memory key-value store specifically designed for caching database query results. The video explicitly states: Memcached will "cache DB query" for the vProfile application.

***

## 1.2 Amazon ElastiCache — The Managed Caching Service

Rather than installing and managing Memcached manually on an EC2 instance, the vProfile project uses **Amazon ElastiCache** — AWS's fully managed caching service. ElastiCache handles the operational burden of running a cache cluster: provisioning, patching, monitoring, failure detection, and recovery.

ElastiCache supports **three cache engines**: **Memcached**, **Valkey**, and **Redis**. Each engine has different capabilities — Redis and Valkey offer richer data structures, persistence, and replication, while Memcached is simpler and focused purely on high-speed key-value caching. For vProfile, we use **Memcached** because that's what the application is configured to connect to.

> 🔍 **Deep Dive:** The choice between cache engines is not arbitrary — it depends on the application's code. The vProfile application's `application.properties` file specifies Memcached connectivity (host, port 11211). The application code uses Memcached client libraries. Choosing Redis or Valkey here would require application-level changes because the protocols and client libraries are different. The infrastructure choice must align with the application's expectations.

***

## 1.3 The Pre-Requisite Resource Pattern: Parameter Group and Subnet Group

Before creating the actual Memcached cache, two supporting resources must be created first: a **Parameter Group** and a **Subnet Group**. The instructor explicitly notes this is the **same pattern as RDS** — the database service also required these two pre-requisites before the main resource could be created.

This is a recurring AWS resource creation pattern: managed services that run inside your VPC and have tunable configurations require you to define *where they run* (subnet group) and *how they're configured* (parameter group) as separate, reusable objects before you create the main resource.

### Parameter Group

A Parameter Group is a **named collection of configuration settings** for the cache engine. It defines the operational behavior of Memcached — things like memory allocation policies, connection limits, timeout values, and other engine-specific tuning parameters. When you create a parameter group, you select a **family** (e.g., `memcached1.6`) which determines which version of the engine's configuration options are available. After creation, you can see and modify the available options as requirements evolve.

The key concept: the parameter group **decouples configuration from the cache instance itself**. You define configuration once in a named group, then attach it to one or more cache clusters. If you need to change a setting, you modify the parameter group — you don't have to recreate the cache.

### Subnet Group

A Subnet Group is a **named collection of subnets** within a VPC where the cache nodes can be placed. It tells ElastiCache: "these are the network locations where you're allowed to deploy cache nodes." Since the project uses the **default VPC** with its **default subnets**, the subnet group simply collects all available subnets in that VPC.

The subnet group serves the same architectural purpose as it does in RDS — it defines the **network boundary** for the managed service within your VPC, controlling which availability zones the service can span.

> 🔍 **Deep Dive:** This pre-requisite pattern (parameter group + subnet group → main resource) exists because AWS separates **configuration concerns** from **networking concerns** from the **compute resource itself**. This separation allows you to reuse parameter groups across multiple clusters, change network placement without reconfiguring the engine, and version-control configuration independently. It's a manifestation of the **separation of concerns** principle applied to infrastructure management.

***

## 1.4 Deployment Models: Serverless vs. Node-Based Cluster

When creating a Memcached cache in ElastiCache, AWS offers two fundamentally different deployment options:

**Serverless** — You simply provide a name and accept default settings. AWS manages everything: capacity, scaling, node management. It's the simplest path — "as simple as it is," as the instructor says. You don't choose instance types, node counts, or availability zone placements.

**Node-based cluster** — You explicitly choose the instance type, number of nodes, placement, and all configuration details. This gives you full control over the infrastructure, cost, and architecture.

The instructor deliberately chooses **Node-based cluster** to expose all the configuration options for learning purposes. Within node-based, there's a further choice: **Easy create** (which selects recommended best practices automatically) vs. **Cluster cache** (where you manually select every option). The instructor selects **Cluster cache** for maximum visibility into all settings.

> ⚠️ **Expert Note:** In production, the choice between Serverless and Node-based depends on your workload predictability and cost model. Serverless is ideal for variable or unpredictable loads where you want AWS to handle scaling. Node-based is better when you have predictable load patterns and want precise cost control. For learning, node-based with manual options is essential to understand what decisions exist.

***

## 1.5 Port Alignment — The Configuration Contract Between Application and Infrastructure

The Memcached default port is **11211**. This port appears in two places that **must match**: the ElastiCache cluster configuration and the application's `application.properties` file.

The instructor navigates to the GitHub repository (`hkhcoder`, branch `awsrefactor`) and opens `src/main/resources/application.properties` to verify this alignment. The file shows:

* Database port: **3306** (MySQL default, kept default in RDS)
* Memcached port: **11211**
* RabbitMQ port: **5671** (specific to the refactor branch)

This is the **configuration contract**: the infrastructure service must listen on the same port the application expects to connect to. A mismatch here means the application's connection attempts will fail — it will send packets to a port where nothing is listening (or where a different service is listening).

> 🔍 **Deep Dive:** The fact that the instructor checks the application.properties file mid-creation is significant. It demonstrates a critical operational habit: **always verify the application's expectations before configuring infrastructure**. The infrastructure doesn't define the port — the application does. The infrastructure must conform to what the application expects, not the other way around. This is especially important in the refactor branch where ports might differ from other branches (e.g., RabbitMQ is 5671 here, not the more common 5672).

***

## 1.6 Location: AWS Cloud vs. On-Premise Management

The creation form includes a **Location** setting with the option of **AWS Cloud** or managing an **on-premise** ElastiCache/Memcached from the AWS console. The instructor keeps **AWS Cloud** since the entire vProfile stack is cloud-based. The on-premise option exists for hybrid architectures where you want AWS management capabilities applied to caching infrastructure running in your own data center, but it's not relevant to this project.

***

## 1.7 Node Type and Sizing — Cost-Conscious Infrastructure Selection

For the cache node type, the instructor searches for **t3** instances and selects **t3.micro** — the smallest available option with **0.5 GB of RAM**. For a learning/development project, this is sufficient. The number of nodes is set to **1** (single node).

With a single node, the **Availability Zone placement** becomes irrelevant — the instructor selects "no preference" because there's only one node to place, so zone distribution doesn't apply. This would matter in a multi-node cluster where you'd want nodes spread across zones for fault tolerance.

***

## 1.8 Encryption in Transit — Why It Must Be Disabled

A critical configuration step: the instructor explicitly says to **uncheck "Encryption in transit."** The reason is direct — the vProfile application **does not have encryption in transit configured for Memcached by default**. If you enable encryption on the ElastiCache side but the application doesn't use TLS when connecting, the connection will fail. The application sends unencrypted Memcached protocol traffic; the cache node would expect TLS-wrapped traffic; the handshake never completes.

This is another instance of the configuration contract: **infrastructure security settings must match application capabilities**. Enabling a security feature on the infrastructure side without the corresponding application-side support doesn't improve security — it breaks connectivity.

> ⚠️ **Expert Note:** In production, you would ideally enable encryption in transit and update the application to use TLS connections to Memcached. Running unencrypted cache traffic means any data flowing between the app and cache (which may include sensitive query results) is visible to anything that can observe the network. For a learning project this is acceptable; for production with sensitive data, it's a security gap to address.

***

## 1.9 Security Group Association — The Backend Security Boundary

The cache cluster must be associated with a **security group** that controls which traffic can reach it. The instructor selects **`vprofile-backend-sg`** — the same security group used for other backend services. This is consistent with the vProfile architecture: all backend services (database, cache, message queue) share a common backend security group that allows traffic from the application tier while blocking unauthorized access.

This is the same security group association pattern seen with RDS — backend services are grouped into a common security boundary, and the application tier's security group is allowed to communicate with the backend group.

***

## 1.10 Engine Version Compatibility

The instructor selects engine version **1.6.22** and notes that "anything 1.6 is fine." This aligns with the parameter group family chosen earlier (`memcached1.6`). The parameter group family and the engine version must be compatible — a `memcached1.6` parameter group works with any 1.6.x engine version. If you chose a parameter group family of a different major version, it wouldn't be compatible with the cluster's engine.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are creating a **managed Memcached caching layer** using Amazon ElastiCache for the vProfile application. This cache will sit between the application and the MySQL database (RDS), storing frequently queried data in memory. The application connects to this cache on port **11211** using the hostname/endpoint provided by ElastiCache.

**Final outcome:** A running Memcached node accessible from within the VPC, on the correct port, with the correct security group, ready for the application to connect and cache database queries.

***

## Step 1: Create a Parameter Group

Navigate to **ElastiCache** in the AWS Console (search for "ElastiCache"). In the left sidebar, click **Parameter Groups**, then click **Create parameter group**.

**Configuration:**

| Field           | Value                           | Purpose                                                             |
| --------------- | ------------------------------- | ------------------------------------------------------------------- |
| **Name**        | `vprofile-rearch-cache-paragrp` | Identifiable name following the project naming convention           |
| **Description** | `vprofile-rearch-cache-paragrp` | Same as name (or any descriptive text)                              |
| **Family**      | `memcached1.6`                  | Must match the engine version you'll select for the cluster (1.6.x) |

Click **Create**.

**Verification:** After creation, your parameter group appears in the list. Clicking on it reveals all configurable Memcached options — these can be tuned later as operational requirements change.

**Connection to flow:** This parameter group will be selected when creating the cache cluster. It defines *how* Memcached behaves.

***

## Step 2: Create a Subnet Group

In the ElastiCache left sidebar, click **Subnet Groups**, then click **Create subnet group**.

**Configuration:**

| Field           | Value                            | Purpose                                     |
| --------------- | -------------------------------- | ------------------------------------------- |
| **Name**        | `vprofile-rearch-cache-subgrp`   | Identifiable name for the subnet collection |
| **Description** | `vprofile-rearch-cache-subgrp`   | Same as name                                |
| **VPC**         | **Default VPC**                  | The VPC where all vProfile instances run    |
| **Subnets**     | Keep defaults (already selected) | All default subnets in the default VPC      |

The subnets should already be pre-selected. If you need to change them, click **Manage** to add or remove specific subnets. For this project, keep the defaults.

Click **Create**.

**Connection to flow:** This subnet group will be selected when creating the cache cluster. It defines *where* (which subnets/AZs) ElastiCache can place cache nodes.

***

## Step 3: Create the Memcached Cache Cluster

Navigate back to **Memcached caches** in the ElastiCache sidebar. Click **Create Memcached cache**.

This is the main resource creation — walk through each section carefully.

***

### 3a: Select Cache Engine and Deployment Type

* **Cache engine:** Ensure **Memcached** is selected (not Valkey or Redis).
* **Deployment option:** Select **Node-based cluster** (not Serverless — we want full control over options).
* **Creation method:** Select **Cluster cache** (not Easy create — we want to configure all options manually).

***

### 3b: Cluster Settings

| Field               | Value                                  | Reasoning                                                                                   |
| ------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Location**        | **AWS Cloud**                          | All vProfile resources are cloud-hosted. The on-premise option is for hybrid architectures. |
| **Cluster name**    | `vprofile-rearch-cache`                | Follows project naming convention                                                           |
| **Engine version**  | `1.6.22`                               | Compatible with the `memcached1.6` parameter group family. Any 1.6.x works.                 |
| **Port**            | `11211`                                | **Must match** the port in `application.properties`. Default Memcached port.                |
| **Parameter group** | Select `vprofile-rearch-cache-paragrp` | The parameter group created in Step 1                                                       |

**Port verification (important):** The instructor navigates to the GitHub repository (`hkhcoder`, branch `awsrefactor`) → `src/main/resources/application.properties` to confirm the application expects Memcached on port **11211**. The same file shows MySQL on 3306 and RabbitMQ on 5671. Always verify your infrastructure port matches the application's expected port.

***

### 3c: Node Configuration

| Field               | Value            | Reasoning                                                                                                 |
| ------------------- | ---------------- | --------------------------------------------------------------------------------------------------------- |
| **Node type**       | `cache.t3.micro` | Smallest available (0.5 GB RAM). Type `t3` in the search to find it quickly. Sufficient for dev/learning. |
| **Number of nodes** | `1`              | Single node — no replication needed for this project                                                      |

***

### 3d: Connectivity

| Field                           | Value                                 | Reasoning                                                           |
| ------------------------------- | ------------------------------------- | ------------------------------------------------------------------- |
| **Subnet group**                | Select `vprofile-rearch-cache-subgrp` | The subnet group created in Step 2. Choose "existing subnet group." |
| **Availability Zone placement** | **No preference**                     | With a single node, zone selection doesn't affect fault tolerance   |

Click **Next**.

***

### 3e: Security Settings (Critical Step)

| Field                     | Value                                                        | Reasoning                                                                                                                                |
| ------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Encryption in transit** | ⚠️ **UNCHECK this**                                          | The vProfile application does NOT support TLS for Memcached connections. Leaving this enabled will break connectivity. (See Theory §1.8) |
| **Security group**        | Click **Manage** → select `vprofile-backend-sg` → **Choose** | The backend security group that allows application-tier traffic to reach backend services                                                |

**This is the most common mistake in this step.** If encryption in transit is left enabled (checked by default), the application will fail to connect to the cache because it sends unencrypted traffic while the cache expects TLS.

***

### 3f: Maintenance and Tagging

| Field                  | Value                                                               |
| ---------------------- | ------------------------------------------------------------------- |
| **Maintenance window** | **No preference** (acceptable for dev/learning)                     |
| **Tag**                | Click **Add new tag** → Key: `Name`, Value: `vprofile-rearch-cache` |

Click **Next**.

***

### 3g: Review and Create

The review screen shows all configured options. **Verify these critical fields:**

* ✅ Engine version: `1.6.22`
* ✅ Port: `11211`
* ✅ Node type: `cache.t3.micro`
* ✅ Encryption in transit: **Disabled**
* ✅ Security group: `vprofile-backend-sg`

If anything is wrong, click **Edit** next to that section to correct it.

Click **Create**.

**What happens next:** ElastiCache begins provisioning the Memcached node. This process takes several minutes. The status will transition from "Creating" to "Available" when ready. The instructor notes: *"This is going to take some time to create."*

***

### Common Mistakes and Failure Scenarios

| Mistake                                                            | Symptom                                                                      | Fix                                                         |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Encryption in transit left **enabled**                             | Application connection to cache times out or fails with TLS handshake errors | Edit cluster settings → disable encryption in transit       |
| Wrong port (not 11211)                                             | Application can't connect — connection refused                               | Recreate with correct port or update application config     |
| Wrong security group                                               | Connection timeout from app to cache                                         | Update security group to `vprofile-backend-sg`              |
| Parameter group family mismatch (e.g., 1.4 family with 1.6 engine) | Creation may fail or behave unexpectedly                                     | Ensure parameter group family matches engine major version  |
| Selected public subnet or wrong VPC                                | Cache node unreachable from app instances                                    | Verify subnet group uses the same VPC as your EC2 instances |
| Selected large node type (e.g., r6g.large)                         | Unnecessary cost                                                             | Delete and recreate with `cache.t3.micro`                   |

> ⚠️ **Expert Note:** After the cluster becomes "Available," the ElastiCache console will provide a **cluster endpoint** (hostname and port). This endpoint is what you'll eventually configure in the application's properties or in Route 53 (if using DNS for service discovery). The endpoint hostname is auto-generated by AWS — it's not the friendly name you gave the cluster.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Position

```
vProfile App (app01)
    │
    ├──→ MySQL (RDS)           — port 3306
    ├──→ Memcached (ElastiCache) — port 11211  ← THIS LECTURE
    └──→ RabbitMQ (Amazon MQ)  — port 5671
```

***

## Resource Creation Dependency Chain

```
Parameter Group (memcached1.6)
        │
Subnet Group (default VPC, default subnets)
        │
        ▼
Memcached Cache Cluster
  ├── uses Parameter Group (config behavior)
  ├── uses Subnet Group (network placement)
  ├── uses Security Group: vprofile-backend-sg (access control)
  └── listens on port 11211
```

**Same pattern as RDS:** Parameter Group + Subnet Group → Main Resource

***

## Creation Flow (Compressed)

```
1. ElastiCache → Parameter Groups → Create
     name: vprofile-rearch-cache-paragrp
     family: memcached1.6

2. ElastiCache → Subnet Groups → Create
     name: vprofile-rearch-cache-subgrp
     VPC: default │ subnets: default (keep as-is)

3. ElastiCache → Memcached Caches → Create
     engine: Memcached │ deploy: Node-based → Cluster cache
     name: vprofile-rearch-cache
     version: 1.6.22 │ port: 11211
     param group: vprofile-rearch-cache-paragrp
     node: cache.t3.micro × 1
     subnet group: vprofile-rearch-cache-subgrp
     AZ: no preference
     ⚠️ encryption in transit: UNCHECK
     security group: vprofile-backend-sg
     tag: Name = vprofile-rearch-cache
     → Review → Create → Wait for "Available"
```

***

## Decision Map

| Decision              | Choice                              | Reason                                       |
| --------------------- | ----------------------------------- | -------------------------------------------- |
| Cache engine          | Memcached (not Redis/Valkey)        | App is coded for Memcached                   |
| Deployment model      | Node-based cluster (not Serverless) | Full control, learning visibility            |
| Creation method       | Cluster cache (not Easy create)     | Manual option selection for learning         |
| Location              | AWS Cloud (not On-premise)          | Entire stack is cloud-native                 |
| Engine version        | 1.6.22                              | Compatible with memcached1.6 parameter group |
| Port                  | 11211                               | Matches application.properties               |
| Node type             | cache.t3.micro                      | Smallest/cheapest; sufficient for dev        |
| Node count            | 1                                   | Single node; no HA needed for learning       |
| AZ placement          | No preference                       | Irrelevant with single node                  |
| Encryption in transit | **Disabled**                        | App doesn't support TLS for Memcached        |
| Security group        | vprofile-backend-sg                 | Shared backend security boundary             |

***

## Configuration Contract (Port Alignment)

```
application.properties          ElastiCache Cluster
─────────────────────          ────────────────────
MySQL:      3306         ←→    RDS:          3306
Memcached:  11211        ←→    ElastiCache:  11211   ← must match
RabbitMQ:   5671         ←→    Amazon MQ:    5671

Source: GitHub hkhcoder / branch: awsrefactor
Path:   src/main/resources/application.properties
```

***

## Critical Failure Point

```
⚠️ ENCRYPTION IN TRANSIT

  ElastiCache default: ENABLED
  vProfile app default: NO TLS for Memcached

  If left enabled:
    App sends plain Memcached protocol → Cache expects TLS → HANDSHAKE FAILS → CONNECTION REFUSED

  Action: UNCHECK encryption in transit during creation
```

***

## Reusable Engineering Pattern: AWS Managed Service Pre-Requisite Chain

```
PATTERN (observed in both RDS and ElastiCache):

  Step 1: Create PARAMETER GROUP   → defines HOW the service behaves (config)
  Step 2: Create SUBNET GROUP      → defines WHERE the service runs (network)
  Step 3: Create MAIN RESOURCE     → references both groups + security group

  WHY:
    Config (parameter group) is reusable across clusters
    Network (subnet group) is reusable across clusters
    Security (security group) is reusable across services
    → Each concern is independently managed and versioned

  WHERE ELSE THIS APPLIES:
    • RDS (same pattern — already seen)
    • Any AWS managed service running inside a VPC with tunable config
```

***

## Reusable Pattern: Infrastructure-Application Configuration Contract

```
PATTERN:
  Application declares: "I will connect to HOST on PORT using PROTOCOL"
  Infrastructure must provide: matching HOST, PORT, and PROTOCOL capability

  MISMATCH CONSEQUENCES:
    Wrong port        → connection refused
    Wrong host        → timeout or wrong service
    TLS mismatch      → handshake failure
    Wrong engine      → protocol error

  RULE:
    Read application.properties FIRST → then configure infrastructure to match
    Infrastructure conforms to application expectations, not the reverse
```

***

## Failure Signature Index

```
Connection timeout to cache     → wrong security group OR encryption mismatch
Connection refused              → wrong port OR node not yet "Available"
TLS handshake failure           → encryption in transit enabled, app doesn't use TLS
Cache miss / no caching         → wrong endpoint configured in app
High cost / billing surprise    → wrong node type (too large)
Parameter group incompatible    → family version doesn't match engine version
```

***

## One-Line Mental Reload Trigger

> *"ElastiCache Memcached: parameter group (1.6) + subnet group (default VPC) → node-based cluster on port 11211, t3.micro ×1, encryption OFF, backend-sg — same pre-requisite pattern as RDS."*

This single sentence reconstructs the entire resource chain, all critical settings, and the architectural pattern. [\[143-elastic-cache \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/143-elastic-cache.txt)

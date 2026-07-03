# 🎓 Deep Learning Material: GCP Project Architecture Overview — VPC, Backend Services, and Load Balancer Flow

**Source:** [289-project-architecture-overview.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt?EntityRepresentationId=bd85ec1b-d9ef-4cf0-89fc-96896f7287dc) (video caption) + three attached architecture diagrams — Video lecture providing a complete architectural overview of a vProfile application deployment on Google Cloud Platform (GCP), covering VPC with public/private subnets, PSA + VPC Peering for managed backend services (Cloud SQL, Memorystore), a Layer 7 HTTPS/HTTP load balancer with managed instance groups, certificate termination, URL maps, and the full request flow from internet to application. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Four-Part Architecture

The entire project deployment on GCP is structured into four sequential parts, each building on the previous. Understanding this sequence is essential because it mirrors the dependency chain — you cannot configure the frontend until the backend exists, and the backend requires the VPC. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

**Part 1 — VPC:** Create the Virtual Private Cloud with four subnets (two public, two private), a bastion host in the public subnet, Cloud NAT + Cloud Router for outbound internet access from private subnets, and Cloud Firewall rules.

**Part 2 — Backend Services:** Create Cloud SQL (MySQL) and Memorystore (Memcache) as managed services. These live in a **separate network** (service producer network) and connect to your VPC via PSA + VPC Peering. This gives your private instances access to these databases and caches securely.

**Part 3 & 4 — Frontend (Load Balancer):** Configure the HTTPS termination (certificate, target HTTPS proxy, URL map), HTTP redirect, backend service with a managed instance group (auto-scaling), health checks, and static public IP. This is where internet traffic enters and gets routed to the application instances in the private subnet.

 [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

***

## 1.2 GCP VPC Architecture — The Foundation

The VPC in this project contains **four subnets**: two public and two private, spread across availability zones. The architecture diagram shows:

* **Public Subnet 1:** Contains the **bastion host** — the only instance directly reachable from the internet. It serves as a jump server to access private instances. Cloud Firewall Rules control what traffic can reach the bastion host from the internet. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

* **Private Subnet 1:** Contains the **private instance** (the vProfile application server). Cloud Firewall Rules control traffic between the bastion host and the private instance. This instance is NOT directly reachable from the internet.

* **Public Subnet 2** and **Private Subnet 2:** Additional subnets for redundancy across availability zones.

* **Cloud NAT + Cloud Router:** Positioned to provide **outbound** internet access for private subnet instances. Private instances cannot receive inbound traffic from the internet, but they can initiate outbound connections (e.g., downloading packages, updates) through Cloud NAT. The Cloud Router manages the routing logic for the NAT gateway.

This mirrors the AWS VPC architecture (public subnets with internet gateway, private subnets with NAT gateway) but uses GCP-specific components (Cloud NAT, Cloud Router, Cloud Firewall Rules instead of security groups). [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

***

## 1.3 PSA + VPC Peering — The GCP-Specific Backend Connection Pattern

This is the most architecturally significant concept in the lecture and represents a **fundamental difference** between GCP and AWS.

In AWS, when you create a managed service like RDS (database) or ActiveMQ (message broker), you can place it directly in your VPC's private subnet. The managed service gets a private IP within your VPC's CIDR range, and your instances access it directly over the private network. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

**GCP works differently.** Managed services like Cloud SQL and Memorystore do NOT live in your VPC. They live in a **service producer network** — a separate, Google-managed network. Your VPC and the service producer network are two completely separate networks. To connect them, you must configure **PSA (Private Service Access) + VPC Peering**. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

PSA is essentially a **private connection** between your VPC and the service producer network. You create an IP range for these services and peer it with your VPC. Once peering is established, your private instances can reach Cloud SQL and Memorystore using private IPs — but the underlying mechanism is VPC peering, not direct subnet placement. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

The architecture diagram (third image) shows this clearly: Cloud SQL (MySQL) and Memorystore (Memcache) sit in a separate box labeled "PSA + VPC PEERING" to the right of the main VPC, connected via a VPC Peering link to the private subnets. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

🔍 **Deep Dive**
The two-network model means:

* You create your VPC and subnets (your network).
* You create Cloud SQL and Memorystore (they get placed in Google's service producer network).
* You allocate an IP range from your VPC for PSA.
* You create a VPC peering connection between your VPC and the service producer network.
* After peering, your private instances can reach the managed services via private IP, as if they were in the same network — but architecturally they are not.

This is a pattern you must understand for GCP. Every time you use a managed service that needs private connectivity, you need PSA + VPC Peering. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

***

## 1.4 The Frontend — Layer 7 Load Balancer Architecture

The frontend is the most complex part of the architecture, and the instructor creates a dedicated flow diagram to explain it. The load balancer in GCP is a **Layer 7 application load balancer** — meaning it operates at the HTTP/HTTPS level and can make routing decisions based on URL paths, hostnames, and other HTTP attributes. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

### The Request Flow

A user on the internet accesses a URL (e.g., `vprogcp.hkhinfotek.xyz`). This URL resolves to a **static public IP** of the load balancer via a **GoDaddy DNS A record**. The DNS simply maps the domain name to the load balancer's static IP address. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

From the static IP, the request enters the load balancer, and the path splits based on protocol:

### HTTPS Path (Port 443)

1. **HTTPS Forwarding Rule (Port 443):** Receives the incoming HTTPS traffic.
2. **Target HTTPS Proxy (`vprofile-app01-https-`):** This is the frontend of the load balancer for HTTPS. It handles the SSL/TLS connection.
3. **Certificate Map Entry (`vprofile-cert-entry`):** Validates the SSL certificate. The certificate is configured for the wildcard domain (e.g., `*.hkhinfotek.xyz`) and mapped via Certificate Manager. If the certificate validates, the request proceeds.
4. **URL Map (`vprofile-app01-url-map`):** A routing table that says: "If the request is for path `/`, route it to this specific backend service." This is what makes it a Layer 7 load balancer — it can have multiple entries routing different URL paths to different backends. In this project, there is just one entry, but the capability exists for many. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

### HTTP Path (Port 80)

1. **HTTP Forwarding Rule (Port 80):** Receives incoming HTTP traffic.
2. **Target HTTP Proxy (`vprofile-app01-http-`):** The frontend for HTTP traffic.
3. **URL Map:** Same routing table — routes to the same backend.

The instructor notes: this HTTP path can optionally redirect to HTTPS. In either case, the request ultimately reaches the same backend. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

The instructor explicitly compares with AWS: "In AWS, this is pretty simple, but in GCP, especially in command line, we need to add many entries." The HTTPS proxy, certificate map entry, URL map, HTTP proxy — these are all separate GCP resources that must be individually created and connected. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

***

## 1.5 The Load Balancer Backend — Managed Instance Group

Regardless of whether the request came via HTTPS or HTTP, after passing through the URL map, it reaches the **backend service** (`vprofile-app01-backend`). [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

The backend service is connected to a **Managed Instance Group (MIG)** (`vprofile-app01-mig`), which is GCP's equivalent of AWS Auto Scaling Groups. The MIG is configured to **autoscale between 1 and 4 instances**. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

A **health check** (`vprofile-app01-hc`) probes the instances to verify they are healthy. In this project, the health check hits **port 8080** over HTTP — which is the port where the Tomcat application server runs on each instance. If an instance fails the health check, the MIG replaces it. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

The instances themselves are created from a **template** — specifically an `e2-micro` instance type running a **custom image** that has the vProfile application pre-deployed on Tomcat, serving on port 8080. The instances are launched in the **private subnet** of the VPC. They do not have public IPs — traffic reaches them only through the load balancer. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

🔍 **Deep Dive**
The URL map concept deserves special attention because it reveals the Layer 7 nature of the load balancer. In AWS, you configure target groups and listener rules. In GCP, the equivalent is: forwarding rules (listeners) → target proxies (protocol handlers) → URL maps (routing rules) → backend services (target groups). Each is a separate resource, which is why GCP command-line setup requires more individual configuration commands than AWS. The instructor warns about this complexity and provides the architecture diagram as a reference to follow during the execution lectures. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

***

## 1.6 The Complete End-to-End Request Flow

Combining all parts, the full request path is:

1. User enters URL in browser → DNS resolves to load balancer static IP.
2. Request hits the load balancer's forwarding rule (port 443 for HTTPS, port 80 for HTTP).
3. Target proxy handles the protocol (validates certificate for HTTPS).
4. URL map routes the request to the correct backend service.
5. Backend service forwards to a healthy instance in the managed instance group.
6. The instance lives in the **private subnet** of the VPC, running Tomcat with vProfile on port 8080.
7. The vProfile application accesses backend services (Cloud SQL for database, Memorystore for caching) through **VPC Peering** (PSA connection to the service producer network). [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

This creates a fully secure architecture: the application servers have no public IPs, the database and cache are in a separate network connected only via private peering, and all public access flows through the load balancer with HTTPS termination and certificate validation. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

***

## 1.7 AWS vs GCP Comparison Points

The instructor draws explicit comparisons throughout:

| Concept                      | AWS                            | GCP                                           |
| ---------------------------- | ------------------------------ | --------------------------------------------- |
| Managed service connectivity | Direct in VPC private subnet   | PSA + VPC Peering to service producer network |
| Auto-scaling group           | Auto Scaling Group             | Managed Instance Group (MIG)                  |
| Load balancer routing        | Target Groups + Listener Rules | URL Map + Target Proxy + Forwarding Rule      |
| Firewall                     | Security Groups                | Cloud Firewall Rules                          |
| NAT                          | NAT Gateway                    | Cloud NAT + Cloud Router                      |
| HTTPS certificate            | ACM (simple)                   | Certificate Manager + Certificate Map Entry   |
| LB frontend config           | "Pretty simple"                | "Many entries needed, especially in CLI"      |

 [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are deploying the vProfile Java web application on GCP with a production-grade architecture: a custom VPC with public and private subnets, managed backend services (Cloud SQL + Memorystore) connected via VPC Peering, a Layer 7 HTTPS load balancer with autoscaling managed instance groups, DNS mapping, and certificate-based HTTPS termination. The final outcome: users access `vprogcp.hkhinfotek.xyz` → HTTPS load balancer → autoscaled Tomcat instances in private subnets → Cloud SQL and Memorystore via VPC Peering. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

***

## Execution Sequence — The Four-Part Build Order

The instructor defines the build order based on architectural dependencies. Each part must be completed before the next can begin.

### Part 1: VPC Setup

**What we create:**

| Resource             | Details                                                |
| -------------------- | ------------------------------------------------------ |
| VPC                  | Custom VPC                                             |
| Public Subnet 1      | Bastion host resides here                              |
| Public Subnet 2      | Redundancy across AZs                                  |
| Private Subnet 1     | Application instances reside here                      |
| Private Subnet 2     | Redundancy across AZs                                  |
| Cloud Router         | Manages routing for Cloud NAT                          |
| Cloud NAT            | Outbound internet access for private subnets           |
| Cloud Firewall Rules | Control traffic: Internet → Bastion, Bastion → Private |
| Bastion Host         | Jump server in public subnet                           |

 [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

**Why this comes first:** Every other resource (instances, managed services, load balancer backends) needs to be placed within the VPC. The network must exist before anything can be deployed into it.

***

### Part 2: Backend Services (Cloud SQL + Memorystore + PSA/Peering)

**What we create:**

| Resource               | Details                                              |
| ---------------------- | ---------------------------------------------------- |
| IP Range Allocation    | Reserve an IP range in VPC for PSA                   |
| PSA + VPC Peering      | Connect VPC to GCP service producer network          |
| Cloud SQL (MySQL)      | Managed database — lives in service producer network |
| Memorystore (Memcache) | Managed cache — lives in service producer network    |

 [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

**Why this comes second:** The application needs its database and cache configured before it can be tested. These services must be reachable from the private subnets via VPC peering.

**Key operational note:** This is NOT like AWS where you just create an RDS in a private subnet. In GCP, you must:

1. Allocate an IP range for private services.
2. Create the VPC peering connection to the service producer network.
3. Only then create Cloud SQL and Memorystore.

***

### Part 3 & 4: Frontend (Load Balancer Configuration)

**What we create (HTTPS path):**

| Resource                          | Name Pattern             | Purpose                             |
| --------------------------------- | ------------------------ | ----------------------------------- |
| Static Public IP                  | Load balancer IP         | Stable IP for DNS mapping           |
| HTTPS Forwarding Rule             | Port 443                 | Receives HTTPS traffic              |
| Target HTTPS Proxy                | `vprofile-app01-https-`  | Frontend for HTTPS                  |
| Certificate (Certificate Manager) | `vprofile-https-cert`    | SSL/TLS certificate                 |
| Certificate Map Entry             | `vprofile-cert-entry`    | Maps wildcard domain to certificate |
| URL Map                           | `vprofile-app01-url-map` | Routes requests to backend          |

 [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

**What we create (HTTP path):**

| Resource             | Name Pattern           | Purpose                |
| -------------------- | ---------------------- | ---------------------- |
| HTTP Forwarding Rule | Port 80                | Receives HTTP traffic  |
| Target HTTP Proxy    | `vprofile-app01-http-` | Frontend for HTTP      |
| URL Map              | Same as above          | Routes to same backend |

**What we create (Backend):**

| Resource               | Name Pattern               | Purpose                      |
| ---------------------- | -------------------------- | ---------------------------- |
| Backend Service        | `vprofile-app01-backend`   | Load balancer backend target |
| Health Check           | `vprofile-app01-hc`        | Probes port 8080 (Tomcat)    |
| Managed Instance Group | `vprofile-app01-mig`       | Autoscale 1–4 instances      |
| Instance Template      | e2-micro with custom image | vProfile app on Tomcat:8080  |

 [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

**DNS Configuration:**

| Resource | Platform    | Details                                                          |
| -------- | ----------- | ---------------------------------------------------------------- |
| A Record | GoDaddy DNS | `vprogcp.hkhinfotek.xyz` → static LB IP (e.g., `136.110.238.20`) |

 [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

**Why this comes last:** The load balancer routes traffic to the managed instance group, which launches instances in the VPC's private subnet. The instances run the vProfile app, which connects to Cloud SQL and Memorystore. Everything upstream must exist first.

***

## Reference Diagrams

The instructor provides three architecture diagrams (available in lecture resources) that should be referenced **during every execution step**:

1. **VPC Diagram:** Shows the four subnets, bastion host, Cloud NAT/Router, and firewall rules.
2. **Load Balancer Flow Diagram:** Shows the complete HTTPS/HTTP path from internet through forwarding rules, proxies, certificate map, URL map, backend service, MIG, to private instances.
3. **Backend Services Diagram:** Shows VPC + PSA/VPC Peering connection to Cloud SQL and Memorystore in the service producer network.

The instructor emphasizes: "You should every time look at this diagram when we configure the load balancer entries." [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

⚠️ **Expert Note**
The GCP load balancer configuration involves significantly more individual resources than AWS. Each component (forwarding rule, target proxy, certificate map entry, URL map, backend service, health check, MIG) is a separate GCP resource created via a separate `gcloud` command. The architecture diagram is your map through this complexity. Without it, the sequence of CLI commands will feel arbitrary. With it, each command clearly corresponds to a box in the diagram. [\[289-projec...e-overview \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/289-project-architecture-overview.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Complete Architecture (End-to-End)

```
INTERNET
  │
  │  DNS: vprogcp.hkhinfotek.xyz → A Record → Static LB IP
  │
  ▼
┌─── LOAD BALANCER (Layer 7) ────────────────────────────────────────┐
│                                                                     │
│  HTTPS (443):                    HTTP (80):                         │
│  Forwarding Rule                 Forwarding Rule                    │
│       ▼                               ▼                             │
│  Target HTTPS Proxy              Target HTTP Proxy                  │
│       ▼                               │                             │
│  Certificate Map Entry                 │                             │
│  (validate cert)                       │                             │
│       ▼                               ▼                             │
│  ┌──────────── URL Map ─────────────────┐                           │
│  │  / → backend service                 │                           │
│  └──────────────────────────────────────┘                           │
│                    ▼                                                 │
│  Backend Service (vprofile-app01-backend)                            │
│       ▼                                                              │
│  Health Check (port 8080) ──► MIG (1-4 instances, autoscaled)       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─── VPC ──────────────────────────────────────────────┐
│                                                       │
│  Public Subnet 1    │  Private Subnet 1               │
│  [Bastion Host] ────►  [vProfile on Tomcat:8080]      │
│     ▲ FW Rules         (e2-micro from template)       │
│     │                         │                       │
│  Public Subnet 2    │  Private Subnet 2               │
│                               │                       │
│  Cloud NAT ◄──────────────────┘ (outbound internet)   │
│  Cloud Router                                         │
└───────────────────────┬───────────────────────────────┘
                        │
                   VPC PEERING (PSA)
                        │
              ┌─────────▼──────────┐
              │ Service Producer    │
              │ Network             │
              │  ┌────────────┐    │
              │  │ Cloud SQL  │    │
              │  │ (MySQL)    │    │
              │  └────────────┘    │
              │  ┌────────────┐    │
              │  │ Memorystore│    │
              │  │ (Memcache) │    │
              │  └────────────┘    │
              └────────────────────┘
```

***

## Build Sequence (Dependency Order)

```
Part 1: VPC
  VPC → Subnets (2 pub + 2 priv) → Cloud Router → Cloud NAT
  → Firewall Rules → Bastion Host

Part 2: Backend Services
  Allocate IP Range → PSA + VPC Peering → Cloud SQL → Memorystore

Part 3+4: Frontend (Load Balancer)
  Static IP → Certificate (Cert Manager) → Certificate Map Entry
  → URL Map → Target HTTPS Proxy → HTTPS Forwarding Rule (443)
  → Target HTTP Proxy → HTTP Forwarding Rule (80)
  → Backend Service → Health Check → MIG → Instance Template
  → DNS A Record (GoDaddy)
```

***

## AWS vs GCP — Quick Mapping

```
AWS                          GCP
──────────────────────       ──────────────────────
Security Groups              Cloud Firewall Rules
NAT Gateway                  Cloud NAT + Cloud Router
RDS (in private subnet)      Cloud SQL (service producer network + PSA/Peering)
ElastiCache                  Memorystore (service producer network + PSA/Peering)
Auto Scaling Group           Managed Instance Group (MIG)
Target Group                 Backend Service
Listener Rules               Forwarding Rule + Target Proxy
ACM Certificate              Certificate Manager + Certificate Map Entry
ALB Routing Rules            URL Map
Direct VPC placement         PSA + VPC Peering (two separate networks)
"Pretty simple"              "Many entries needed, especially in CLI"
```

***

## PSA + VPC Peering (The GCP-Specific Pattern)

```
YOUR VPC                          GCP SERVICE PRODUCER NETWORK
  │                                        │
  │  allocate IP range                     │  Cloud SQL (MySQL)
  │  for private services                  │  Memorystore (Memcache)
  │                                        │
  └────────── VPC PEERING ─────────────────┘

AWS: managed service → directly in your VPC subnet
GCP: managed service → separate network → must peer to access

This is MANDATORY for any GCP managed service needing private connectivity
```

***

## Load Balancer Component Chain (GCP)

```
HTTPS flow:
  Forwarding Rule (443) → Target HTTPS Proxy → Certificate Map Entry
    → URL Map → Backend Service → MIG → Instances

HTTP flow:
  Forwarding Rule (80) → Target HTTP Proxy → URL Map
    → Backend Service → MIG → Instances

Each arrow = separate GCP resource = separate gcloud command
```

***

## URL Map — Layer 7 Routing

```
URL Map = routing table for HTTP paths

Entry: path "/" → backend service "vprofile-app01-backend"
Entry: path "/api" → could route to different backend (not in this project)

This is what makes it Layer 7 (application-level routing)
AWS equivalent: ALB listener rules + target groups
```

***

## MIG + Instance Template

```
Instance Template:
  Type: e2-micro
  Image: custom (vProfile app pre-installed)
  App: Tomcat serving vProfile on port 8080
  Network: private subnet (no public IP)

MIG:
  Autoscale: 1–4 instances
  Health Check: HTTP on port 8080
  Unhealthy → replaced automatically
```

***

## DNS Configuration

```
GoDaddy DNS:
  Type: A Record
  Name: vprogcp.hkhinfotek.xyz
  Value: <Static LB IP> (e.g., 136.110.238.20)

Static IP → Load Balancer → Backend → Private Instance
```

***

## Security Architecture

```
Internet → only reaches Load Balancer (static public IP)
LB → routes to instances in PRIVATE subnet (no public IP)
SSH → only via Bastion Host in public subnet (firewall-controlled)
Backend services → private IPs only, accessed via VPC Peering
Outbound from private → Cloud NAT (no inbound possible)

No direct internet exposure for application or data tier
```

***

## Key Engineering Patterns

| Pattern                                     | Manifestation                                                                                                                           |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Two-network model (GCP-specific)**        | Your VPC + service producer network, connected via PSA/Peering — fundamentally different from AWS's single-VPC model                    |
| **Layered security**                        | Internet → LB → private subnet → VPC peering → managed services. Each layer adds isolation                                              |
| **Decomposed load balancer**                | GCP decomposes LB into atomic resources (forwarding rule, proxy, cert map, URL map, backend) — more CLI work, but more granular control |
| **Template-based autoscaling**              | Custom image baked into instance template → MIG autoscales identical instances                                                          |
| **Architecture diagram as execution guide** | Complex CLI sequences become navigable when each command maps to a diagram component                                                    |
| **Dependency-ordered provisioning**         | VPC → Backend services → Frontend — strict order because each layer depends on the previous                                             |

***

## Project Continuity

```
BEFORE: GCP VPC concepts (previous lecture)
THIS:   Full architecture overview — all 4 parts explained before execution
NEXT:   Part 1 execution — create VPC, subnets, Cloud NAT, bastion host via gcloud CLI
```

***

This completes the full reconstruction. **Theory** explains every architectural component and the critical GCP-specific patterns (PSA/Peering, decomposed load balancer). **Practical** gives you the exact build sequence, resource names, and the four-part dependency order. The **Compression Map** lets you mentally reload the entire end-to-end request flow, the AWS-vs-GCP mapping, and the component chain in under two minutes. Let me know if you'd like Anki flashcards or any section expanded! 🚀

# 🎓 Deep Learning Material: Networking Protocols, Ports & the OSI/TCP-IP Model

*Reconstructed from video captions — [76-protocols-ports-etc.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt?EntityRepresentationId=9e0c283e-1449-4f01-841f-1964ccb042d3)* [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 What Is a Protocol?

A protocol, in its most fundamental sense, is a **set of rules**. In networking communication specifically, a protocol is a **formal specification** that defines the exact procedures two parties — a sender and a receiver — must follow in order to exchange information successfully. It is not a vague guideline; it is a rigid, agreed-upon contract that both sides must honor for communication to work. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

A protocol governs several critical dimensions of communication: the **format** of the data (how it is structured), the **timing** (when data is sent and how long to wait), the **sequence** (the order in which messages flow), and **error handling** (what happens when something goes wrong during transmission). These are not optional features — they are built into the protocol's definition, and every device or application that implements the protocol must respect all of them. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

Examples include **HTTP** (for web communication), **FTP** (for file transfer), and **SSH** (for secure remote access). When a client and a server both understand a given protocol, they know exactly how to communicate — what to send, when to send it, what to expect back, and what to do if something fails. The protocol eliminates ambiguity. Without it, two machines have no shared language. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

> 🔍 **Deep Dive:** Think of a protocol not just as "rules" but as a **communication contract with enforcement**. If a web browser sends an HTTP request, the server knows exactly what headers to expect, what methods are valid (GET, POST, etc.), and what response codes to return. Neither side invents its own format — both sides conform to the protocol. This is what makes the internet work at scale: millions of devices from different manufacturers, running different operating systems, all speaking the same protocol.

***

## 1.2 The Transport Layer: TCP vs. UDP

At **Layer 4** of the OSI model — the **Transport Layer** — sit two foundational protocols: **TCP** (Transmission Control Protocol) and **UDP** (User Datagram Protocol). This is a critical architectural point: **all the protocols you see at layers 5, 6, and 7 are ultimately carried by either TCP or UDP.** Every application-layer protocol (HTTP, FTP, DNS, SMTP, etc.) rides on top of one of these two transport mechanisms. Understanding TCP and UDP is therefore understanding the backbone on which everything else is built. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

### 1.2.1 TCP — The Reliable Protocol

TCP is called a **reliable protocol**, and this word "reliable" has a very specific technical meaning. It means TCP **guarantees delivery** — it ensures that data sent from the source arrives at the destination completely, correctly, and in the right order. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

How does it achieve this?

**Connection-oriented nature:** Before any data flows, TCP establishes a formal connection between the source and the destination. This is not a physical wire — it is a logical agreement that both sides are ready to communicate. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

**Three-way handshake:** This connection is established through a **three-way handshake** — a specific sequence of three messages (SYN → SYN-ACK → ACK) exchanged before any actual data transfer begins. Only after this handshake succeeds does data transmission start. This ensures both sides are alive, reachable, and synchronized. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

**Acknowledgement-based communication:** Every piece of data sent via TCP is **acknowledged** by the receiver. The sender knows whether each segment arrived. If an acknowledgement is not received within a timeout period, the sender retransmits the data. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

**Error detection and retransmission:** If a packet is **dropped** in transit (lost by a router, for example) or arrives **corrupted** (bits flipped during transmission), TCP detects this through checksums and sequence numbers. The corrupted or missing data is **retransmitted** automatically. This is why TCP is reliable — it actively monitors and recovers from failures. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

The practical consequence: when you send an email, upload a picture via HTTPS, or browse a website, TCP guarantees that your email arrives intact, your picture uploads without corruption, and the webpage renders correctly. Developers choose TCP-based protocols (HTTP, HTTPS, FTP, SMTP) when **data integrity is non-negotiable**. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

> 🔍 **Deep Dive:** Reliability in TCP comes at a cost — **overhead**. The three-way handshake adds latency before data flows. Acknowledgements consume bandwidth. Retransmissions introduce delays. Error checking requires computational resources. TCP is not slow, but it is *heavier* than UDP. This is an engineering trade-off: you pay in performance for the guarantee of correctness.

***

### 1.2.2 UDP — The Unreliable (But Faster) Protocol

UDP is called an **unreliable protocol**, and this is not a criticism — it is a deliberate design choice that serves a real engineering need. UDP is **connectionless**: the sender simply transmits data and moves on. There is no handshake, no connection establishment, no acknowledgement, and no guaranteed sequencing of data. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

The sender has **no confirmation** that the data reached its destination. If a packet is lost or corrupted, UDP does not detect it and does not retransmit. The data is simply gone. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

Why would anyone want this? Because **speed matters more than reliability in certain scenarios.** UDP is significantly **faster** than TCP precisely because it skips all the overhead — no handshake delay, no acknowledgement traffic, no retransmission logic. The data goes out immediately. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

Protocols that use UDP include **DNS** (translating a URL into an IP address must happen almost instantly), **DHCP** (a client requesting an IP address on the network needs a fast response), and **TFTP** (Trivial File Transfer Protocol, used for lightweight, fast transfers). In all these cases, the cost of occasionally losing a packet is far less than the cost of slowing down every single transaction with reliability overhead. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

> ⚠️ **Expert Note:** The TCP vs. UDP decision is one of the most fundamental **engineering trade-offs** in network application design. Developers don't choose randomly — they evaluate whether their application can tolerate data loss (use UDP) or whether every byte must arrive intact (use TCP). Real-world systems often use both: a web application may use TCP for page loads but UDP for real-time status pings.

***

## 1.3 Port Numbers — Addressing Services Within a Machine

Every protocol has a **default port number**. This is a standardized numeric identifier that tells the network *which service* on a machine should receive the incoming data. The key ports referenced in the video: [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

| Protocol | Port  | Transport   |
| -------- | ----- | ----------- |
| DNS      | 53    | UDP and TCP |
| HTTP     | 80    | TCP         |
| HTTPS    | 443   | TCP         |
| SSH      | 22    | TCP         |
| SMTP     | 25    | TCP         |
| MySQL    | 3306  | TCP         |
| Tomcat   | 8080  | TCP         |
| RabbitMQ | 5672  | TCP         |
| Memcache | 11211 | TCP         |

These are **default** ports — the ports that services use unless explicitly reconfigured. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

***

## 1.4 The Relationship Between IP Addresses and Port Numbers

This is a core architectural concept. A computer on a network is identified by its **IP address** — this gets traffic to the right *machine*. But a single machine can run **multiple services** simultaneously (a web server, a database, an SSH daemon, etc.). The **port number** identifies which *service* on that machine should handle the traffic. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

The video uses a powerful analogy: imagine a **food court**. The food court itself has a physical **address** — this is like the IP address. You use the address to find the food court. But once inside, there are multiple **stalls** — stall 1 serves Indian food, stall 2 serves Chinese, stall 3 serves Italian, stall 4 serves Thai. Each stall number is like a **port number**. The address gets you to the building; the stall number gets you to the specific service you want. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

Similarly, a single computer with one IP address can serve SSH on port 22, HTTP on port 80, HTTPS on port 443, and SMTP on port 25 — all simultaneously. When traffic arrives, the combination of **IP address + port number** routes it to the exact correct service. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

> 🔍 **Deep Dive:** This IP:Port combination is technically called a **socket**. Every network connection is defined by a source IP:port and a destination IP:port. This is how millions of simultaneous connections can coexist — each has a unique socket pair. Understanding this concept is critical when configuring **firewalls** (Security Groups, NACLs in AWS), because firewall rules operate on IP addresses AND port numbers. You don't just allow traffic to a machine — you allow traffic to a specific service on that machine by specifying the port. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

***

## 1.5 OSI 7-Layer Model vs. TCP/IP Protocol Model

The video presents the mapping between the two standard networking models side by side: [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

The **OSI model** has 7 layers. The **TCP/IP model** consolidates these into fewer layers:

* **TCP/IP Application Layer** = OSI Layers 5, 6, and 7 (Session, Presentation, Application). Protocols at this combined layer include Telnet, FTP, DHCP, TFTP, SMTP, HTTP, and many others. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)
* **TCP/IP Transport Layer** = OSI Layer 4. Protocols: TCP and UDP. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)
* **TCP/IP Internet Layer** = OSI Layer 3 (Network). Protocols: IP, ICMP, ARP, RARP. This is where IP addressing lives. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)
* **TCP/IP Network Interface Layer** = OSI Layers 1 and 2 (Physical and Data Link). This handles the actual physical transmission and local network framing. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

The key takeaway: the TCP/IP model is the **practical model** used in real networking. The OSI model is the **conceptual reference model** used for teaching and understanding. They describe the same reality at different levels of granularity. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

***

## 1.6 How IP + Port + Protocol Work Together in Real Systems

The video demonstrates this with a concrete example: a **Tomcat** application server needs to store data in a **MySQL** database server. Tomcat sends traffic to the **destination IP address** of the MySQL server, targeting **port 3306** (MySQL's default port). The combination of IP + port gives Tomcat the **assurance** that its traffic will reach the MySQL service specifically, not some other service that might be running on the same machine. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

This is the fundamental pattern of all networked communication: **source IP:port → destination IP:port, using a specific protocol.** When you work with any project involving multiple services, you must know three things for every connection: the **IP address** of the target machine, the **port number** of the target service, and the **protocol** being used. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

***

## 1.7 The vProfile Project — Multi-Service Architecture Preview

The video introduces a project called **vProfile**, a Java-based application that consists of multiple services, each running on a separate virtual machine (both locally and on the cloud): [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

| Service  | Port  | Role                       |
| -------- | ----- | -------------------------- |
| Nginx    | 80    | Web server / reverse proxy |
| Tomcat   | 8080  | Java application server    |
| RabbitMQ | 5672  | Message queue              |
| Memcache | 11211 | Caching layer              |
| MySQL    | 3306  | Database                   |

Every VM has its own IP address, runs a specific service, and that service listens on a specific port. All these services **communicate with each other** across the network. The critical operational point: when connecting these services, you need to configure **firewalls** and networking rules, which requires knowing every service's IP address, port number, and protocol. Without this knowledge, you cannot open the correct ports, and services cannot communicate. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

> ⚠️ **Expert Note:** This multi-VM, multi-service architecture is the foundation of how real-world applications are deployed. Whether you're working on-premise or in AWS, understanding which service talks to which, on what port, using what protocol, is the prerequisite for every firewall rule, every security group entry, every NACL configuration, and every troubleshooting session. This is not theoretical — it is daily operational work.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

This section doesn't cover a hands-on lab, but rather the **operational knowledge framework** that the video teaches — the practical understanding you need to correctly configure, connect, and troubleshoot networked services. The "final operational outcome" is: you can look at any multi-service architecture, identify each service's protocol, port, and IP, and correctly configure network connectivity (including firewall rules) between them. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

***

## Step 1: Identifying Whether a Protocol Uses TCP or UDP

**What we are doing:** Before configuring any network rule, you must determine whether the protocol in question rides on TCP or UDP, because firewall rules require you to specify the transport protocol.

**How to decide operationally:**

* Does the application need **guaranteed delivery** (email, web browsing, file upload, database queries)? → **TCP**
* Does the application need **speed over reliability** (DNS lookups, DHCP requests, trivial file transfers)? → **UDP**
* Some protocols use **both** — DNS uses port 53 on both TCP and UDP. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

**Common mistake:** Assuming all traffic is TCP. DNS, DHCP, and TFTP are UDP. If you create a firewall rule allowing only TCP on port 53, DNS resolution may fail for certain query types.

**Verification:** Once a rule is in place, test the connection. If a service that should work is failing, check whether you've allowed the correct transport protocol (TCP vs. UDP) — not just the correct port.

**Connection to larger flow:** This determination is the first decision point in every firewall or security group configuration.

***

## Step 2: Mapping Services to Their Default Ports

**What we are doing:** For any project or architecture, you must create a clear map of every service, its default port, and which machine it runs on. This is the foundation for all networking configuration.

**The operational port reference from the video:** [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

```
SSH       → 22
DNS       → 53
HTTP      → 80
HTTPS     → 443
SMTP      → 25
MySQL     → 3306
Tomcat    → 8080
RabbitMQ  → 5672
Memcache  → 11211
```

**Why this matters operationally:** When you configure a Security Group in AWS, you write rules like: "Allow inbound TCP on port 3306 from IP range X." If you don't know that MySQL uses port 3306, you cannot write this rule. If you write port 3307 by mistake, the connection silently fails. [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

**Common mistake:** Forgetting that services can be reconfigured to use non-default ports. Always verify the **actual** port a service is running on, not just the default. Check service configuration files or use commands like `netstat` or `ss` to confirm.

**Connection to larger flow:** This port map becomes the input to every firewall rule and every service configuration file that references another service.

***

## Step 3: Understanding IP + Port as a Complete Service Address

**What we are doing:** Operationally connecting two services requires specifying the **full address**: IP + port. Neither alone is sufficient.

**Operational example from the video:** [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

A Tomcat server needs to reach a MySQL database. The configuration inside Tomcat must specify:

* **Destination IP:** The IP address of the VM running MySQL
* **Destination Port:** `3306`

```
# Conceptual connection string pattern:
mysql://<MySQL_Server_IP>:3306/database_name
```

**What happens internally:** The Tomcat application creates a TCP connection to the MySQL server's IP on port 3306. The operating system on the MySQL server receives this traffic and routes it to the MySQL process because MySQL is *listening* on port 3306.

**Common mistakes:**

* Using the wrong IP (pointing to the wrong machine)
* Using the wrong port (pointing to the wrong service on the right machine)
* Forgetting that firewalls between the two machines must explicitly allow traffic on this port

**Verification:** After configuring the connection, test it. If the connection fails, systematically check: (1) Is the destination IP correct and reachable? (2) Is the service actually running on the expected port? (3) Are firewalls between source and destination allowing traffic on that port?

**Connection to larger flow:** Every inter-service connection in the vProfile project (and in any real project) follows this exact pattern.

***

## Step 4: Mapping the vProfile Project Architecture

**What we are doing:** Applying the IP + port + protocol framework to a real multi-service project.

**The vProfile architecture:** [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

```
[User] → Nginx (Port 80) → Tomcat (Port 8080) → RabbitMQ (Port 5672)
                                                → Memcache (Port 11211)
                                                → MySQL (Port 3306)
```

Each service runs on a **separate VM**, each VM has its own **IP address**, and each service listens on its **specific port**.

**Operational requirements to connect them:**

1. Know every VM's IP address
2. Know every service's port number
3. Configure firewall rules on each VM to allow inbound traffic on the correct port from the correct source IP
4. Configure each service's connection settings to point to the correct destination IP:port

**Common mistake:** Configuring the services correctly but forgetting the firewall. The services know where to connect, but the firewall blocks the traffic. This is the most common source of "connection refused" or "connection timed out" errors in multi-VM architectures.

> ⚠️ **Expert Note:** In AWS, these firewall rules are **Security Groups** (instance-level, stateful) and **NACLs** (subnet-level, stateless). For the vProfile project, each VM's Security Group must allow inbound traffic on its service port from the IPs of the VMs that need to connect to it. For example, the MySQL VM's Security Group must allow inbound TCP on port 3306 from the Tomcat VM's IP. Miss one rule, and the entire chain breaks.

***

## Step 5: Using the OSI/TCP-IP Model for Troubleshooting

**What we are doing:** Using the layered model as a **troubleshooting framework**.

When a connection between two services fails, you can systematically work through the layers: [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

1. **Layer 1-2 (Network Interface):** Is there physical/virtual network connectivity? Can the machines see each other at the network level?
2. **Layer 3 (Internet/Network):** Can you ping the destination IP? Is routing configured correctly? Are IP addresses correct? (Protocols: IP, ICMP, ARP)
3. **Layer 4 (Transport):** Is the correct transport protocol (TCP/UDP) being used? Is the port open? Is the firewall allowing traffic on this port?
4. **Layer 5-7 (Application):** Is the service actually running? Is it listening on the expected port? Is the application-level configuration correct?

**Operational pattern:** Always troubleshoot **bottom-up** — start from Layer 1 and work your way up. There's no point debugging application configuration if the machines can't even reach each other at the network level.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## 🏗️ Core Architecture

```
PROTOCOL = Formal communication contract (format + timing + sequence + error handling)
    └── Every protocol rides on either TCP or UDP (Layer 4)
        ├── TCP = Reliable | Connection-oriented | 3-way handshake | ACK | Retransmit
        └── UDP = Unreliable | Connectionless | No ACK | Fast | Fire-and-forget
```

## 🔀 TCP vs. UDP Decision Chain

```
Need guaranteed delivery? ──YES──→ TCP (HTTP, HTTPS, FTP, SMTP, SSH, MySQL)
         │
         NO
         │
         ▼
Need maximum speed? ──YES──→ UDP (DNS, DHCP, TFTP)
```

## 🔑 Port Number = Service Identifier Within a Machine

```
IP Address  → identifies the MACHINE
Port Number → identifies the SERVICE on that machine
IP + Port   → complete service address (socket)

Analogy: Food Court Address = IP | Stall Number = Port
```

## 📋 Critical Port Map

```
22    = SSH          │  443   = HTTPS
53    = DNS (TCP+UDP)│  3306  = MySQL
80    = HTTP         │  8080  = Tomcat
25    = SMTP         │  5672  = RabbitMQ
                     │  11211 = Memcache
```

## 🗺️ OSI ↔ TCP/IP Layer Mapping

```
OSI 7,6,5 (App+Pres+Session) ═══ TCP/IP Application   → Telnet,FTP,DHCP,SMTP,HTTP...
OSI 4     (Transport)         ═══ TCP/IP Transport      → TCP, UDP
OSI 3     (Network)           ═══ TCP/IP Internet        → IP, ICMP, ARP, RARP
OSI 2,1   (DataLink+Physical) ═══ TCP/IP Network Interface
```

## 🔗 Inter-Service Connection Pattern

```
Source App → Destination IP : Destination Port → Target Service

Example: Tomcat ──→ MySQL_IP:3306 ──→ MySQL Service
Requires: Correct IP + Correct Port + Firewall OPEN on that port
```

## 🏢 vProfile Multi-Service Architecture

```
User → [Nginx:80] → [Tomcat:8080] ─┬─→ [RabbitMQ:5672]
                                    ├─→ [Memcache:11211]
                                    └─→ [MySQL:3306]

Each service = Separate VM = Own IP = Own Port = Own Firewall Rules
```

## 🔧 Firewall Configuration Mental Model

```
For EACH service:
  Allow INBOUND on [service port] + [TCP/UDP] from [source IPs that need access]

Miss one rule → "Connection refused" / "Connection timed out"

AWS: Security Group (instance, stateful) + NACL (subnet, stateless)
```

## 🛠️ Troubleshooting Sequence (Bottom-Up)

```
Layer 1-2: Network connectivity? → ping at L2?
Layer 3:   IP reachable? → ping destination IP
Layer 4:   Port open? Firewall allowing? TCP/UDP correct?
Layer 5-7: Service running? Listening on expected port? Config correct?

ALWAYS: Start from bottom. Don't debug app config if network is broken.
```

## 🔁 Reusable Engineering Patterns Extracted

| Pattern                             | Manifestation                                                        |
| ----------------------------------- | -------------------------------------------------------------------- |
| **Contract-based communication**    | Protocols define rigid rules both sides must follow                  |
| **Reliability vs. speed trade-off** | TCP vs. UDP — fundamental engineering decision                       |
| **Layered addressing**              | IP (machine) + Port (service) = hierarchical address resolution      |
| **Multi-service isolation**         | One service per VM, each with own IP and port                        |
| **Firewall as gate control**        | Every inter-service link requires explicit firewall permission       |
| **Bottom-up troubleshooting**       | Debug from physical layer upward, not top-down                       |
| **Default-but-configurable**        | Ports have defaults but can be changed — always verify actual config |

***

This completes the full reconstruction. All content is grounded exclusively in the video captions. Want me to generate Anki flashcards (CSV) from this material, or would you like me to expand any specific section further? [\[76-protoco...-ports-etc \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/76-protocols-ports-etc.txt)

# 🖧 Linux Networking Commands — Deep Learning Material

**Source:** Video caption file — [77-networking-commands.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt?EntityRepresentationId=1a2704d4-d1c3-42aa-9cb4-46eab22f05c2) [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Video Context:** The instructor demonstrates essential Linux (and some Windows) networking commands using two Vagrant-provisioned VMs: **web01** (Ubuntu, Apache2, IP `192.168.40.11`, port 80) and **db01** (MariaDB, IP `192.168.40.12`, port 3306). Commands are executed primarily from web01 as the root user.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Lab Environment — Why It Matters Before Any Command

Before any networking command makes sense, you need to understand the environment it operates in. The instructor built a two-VM lab using a Vagrant multi-VM setup. **web01** is an Ubuntu machine running the Apache2 web service on port 80. **db01** runs MariaDB on port 3306. web01's static IP is `192.168.40.11`; db01's is `192.168.40.12`. Both VMs also have a NAT network interface assigned by VirtualBox (on the `10.0.2.x` subnet). [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

This setup creates a realistic miniature infrastructure: a web server that needs to talk to a database server across a network. Every command demonstrated in this video answers a real operational question that arises in exactly this kind of architecture — "Can I reach the DB?", "Is the port open?", "What's blocking the connection?", "Where is the latency?" Understanding the lab is understanding the *why* behind every command.

***

## 1.2 Network Interfaces and IP Addressing — `ifconfig` and `ip addr show`

A Linux machine can be connected to multiple networks simultaneously. Each connection is represented by a **network interface**, and each interface has a name and an IP address. The command `ifconfig` displays all **active** network interfaces, their names, and their assigned IP addresses. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

In the lab, web01 shows three interfaces:

* **NAT interface** — connected to VirtualBox's NAT network (the `10.0.2.x` range). This is how the VM reaches the outside internet through the host machine.
* **Host-only / static IP interface** — this carries the IP `192.168.40.11`, which is the static IP explicitly assigned in the Vagrantfile. This is the address used for VM-to-VM communication within the lab.
* **Loopback interface (`lo`)** — IP address `127.0.0.1`. This is a virtual interface the machine uses to refer to **itself**. When a process on the machine needs to talk to another process on the same machine via the network stack, it uses the loopback address. It never leaves the machine. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

The key insight is: a single computer can have multiple IP addresses because it can be connected to multiple networks. Each interface = one network membership. The machine is simultaneously "living" on the `10.0.2.x` network AND the `192.168.40.x` network.

If `ifconfig` is not available on your Linux distribution (some modern distros have removed it from default packages), the equivalent replacement is `ip addr show`. It provides the same information — interface names, IP addresses, network membership — using the newer `iproute2` toolset. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

🔍 **Deep Dive:** `ifconfig` belongs to the older `net-tools` package. `ip addr show` belongs to `iproute2`, which is now the standard on most modern Linux distributions. Functionally, for viewing interfaces and IPs, they overlap. But `ip` is more powerful — it can also manipulate routes, tunnels, and network namespaces. If you're learning fresh, prefer `ip addr show`, but know `ifconfig` because you'll encounter it everywhere in legacy documentation and scripts.

***

## 1.3 Testing Network Connectivity — `ping` and ICMP

Once you know your own IP address and the IP of a target machine, the most fundamental question is: **"Can I reach it?"** The `ping` command answers this. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

`ping` works by sending **ICMP (Internet Control Message Protocol) packets** to the target IP address. When the target machine's network interface receives these packets, it replies back. If replies come back, there is network connectivity. If they don't, something is blocking communication — a firewall, a misconfigured route, the target being down, etc.

**Behavioral difference between platforms:** On Windows, `ping` sends exactly **4 packets** and stops. On Linux, `ping` sends packets **continuously, indefinitely**, until you press `Ctrl+C` to stop it. After stopping, it shows a summary: how many packets were transmitted, how many were received, and the **packet loss percentage**. Zero percent packet loss = healthy connectivity. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

The instructor pings `192.168.40.12` (db01) from web01 and gets 12 transmitted, 12 received, 0% loss — confirming clean connectivity between the two VMs.

⚠️ **Expert Note:** `ping` only proves ICMP-level reachability. A machine can be reachable by ping but still refuse connections on specific ports due to firewall rules or the service being down. Ping answers "Is the network path alive?" — not "Is the service available?" Those are different questions requiring different tools (like `telnet` or `nmap`, covered later).

***

## 1.4 Name Resolution — `/etc/hosts`, DNS, `dig`, and `nslookup`

Humans prefer names; machines use IP addresses. The system that translates names to IPs is called **DNS (Domain Name System)**. But there's a simpler, local alternative: the `/etc/hosts` file. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

The `/etc/hosts` file exists on virtually every operating system. You can manually add entries in the format: `<IP address>  <hostname>`. Once an entry is added, you can use the hostname instead of the IP anywhere on that machine. The instructor adds `192.168.40.12  db01` to `/etc/hosts` on web01, and after that, `ping db01` works — it resolves `db01` to `192.168.40.12` automatically. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

For internet-scale name resolution, DNS servers are used. Two commands query DNS:

**`dig`** performs a DNS lookup for a given domain name. When the instructor runs `dig www.google.com`, it returns the **A record** (the IPv4 address mapping) from the DNS server, and also shows **which DNS server** answered the query. `dig` is the modern, detailed DNS diagnostic tool. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**`nslookup`** does essentially the same thing — resolves a name to an IP — but is considered an **older version** of `dig`. It shows the name, the resolved IPv4 address, the IPv6 address (if available), and the DNS server that resolved it along with its port number. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

The primary use case for both commands: **verifying that DNS resolution is working from your machine.** If a service is unreachable by name but reachable by IP, the problem is DNS — and `dig`/`nslookup` will reveal it.

🔍 **Deep Dive:** The resolution order on Linux is controlled by `/etc/nsswitch.conf`. Typically, the system checks `/etc/hosts` first, then DNS. This means a local `/etc/hosts` entry will override DNS. This is both powerful (for quick local overrides) and dangerous (if stale entries remain, they silently redirect traffic).

***

## 1.5 Tracing the Network Path — `traceroute` / `tracert` and `mtr`

`ping` tells you *whether* you can reach a destination. **Traceroute** tells you *how* you reach it — the complete path of network hops (routers) your packets traverse to get from source to destination. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

The command is `traceroute` on Linux and `tracert` on Windows. The instructor runs `tracert www.google.in` from the Windows host (because traceroute doesn't work reliably inside VirtualBox VMs). The output shows each **hop** — each router the packet passes through — along with its IP address or hostname, and the **latency** (round-trip time) for three packets sent to each hop. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

In the instructor's example, the path to Google took **8 hops**. For each hop, three packets are sent, and the time for each is displayed. The first packet to the first router took 256ms (an anomaly — likely a cold start), while subsequent packets took \~1ms.

**The diagnostic power of traceroute:** If you see all three packets at a particular hop showing very high latency, the problem is at or near that hop — not at your local network and not at the destination server. It's somewhere in the middle, on the internet. This is how network engineers **localize latency problems**. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**`mtr`** is an enhanced, **live, continuous** version of traceroute. Instead of running once and stopping, `mtr` keeps sending packets and dynamically updates the display, showing ongoing packet loss percentages at each hop. This makes it superior for diagnosing **intermittent** connectivity issues — problems that appear and disappear. If you're experiencing slow internet or intermittent drops, `mtr` will show you exactly which hop is losing packets, and whether the loss is consistent or sporadic. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

If `mtr` shows 100% packet loss starting at a specific hop, the problem is at that exact point. You can then determine: is it your local network? The ISP? A specific backbone router? The destination server?

⚠️ **Expert Note:** Traceroute/mtr inside VirtualBox VMs is unreliable because VirtualBox's NAT networking handles routing in a way that breaks the hop-by-hop discovery mechanism. Always run these from the **host machine** or a machine with direct network access for accurate results.

***

## 1.6 Discovering Open Ports and Services — `netstat`, `ss`, and `nmap`

Knowing which **ports are open** on a machine is fundamental to network troubleshooting. A port is an endpoint where a service listens for incoming connections. If a service isn't reachable, one of the first questions is: "Is the port actually open?" [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**`netstat -antp`** shows all open **TCP** ports on the current machine, along with the **process ID (PID)** and **process name** that owns each port. The flags mean: `-a` = all connections, `-n` = numeric (don't resolve names), `-t` = TCP only, `-p` = show PID/program name. On web01, this reveals port 22 (SSHD) and port 80 (Apache2). [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Important:** The `-p` flag requires **root privileges** to display PID and process names. Without root, those columns appear blank. This is why the instructor switches to root before running the command. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**`ss -tunlp`** is the modern replacement for `netstat`. It provides the same information — open ports, associated PIDs, process names — but is faster and part of the `iproute2` suite. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**`nmap`** is fundamentally different from `netstat` and `ss`. While `netstat`/`ss` show open ports **on the local machine**, `nmap` scans open ports **on a remote target machine**. This is its primary purpose: remote port scanning. The instructor runs `nmap db01` and discovers ports 22 (SSH), 111 (rpcbind), and 3306 (MySQL/MariaDB) are open on db01. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

`nmap` is not installed by default — you must install it (`apt install nmap`). And critically: **use `nmap` carefully.** In some countries, port scanning is **illegal**. Even where legal, scanning public websites or networks you don't own can be considered hostile activity. Use it only for troubleshooting systems you are authorized to manage. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

The real-world troubleshooting pattern: when two machines can't connect, you use `nmap` (or `telnet`) from the source machine to check whether the required port on the target is actually open and reachable through any firewalls in between.

***

## 1.7 Mapping Processes to Ports — `ps -ef` and `grep`

Once you see a port is open via `netstat` or `ss`, you know the PID. But sometimes you need to go the other direction: you know a process, and you want to find out **which port it's using**. Or you want more details about the process behind a PID. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

`ps -ef` lists **all running processes** with full details. By piping it through `grep`, you can filter for a specific process name or PID. The instructor demonstrates: find the Apache2 process, note its PID, then grep the `netstat` output for that PID to confirm it's running on port 80. This bidirectional lookup — **port → process** and **process → port** — is a core troubleshooting skill. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

***

## 1.8 Routing and Gateways — `route`

Every machine needs to know **where to send packets** that are destined for networks it's not directly connected to. This is handled by the **routing table**, and the key concept is the **gateway** — the next-hop router that forwards traffic toward its destination. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

`route -n` displays the routing table with numeric addresses (no DNS resolution). It shows which gateway is used for each network interface. `route` without `-n` shows the same information but with resolved hostnames. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

The `route` command can also be used to **modify** the routing table (add or delete routes), but the instructor notes that in practice, it's most commonly used just to **view** gateways — to verify that the machine knows how to reach external networks.

***

## 1.9 ARP Table — `arp`

The **ARP (Address Resolution Protocol) table** maps IP addresses to **MAC (hardware) addresses** on the local network. The kernel maintains this table automatically. When your machine communicates with another machine on the same network segment, it needs the target's MAC address to construct Ethernet frames — even though it already knows the IP. ARP handles this translation. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

The `arp` command views (and can add entries to) this table. The instructor's example shows db01's IP mapped to its MAC address. This is useful for diagnosing low-level network issues like IP conflicts or ARP poisoning. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

***

## 1.10 Port-Level Connectivity Testing — `telnet`

While `nmap` scans all (or many) ports on a target, `telnet` tests connectivity to **one specific port**. You specify the target host and port number, and `telnet` attempts to open a TCP connection. If it says "Connected," the port is open and reachable. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

The instructor demonstrates: `telnet 192.168.40.12 3306` — this attempts to connect to MariaDB's port on db01. The connection succeeds (port is open), but MariaDB rejects the session because telnet isn't a proper MySQL client. The important takeaway: **"Connected" means the port is open and reachable** — it doesn't mean the service will accept your session. The instructor also tests port 22 (SSH), which both connects and responds with the SSH banner. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

To exit a telnet session: press `Ctrl+]` (Control + right square bracket), hit Enter, then type `quit`. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

⚠️ **Expert Note:** `telnet` is the simplest, most direct way to test "Can I reach this specific port from this specific machine?" It cuts through abstraction — no application-level client needed. In production troubleshooting, `telnet <host> <port>` is often the first thing you try when a service connection fails.

***

## 1.11 Additional Tools Mentioned

The instructor briefly mentions **`tcpdump`** and **`Wireshark`** as more advanced networking tools, but states that for **basic network troubleshooting**, the commands covered in the video are sufficient. These advanced tools capture and analyze actual network traffic (packet-level inspection) and are used for deeper diagnostic work. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

Also, the instructor notes a general principle: if any command is not found on your system, you can search the internet for the correct package name, install it, and the command becomes available. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Doing

We are executing a comprehensive set of Linux networking commands to **diagnose, inspect, and troubleshoot** network connectivity, name resolution, port availability, routing, and service-to-port mapping between two machines. The final operational outcome: you can independently determine whether two machines can talk to each other, identify where failures occur, and pinpoint which services are running on which ports.

**Lab:** Two Vagrant VMs — web01 (`192.168.40.11`, Apache2 on port 80) and db01 (`192.168.40.12`, MariaDB on port 3306). All commands are run from web01 unless stated otherwise.

***

## Step 0: Prepare the Environment

Log into web01 and switch to root. Many networking commands require root privileges to display full information (like process IDs).

```bash
vagrant ssh web01
sudo -i
```

**Why root:** Commands like `netstat -antp` won't show PID/process-name columns without root. You'll get incomplete output and may wrongly conclude that no process owns a port. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

***

## Step 1: View Your Own Network Interfaces and IP Addresses

### Command:

```bash
ifconfig
```

**Breakdown:** No flags needed. Displays all **active** network interfaces with their names and IP addresses. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Expected output:** Three interfaces on web01:

* NAT interface (`10.0.2.x` range) — VirtualBox's internet-access path
* Static IP interface (`192.168.40.11`) — the lab network address
* Loopback `lo` (`127.0.0.1`) — self-referencing interface

**Verification:** Confirm your static IP (`192.168.40.11`) appears. If it doesn't, the Vagrant network configuration has a problem.

### Alternative command:

```bash
ip addr show
```

**When to use:** If `ifconfig` returns "command not found." This is the modern equivalent. Same information, different format. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Connection to larger flow:** You need to know your own IP and network membership before you can test connectivity to other machines.

***

## Step 2: Test Connectivity to Another Machine

### Command:

```bash
ping 192.168.40.12
```

**Breakdown:**

* `ping` — the command
* `192.168.40.12` — target IP address (db01)

Sends ICMP packets continuously on Linux. Press `Ctrl+C` to stop. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Expected output:** Lines showing replies from `192.168.40.12`, and a summary showing packets transmitted, received, and `0% packet loss`.

**Verification:** 0% packet loss = connectivity confirmed.

**Common mistakes:**

* Forgetting that Linux ping runs indefinitely — you must `Ctrl+C`
* Misreading the summary — look at the loss percentage, not just whether packets appear

**Failure scenarios:** If 100% loss: check if db01 is running, check if IPs are on the same network, check for firewall rules blocking ICMP. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Connection to larger flow:** Ping confirms Layer 3 (IP-level) connectivity. Next steps test name resolution and port-level access.

***

## Step 3: Set Up Local Name Resolution

### Command:

```bash
vi /etc/hosts
```

Add this line:

```
192.168.40.12  db01
```

Save and exit. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**What this does:** Maps the name `db01` to IP `192.168.40.12` locally on this machine. No DNS server needed.

**Verification:**

```bash
ping db01
```

Should resolve to `192.168.40.12` and show replies.

**Common mistakes:** Typos in the IP address. Extra spaces or tab issues. Forgetting to save the file.

**Connection to larger flow:** From now on, you can use `db01` instead of typing the IP everywhere. This mimics how DNS works but at the local machine level.

***

## Step 4: Trace the Network Path (From Host Machine)

### Command (Windows):

```cmd
tracert www.google.in
```

### Command (Linux — from host, not VM):

```bash
traceroute www.google.in
```

**Breakdown:**

* `tracert` / `traceroute` — the command
* `www.google.in` — the destination [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Expected output:** A numbered list of hops (routers), each showing three latency values (for three packets sent) and the router's IP/hostname. The last hop is the destination.

**What to look for:**

* High latency at a specific hop = potential bottleneck at that point
* `* * *` at a hop = that router doesn't respond to traceroute probes (not necessarily a failure)
* All three packets showing high latency at the same hop = consistent problem

**Why from host machine:** VirtualBox NAT breaks the hop-discovery mechanism. Traceroute results from inside a VM are unreliable. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Connection to larger flow:** Traceroute answers "where is the problem?" when ping shows high latency or partial packet loss.

***

## Step 5: View Open Ports on the Local Machine

### Command:

```bash
netstat -antp
```

**Breakdown:**

* `netstat` — network statistics command
* `-a` — show all connections (listening + established)
* `-n` — numeric output (don't resolve hostnames — faster, clearer)
* `-t` — TCP connections only
* `-p` — show PID and program name owning each port [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Expected output on web01:**

* Port 22 — `sshd`
* Port 80 — `apache2`

**Verification:** Confirm the services you expect (Apache, SSH) are listed. If a service is missing, it's either not running or listening on a different port.

**Critical:** Must be run as **root** for the `-p` flag to show PIDs. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

### Alternative:

```bash
ss -tunlp
```

**Breakdown:**

* `ss` — socket statistics (modern replacement for netstat)
* `-t` — TCP
* `-u` — UDP
* `-n` — numeric
* `-l` — listening sockets only
* `-p` — show process info [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

Same information, faster execution, modern tool.

**Connection to larger flow:** Knowing what ports are open locally lets you verify your services are running. Next: scan remote ports.

***

## Step 6: Map a Process to Its Port (and Vice Versa)

### Finding the process behind a port:

From `netstat -antp` output, note the PID (e.g., `3333` for Apache2).

```bash
ps -ef | grep 3333
```

### Finding the port a process uses:

```bash
ps -ef | grep apache2
```

Note the PID, then:

```bash
netstat -antp | grep <PID>
```

 [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**What this achieves:** Bidirectional mapping — port→process and process→port. Essential when troubleshooting "what's running on this port?" or "is my service actually listening?"

***

## Step 7: Scan Ports on a Remote Machine

### Install nmap:

```bash
apt install nmap
```

### Scan localhost:

```bash
nmap localhost
```

### Scan a remote target:

```bash
nmap db01
```

**Expected output for db01:**

* Port 22 — SSH
* Port 111 — rpcbind
* Port 3306 — MySQL/MariaDB

 [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Operational use:** When two machines fail to connect, `nmap` from the source machine targeting the destination reveals whether the required port is open and reachable through all firewalls in between.

⚠️ **Expert Note:** Never run `nmap` against machines or networks you don't own or have explicit authorization to scan. In some jurisdictions, unauthorized port scanning is a criminal offense. Use it strictly for troubleshooting your own infrastructure. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

***

## Step 8: Test Connectivity to a Specific Port

### Command:

```bash
telnet 192.168.40.12 3306
```

**Breakdown:**

* `telnet` — the command
* `192.168.40.12` — target IP (db01)
* `3306` — target port (MariaDB) [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Expected result:** "Connected" message — confirms port 3306 is open on db01. MariaDB then rejects the telnet session (because telnet isn't a MySQL client), but that's irrelevant — the connectivity test succeeded.

### Test SSH port:

```bash
telnet 192.168.40.12 22
```

Shows "Connected" and the SSH banner.

### Exiting telnet:

Press `Ctrl+]`, hit Enter, type `quit`. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**When to use over nmap:** When you already know which specific port you need to test. `telnet` is faster and more targeted than a full `nmap` scan.

**Connection to larger flow:** `telnet` is the definitive "can I reach this specific service from here?" test.

***

## Step 9: DNS Queries

### Command:

```bash
dig www.google.com
```

Shows the A record (IPv4 address), the DNS server that answered, and detailed query metadata. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

### Alternative:

```bash
nslookup www.google.com
```

Shows name, IPv4, IPv6, and the resolving DNS server with its port. Simpler output, older tool. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Operational use:** When a service is reachable by IP but not by hostname, run `dig` or `nslookup` to verify DNS resolution is working.

***

## Step 10: View Routing Table and Gateways

### Command:

```bash
route -n
```

**Breakdown:**

* `route` — display/modify routing table
* `-n` — numeric output (no DNS resolution) [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Expected output:** Shows the gateway for each network interface. This tells you where outbound traffic for each network is directed.

**Without `-n`:**

```bash
route
```

Same info but with resolved hostnames (slower).

***

## Step 11: View the ARP Table

### Command:

```bash
arp
```

Shows IP-to-MAC-address mappings maintained by the kernel. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Expected output:** db01's IP (`192.168.40.12`) mapped to its MAC address.

**Operational use:** Diagnosing Layer 2 issues — IP conflicts, ARP spoofing, or verifying that the machine is actually communicating with the intended hardware address.

***

## Step 12: Live Path Tracing with Packet Loss Detection

### Command:

```bash
mtr www.google.com
```

**What it does:** Continuously traces the route and shows **live packet loss** at each hop. The display updates dynamically. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**What to look for:**

* Any hop showing persistent packet loss → that's the problem location
* 100% loss starting at a hop → the path is broken at that point
* Helps distinguish: local network problem vs. ISP problem vs. server problem vs. internet backbone problem

Press `Ctrl+C` to stop. [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

**Same VM caveat as traceroute:** Results from inside VirtualBox VMs may be unreliable. Best run from the host machine.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ Command Classification by Purpose

```
WHAT IS MY IDENTITY?
├── ifconfig              → Show my interfaces + IPs
└── ip addr show          → Modern equivalent

CAN I REACH THE TARGET?
├── ping <IP/host>        → ICMP connectivity test (Layer 3)
├── telnet <host> <port>  → Specific port reachability (Layer 4)
└── nmap <host>           → Scan ALL open ports on target (Layer 4)

HOW DO I REACH THE TARGET?
├── traceroute / tracert  → One-time path trace + latency per hop
└── mtr                   → Live continuous path trace + packet loss

WHAT IS RUNNING ON MY MACHINE?
├── netstat -antp         → Open TCP ports + PIDs (needs root for -p)
├── ss -tunlp             → Modern netstat replacement
└── ps -ef | grep <X>     → Process details ↔ port mapping

CAN NAMES RESOLVE TO IPs?
├── /etc/hosts            → Local static name→IP mapping
├── dig <domain>          → DNS lookup (detailed, modern)
└── nslookup <domain>     → DNS lookup (simple, older)

WHAT IS MY NETWORK ROUTING?
├── route -n              → Gateways + routing table
└── arp                   → IP→MAC mappings (Layer 2)
```

***

## 🔗 Troubleshooting Decision Chain

```
"Service X on Machine B is unreachable from Machine A"

Step 1: ping B                    → Is B reachable at all?
        ├── YES → go to Step 2
        └── NO  → Check: Is B running? IPs on same network? Firewall blocking ICMP?

Step 2: nmap B  OR                → Is the specific port open on B?
        telnet B <port>
        ├── OPEN → go to Step 3
        └── CLOSED → Service not running, wrong port, or firewall blocking

Step 3: On Machine B:             → Is the service actually listening?
        netstat -antp | grep <port>
        ├── LISTENING → Check application-level auth/config
        └── NOT LISTED → Service crashed or misconfigured

Step 4: traceroute/mtr B          → Where is latency or packet loss?
        └── Identifies exact hop causing problems
```

***

## ⚡ Instant Recall Pairs

```
View my IPs              → ifconfig / ip addr show
Test basic connectivity   → ping
Test specific port        → telnet <host> <port>
Scan remote ports         → nmap <host>  (install first, use carefully)
Local open ports + PIDs   → netstat -antp  (as root)
Modern netstat            → ss -tunlp
Trace path + latency      → traceroute (one-shot) / mtr (live)
DNS working?              → dig / nslookup
Local name→IP override    → /etc/hosts
View gateways             → route -n
View MAC mappings         → arp
Process ↔ Port lookup     → ps -ef | grep + netstat -antp | grep
```

***

## 🏗️ Reusable Engineering Patterns

**Pattern 1: Layer-by-Layer Diagnosis**
Network troubleshooting always moves through layers: L2 (ARP/MAC) → L3 (IP/ping) → L4 (port/telnet) → L7 (application). Never skip layers — start with ping, then check ports, then check the service.

**Pattern 2: Local vs. Remote Inspection**
`netstat`/`ss` = inspect **your own machine's** state. `nmap`/`telnet` = inspect a **remote machine's** state. Confusing which perspective you're looking from is a common troubleshooting mistake.

**Pattern 3: Dual-Direction Mapping**
Port → Process (`netstat` → find PID → `ps -ef | grep PID`). Process → Port (`ps -ef | grep name` → find PID → `netstat | grep PID`). Both directions are needed in different scenarios.

**Pattern 4: Older Tool → Modern Replacement**
`ifconfig` → `ip addr show` | `netstat` → `ss` | `nslookup` → `dig` | `traceroute` → `mtr`. Know both — legacy docs use old tools, new systems ship with new ones.

**Pattern 5: Root Privilege Gate**
Many networking commands produce **incomplete output without root**. If output looks wrong or missing fields, check if you're running as root before assuming a problem.

***

## 🧱 Lab Architecture (Quick Recall)

```
┌─────────────────────┐         ┌─────────────────────┐
│       web01         │         │        db01         │
│  192.168.40.11      │◄───────►│  192.168.40.12      │
│  Apache2 :80        │  ping   │  MariaDB :3306      │
│  SSHD    :22        │  telnet │  SSHD    :22        │
│  Ubuntu             │  nmap   │  rpcbind :111       │
└─────────────────────┘         └─────────────────────┘
        │                               │
        └──── Both on 192.168.40.x ─────┘
        └──── Both on 10.0.2.x (NAT) ──┘
        └──── Both have lo: 127.0.0.1 ──┘
```

***

## 🎯 One-Line System Summary

> **These commands answer a layered set of diagnostic questions: Who am I on the network? → Can I reach the target? → How does my traffic get there? → What ports are open? → What services own those ports? → Is DNS working? — each tool targeting a specific layer of the network stack.** [\[77-network...g-commands \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/77-networking-commands.txt)

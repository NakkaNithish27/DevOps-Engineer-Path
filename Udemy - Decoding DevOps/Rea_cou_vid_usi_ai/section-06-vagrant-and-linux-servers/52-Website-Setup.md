**Source:** [52-website-setup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/52-website-setup.txt?EntityRepresentationId=6919eacd-2547-4807-9e87-ffbb5c07c0ee) — Video lecture on Linux server management: deploying an HTML website on CentOS using httpd

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 Where This Fits — Linux Server Management as the Next Layer

Up until this point in the course, the learner has covered foundational Linux skills: file systems, filters, users and groups, sudo, software management, services, and processes. All of that was **operating system literacy** — knowing how to navigate and control a Linux machine. This lecture transitions into **server management**, which is fundamentally different in intent. Server management is about making a Linux machine *serve something to others* — transforming it from a personal workstation into a network-accessible service provider. The specific task here is deploying a web server that hosts an HTML website, which is one of the simplest and most universal examples of server management. This same pattern — install, configure, deploy, validate — recurs in every service you'll ever manage on Linux, whether it's a database server, an application server, or a message queue.

The instructor explicitly frames this as a **confidence-building exercise** and a precursor to doing the same thing on AWS Cloud later. The progression is: manual setup first → automation (Vagrant provisioning) later. This is a deliberate pedagogical pattern: understand the manual process deeply before automating it, so you know what the automation is actually doing underneath.

## 1.2 httpd — The Web Server Package on CentOS

On CentOS (and RHEL-family systems), the Apache HTTP Server is packaged and referred to as **httpd**. This is both the **package name** (what you install via `yum`) and the **service name** (what you manage via `systemctl`). On Ubuntu/Debian-family systems, the exact same underlying software is packaged and referred to as **apache2** — both the package name and service name become `apache2`. This is a critical distinction that trips up beginners who switch between distributions. The software is identical; only the naming convention differs due to different packaging traditions.

httpd's core job is simple: it listens on a network port (default: port 80 for HTTP), and when a browser sends a request, it looks up the corresponding file on disk and sends it back. The *where* it looks on disk is the **document root**, discussed next.

## 1.3 The Document Root — `/var/www/html/`

The document root is the directory on the server's filesystem that the web server maps to the root URL (`/`). For httpd on CentOS, this is `/var/www/html/` by default. When a browser requests `http://192.168.56.22/`, httpd looks inside `/var/www/html/` for a file to serve. This is not arbitrary — it is configured in httpd's configuration files, but the default is this path, and for basic deployments you simply place your content there.

The relationship is direct: **filesystem path maps to URL path**. A file at `/var/www/html/images/logo.png` becomes accessible at `http://<server-ip>/images/logo.png`. Understanding this mapping is the foundation of all web server administration.

## 1.4 `index.html` — The Default Served File

When a browser requests a directory (like the root `/`), httpd does not show a directory listing by default. Instead, it looks for a file named **`index.html`** inside that directory and serves it automatically. This is why the instructor creates a file called exactly `index.html` inside `/var/www/html/` — not `home.html`, not `main.html`, but specifically `index.html`. The name is a convention enforced by the web server's configuration (the `DirectoryIndex` directive). If `index.html` does not exist, httpd either shows its default test page (if nothing is in the document root) or returns an error/listing depending on configuration.

The default httpd test page — the one you see immediately after installing and starting httpd with an empty document root — is a built-in fallback page. It confirms the server is running but explicitly tells you: "add your content to `/var/www/html/`." Once you place an `index.html` file there, it takes over.

## 1.5 Service Lifecycle — Start, Enable, Restart, Reload

Linux services managed by `systemd` have a lifecycle that is crucial to internalize:

**Start** (`systemctl start httpd`) — launches the service process right now, in the current session. If you reboot the machine, the service will **not** come back up automatically. Starting is a *runtime-only* action.

**Enable** (`systemctl enable httpd`) — creates a symbolic link so that the service is automatically started at boot time. Enable does **not** start the service right now; it only ensures it will start on the next reboot. This is why you almost always need both `start` and `enable` together for a new service.

**Restart** (`systemctl restart httpd`) — stops and then starts the service. This is necessary whenever you change the service's configuration or the content it serves, because the running process may be caching the old state. The instructor emphasizes this as a **thumb rule**: whenever you make a change, restart (or at least reload) the service.

**Reload** — tells the service to re-read its configuration without fully stopping. Not all services support reload, but httpd does. Reload is gentler than restart (no downtime), but restart is safer when you're unsure.

> ⚠️ **Expert Note:** In production, you prefer `reload` over `restart` to avoid dropping active connections. But during learning and development, `restart` is simpler and ensures a clean state.

## 1.6 Dependencies — The First Step in Any Server Setup

Before a server can function, its **dependencies** must be installed. Dependencies are the packages that the service needs either directly or that you need for the setup process. In this exercise, the dependencies are:

| Package | Why It's Needed                                             |
| ------- | ----------------------------------------------------------- |
| `httpd` | The web server itself                                       |
| `wget`  | To download the HTML template zip file from the internet    |
| `vim`   | To edit configuration files or content                      |
| `unzip` | To extract the downloaded zip archive                       |
| `zip`   | Not strictly needed here, but installed for general utility |

The instructor makes a key conceptual point: **"The first thing always is to install the dependencies."** This is a universal server deployment principle. Before you start configuring or deploying anything, ensure all the tools and packages you'll need are present. Skipping this step leads to mid-process failures.

## 1.7 Firewall (`firewalld`) and Its Effect on Service Accessibility

A running web server is useless if the firewall blocks incoming connections to it. On CentOS, the firewall service is `firewalld`. The instructor notes a platform-specific behavior:

* **CentOS on Windows (VirtualBox):** `firewalld` is typically **inactive** by default, so no action needed.
* **Fedora on Mac (VMware):** `firewalld` is typically **active** by default, and you must stop and disable it or the website won't be accessible from outside the VM.

The commands are `systemctl stop firewalld` (stop it now) and `systemctl disable firewalld` (prevent it from starting on boot). The instructor explicitly warns: **in production, shutting down the firewall entirely is bad practice**. The correct approach is to open specific ports (like port 80 for HTTP). But for this learning exercise, the focus is on provisioning, not firewall rule management, which is covered later.

> 🔍 **Deep Dive:** The reason firewalld blocks httpd by default is defense-in-depth. A fresh server should expose nothing until explicitly told to. You'd normally run `firewall-cmd --add-service=http --permanent` followed by `firewall-cmd --reload` to allow HTTP traffic while keeping the firewall active.

## 1.8 Networking — Static IP and Access from the Browser

The Vagrant VM is configured with a **private network static IP** (e.g., `192.168.56.22`). This IP is what allows the host machine's browser to reach the web server running inside the VM. The instructor warns: **make sure this IP doesn't collide with other existing VMs** — IP conflicts cause network failures for both VMs. The recommendation to delete old VMs before starting is specifically to avoid this.

The `10.0.x.x` IP that also appears on the VM is the **NAT adapter** IP — it's used for the VM's outbound internet access (so `wget` can download files) but is not routable from the host machine. You must use the `192.168.x.x` IP (private network) or a bridged/public IP to access the web server from your browser.

## 1.9 The Four-Step Server Deployment Methodology

At the end of the exercise, the instructor distills the entire process into a **four-step methodology** that applies universally to any Linux service deployment:

1. **Install dependencies/packages** — get all required software onto the machine
2. **Manage the service** — start it, enable it for boot persistence
3. **Configuration changes** — modify config files if needed (in this exercise, none were needed, but in real deployments this step is almost always present)
4. **Deploy the data** — place the actual content/application into the correct location and restart the service

This is a **reusable mental model**. Whether you're deploying MySQL, Nginx, Jenkins, or a custom application, the pattern is the same: install → manage service → configure → deploy. The instructor explicitly says this methodology will be formalized further after the WordPress exercise.

## 1.10 The Template Download Workflow — Finding the Real Download Link

The HTML templates are hosted on `tooplate.com`. The instructor recommends **Brave browser** specifically because it blocks marketing popups and makes it easier to find the download link.

The critical skill taught here is: **the visible "Download" button on a website does not always give you a direct download URL**. The link you get from "Copy Link Address" may be a redirect, a JavaScript trigger, or a tracking URL — not the actual file URL. To get the **real download link**, you must:

1. Open browser Developer Tools (F12)
2. Go to the **Network** tab
3. Click the Download button on the page
4. Find the `.zip` request in the Network tab
5. Click on it → go to **Headers** → find the actual request URL

This is the URL you feed to `wget` on the server. This technique is transferable to any situation where you need to find the real download URL behind a website's UI.

## 1.11 Why `/tmp` for Temporary Downloads

The instructor deliberately downloads the zip file into `/tmp`, not into `/var/www/html` or the home directory. The reasoning is explicit: this is a **temporary file** — you need it only long enough to unzip and copy the contents. `/tmp` is the standard Linux location for transient files. It keeps the filesystem clean and signals intent: anything in `/tmp` is disposable.

## 1.12 Course Roadmap Context — Manual → Automation → Cloud

The lecture establishes a clear progression path:

1. **Manual setup on CentOS** (this lecture — HTML template with httpd)
2. **Manual setup on Ubuntu** (next — WordPress on LAMP stack: Linux + Apache + MySQL + PHP)
3. **Automation via Vagrant provisioning** (both setups automated into Vagrantfiles)
4. **Cloud deployment on AWS** (same concepts, cloud infrastructure)

This progression ensures the learner understands the *why* and *how* before the automation layer abstracts it away. The two Vagrantfiles produced at the end represent the automation of everything done manually in the first two exercises.

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are setting up a **web server on a CentOS virtual machine** that serves a pre-built HTML website template downloaded from the internet. The final outcome: opening a browser on the host machine and seeing a fully styled, professional-looking website served from the CentOS VM.

## Step 1: Clean Up Existing VMs

Before starting, ensure no other Vagrant VMs are running that might cause IP conflicts.

```bash
vagrant global-status
```

This lists all tracked Vagrant VMs across your machine. If any are running, navigate to their directories and destroy them:

```bash
vagrant destroy
```

**Why:** IP collisions between VMs cause network failures. Starting clean eliminates this risk.

## Step 2: Create the Project Directory

```bash
mkdir -p F:\vagrant-vms\finance
cd F:\vagrant-vms\finance
```

* `mkdir -p` — creates the directory (and parent directories if needed)
* The folder name `finance` matches the chosen template name from tooplate.com — a naming convention for project clarity
* You can choose any folder path you prefer

## Step 3: Initialize the Vagrant VM

First, confirm you have a CentOS box available:

```bash
vagrant box list
```

This shows all locally cached Vagrant boxes. You should see a `eurolinux` CentOS box.

Now initialize:

```bash
vagrant init eurolinux/centos-stream-9
```

* `vagrant init` — generates a `Vagrantfile` in the current directory
* `eurolinux/centos-stream-9` — specifies which box (OS image) to use

**What happens internally:** A `Vagrantfile` (Ruby-based configuration file) is created with default settings. This file defines the VM's configuration.

## Step 4: Configure the Vagrantfile

Open the Vagrantfile in any editor (Notepad, Vim, etc.) and make two changes:

**a) Set a static private IP:**

```ruby
config.vm.network "private_network", ip: "192.168.56.22"
```

* This gives the VM a fixed IP on a host-only network, accessible from your host browser
* **Critical:** Ensure this IP is not used by another VM

**b) Set RAM to 1 GB:**

```ruby
config.vm.provider "virtualbox" do |vb|
  vb.memory = "1024"
end
```

Save and close the file.

## Step 5: Bring Up the VM

```bash
vagrant up
```

This downloads the box (if not cached), creates the VM in VirtualBox, boots it, and configures networking per the Vagrantfile. Wait for it to complete.

Then log in:

```bash
vagrant ssh
```

Switch to root:

```bash
sudo -i
```

**Why root:** Package installation, service management, and writing to `/var/www/html` require root privileges.

## Step 6 (Optional): Change the Hostname

```bash
vi /etc/hostname
```

Replace the content with `finance`, then run:

```bash
hostname finance
```

Log out and log back in to see the new hostname in the prompt. This is **not mandatory** — it's purely for readability and identification when managing multiple VMs.

## Step 7: Install Dependencies

```bash
yum install httpd wget vim unzip zip -y
```

**Command breakdown:**

| Part          | Meaning                                            |
| ------------- | -------------------------------------------------- |
| `yum install` | CentOS package manager install command             |
| `httpd`       | Apache web server                                  |
| `wget`        | Command-line file downloader                       |
| `vim`         | Text editor                                        |
| `unzip`       | Zip archive extractor                              |
| `zip`         | Zip archive creator (not strictly needed here)     |
| `-y`          | Auto-confirm all prompts (skip "yes/no" questions) |

**What happens internally:** `yum` resolves dependencies for each package, downloads them from configured repositories, and installs them.

**Verification:** No errors in the output. You can verify individual packages with `rpm -q httpd` etc.

**Connection to larger flow:** This is **Step 1 of the 4-step deployment methodology** — install dependencies before doing anything else.

## Step 8: Start and Enable httpd

```bash
systemctl start httpd
systemctl enable httpd
```

* `start` — launches httpd right now (begins listening on port 80)
* `enable` — ensures httpd starts automatically on every future boot

**Verification:**

```bash
systemctl status httpd
```

You should see `active (running)`. Press `q` to quit the status view.

**Connection to larger flow:** This is **Step 2** — manage the service.

## Step 9: Verify the Default Page from Browser

Get the VM's IP:

```bash
ip addr show
```

Look for the `192.168.56.22` IP (or whichever you configured). **Ignore** the `10.0.x.x` NAT IP.

Open a browser on your host machine and navigate to:

```
http://192.168.56.22
```

You should see the **default httpd test page** — a page that says the server is working and instructs you to add content to `/var/www/html/`.

## Step 10: Test with a Simple `index.html`

```bash
cd /var/www/html/
vi index.html
```

Type any text, e.g.: `This is my first website setup`

Save and exit (`:wq`). Then restart the service:

```bash
systemctl restart httpd
```

Refresh the browser — you should see your text instead of the default page.

**Why this step matters:** It proves the document root → browser mapping works. It builds understanding before deploying the real template. This is a **diagnostic checkpoint**, not a production step.

## Step 11: Get the Template Download Link

1. Open `tooplate.com` in **Brave browser** (to avoid popups)
2. Choose a template (e.g., "Mini Finance")
3. Press **F12** to open Developer Tools
4. Click the **Network** tab
5. Click the **Download** button on the page
6. In the Network tab, find the `.zip` request
7. Click it → **Headers** → copy the full URL

This gives you the **direct download URL** for the zip file.

## Step 12: Download the Template to the VM

```bash
cd /tmp
wget <paste-the-download-URL>
```

**Command breakdown:**

* `cd /tmp` — navigate to the temp directory (appropriate for transient downloads)
* `wget <URL>` — downloads the file from the URL and saves it in the current directory

**Verification:** `ls` should show the `.zip` file in `/tmp`.

## Step 13: Unzip and Deploy

```bash
unzip <filename>.zip
ls
cd <unzipped-folder-name>
ls
```

Verify you can see the template contents including `index.html`.

Now copy everything to the document root:

```bash
cp -r * /var/www/html/
```

**Command breakdown:**

| Part             | Meaning                                                       |
| ---------------- | ------------------------------------------------------------- |
| `cp`             | Copy command                                                  |
| `-r`             | Recursive — includes subdirectories (images, css, js folders) |
| `*`              | All files and folders in the current directory                |
| `/var/www/html/` | Destination — the httpd document root                         |

When prompted to overwrite `index.html`, type **yes** — you're replacing the test file from Step 10 with the real template's `index.html`.

**Verification:**

```bash
ls /var/www/html/
```

You should see all the template files (css, js, images, index.html, etc.).

**Connection to larger flow:** This is **Step 4** — deploy the data.

## Step 14: Final Restart and Validation

```bash
systemctl restart httpd
```

Now perform the **validation checklist:**

```bash
systemctl status httpd          # Service should be active (running)
ls /var/www/html/               # Content should be present
systemctl status firewalld      # Should be inactive (on CentOS/Windows)
```

If `firewalld` is active (Fedora/Mac scenario):

```bash
systemctl stop firewalld
systemctl disable firewalld
```

Finally, get the IP and check from the browser:

```bash
ip addr show
```

Navigate to `http://192.168.56.22` — you should see the **fully styled website template**.

> ⚠️ **Expert Note:** The validation checklist — service status, content presence, firewall state, IP verification — is a transferable pattern. For any service that isn't working, walk through these four checks systematically. Most "it doesn't work" problems are one of: service not running, content not in the right place, firewall blocking, or wrong IP.

## Step 15: Cleanup

```bash
exit                  # Exit root shell
exit                  # Exit vagrant SSH
vagrant halt          # Power off the VM
vagrant destroy       # Delete the VM entirely
```

The instructor explicitly says to **destroy the VM** after completing the exercise — it's not needed anymore and keeps the environment clean for the next exercise (WordPress on Ubuntu).

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## 🏗️ System Architecture

```
Host Machine (Windows/Mac)
│
├── Vagrant (VM orchestrator)
│   └── Vagrantfile (config: box, IP, RAM)
│
├── VirtualBox (hypervisor)
│   └── CentOS VM
│       ├── httpd (web server, port 80)
│       │   └── Document Root: /var/www/html/
│       │       └── index.html + assets (css/js/images)
│       ├── firewalld (must be inactive for access)
│       └── Network Interfaces:
│           ├── 10.0.x.x (NAT — outbound internet only)
│           └── 192.168.56.22 (private — host ↔ VM)
│
└── Browser → http://192.168.56.22 → httpd → /var/www/html/index.html
```

## 🔄 The Universal 4-Step Server Deployment Pattern

```
1. INSTALL DEPENDENCIES  →  yum install <packages> -y
2. MANAGE SERVICE        →  systemctl start|enable <service>
3. CONFIGURE             →  edit config files (skipped here, none needed)
4. DEPLOY DATA           →  copy content → document root → restart service
```

*This pattern applies to ANY Linux service deployment.*

## ⚡ Operational Flow (This Exercise)

```
Clean old VMs
  → mkdir project dir → vagrant init <box>
    → edit Vagrantfile (IP + RAM)
      → vagrant up → vagrant ssh → sudo -i
        → yum install httpd wget vim unzip zip -y
          → systemctl start httpd → systemctl enable httpd
            → (test with dummy index.html → verify in browser)
              → F12 Network tab → get real download URL
                → cd /tmp → wget <URL>
                  → unzip → cd <folder> → cp -r * /var/www/html/
                    → systemctl restart httpd
                      → VALIDATE: status + content + firewall + IP
                        → Browser: http://192.168.56.22 ✓
```

## 🔑 Key Mappings to Remember

```
CentOS package/service name  →  httpd
Ubuntu package/service name  →  apache2
(Same software, different naming)

Document root                →  /var/www/html/
Default served file          →  index.html
Temp downloads go to         →  /tmp

start   = run NOW (session only)
enable  = run on BOOT (persistent)
restart = apply changes (stop + start)

10.0.x.x IP  = NAT (ignore for browser access)
192.168.x.x  = Private network (use this)
```

## 🛡️ Validation Checklist (Reusable for Any Service)

```
□ Service running?        →  systemctl status <service>
□ Content deployed?       →  ls <document-root>
□ Firewall blocking?      →  systemctl status firewalld
□ Correct IP?             →  ip addr show (use private, not NAT)
```

## 🔗 Dependency Chain

```
Website visible in browser
  ← httpd running + enabled
    ← content in /var/www/html/
      ← cp -r from unzipped template
        ← unzip archive
          ← wget downloaded zip
            ← real URL found via F12 → Network → Headers
              ← tooplate.com (Brave browser recommended)
    ← firewalld inactive
    ← correct IP (private network, not NAT)
```

## 🧩 Reusable Engineering Patterns Extracted

| Pattern                                     | Instance in This Exercise                                            |
| ------------------------------------------- | -------------------------------------------------------------------- |
| **Install → Configure → Deploy → Validate** | The 4-step methodology                                               |
| **Document root mapping**                   | Filesystem path ↔ URL path (any web server)                          |
| **Convention-based defaults**               | `index.html` auto-served without explicit config                     |
| **Runtime vs persistent state**             | `start` vs `enable` — session vs boot                                |
| **Manual-first → automate-later**           | Understand manually, then write Vagrantfile provisioning             |
| **Temp workspace for transient artifacts**  | `/tmp` for downloads you won't keep                                  |
| **Validation as a systematic checklist**    | Service + content + firewall + network                               |
| **Platform-aware execution**                | CentOS→httpd vs Ubuntu→apache2; firewalld behavior varies by host OS |

## 🗺️ Course Progression Map

```
[THIS LECTURE] Manual HTML on CentOS (httpd)
       ↓
[NEXT] Manual WordPress on Ubuntu (LAMP: apache2 + MySQL + PHP)
       ↓
[THEN] Automate both via Vagrant provisioning (2 Vagrantfiles)
       ↓
[LATER] Same concepts on AWS Cloud
```

# 🎓 Jenkins, Nexus & SonarQube Setup — Deep Learning Material

*Reconstructed from the video caption file* [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. The Architecture We Are Building

This video is about setting up two critical servers in a CI/CD pipeline — **Nexus Server** and **SonarQube Server** — each on its own AWS EC2 instance. These servers don't operate in isolation; they are designed to work **together with Jenkins**, which was already set up in a prior lecture. The three servers form a triad: Jenkins orchestrates the pipeline, Nexus stores the built artifacts (compiled code packages), and SonarQube analyzes the source code for quality and bugs. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

The instructor draws an explicit architectural parallel to the **VProfile project** that was built earlier in the course. In VProfile, the pattern was: **NGINX (frontend) → Tomcat (application server) → MySQL (database)**, and each component ran on a **separate machine**. SonarQube follows the same three-tier pattern — **NGINX (frontend) → SonarQube (application) → PostgreSQL (database)** — but with one key difference: **all three services run on a single machine**. This is an important architectural decision. In a learning environment, consolidating services onto one instance saves cost and simplifies management. In production, you would typically separate them for scalability and fault isolation. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

> 🔍 **Deep Dive (Optional)**
> The reason SonarQube uses PostgreSQL instead of MySQL is a design choice by the SonarQube project — PostgreSQL is the recommended and most commonly used database backend for SonarQube. The VProfile project used MySQL because its Java/Spring application was designed for it. These are not interchangeable decisions; each application dictates its own database requirements.

***

## 2. User Data Scripts — Automating Server Setup

Instead of manually SSH-ing into each EC2 instance and running commands one by one, the instructor uses **user data scripts**. A user data script is a shell script that AWS EC2 executes **automatically at first boot** of the instance. You paste it during instance launch, and EC2 runs it as the `root` user once the machine starts. This is the same technique used earlier in the course to set up Tomcat. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

The scripts live in a GitHub repository at `github.com/hkcoder/vprofile-project`, on the **atom** branch, inside a folder called `user data`. There are two scripts: [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

*   **`nexus-setup.sh`** — sets up the Nexus server
*   **`sonar-setup.sh`** — sets up SonarQube along with PostgreSQL and NGINX

The general pattern of both scripts follows the same logical structure used for Tomcat setup earlier: **install JDK → download the binary → create a dedicated system user → create a systemd service file → start and enable the service**. This pattern is repeated across almost every service in Linux-based DevOps, so recognizing it is important. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

## 3. What the Nexus Setup Script Does

The `nexus-setup.sh` script performs these operations in order: [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

1.  Downloads the package signing key and sets up the repository file (so `yum`/`dnf` knows where to find the packages)
2.  Installs **JDK 17** (Nexus requires Java to run)
3.  Creates the `/opt/nexus` directory
4.  Downloads the Nexus binary and extracts it
5.  Creates a dedicated **Nexus user** (a system user that owns and runs the Nexus process)
6.  Creates a **systemd service file** for Nexus (so you can manage it with `systemctl start nexus`, `systemctl enable nexus`, etc.)
7.  Starts and enables the Nexus service

This is straightforward and follows the same pattern as Tomcat setup. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

## 4. What the SonarQube Setup Script Does

The `sonar-setup.sh` script is more complex because it sets up **three services on one machine**: SonarQube itself, PostgreSQL (the database), and NGINX (the reverse proxy frontend). [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

### 4a. Operating System–Level Changes (sysctl.conf and limits.conf)

Before anything else, the script makes **OS-level kernel tuning changes**. This is necessary because SonarQube is resource-hungry — it consumes significant memory and opens many files during code analysis. By default, Linux limits how many files a process can open and how large those files can be. These defaults are too restrictive for SonarQube. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

Two files are modified:

*   **`/etc/sysctl.conf`** — Controls kernel parameters. The script increases the **maximum file size** that can be opened by processes. This is a system-wide setting.
*   **`/etc/security/limits.conf`** — Controls per-user/per-process resource limits. The script sets how many files the **SonarQube process specifically** is allowed to open simultaneously.

These changes come directly from the **SonarQube official documentation**. They are not arbitrary — without them, SonarQube will either fail to start or crash under load. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**Critically**, after making these changes, the machine **must be rebooted** for the new kernel parameters to take effect. This is why the script includes a `reboot` command at the very end. This reboot is the reason the SonarQube instance takes longer to become available than Nexus. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

> 🔍 **Deep Dive (Optional)**
> `sysctl.conf` controls parameters in the `/proc/sys/` virtual filesystem — these are runtime kernel tuning knobs. `limits.conf` is read by PAM (Pluggable Authentication Modules) and applies when a user session is created. Both are standard Linux mechanisms for resource tuning, and you'll encounter them whenever deploying resource-intensive applications like Elasticsearch, SonarQube, or large database servers.

### 4b. JDK and PostgreSQL Installation

After the OS-level changes, the script installs **JDK** (SonarQube is a Java application), then installs and starts **PostgreSQL**. The database setup mirrors what was done with MySQL for VProfile: create a database, create a user (`sonar`), set a password (`admin123`), and grant privileges to that user on the database. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

### 4c. SonarQube Application Setup

The SonarQube application itself is set up the same way as Nexus or Tomcat: download binary → extract → create dedicated system user → create systemd file → start and enable. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

### 4d. The sonar.properties File

SonarQube has a configuration file called **`sonar.properties`**. This is the equivalent of the `application.properties` file in a Spring/VProfile application. It contains the **database connection details** — specifically the database username and password — so SonarQube knows how to connect to PostgreSQL. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

### 4e. NGINX as a Reverse Proxy

NGINX is installed as the **frontend reverse proxy**. It listens on **port 80** (standard HTTP) and forwards all requests internally to **port 9000**, which is SonarQube's native web port. This means when you access SonarQube from a browser, you just use the IP address without specifying a port — it defaults to port 80, and NGINX handles the routing. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

NGINX is restarted after configuration, and then the final `reboot` command runs to apply the OS-level changes made at the beginning of the script. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

## 5. Service Port Numbers

The instructor explicitly lists the port numbers for each service in the ecosystem. These are essential to memorize because they directly affect security group rules, firewall configuration, and inter-service communication: [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

| Service                   | Port | Notes                                    |
| ------------------------- | ---- | ---------------------------------------- |
| **Jenkins**               | 8080 | Web UI and API                           |
| **Nexus**                 | 8081 | Web UI and artifact upload/download      |
| **Tomcat**                | 8080 | Application server (VProfile)            |
| **SonarQube**             | 9000 | Native web port (internal)               |
| **NGINX** (for SonarQube) | 80   | Reverse proxy — externally accessed port |

SonarQube's port 9000 is configurable via its configuration file, but port 80 is what external clients (browsers, Jenkins) connect to because NGINX sits in front. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

## 6. Security Groups — Controlling Inter-Service Communication

This is one of the most important concepts in the video. AWS Security Groups act as **virtual firewalls** around each EC2 instance. Every rule you add explicitly allows traffic; anything not allowed is **denied by default**.

The key insight the instructor emphasizes is that these three servers (Jenkins, Nexus, SonarQube) need to **talk to each other**, and you must explicitly allow that communication through security group rules. Simply having them in the same AWS account or even the same VPC is **not enough** — the security group must permit the traffic. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

### The Communication Flows

**Jenkins → Nexus (port 8081):** Jenkins uploads built artifacts to Nexus. So the Nexus security group must allow inbound traffic on port 8081 from the Jenkins security group. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**Jenkins → SonarQube (port 80):** Jenkins sends code analysis results to SonarQube. So the SonarQube security group must allow inbound traffic on port 80 from the Jenkins security group. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**SonarQube → Jenkins (port 8080):** This is the one people miss. The communication is **bidirectional**. After SonarQube finishes analyzing the code, it sends back the result status (pass/fail) to Jenkins on port 8080. So the Jenkins security group must also allow inbound traffic on port 8080 from the SonarQube security group. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

The instructor explicitly calls this out as a **separate step** that must be done after both servers are created — you go back to the Jenkins security group and add a new inbound rule for port 8080 from the SonarQube security group. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

> ⚠️ **Expert Note**
> Referencing security groups by their **group ID** (rather than by IP address) is an AWS best practice. EC2 instances get new public IPs on every stop/start cycle (unless you use Elastic IPs). By referencing the security group itself, the rule remains valid regardless of IP changes. This is exactly what the instructor does throughout.

***

## 7. Nexus as a Software Repository

The instructor briefly explains that **Nexus is a software repository**. When you click "Browse" in the Nexus web UI, you can see different repositories. In later lectures, the instructor will show how to **create custom repositories** and **store artifacts** (compiled packages from your build pipeline) in Nexus. This is Nexus's core purpose — it's a centralized place to store, version, and retrieve build artifacts so that deployment pipelines can pull from a known, reliable source. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

## 8. SonarQube Dashboard and Jenkins Integration

The instructor previews that SonarQube will be used **automatically from Jenkins** — Jenkins will create projects in SonarQube and upload code analysis results. The SonarQube dashboard displays these results with **charts and graphs**, giving visual feedback on code quality metrics like bugs, vulnerabilities, code smells, and test coverage. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

## 9. VPN/Proxy Troubleshooting

The instructor gives an important **practical warning**: if you have any VPN, browser-based proxy, or network-level proxy active, you may not be able to access the Nexus setup wizard after login. The symptoms are that the page loads but the wizard or sign-in popup doesn't appear. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

The solution is: [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

1.  Stop/disable your VPN or proxy
2.  **Update the security group rule** — because stopping your VPN may change your public IP address, and the security group rule is set to "My IP"
3.  If the problem persists and there's nothing on your computer, try switching to a **different network** entirely

***

## 10. Cost Management — Shutting Down Non-Micro Instances

The instructor repeatedly emphasizes: **shut down Nexus and SonarQube instances when you're not using them**. Both require **T2 Medium or T3 Medium** instance types (not T2 Micro, which is free-tier eligible). Medium instances cost money every minute they run. Only power them on when you're actively working with them in the course. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up two EC2 instances on AWS:

1.  **Nexus Server** on Amazon Linux 2023 — an artifact repository where Jenkins will store compiled build outputs
2.  **SonarQube Server** on Ubuntu 24 — a code quality analysis platform where Jenkins will upload scan results

After this setup, combined with the already-existing Jenkins server, we will have the three core CI/CD infrastructure servers ready. The final outcome is: all three servers running, accessible via browser, and their security groups configured to allow inter-service communication. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

## Pre-Requisite

You should already have a **Jenkins server** set up from a prior lecture. You **do not** need to start it for this lecture — it can stay shut down. You only need the Jenkins **security group** to exist (for referencing in rules). [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

## Step 1: Launch the Nexus EC2 Instance

Go to the AWS EC2 console and click **Launch Instance**. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**Name:** `Nexus Server` [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**AMI (Operating System):** Amazon Linux 2023 AMI. This is the OS Nexus will run on. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**Instance Type:** **T2 Medium** or **T3 Medium**. This is critical — Nexus requires more than the 1GB of RAM that T2 Micro provides. Medium instances have **4GB of RAM**, which is sufficient. This is not free-tier eligible, so costs apply. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**Key Pair:** Create a **new key pair**. The instructor names it `Nexus key`. This downloads a `.pem` file you'll use for SSH access. Keep it safe. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**Security Group:** Create a **new security group** named `Nexus-sg`. Add three inbound rules: [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

| Rule       | Port | Source                 | Purpose                                          |
| ---------- | ---- | ---------------------- | ------------------------------------------------ |
| SSH        | 22   | My IP                  | So you can SSH into the instance                 |
| Custom TCP | 8081 | My IP                  | So you can access Nexus web UI from your browser |
| Custom TCP | 8081 | Jenkins Security Group | So Jenkins can upload artifacts to Nexus         |

The third rule is the most important one architecturally — it allows the Jenkins server to communicate with Nexus on port 8081 for artifact uploads. The instructor adds a description: "Allow Jenkins to communicate with Nexus." [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**User Data:** Scroll down to **Advanced Details → User Data**. Go to the GitHub repository (`github.com/hkcoder/vprofile-project`, branch `atom`, folder `user data`), open `nexus-setup.sh`, click the copy button to copy the entire script, and paste it into the User Data field. **Double-check the pasted content before proceeding.** [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

Click **Launch Instance**. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

## Step 2: Launch the SonarQube EC2 Instance

Without waiting for Nexus to finish, immediately launch the second instance. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**Name:** `Sonar Server` [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**AMI:** **Ubuntu 24** (not Amazon Linux — SonarQube's setup script is written for Ubuntu). The instructor notes this is free-tier eligible for the AMI itself, but the instance type won't be. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**Instance Type:** **T2 Medium** or **T3 Medium**. The instructor emphasizes: "We need 4GB of memory." [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**Key Pair:** Create a **new key pair** named `Sonar Key`. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**Security Group:** Create a **new security group** named `sonar-sg`. Add three inbound rules: [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

| Rule | Port | Source                 | Purpose                                            |
| ---- | ---- | ---------------------- | -------------------------------------------------- |
| SSH  | 22   | My IP                  | SSH access                                         |
| HTTP | 80   | My IP                  | Access SonarQube via browser (NGINX frontend)      |
| HTTP | 80   | Jenkins Security Group | Jenkins uploads code analysis results to SonarQube |

Note the port difference from Nexus: SonarQube uses **port 80** (not 9000) because NGINX is the frontend. You can select "HTTP" from the type dropdown instead of manually typing port 80 — it's the same thing. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**User Data:** Go to the same GitHub repo, open `sonar-setup.sh`, copy the entire script, paste into User Data. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

Click **Launch Instance**. The instructor notes this will take longer than Nexus because the script has more steps **and** includes a reboot at the end. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

## Step 3: Verify Nexus Server via SSH

Once the Nexus instance is running, copy its **public IP** from the EC2 console. Open **Git Bash** (or any terminal) and SSH in: [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

```bash
ssh -i <path-to-nexus-key.pem> ec2-user@<public-ip>
```

*   **`ssh`** — the command to initiate a secure shell connection
*   **`-i <path-to-nexus-key.pem>`** — specifies the private key file for authentication (`-i` = identity file)
*   **`ec2-user`** — the default username on Amazon Linux instances (Ubuntu uses `ubuntu`, Amazon Linux uses `ec2-user`)
*   **`@<public-ip>`** — the public IP address of your Nexus EC2 instance

Accept the fingerprint prompt by typing `yes`. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

Once logged in, switch to root:

```bash
sudo su -
```

Check the Nexus service status:

```bash
systemctl status nexus
```

You should see **`active (running)`**. This confirms the user data script executed successfully and the Nexus service started. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

Optionally verify the installation directory and Java version:

```bash
ls /opt/nexus
java -version
```

`/opt/nexus` is the Nexus home directory where all binaries live. Java should report **version 17**. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

## Step 4: Access Nexus from the Browser and Complete Initial Setup

Take the Nexus instance's **public IP** and enter in your browser:

    http://<public-ip>:8081

You should see the Nexus web UI. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

**⚠️ Troubleshooting:** If the page doesn't load or the sign-in wizard doesn't appear, check for VPNs or proxies. Disable them, then update the Nexus security group's "My IP" rules (your IP may have changed). If it still doesn't work, try a different network. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

### Initial Login

Click **Sign In**. The dialog tells you the initial admin password is stored in a file on the server. The file path is displayed on screen: [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

```bash
cat /path/shown/on/screen
```

Run this command in your SSH session (as root). The output is the password — **copy it carefully**. The instructor warns: there is no newline character at the end of the output, so the terminal prompt starts immediately after the password. Copy only up to where the prompt's square bracket `[` begins. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

Enter: [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

*   **Username:** `admin`
*   **Password:** (paste the copied password)

Click **Sign In**. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

### Setup Wizard

The wizard asks you to set a **new password**. The instructor sets `admin123` for simplicity (and explicitly states this is for the course only — in production, use a long, complex password). **Remember this password** — you will need it when configuring the Nexus plugin in Jenkins pipelines. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

Next, the wizard asks about **anonymous access**. The instructor **enables** it. This allows anyone to **download** from the repository without authentication, which simplifies setup for learning. Uploading still requires authentication. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

Click **Next → Next → Finish**. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

You are now logged into Nexus. Click **Browse** in the left menu to see the default repositories. In later lectures, you'll create custom repositories and push artifacts from Jenkins. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

> ⚠️ **Expert Note**
> The credentials you set here (admin/admin123) will appear in the Jenkins pipeline code. In a real environment, you would use Jenkins credentials store or a secrets manager to avoid hardcoding passwords.

***

## Step 5: Verify SonarQube from the Browser

Copy the SonarQube instance's **public IP** and enter it directly in the browser:

    http://<public-ip>

No port number is needed — NGINX is listening on port 80 (the default HTTP port), so the browser connects to it automatically. NGINX then internally routes the request to SonarQube on port 9000. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

The page may take time to load because the instance went through a reboot (due to OS-level changes). Wait and refresh if needed. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

Once the login screen appears: [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

*   **Username:** `admin`
*   **Password:** `admin`

The system will prompt you to **change the password** — do so. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

You now see the SonarQube **dashboard**. In later lectures, Jenkins will automatically create projects here and upload code analysis results, which will be displayed as charts and graphs showing code quality metrics. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

## Step 6: Add SonarQube → Jenkins Security Group Rule

This is the step most people forget. Communication between Jenkins and SonarQube is **bidirectional**: [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

*   Jenkins → SonarQube (port 80): already handled by the `sonar-sg` rule
*   **SonarQube → Jenkins (port 8080):** NOT yet configured

SonarQube needs to send the analysis result status (pass/fail) back to Jenkins. This happens on **port 8080**. You must add this rule to the **Jenkins security group**. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

### Steps:

1.  In the EC2 console, go to the **Jenkins instance**
2.  Click on its **Security** tab → click the **Jenkins Security Group**
3.  Click **Inbound Rules → Edit Inbound Rules**
4.  Click **Add Rule**:
    *   **Type:** Custom TCP
    *   **Port:** 8080
    *   **Source:** SonarQube Security Group (`sonar-sg`)
    *   **Description:** "Allow SonarQube" (so you can identify this rule later)
5.  Click **Save Rules**

This completes the full network communication setup between all three servers. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

## Step 7: Shut Down Instances

Since both Nexus and SonarQube run on **T2/T3 Medium** instances (not free-tier), **stop them immediately** when you're done verifying. Only start them again when the course requires them. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

In the EC2 console, select each instance → **Instance State → Stop Instance**. [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

## 🔗 Final State — How Everything Connects

After completing this lecture, your infrastructure looks like this:

    ┌──────────────┐        port 8081        ┌──────────────┐
    │              │ ───────────────────────▶ │              │
    │   Jenkins    │                          │    Nexus     │
    │  (port 8080) │                          │ (port 8081)  │
    │              │ ◀─────────────────────── │              │
    └──────┬───────┘        (no return)       └──────────────┘
           │
           │  port 80                         ┌──────────────┐
           │ ──────────────────────────────▶  │    NGINX     │
           │                                  │  (port 80)   │
           │        port 8080                 │      ↓       │
           │ ◀──────────────────────────────  │  SonarQube   │
           │                                  │ (port 9000)  │
                                              │      ↓       │
                                              │  PostgreSQL  │
                                              └──────────────┘

*   Jenkins pushes artifacts to **Nexus** on port **8081**
*   Jenkins pushes code analysis to **SonarQube** via NGINX on port **80**
*   SonarQube sends result status back to **Jenkins** on port **8080**
*   All communication is governed by **security group rules** referencing each other by group ID [\[165.-Jenki...qube-Setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/165.-Jenkins,-Nexus-%26-Sonarqube-Setup.txt)

***

This covers the complete content of the video. Would you like me to save this as a downloadable Markdown file?

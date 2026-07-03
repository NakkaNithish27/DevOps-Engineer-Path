# 📘 Linux Package Management — Complete Deep Learning Analysis

**Source:** Video captions from *"Software Management / Package Management"* lecture [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

This lecture teaches the complete package management ecosystem in Linux — from the most manual, low-level method of downloading and installing individual packages to using high-level package managers that handle everything automatically, including dependency resolution and repository management. The instructor demonstrates the entire spectrum on a CentOS VM, exposing the **dependency problem** that drives the need for tools like yum/dnf, and teaches what to do when packages aren't available in default repositories.

***

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

### 1. Package Management — What It Is and Why It Matters

The instructor opens by framing this in universal terms: *"In your life you must have installed or uninstalled many softwares on your computer, on your smartphone, or any other software-based devices."* Package management in Linux is the same fundamental activity — installing, removing, updating software — but done through a structured system of packages, repositories, and management tools. In Linux, the term **package** is used instead of "software" — a package is a pre-built, bundled unit of software ready for installation. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

The critical context established immediately: **the major difference between CentOS and Ubuntu is the package management system.** CentOS is RPM-based, Ubuntu is Debian-based. This distinction, introduced in the earlier Introduction to Linux lecture, now becomes operationally real. Everything from package file formats to installation commands to repository structures differs between these two families. The lecture focuses on the RPM/CentOS side, with Debian/Ubuntu covered separately. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

The lecture structure follows a deliberate progression from **most manual to most automated**: start with downloading and installing a single RPM file by hand → encounter the dependency problem → introduce yum/dnf as the solution → handle cases where packages aren't in default repositories. This progression is pedagogically intentional — you must understand the manual layer to appreciate what the automated layer does for you. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

***

### 2. Identifying Your OS Type and Architecture — The Pre-Installation Knowledge

Before installing any package, you need two pieces of information: **what OS family you're running** and **what CPU architecture you have**. These determine which package to download. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**OS identification:** The file `/etc/os-release` contains operating system identification data. Reading it with `cat /etc/os-release` reveals fields like `ID="centos"` and `ID_LIKE="rhel fedora"`, confirming this is an RPM-based system. The instructor also provides a quick verification test: if `rpm -qa` works (lists all installed RPM packages), you're on an RPM-based OS. If `dpkg -l` works, you're on a Debian-based OS. On a CentOS system, `dpkg -l` will fail because the Debian package tool doesn't exist there. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Architecture identification:** The `arch` command or `uname -m` displays the CPU architecture (e.g., `x86_64` for 64-bit Intel/AMD). The architecture matters because: a 64-bit CPU runs a 64-bit OS, and a 64-bit OS needs 64-bit packages. When browsing package repositories, you'll see multiple architecture options (aarch64, ppc, s390x, x86\_64) — you must select the one matching your system. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

🔍 **Deep Dive:**
The architecture chain is a three-layer compatibility requirement: **CPU architecture → OS architecture → package architecture**. All three must align. `x86_64` is the most common architecture for servers and desktops (standard Intel/AMD 64-bit). `aarch64` is ARM 64-bit (used in AWS Graviton, Apple Silicon, mobile). If you install a package built for the wrong architecture, it simply won't work.

***

### 3. The Low-Level Package Tool — RPM

RPM (Red Hat Package Manager) is the **low-level, foundational package tool** for RPM-based Linux systems. An RPM file (ending in `.rpm`) is a single, self-contained package — the equivalent of an `.exe` or `.msi` on Windows, or `.apk` on Android. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

The RPM tool can perform basic operations directly on individual package files:

* `rpm -ivh package.rpm` — **i**nstall, **v**erbose (print progress), **h**uman-readable format
* `rpm -e package_name` — **e**rase (uninstall) a package
* `rpm -qa` — **q**uery **a**ll installed packages (lists every RPM on the system)
* `rpm -qa | grep name` — search the installed package list for a specific name

The installation process with raw RPM is entirely manual: you must find the RPM file on the internet (at a repository site like rpmfind.net), verify it matches your OS version and architecture, download it to your Linux machine, then install it with `rpm -ivh`. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

***

### 4. The Dependency Problem — Why Raw RPM Isn't Enough

This is the **central problem** that drives the entire package management architecture, and the instructor demonstrates it live. When attempting to install `httpd` (the Apache web server) using raw RPM (`rpm -ivh httpd-...rpm`), the installation **fails** because httpd depends on other packages that aren't installed yet. The error lists the missing dependencies. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

The instructor states: *"It simply tries to install the software, but the software may have many dependencies. Here you just see two, but there could be 20, hundreds of dependencies. In that case, you need to install those dependencies first and then you can install your package."* He adds from personal experience: *"Trust me, I did those things in my old system admin days. It's a very hectic process."* [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

This is the fundamental limitation of the low-level RPM tool: **it operates on individual packages and has no awareness of dependencies.** It doesn't know where to find missing dependencies, doesn't download them, doesn't install them. You would have to manually find, download, and install each dependency — and those dependencies might have their own dependencies, creating a potentially deep chain. This manual dependency resolution process is impractical for any non-trivial software.

🔍 **Deep Dive:**
The dependency problem reveals a core software engineering truth: real software is never isolated. Every program depends on libraries, frameworks, and other tools. A web server needs SSL libraries, compression libraries, configuration parsers, and more. Each of those may need further libraries. The dependency graph can be deep and wide. The low-level tool (rpm/dpkg) operates at the leaf level — individual packages. What's needed is a tool that understands the **entire graph** and resolves it automatically. That's exactly what yum/dnf/apt do.

***

### 5. The Repository System — Where Packages Live

Before understanding yum/dnf, you need to understand **repositories**. A repository is a remote storage location where packages are kept — organized, indexed, and accessible over the network. Think of it as an app store for Linux packages. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

Repository configuration files live in `/etc/yum.repos.d/`. Each file in this directory defines one or more repositories with: a **name**, a **URL** (the remote location of the packages), whether the repository is **enabled** or not, and other metadata. When you install the OS, it comes with default repository configuration files that point to the official package sources for that distribution. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

The repository system is the **data layer** that the high-level package managers (yum/dnf) read from. When yum searches for a package, it queries all enabled repositories defined in these configuration files. When it installs a package, it downloads from the repository URL. When it resolves dependencies, it searches across all repositories to find every required package. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

⚠️ **Expert Note:**
The repository system is the trust boundary for package management. Packages from official repositories are tested and verified. Adding third-party repositories (like Jenkins's repo, or EPEL) extends your package access but also extends your trust boundary. In production, repository sources should be carefully controlled — only trusted repositories should be enabled.

***

### 6. High-Level Package Managers — Yum and DNF

**Yum** (Yellowdog Updater Modified) and **DNF** (Dandified Yum) are the **high-level package management tools** for RPM-based systems. DNF is described as the "new generation" tool — it is the modern replacement for yum. Both can be used, but the instructor advises: *"Alternatively, most of the time try to use DNF. It's a new generation command."* [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

These tools solve the dependency problem completely. When you run `yum install httpd` or `dnf install httpd`, the tool: searches through all configured repositories → finds the httpd package → identifies all dependencies (and "weak dependencies") → downloads everything → installs everything in the correct order. The instructor demonstrates this: installing httpd pulls in **11 total packages** — the main package plus all its dependencies. *"Imagine downloading, installing all those RPMs one by one manually. It's going to take time."* [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

The key operations available through yum/dnf: [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

* **search** — find packages by name across all repositories
* **install** — download and install a package with all dependencies
* **remove** — uninstall a package (also removes unused dependencies)
* **reinstall** — reinstall a package that may not have installed properly
* **upgrade** — upgrade a specific package or all packages on the system
* **repolist** — list all enabled repositories
* **clean all** — clear the local cache (useful when repository changes aren't being picked up)
* **history** — view a log of all yum/dnf operations performed
* **grouplist / groupinstall** — list or install groups of related packages (e.g., "Development Tools")
* **--help** — display all available options

The `-y` flag auto-answers "yes" to confirmation prompts: `dnf install httpd -y` installs without asking for confirmation. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Removing packages intelligently:** When you `dnf remove httpd`, it also removes **unused dependencies** — but only if those dependencies aren't required by any other installed package. This prevents orphaned packages from accumulating while avoiding breaking other software. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Upgrading the system:** `yum upgrade` or `dnf upgrade` upgrades all packages on the system to their latest versions available in the configured repositories. The instructor emphasizes: *"In real time when you set up any new OS, when you start using it, before you start using it, you upgrade it. It patches all the vulnerabilities and bug fixes."* This is a critical operational practice — upgrading before first use ensures you're running patched, secure software. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

***

### 7. When Packages Aren't in Default Repositories — The Jenkins Example

Not every package is available in the OS's default repositories. The instructor demonstrates this with **Jenkins** (a continuous integration tool): `yum install jenkins` returns *"No match for argument: jenkins"* — the package doesn't exist in any configured repository. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

The resolution follows a clear pattern: **search the internet for the vendor's official installation instructions.** The instructor searches "install jenkins," finds the official Jenkins website (jenkins.io), navigates to the Linux installation page, and selects the Red Hat/Fedora/CentOS instructions. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

The vendor-provided instructions typically involve three steps:

1. **Add the vendor's repository** — download a `.repo` file into `/etc/yum.repos.d/` using wget or curl. This file contains the URL of the vendor's package repository.
2. **Import the repository's GPG key** — some repositories require an access key for security verification, imported with `rpm --import <key_url>`.
3. **Install dependencies and the package** — now that the repository is configured, standard `yum install` or `dnf install` works because the package is accessible. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

The instructor's conclusion: *"Do not worry about installing packages. It's going to be always the easiest thing that you do in Linux. But you need to understand the mechanism behind it to find out the right package for you, for your OS, for your architecture."* [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

🔍 **Deep Dive:**
The Jenkins installation also reveals the concept of **dependency declaration by vendors.** Jenkins depends on Java 17 and fontconfig. The vendor's instructions explicitly tell you to install these before Jenkins. This is a layer above what yum handles automatically — the vendor knows their software requires Java 17, and while yum resolves package-level dependencies, the Java requirement is an **application-level dependency** that the vendor communicates through documentation.

***

### 8. EPEL — Extending Your Repository Access

The instructor introduces a special package: `epel-release`. EPEL (Extra Packages for Enterprise Linux) is a repository package — installing it doesn't install an application, it **adds new repositories** to your system. After installing epel-release, `dnf repolist` shows additional repositories available, giving access to many more packages that aren't in the default CentOS/RHEL repositories. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

This is a meta-package concept: a package whose purpose is to configure access to more packages. It's the repository system's self-extension mechanism.

***

### 9. Download Tools — curl vs wget

Both `curl` and `wget` can access remote URLs, but they have different primary use cases as presented in the video: [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**curl** — described as a "text-based browser." It accesses a URL and can output the content. To save the output to a file, use `-o filename`: `curl <url> -o <filename>`. curl has many use cases beyond downloading (API calls, testing endpoints, etc.).

**wget** — primarily used to **download** files from remote URLs. You simply say `wget <url>` and it downloads the file. Simpler for pure download tasks.

The instructor's guidance: *"You can use wget if you just want to download. Curl has many other use cases."* [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

***

### 10. The Multi-Line Command Syntax

When vendor instructions show long commands, they often split them across multiple lines using a **backslash (`\`)** at the end of each line. The instructor explains: *"If you want to give a command in multiple lines, you can separate it by a backward slash."* The shell treats the backslash-newline combination as a continuation of the same command, not as a new command. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

***

### 11. The Cache Problem and dnf clean all

Sometimes after adding a new repository, packages from that repository aren't immediately available to install. This can happen because of **caching** — yum/dnf caches repository metadata locally for performance. If the cache is stale (doesn't include the newly added repository's data), installations may fail. The solution is `dnf clean all` or `yum clean all`, which clears the local cache. The next install/search command will re-scan all repositories from scratch. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

***

### 12. The Instructor's Operational Philosophy on Package Management

The instructor repeatedly emphasizes a practical mindset: *"Don't try to mug up all those things"* (don't memorize every option). Instead, know that `dnf --help` exists, and you'll encounter these commands so frequently throughout the course that they'll become second nature. The `history` command (`dnf history`) lets you review everything you've done. And the `history` shell command shows all commands executed in the session — the instructor recommends running it at the end of each lecture to review. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

***

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

### What We Are Building and Why

We are building the ability to **install, remove, search, and manage software packages on RPM-based Linux systems** using both low-level tools (rpm) and high-level tools (yum/dnf). The final operational outcome: you can install any package on a CentOS/RHEL system — whether it's in the default repositories, requires adding a vendor repository, or needs manual RPM download. All work is done on the CentOS VM created in the virtualization section. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

***

### Step 1: Log Into CentOS VM and Become Root

```bash
vagrant ssh
```

Connects to the CentOS VM via SSH through Vagrant. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

```bash
sudo -i
```

Switches to root user. Package management requires root privileges — installing and removing system-wide software is an administrative task. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

***

### Step 2: Identify Your OS and Architecture

**Check the OS type:**

```bash
cat /etc/os-release
```

Look for `ID="centos"` and `ID_LIKE="rhel fedora"`. This confirms you're on an RPM-based system. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Verify RPM-based OS (functional test):**

```bash
rpm -qa
```

* `rpm` = the RPM package tool
* `-q` = query mode
* `-a` = all installed packages

This lists every RPM package installed on the system. If this command works, you're on an RPM-based OS. On a Debian system, the equivalent is `dpkg -l` (which would fail on CentOS). [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Check CPU architecture:**

```bash
arch
```

Or equivalently:

```bash
uname -m
```

* Expected output: `x86_64` (64-bit Intel/AMD)

**Why this matters:** When downloading packages, you must select the version matching your OS version AND your architecture. A package for `aarch64` won't work on `x86_64`. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

***

### Step 3: Manual Package Installation — The RPM Way (Telnet Example)

**Attempt to run a command that isn't installed:**

```bash
telnet
```

**Expected error:** `No such file or directory` or `command not found`. This means the telnet package isn't installed. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Find the RPM on the internet:**

1. Search for "telnet rpm" in your browser
2. Go to rpmfind.net (a popular RPM repository site)
3. Search for "telnet"
4. Find the version matching your OS: CentOS Stream 9, x86\_64
5. Right-click the link → Copy link address [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Download the RPM to your Linux machine:**

```bash
curl https://rpmfind.net/linux/centos-stream/9-stream/AppStream/x86_64/os/Packages/telnet-0.17-85.el9.x86_64.rpm -o telnet-0.17-85.el9.x86_64.rpm
```

* `curl` = text-based browser / URL access tool
* The full URL = the direct link to the RPM file
* `-o` = **o**utput — save the downloaded content to this filename
* `telnet-0.17-85.el9.x86_64.rpm` = the output filename (use the same name as the RPM)

**Verify the download:**

```bash
ls
```

You should see the `.rpm` file in your current directory. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Install the RPM:**

```bash
rpm -ivh telnet-0.17-85.el9.x86_64.rpm
```

* `rpm` = the package tool
* `-i` = **i**nstall
* `-v` = **v**erbose (print progress details)
* `-h` = **h**uman-readable format (show hash marks for progress)
* The RPM file path follows

**Verify installation:**

```bash
telnet
```

The telnet shell opens — the command now works. Type `quit` to exit. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Alternative verification — check installed packages:**

```bash
rpm -qa | grep telnet
```

Pipes the full installed package list through grep to search for "telnet." If installed, the package name appears. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Uninstall the package:**

```bash
rpm -e telnet-0.17-85.el9.x86_64
```

* `-e` = **e**rase (remove)
* Use the package name as shown by `rpm -qa` output (not the filename)

**Verify removal:**

```bash
telnet
```

Error returns — command not found again. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Connection to larger flow:** This manual process works for simple packages with no dependencies. The next step reveals why it fails for complex packages.

***

### Step 4: Encountering the Dependency Problem (httpd Example)

**Download httpd RPM using wget:**

```bash
wget https://rpmfind.net/linux/.../httpd-2.4.x-xx.el9.x86_64.rpm
```

* `wget` = download tool (simpler than curl for pure downloads — just give the URL)
* The RPM file downloads to the current directory [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Attempt to install:**

```bash
rpm -ivh httpd-2.4.x-xx.el9.x86_64.rpm
```

**Expected result: FAILURE.** The installation fails with dependency errors listing packages that must be installed first. The instructor notes there could be "20, hundreds of dependencies." [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**This is the dependency problem in action.** The raw `rpm` tool cannot resolve this. You would need to manually find, download, and install each dependency — and their dependencies. This motivates the need for high-level package managers.

***

### Step 5: Understanding the Repository Configuration

**Navigate to the repository config directory:**

```bash
cd /etc/yum.repos.d/
ls
```

You'll see `.repo` files — these define where yum/dnf downloads packages from. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Examine a repo file:**

```bash
cat centos.repo
```

Each section defines a repository with: name, baseurl (the remote package location), enabled status, and other metadata. Default repos come with the OS installation. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Connection to larger flow:** This is the data layer that yum/dnf reads. Understanding this structure is essential for Step 7 (adding custom repositories).

***

### Step 6: Installing with yum/dnf — Automatic Dependency Resolution

**Search for a package:**

```bash
yum search httpd
```

Searches all configured repositories and lists every package with "httpd" in the name. You'll see httpd, httpd-devel, httpd-filesystem, httpd-manual, etc. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Install the package with all dependencies:**

```bash
yum install httpd
```

Yum displays: the package to install, its architecture, all dependencies, weak dependencies, and the total count. The instructor's example shows **11 packages** total. Type `y` to confirm. Yum downloads and installs everything. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Using DNF (new generation, recommended):**

```bash
dnf install httpd
```

If already installed: *"Nothing to do."* Same result, newer tool. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Install without confirmation prompt:**

```bash
dnf install httpd -y
```

* `-y` = auto-answer yes — no confirmation question, installs immediately [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Remove a package:**

```bash
dnf remove httpd
```

Also removes **unused** dependencies — those not needed by any other package. Confirm with `y`. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Upgrade all system packages:**

```bash
yum upgrade
```

Lists all packages that have newer versions available. The instructor's example shows **161 packages** to upgrade plus 6 new ones. This patches vulnerabilities and applies bug fixes. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

⚠️ **Expert Note:**
Always upgrade a new OS before using it in production. The instructor states this explicitly: *"When you set up any new OS, before you start using it, you upgrade it. It patches all the vulnerabilities and bug fixes."* This is a critical security practice.

**Verify installation via DNF history:**

```bash
dnf history
```

Shows a log of all package management operations: installs, removes, upgrades. Useful for auditing what changes were made to the system. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

***

### Step 7: Adding a Custom Repository — The Jenkins Example

**Attempt to install a package not in default repos:**

```bash
yum install jenkins
```

**Expected error:** *"No match for argument: jenkins."* The package doesn't exist in any configured repository. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Find the vendor's installation instructions:**

1. Search "install jenkins" in your browser
2. Go to jenkins.io → Linux → Red Hat/Fedora/CentOS section
3. The vendor provides step-by-step commands [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Step 7a — Add the Jenkins repository:**

```bash
wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
```

* `wget` = download
* `-O /etc/yum.repos.d/jenkins.repo` = save the downloaded file directly into the repo config directory with the name `jenkins.repo`
* The URL points to Jenkins's official repository configuration file

**Verify:**

```bash
cat /etc/yum.repos.d/jenkins.repo
```

You should see repository information — name, URL, enabled status. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Step 7b — Import the repository's GPG key:**

```bash
rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
```

* `rpm --import` = import a public key for repository verification
* Some repositories require cryptographic keys for security — this key lets yum verify that packages from this repository are authentic [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Step 7c — Upgrade the system (recommended):**

```bash
yum upgrade -y
```

Ensures all existing packages are up to date before installing new software. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Step 7d — Install Jenkins dependencies:**

```bash
dnf install fontconfig java-17-openjdk -y
```

Jenkins requires Java 17 and fontconfig. Install them first. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Step 7e — Install Jenkins:**

```bash
dnf install jenkins -y
```

Now that the Jenkins repository is configured and the key is imported, this command works — dnf can find and download Jenkins from the newly added repository. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Verify the new repository is listed:**

```bash
dnf repolist
```

The Jenkins repository should now appear alongside the default OS repositories. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Connection to larger flow:** This pattern — add repo → import key → install — applies to any third-party software: Docker, Kubernetes tools, monitoring agents, etc. The vendor always provides these instructions.

***

### Step 8: Install EPEL for Extended Package Access

```bash
dnf install epel-release -y
```

* `epel-release` = a meta-package that adds the EPEL (Extra Packages for Enterprise Linux) repositories
* After installation, `dnf repolist` shows new repositories, giving access to many additional packages not in default CentOS repos [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

***

### Step 9: Utility Operations

**Clear the package cache:**

```bash
dnf clean all
```

Clears cached repository metadata. Use this when: you've added a new repository but packages aren't showing up, or you suspect stale cache is causing installation issues. After clearing, the next dnf command re-scans all repositories. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**View all available options:**

```bash
dnf --help
```

Lists all available dnf subcommands and options. The instructor emphasizes: don't memorize everything — know that `--help` exists. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Review package management history:**

```bash
dnf history
```

Shows chronological list of all yum/dnf operations performed on the system. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

**Review all commands from this session:**

```bash
history
```

Shows all shell commands executed. The instructor recommends running this at the end of each lecture to review what was practiced. [\[33-package...management \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/33-package-management.txt)

***

***

## 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

### Package Management — Two-Tier Architecture

```
HIGH-LEVEL (controller):  yum / dnf (RPM-based)  |  apt (Debian-based)
  → reads /etc/yum.repos.d/*.repo               |  → reads /etc/apt/sources.list
  → searches ALL configured repositories          |
  → resolves ALL dependencies automatically       |
  → downloads + installs in correct order          |
  → removes unused deps on uninstall              |
        ↓ wraps ↓
LOW-LEVEL (engine):       rpm                     |  dpkg
  → operates on SINGLE .rpm files                 |  → operates on SINGLE .deb files
  → NO dependency resolution                      |
  → FAILS if dependencies missing                 |
  → manual find → download → install              |
```

***

### Pre-Installation Checklist

```
1. What OS family?     → cat /etc/os-release → ID="centos" = RPM-based
                       → rpm -qa works? = RPM-based
                       → dpkg -l works? = Debian-based

2. What architecture?  → arch  OR  uname -m  → x86_64 (most common)

3. Match both when selecting packages from repositories
```

***

### Installation Methods — Decision Tree

```
WANT TO INSTALL A PACKAGE?
  │
  ├─ Try: dnf install <package> -y
  │    ├─ SUCCESS → done (deps auto-resolved)
  │    └─ FAIL: "No match for argument"
  │         │
  │         ├─ Search internet: "install <package> on centos/rhel"
  │         │    ├─ Vendor provides repo file → download to /etc/yum.repos.d/
  │         │    ├─ Vendor provides GPG key → rpm --import <key_url>
  │         │    ├─ Vendor lists dependencies → install deps first
  │         │    └─ Then: dnf install <package> -y → SUCCESS
  │         │
  │         └─ Still failing? → dnf clean all → retry
  │
  └─ Manual (last resort / learning only):
       ├─ Find .rpm on rpmfind.net (match OS + arch)
       ├─ Download: curl <url> -o <file>  OR  wget <url>
       └─ Install: rpm -ivh <file>
            └─ ⚠️ Fails if dependencies exist → use dnf instead
```

***

### RPM Command Quick-Reference

```
rpm -ivh <file.rpm>        → Install (verbose, human-readable)
rpm -e <package_name>      → Erase (uninstall)
rpm -qa                    → Query all installed packages
rpm -qa | grep <name>      → Search installed packages
rpm --import <key_url>     → Import GPG key for repo verification
```

***

### yum/dnf Command Quick-Reference

```
dnf search <name>          → Find packages in repos
dnf install <pkg> -y       → Install + all deps (auto-yes)
dnf remove <pkg>           → Remove + unused deps
dnf reinstall <pkg>        → Reinstall (fix broken installs)
dnf upgrade                → Upgrade ALL packages (security patches!)
dnf repolist               → List all enabled repositories
dnf clean all              → Clear cache (fix repo detection issues)
dnf history                → View all past operations
dnf grouplist              → List package groups
dnf groupinstall "Name"    → Install entire package group
dnf --help                 → Show all options
dnf install epel-release   → Add EPEL repos (more packages)
```

***

### Download Tools — curl vs wget

```
wget <url>                 → Download file (simple, direct)
curl <url> -o <filename>   → Download with output filename control
curl                       → Also: API calls, testing, many use cases
wget -O <path> <url>       → Download to specific path (used for .repo files)
```

***

### Repository System — Data Flow

```
/etc/yum.repos.d/
  ├── centos.repo          → default OS repos (comes with install)
  ├── epel.repo            → added by: dnf install epel-release
  ├── jenkins.repo         → added by: wget -O ... vendor_url
  └── [any_vendor].repo    → added per vendor instructions

Each .repo file contains:
  [repo_name]
  baseurl = https://...    → where packages are stored
  enabled = 1              → whether yum/dnf uses this repo
  gpgcheck = 1             → whether to verify package signatures
  gpgkey = ...             → key for verification

dnf reads ALL enabled .repo files → searches ALL repos → resolves deps across ALL
```

***

### Adding Third-Party Software — Universal Pattern

```
Step 1: wget/curl repo file → /etc/yum.repos.d/<vendor>.repo
Step 2: rpm --import <vendor_gpg_key_url>
Step 3: dnf clean all (optional, if cache issues)
Step 4: dnf install <package> -y

This pattern applies to: Jenkins, Docker, Kubernetes, Grafana, etc.
Vendor ALWAYS provides these steps on their website.
```

***

### Operational Best Practices Extracted

```
New OS setup sequence:
  1. yum upgrade -y              → patch vulnerabilities first
  2. dnf install epel-release -y → extend package access
  3. Install needed software     → dnf install ...

Troubleshooting installs:
  Package not found?   → Check: dnf repolist (is the repo there?)
                       → Fix: add vendor repo, then dnf clean all
  Install broken?      → dnf reinstall <pkg>
  Cache stale?         → dnf clean all → retry
  Don't memorize?      → dnf --help (always available)
  Audit changes?       → dnf history
```

***

### Dependency Problem — Core Mental Model

```
SOFTWARE → depends on → LIBRARIES/TOOLS → depend on → MORE LIBRARIES
     (httpd)              (mod_ssl, apr)              (openssl, zlib)

rpm sees:    ONE package. Fails if deps missing.
dnf sees:    ENTIRE dependency graph. Resolves everything.

rpm  = "Here's one brick. Build it yourself."
dnf  = "Here's the blueprint. I'll get all the bricks."
```

***

### Key Behavioral Rules

| If you forget...                     | Remember...                                        |
| ------------------------------------ | -------------------------------------------------- |
| rpm handles dependencies?            | NO. Use dnf/yum for that                           |
| Which tool is newer, yum or dnf?     | DNF (new generation). Prefer it                    |
| How to find unknown packages?        | Search vendor website → follow their install steps |
| Package not found after adding repo? | `dnf clean all` → clears stale cache               |
| How to extend default repos?         | `dnf install epel-release`                         |
| Where are repo configs?              | `/etc/yum.repos.d/*.repo`                          |
| How to check architecture?           | `arch` or `uname -m`                               |
| How to check OS type?                | `cat /etc/os-release`                              |
| Remove also cleans deps?             | YES — dnf removes UNUSED deps automatically        |
| First thing on new OS?               | `yum upgrade -y` → patch everything                |
| Multiline command syntax?            | `\` at end of line = continuation                  |

***

This completes the full analysis of the Package Management lecture. Every concept, command, failure scenario, and operational pattern from the video has been preserved across the three complementary sections. <cite>turn5search5</cite>

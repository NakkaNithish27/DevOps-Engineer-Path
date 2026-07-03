# 📘 Installing Prerequisites for DevOps — Deep Learning Material

> **Source:** Lecture 10 — *Installing Softwares* (Caption file + Companion PDF) [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt), [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

***

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

### 1. Command-Line Software Installation via Package Managers

The foundational idea of this lecture is that software installation should be done **through the command line using a package manager**, not through the traditional GUI workflow of "find → download → click installer → next → next → finish." The instructor explicitly rejects the manual method, calling it "the boring way." [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

A **package manager** is a system tool that automates the process of installing, upgrading, configuring, and removing software. It connects to a **package registry** (a centralized online repository of software packages), resolves what's needed, downloads the correct binaries, places them in the right directories, sets up PATH entries, and handles dependencies — all from a single command. The value is threefold: **speed** (one command per tool), **reproducibility** (the same command yields the same result on any machine), and **auditability** (you have a clear record of what was installed and at what version).

This course uses two package managers, one per operating system:

* **Chocolatey** — for Windows
* **Homebrew (Brew)** — for macOS

Both serve the same purpose but are designed for their respective OS ecosystems. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

> 🔍 **Deep Dive (Optional)**
>
> Package managers operate on a **registry-client model**. The client (`choco` or `brew` CLI) communicates with a remote registry (chocolatey.org packages or Homebrew formulae/casks on GitHub). When you run `choco install git`, Chocolatey looks up "git" in its registry, finds the matching package definition (which includes download URLs, install scripts, checksums), downloads the installer, runs it silently (with `/S` or `-y` flags to suppress prompts), and registers the installed package in its local database. Homebrew works similarly but compiles some packages from source (formulae) or downloads pre-built macOS apps (casks).

***

### 2. Chocolatey and Homebrew — Platform-Specific Package Managers

**Chocolatey** is installed from [chocolatey.org/docs/installation](https://chocolatey.org/docs/installation). Once installed, it provides the `choco` command in PowerShell. Windows users must run PowerShell **as Administrator** because software installation modifies system-level directories and the Windows registry, which requires elevated privileges. [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf), [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

**Homebrew** is installed from [brew.sh](https://brew.sh/). Once installed, it provides the `brew` command in the macOS Terminal. Homebrew has a critical distinction: it differentiates between **formulae** (command-line tools, installed via `brew install <name>`) and **casks** (GUI applications, installed via `brew install --cask <name>`). This distinction appears throughout the macOS installation commands — tools like `git` and `maven` are formulae, while VirtualBox, Vagrant, VSCode, IntelliJ, and Sublime are casks. [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

> 🔍 **Deep Dive (Optional)**
>
> The `--cask` flag tells Homebrew to look in its **Cask** repository instead of its **Formula** repository. Formulae are typically compiled from source or installed as command-line binaries into Homebrew's prefix (`/opt/homebrew` on Apple Silicon, `/usr/local` on Intel). Casks, on the other hand, download `.dmg` or `.pkg` files and install them into `/Applications` like a normal macOS app. The distinction matters because GUI applications have different installation mechanisms (drag-to-Applications, `.pkg` installers) than CLI tools.

***

### 3. The `.curlrc` Configuration — macOS-Specific Prerequisite

Before installing any software on macOS, the lecture requires creating a file called `.curlrc` in the user's home directory, containing just `-k`. [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf), [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

The `-k` flag is `curl`'s option to **skip SSL certificate verification**. Homebrew internally uses `curl` to download packages and formulae. In certain network environments — corporate networks, university firewalls, or setups with SSL-inspecting proxies — the SSL certificates presented to `curl` are not trusted by the system's certificate store, causing downloads to fail with certificate errors. The `.curlrc` file is a **persistent configuration file** for `curl` — any flag placed in it is automatically applied to every `curl` invocation on that machine. By placing `-k` there, every Homebrew download silently skips certificate verification, preventing SSL-related failures. [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

The instructor verifies this by running `cat ~/.curlrc`, which should print `-k`. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

> ⚠️ **Expert Note (Optional)**
>
> Disabling SSL verification (`-k` / `--insecure`) is a security trade-off. It makes you vulnerable to man-in-the-middle attacks because `curl` will accept any certificate, even forged ones. In a production or sensitive environment, the correct fix is to add the proxy/corporate CA certificate to the system trust store. For a learning/course environment, `-k` is an acceptable workaround.

***

### 4. Version Pinning

The Chocolatey commands for VirtualBox and Vagrant include explicit `--version` flags: `--version=7.2.6` for VirtualBox and `--version=2.4.9` for Vagrant. [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**Version pinning** means installing a specific, known-good version of software instead of the latest available. This is important in a course environment because the instructor has tested all exercises against these specific versions. If you install a newer version, subtle differences in behavior, UI, or configuration could cause exercises to fail or look different. The instructor also notes: "You may see a different version in the document. Whatever version you see, simply copy that and run it." — meaning the document is the source of truth for versions. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

Other tools (`git`, `maven`, `awscli`, etc.) are installed without version pinning, meaning you get the latest version. This is acceptable because those tools have stable CLI interfaces that rarely break across minor versions.

***

### 5. Environment Cleanliness — Pre-Installation Verification

Before installing anything, the instructor requires a critical verification step: checking whether Maven or Java are **already installed** on the machine. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

The commands `mvn -version` and `java -version` check for existing installations. Two outcomes are possible:

* **Error / command not found** — This means neither tool is installed. This is the **desired state**. You can proceed with installation. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)
* **Version information appears** — This means a previous installation exists. You **must uninstall it first** before proceeding. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

Why is this important? Multiple installations of Java or Maven can coexist on a machine, creating **PATH conflicts**. When you type `java`, the OS searches the `PATH` environment variable in order and uses the first match. If an old Java 8 sits earlier in the PATH than the newly installed Corretto 17, your system silently uses Java 8 — and everything breaks in confusing, hard-to-debug ways. Uninstalling the old version first eliminates this class of problems entirely. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

The `choco list` / `brew list` commands show all packages currently managed by the respective package manager. This list is also how you find the exact **package name** to use for uninstalling — the instructor emphasizes that the package name might differ from the common name (e.g., the Java package might be called `corretto17jdk`, `jdk17`, or something else depending on what was previously installed). [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

> 🔍 **Deep Dive (Optional)**
>
> `choco list` shows packages in the format `<package-name> <version>`. The instructor explicitly points this out: "this is the package name, this is the version." The package name is what you pass to `choco uninstall`. On macOS, `brew list` shows formulae and `brew list --cask` shows casks. Uninstalling uses the same package name: `brew uninstall <name>`.

***

### 6. The Source Code Repository and Prerequisites Branch

The course uses a GitHub repository at `github.com/hkhcoder/vprofile-project`. This repository contains the project source code, but it also has a dedicated branch called **`prereqs`** that holds the prerequisite installation documents. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

The use of a **branch** for prerequisites (instead of putting them in the main branch or a separate repo) is an organizational decision — it keeps setup documentation version-controlled alongside the project, accessible via the same repository URL, but separated from the actual project code. The documents exist in multiple formats (PDF, MD) for convenience. The instructor also mentions the documents are available as lecture resources (downloadable from the course platform). [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

***

### 7. The Tool Ecosystem — What's Being Installed and Why

The lecture installs a specific set of tools. Each serves a distinct purpose in the DevOps workflow that the course will teach. The instructor deliberately says: "Please don't worry about what are these tools, how to use them... in due time, you will be master of these tools."  This means the lecture is purely about **getting the environment ready**, not about understanding each tool. However, knowing their roles at a high level provides useful context: [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

| Tool                         | Category        | Role in DevOps                                  |
| ---------------------------- | --------------- | ----------------------------------------------- |
| **VirtualBox**               | Hypervisor      | Runs virtual machines locally                   |
| **Vagrant**                  | VM automation   | Automates VM creation/provisioning via code     |
| **Git**                      | Version control | Tracks and manages source code                  |
| **Corretto 17 / OpenJDK 17** | Runtime         | Java runtime for building/running Java projects |
| **Maven**                    | Build tool      | Compiles, tests, packages Java projects         |
| **AWS CLI**                  | Cloud CLI       | Interacts with AWS services from terminal       |
| **IntelliJ IDEA**            | IDE             | Java-focused code editor                        |
| **VSCode**                   | IDE             | General-purpose code editor                     |
| **Sublime Text**             | Text editor     | Lightweight file editor                         |

The instructor recommends **VSCode** as the primary editor and notes that IntelliJ will be used specifically for Java work. Both are installed. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

> ⚠️ **Expert Note (Optional)**
>
> VirtualBox is explicitly marked as **"Not For MacOS M1/M2"** in the PDF document.  Apple Silicon Macs (M1, M2, M3 chips) use ARM architecture, and VirtualBox has limited/no support for ARM-based macOS. M-series Mac users would need alternatives like UTM or Docker Desktop for local virtualization. The lecture doesn't address this directly, but the document flags it. [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

***

### 8. The macOS Java Symlink and Shell Reload

Two macOS-specific commands appear in the PDF that are not discussed verbally but are critical:

**The symlink command:**

```bash
sudo ln -sfn $HOMEBREW_PREFIX/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk
```

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

When Homebrew installs OpenJDK, it places the JDK files inside Homebrew's own directory structure. But macOS expects Java installations to be registered in `/Library/Java/JavaVirtualMachines/` — this is where macOS's built-in `/usr/libexec/java_home` utility looks to discover installed JDKs. The symlink bridges this gap: it creates a link from where macOS expects Java to be, pointing to where Homebrew actually installed it. Without this, commands like `java -version` and tools like Maven may not find the JDK.

**The shell reload command:**

```bash
exec zsh -l
```

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

After installing tools that modify PATH or shell configuration, the current terminal session still has the **old** environment loaded in memory. `exec zsh -l` replaces the current shell process with a fresh login shell (`-l`), which re-reads all configuration files (`.zshrc`, `.zprofile`, etc.) and picks up new PATH entries. Without this, newly installed commands may not be found until you manually open a new terminal window.

***

### 9. The `-y` Flag — Non-Interactive Installation

Every Chocolatey command includes the `-y` flag (e.g., `choco install git -y`). This flag means **"yes to all prompts"** — it auto-confirms any questions Chocolatey asks during installation (license agreements, dependency confirmations, etc.). Without `-y`, each installation would pause and wait for manual confirmation, making batch installation tedious. [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

The instructor also mentions: "It might ask you a question yes or no. You have to say Yes to install." — this refers to cases where the `-y` flag doesn't suppress all prompts (some packages have additional confirmation steps). [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

***

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

### What We Are Building

We are setting up a **complete local DevOps development environment** by installing all prerequisite tools needed for the course. The final outcome: a machine with VirtualBox, Vagrant, Git, Java 17, Maven, AWS CLI, IntelliJ, VSCode, and Sublime Text — all installed via command-line package managers, verified and conflict-free. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

***

### Phase 0: Access the Prerequisite Document

Open a browser and navigate to: [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

```
github.com/hkhcoder/vprofile-project
```

* Click the **branch dropdown** (shows `main` by default)
* Find and select the branch called **`prereqs`**
* You'll see four documents (same content, different formats: PDF, MD, etc.)
* Click the **MD file** to view directly, or download the **PDF** for offline reference
* Alternatively, download from the **lecture resources** section of the course platform

This document contains every command you'll need. Keep it open throughout. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

***

### Phase 1: Install the Package Manager

**Windows — Install Chocolatey:**

Follow instructions at <https://chocolatey.org/docs/installation>. [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

After installation, open **PowerShell as Administrator** (search for PowerShell → right-click → "Run as Administrator"). All subsequent Windows commands must run in this elevated PowerShell session. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

**macOS — Install Homebrew:**

Follow instructions at <https://brew.sh/>. [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

After installation, open **Terminal**. Then create the `.curlrc` file:

```bash
echo -k > ~/.curlrc
```

* `echo` — prints the string `-k` to standard output
* `-k` — the curl flag to skip SSL certificate verification
* `>` — redirects the output, **overwriting** the file `~/.curlrc` (creates it if it doesn't exist)
* `~/.curlrc` — file in the user's home directory; `~` expands to `/Users/<your-username>`

Verify it worked: [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

```bash
cat ~/.curlrc
```

**Expected output:** `-k` printed on screen. If you see `-k`, proceed. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

***

### Phase 2: Pre-Installation Cleanup Check

This step prevents version conflicts. Run these commands on your terminal (PowerShell or Terminal):

**Check what's already installed via the package manager:**

```bash
choco list        # Windows
brew list          # macOS
```

* These list all packages currently managed by the respective package manager [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

**Check for existing Java and Maven:**

```bash
java -version
mvn -version
```

 [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

**If you get errors ("command not found" or similar)** → Good. No prior installation exists. Skip to Phase 3.

**If you see version numbers** → You must uninstall first:

```bash
# Windows
choco uninstall <package-name>

# macOS
brew uninstall <package-name>
```

<cite>turn2search2</cite>

To find the correct package name: look at the output of `choco list` / `brew list`. Find the entry for Java or Maven. The package name is the **first column** — it might be something like `corretto17jdk`, `jdk11`, `maven`, etc. Use that exact name in the uninstall command. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

**How to verify uninstall succeeded:** Run `java -version` and `mvn -version` again. Both should now return errors. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

***

### Phase 3: Install All Tools

Execute each command **one at a time**, waiting for each to complete before starting the next. The instructor installs them sequentially and waits for completion. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

***

#### 🖥️ Windows (PowerShell as Admin)

**1. VirtualBox:**

```powershell
choco install virtualbox --version=7.2.6 -y
```

* `choco install` — invoke Chocolatey's install command
* `virtualbox` — package name in Chocolatey's registry
* `--version=7.2.6` — install this exact version (version pinning)
* `-y` — auto-confirm all prompts

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**2. Vagrant:**

```powershell
choco install vagrant --version=2.4.9 -y
```

* Same structure. Vagrant is version-pinned to `2.4.9`. This installation may take a **long time** — the instructor explicitly notes this. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt), [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**3. Git:**

```powershell
choco install git -y
```

* No version pin — latest stable version is fine. [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**4. Java (Amazon Corretto 17):**

```powershell
choco install corretto17jdk -y
```

* `corretto17jdk` — Amazon's distribution of OpenJDK 17. [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**5. Maven:**

```powershell
choco install maven -y
```

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**6. AWS CLI:**

```powershell
choco install awscli -y
```

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**7. IntelliJ IDEA Community Edition:**

```powershell
choco install intellijidea-community -y
```

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**8. VSCode:**

```powershell
choco install vscode -y
```

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**9. Sublime Text 3:**

```powershell
choco install sublimetext3 -y
```

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

***

#### 🍎 macOS (Terminal)

**1. VirtualBox:**

```bash
brew install --cask virtualbox
```

* `--cask` — installs a GUI application (not a CLI formula)
* ⚠️ **Not for M1/M2 Macs** — skip this if you have Apple Silicon [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**2. Vagrant:**

```bash
brew install --cask vagrant
```

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**3. Vagrant Manager:**

```bash
brew install --cask vagrant-manager
```

* macOS-specific GUI utility for managing Vagrant VMs from the menu bar [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**4. Git:**

```bash
brew install git
```

* No `--cask` — Git is a CLI tool (formula) [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**5. Java (OpenJDK 17):**

```bash
brew install openjdk@17
```

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

Then **create the Java symlink** so macOS discovers the JDK:

```bash
sudo ln -sfn $HOMEBREW_PREFIX/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk
```

* `sudo` — run with root privileges (required to write to `/Library/Java/`)
* `ln` — create a link
* `-s` — symbolic link (not hard link)
* `-f` — force: overwrite if a link already exists there
* `-n` — treat the target as a normal file if it's already a symlink (prevents recursion)
* `$HOMEBREW_PREFIX/opt/openjdk@17/...` — where Homebrew actually installed the JDK
* `/Library/Java/JavaVirtualMachines/openjdk.jdk` — where macOS expects to find JDKs

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

Then **reload the shell** to pick up the new Java PATH:

```bash
exec zsh -l
```

* `exec` — replaces the current process (instead of spawning a child)
* `zsh` — the default macOS shell
* `-l` — login shell: re-reads all profile/configuration files

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**6. Maven:**

```bash
brew install maven
```

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**7. VSCode:**

```bash
brew install --cask visual-studio-code
```

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**8. IntelliJ IDEA:**

```bash
brew install --cask intellij-idea
# OR community edition:
brew install --cask intellij-idea-ce
```

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**9. Sublime Text:**

```bash
brew install --cask sublime-text
```

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

**10. AWS CLI:**

```bash
brew install awscli
```

 [\[10-Prereqs_doc \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-Prereqs_doc.pdf)

***

### Phase 4: Post-Installation Verification

After all installations complete, you should have these tools available: [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

| Tool         | Verify With                                             |
| ------------ | ------------------------------------------------------- |
| VirtualBox   | Open VirtualBox GUI or `VBoxManage --version`           |
| Git          | `git --version`                                         |
| Vagrant      | `vagrant --version`                                     |
| Java 17      | `java -version`                                         |
| Maven        | `mvn -version`                                          |
| AWS CLI      | `aws --version`                                         |
| IntelliJ     | Open from Start Menu / Applications                     |
| VSCode       | `code --version` or open from Start Menu / Applications |
| Sublime Text | Open from Start Menu / Applications                     |

The instructor confirms installation success by visually checking each tool completes without error and mentions: "If you have these tools now ready, then we can get on to the next thing, which is signing up at few accounts." [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

**Common failure scenarios:**

* **PowerShell not elevated** → Chocolatey commands fail with permission errors. Fix: close PowerShell, reopen as Administrator.
* **Network/proxy issues on macOS** → Brew downloads fail with SSL errors. Fix: ensure `.curlrc` contains `-k`.
* **Old Java/Maven still in PATH** → `java -version` shows wrong version after installation. Fix: uninstall old version (Phase 2), restart terminal.
* **Vagrant takes very long** → Normal. The installer is large. Wait patiently. [\[10-install...-softwares \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/10-installing-softwares.txt)

***

***

## 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

### System Architecture

```
LOCAL MACHINE (Windows / macOS)
│
├── Package Manager Layer
│   ├── Windows: Chocolatey (choco) ← requires Admin PowerShell
│   └── macOS:  Homebrew (brew)     ← requires .curlrc (-k) pre-config
│               ├── Formulae (CLI tools): git, maven, openjdk, awscli
│               └── Casks (GUI apps):     virtualbox, vagrant, vscode, intellij, sublime
│
├── Tools Installed
│   ├── Infrastructure:  VirtualBox (hypervisor) + Vagrant (VM automation)
│   ├── Version Control: Git
│   ├── Build Chain:     JDK 17 (runtime) + Maven (build tool)
│   ├── Cloud:           AWS CLI
│   └── Editors:         VSCode (primary) + IntelliJ (Java) + Sublime (lightweight)
│
└── Source of Truth
    └── github.com/hkhcoder/vprofile-project → branch: prereqs → PDF/MD docs
```

***

### Operational Flow

```
1. GET DOCUMENT
   repo → prereqs branch → open MD/PDF

2. INSTALL PACKAGE MANAGER
   Windows: chocolatey.org/docs/installation → choco available
   macOS:   brew.sh → brew available
            └── then: echo -k > ~/.curlrc (SSL bypass for curl)

3. CLEAN ENVIRONMENT
   choco list / brew list → inventory
   java -version, mvn -version
   ├── error → clean → proceed
   └── version found → choco/brew uninstall <pkg> → re-verify → proceed

4. INSTALL ALL TOOLS (sequential, wait for each)
   choco install <pkg> [--version=X] -y    # Windows
   brew install [--cask] <pkg>              # macOS

5. macOS EXTRA: Java registration
   symlink: Homebrew JDK path → /Library/Java/JavaVirtualMachines/
   shell reload: exec zsh -l

6. VERIFY → next lecture (account signups)
```

***

### Key Decision Logic

```
Version pinned?
├── VirtualBox, Vagrant → YES (course-tested versions)
└── Everything else     → NO  (latest stable OK)

macOS: formula vs cask?
├── CLI tool (git, maven, awscli, openjdk) → brew install <name>
└── GUI app (virtualbox, vagrant, vscode, intellij, sublime) → brew install --cask <name>

M1/M2 Mac?
├── YES → skip VirtualBox
└── NO  → install normally

Pre-existing Java/Maven found?
├── YES → uninstall first (PATH conflict risk)
└── NO  → proceed directly
```

***

### Cause → Effect Chains

```
No .curlrc with -k   → brew downloads hit SSL errors → installation fails (macOS)
Old Java in PATH      → new JDK installed but old one used → builds break silently
No admin PowerShell   → choco has no write permission → install fails (Windows)
No symlink on macOS   → macOS can't find JDK → java -version fails
No shell reload       → PATH stale → newly installed commands "not found"
No version pinning    → newer version installed → course exercises may behave differently
```

***

### Reusable Engineering Patterns

**Pattern: Clean-Before-Install**
Check environment state → remove conflicts → install fresh → verify.
*Applies to:* any tool installation, CI/CD agent setup, Docker image builds, server provisioning.

**Pattern: Registry-Client Package Management**
Single command → client queries remote registry → resolves dependencies → downloads → installs → registers locally.
*Applies to:* `choco`, `brew`, `apt`, `yum`, `pip`, `npm`, `cargo` — every modern package ecosystem.

**Pattern: Version Pinning for Reproducibility**
Pin versions for components where behavior differences matter; leave unpinned for stable-interface tools.
*Applies to:* Dockerfiles, CI pipelines, IaC (Terraform providers), dependency manifests.

**Pattern: Post-Install Bridge Configuration**
After automated install, manually bridge the gap between where the tool was placed and where the OS expects it (symlinks, PATH edits, config files).
*Applies to:* Java symlink on macOS, `alternatives` on Linux, PATH manipulation in CI runners.

***

### Recall Triggers

| If you're thinking about...                    | Remember...                                                           |
| ---------------------------------------------- | --------------------------------------------------------------------- |
| "How do I install tools for this course?"      | `choco install` / `brew install` from the prereqs document            |
| "Why did my install fail on macOS?"            | Check `.curlrc`, check `--cask` vs formula, check M1/M2 compatibility |
| "Why does `java -version` show wrong version?" | Old installation in PATH → uninstall first → restart terminal         |
| "Where's the prereqs document?"                | `github.com/hkhcoder/vprofile-project` → `prereqs` branch             |
| "What editor does the course use?"             | VSCode primarily, IntelliJ for Java                                   |
| "Why pin VirtualBox/Vagrant versions?"         | Course exercises tested against specific versions                     |

***

This completes the full reconstruction. All three sections are designed to be complementary — Theory builds understanding, Practical guides execution, and the Compression Map enables rapid reload without re-reading everything. Want me to generate this as a downloadable Markdown or PDF file?

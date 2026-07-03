# 📘 Introduction to Git & Version Control Systems — Complete Deep Learning Analysis

**Source:** Video captions from *"Introduction to Git"* lecture [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

This lecture introduces **version control** from first principles — starting with the raw problem of managing file changes, progressing through the evolution of version control system types (localized → centralized → distributed), and arriving at **Git** as the dominant distributed VCS. The instructor demonstrates the manual versioning problem live, builds the conceptual need for a tool, and explains exactly where Git fits in the DevOps workflow and why every DevOps engineer must master it.

***

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

### 1. Why a DevOps Engineer Needs Git — Two Distinct Reasons

The instructor opens with two explicit reasons why Git is essential for DevOps, and they address two different sides of the role: [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

**Reason 1 — Working with developers.** As a DevOps engineer, you will work alongside developers. When they make changes to their code, you are responsible for **fetching that code, building it, testing it, and deploying it to servers.** To do this, you must communicate with developers and understand their language. Git is that language — it's how code moves, how changes are tracked, and how versions are managed. Without understanding Git, you cannot participate in the software delivery pipeline.

**Reason 2 — Your own work is text-based.** A DevOps engineer writes scripts, automation code, infrastructure-as-code, configuration files, and many other forms of text-based data. All of this text needs version control — you need to track changes, roll back mistakes, collaborate with team members, and maintain history. Git serves as your personal and team versioning system for everything you create. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

The section roadmap includes: understanding VCS concepts, centralized vs distributed systems, Git itself, creating and working with Git repositories, versioning operations, expanding to GitHub (remote repositories), Git concepts and commands, SSH login to GitHub, and GitHub Copilot (AI tool — setup only in this section, usage in later sections). [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

***

### 2. The Raw Problem — Manual Versioning and Its Failures

Before introducing any tool, the instructor demonstrates the **exact problem** that version control solves, using a live scenario. He plays the role of a DevOps engineer working with shell scripts in a folder. The workflow is: open a script → make changes → save → execute → if it breaks, you need to revert. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

**For small changes**, reverting is manageable — you or a team member remembers what was changed, communicates, and undoes it. But as changes accumulate, **rolling back becomes increasingly difficult.** You can't remember exactly what changed, when, or by whom.

The traditional solution, which the instructor practiced early in his career as a system administrator, was to **take a backup of the file with a timestamp before making changes.** The pattern: copy the file with the same name plus a timestamp appended (date, and if multiple changes per day, also hour and minute). For example: `multi_os_setup_web_setup.sh.27May2025_1430.backup`. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

With the backup, you can modify the original freely and roll back by overwriting the original with the backup copy. This gives you **rollback capability** — you can return to any point-in-time version by finding the backup with the right timestamp.

**But this creates new problems:**

* You quickly accumulate **many backup files** (potentially hundreds)
* You must **manage, archive, and store** these backups alongside the originals
* **Comparing versions** across many backups is tedious
* **Finding the right version** to roll back to requires scanning timestamps
* The entire process is manual, error-prone, and scales badly
* There's no built-in mechanism for **who** changed **what** and **why** [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

The instructor makes the key conceptual pivot: *"What do we have now? We have multiple versions of the same file. This is what exactly versioning means — managing multiple versions of a text file."* The problem is clear, the manual method is inadequate, and the stage is set for a tool that handles all of this automatically. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

🔍 **Deep Dive:**
This manual demonstration is pedagogically powerful because it grounds the abstract concept of "version control" in a visceral, concrete problem. Every learner has experienced the anxiety of editing a file and not knowing how to get back to a working state. The timestamp-backup method is real — many professionals actually did (and some still do) this. Understanding the pain of manual versioning makes the value of Git immediately obvious and deeply felt.

***

### 3. Version Control System — What It Is

A version control system (VCS) is a tool that manages multiple versions of your documents, programs, websites, or any text-based content. It is described as a **"time machine"** — it keeps the complete history of all files and tracks every change. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

Internally, a VCS maintains its own **special kind of database** (not a regular file system or SQL database) that stores: every version of every tracked file, what changed between versions, when changes were made, and who made them. It uses better versioning methods than manual timestamps — structured identifiers that precisely identify each version. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

**Why use a VCS?** The instructor builds the case progressively: [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

* **For individuals:** You get a time machine to go back to any previous version of any file.
* **For projects:** When you have many files in a project, tracking all their versions manually becomes impractical. A VCS handles this automatically.
* **For teams (the best part):** In organizations, multiple people work on the same code. A VCS allows multiple people to commit to the same repository, tracks who made what change, when, and why. It enables **collaboration** — people working together on the same codebase without overwriting each other's work. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

The instructor emphasizes that version control is not new — it's been around for a long time, and there are different kinds.

***

### 4. Types of Version Control Systems — The Evolution

The lecture presents three types, forming an evolutionary progression where each solves the problems of the previous: [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

**Localized Version Control System** — for individuals only. You control versioning of files on your local machine. You have local copies and local version history. This is essentially the manual backup approach but managed by a tool. **Problem:** single point of failure. If your system fails, your code is gone. Not dependable. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

**Centralized Version Control System (CVCS)** — introduces a **server** that holds the main (complete) copy of the repository, with multiple clients connecting to it. The workflow: clients fetch code from the server, make changes locally on their **working copy**, and push changes back to the server. The server maintains all versions and history. Examples: **Subversion (SVN), CVS, Perforce.** [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

Key terminology for CVCS: **checkout** means pulling the code to your local system. The server holds the "official copy" — the entire history of the repository. Your workstation has only the working copy.

**Problem with CVCS:** Still has a **single point of failure** — the server. If the server is down or not performing, you cannot do versioning. You cannot commit, you cannot check out, you cannot access history. Your work is blocked until the server recovers. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

**Distributed Version Control System (DVCS)** — solves the single-point-of-failure problem fundamentally. In a DVCS, **every individual has the full copy of the repository** — not just a working copy, but the complete repository with all history. When you make changes, you make them to your **local repository** first. You do all versioning operations (commits, history, branching) locally. When you're ready, you **sync** your local repository with the remote (server) repository. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

The critical advantage: **even if the centralized/remote repository is down, you can still work on your local system with your full copy.** You lose nothing. Your local repository is "just as good as theirs" — it contains everything the server has. Most operations are local, meaning they're fast (no network dependency) and always available.

Key DVCS operations: [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

* **Clone** — download the entire repository (complete copy) to your local machine. This is the first thing you do.
* **Commit** — save a version in your local repository (the term used instead of "check in")
* **Push** — send your local commits to the remote repository
* **Pull** — download other people's changes from the remote repository to your local copy

Examples of DVCS: **Git** (the biggest example), Mercurial. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

🔍 **Deep Dive:**
The architectural shift from centralized to distributed is profound. In CVCS, the server is the single source of truth and the bottleneck — all operations require server connectivity. In DVCS, the repository is **replicated** across every participant. This is a **peer-to-peer architecture** for version control. The "central" repository (like GitHub) is central by **convention**, not by architectural necessity — any clone is technically a complete repository. This means the system is inherently fault-tolerant: if the server disappears, any clone can become the new server.

***

### 5. Git — What It Is and Why It Dominates

Git is a **distributed version control system**, and it is the most popular VCS in the world. The instructor lists why: [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

* **Ease and speed** — operations are fast because most are local
* **Supports non-linear development** — you can work on multiple lines of development simultaneously (branching)
* **Fully distributed** — every clone is a complete repository
* **Handles large projects** — designed for scale (originally built for the Linux kernel)
* **Easy to use** — powerful yet accessible

Git was created by **Linus Torvalds** — the same person who created the Linux kernel. He needed a better version control system for Linux kernel development, so he built Git. Initially used for versioning the Linux kernel code, it was then made available to everyone — following the same open-source spirit as Linux itself. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

**Cloud-based remote repository providers** host Git repositories in the cloud, providing a central place for teams to sync their distributed repositories: [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

* **GitHub** — the most popular
* **Bitbucket**
* **AWS CodeCommit**
* **Azure Repos** (on Azure)
* **Google Cloud Source Repositories** (on Google Cloud)

These are not Git itself — they are **hosting platforms** for Git repositories, adding features like web interfaces, pull requests, access control, and CI/CD integration on top of Git's core functionality.

***

### 6. Git Installation — Platform Coverage

Git installation is described as "super easy" and often already present: [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

* **Windows:** Already installed in the prerequisites section. Git Bash (the terminal used throughout the course) **is** the Git installation — it includes both the Git version control system and a Linux-like terminal.
* **macOS:** Installed in the prerequisites through Homebrew: `brew install git`.
* **Linux (Ubuntu/Fedora):** Install via the OS package manager: `yum install git` or `apt install git`.

Many operating systems come with Git by default. The verification command is `git --version` — if it returns a version number, Git is installed. If you get "command not found," you need to install it. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

***

### 7. GitHub Copilot — Brief Introduction

The section will include setting up **GitHub Copilot**, described as an "AI tool from Git" that "makes our life way lot easier and also fun." In this section, only the setup will be covered. Actual usage and exploration of Copilot will happen in later sections of the course. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

***

### 8. The Nature of DevOps Work — Text Creation

The instructor frames the daily work of a developer, DevOps engineer, or tester as fundamentally: **creating text, saving text, editing text — repeatedly.** The "text" is not essays or documents — it's scripts, automation code, configuration files, infrastructure definitions, and other technical artifacts. All of these are text files, and all of them change over time, making version control essential for every role in software delivery. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

***

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

### What We Are Building and Why

This lecture is primarily conceptual — it builds the understanding needed before hands-on Git work begins in the next lecture. The practical elements here are: (1) understanding the manual versioning workflow and its failures, (2) verifying Git is installed, and (3) knowing how to install Git if it isn't. The final operational outcome of this lecture: you understand exactly what problem Git solves, how it works at a high level, and you've confirmed Git is ready on your system for the next lecture. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

***

### Step 1: Understanding Manual Versioning (Demonstration — Watch Only)

The instructor demonstrates this live. You do **not** need to replicate this — it's a conceptual demonstration. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

**The scenario:** A DevOps engineer has shell scripts (`.sh` files) in a folder that they regularly use and modify.

**The workflow demonstrated:**

1. Open a script file → make changes → save → execute
2. If it breaks → need to revert → open file again → undo changes → save
3. For small changes: manageable. For larger/repeated changes: increasingly difficult to remember and roll back.

**The backup method:**

```bash
date
```

Check current date and time to create the timestamp. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

```bash
cp multi_os_setup_web_setup.sh multi_os_setup_web_setup.sh.27May2025_1430.backup
```

* `cp` = copy
* Original filename → same name + `.27May2025_1430.backup` appended
* The timestamp includes date and time (hour + minute) because multiple changes per day are common

**Rolling back:**

```bash
cp multi_os_setup_web_setup.sh.27May2025_1430.backup multi_os_setup_web_setup.sh
```

Copy the backup over the original, overwriting it with the previous version. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

**The problem that emerges:** After many changes, you accumulate many `.backup` files. These need to be managed, archived, and stored safely. Comparing versions and finding the right rollback point becomes tedious. This is **manual versioning** — it works, but it's painful at scale.

**Key takeaway:** This is exactly what a version control system automates — managing multiple versions, tracking history, enabling rollback, and doing it efficiently without cluttering your workspace with backup files. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

***

### Step 2: Verify Git Installation

**Open your terminal:**

* Windows: Git Bash (already installed from prerequisites)
* macOS: Terminal
* Linux: Terminal

```bash
git --version
```

* `git` = the Git command
* `--version` = display the installed version

**Expected output:** A version string like `git version 2.x.x`. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

**If you get "command not found":**

**On Windows:** Git Bash should already be installed from the prerequisites section. If not, reinstall it.

**On macOS:**

```bash
brew install git
```

Uses Homebrew (installed in prerequisites) to install Git. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

**On Ubuntu:**

```bash
apt install git
```

**On CentOS/Fedora:**

```bash
yum install git
```

Uses the OS package manager (covered in the package management lecture). [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

**Verification after install:**

```bash
git --version
```

Should now return a version number. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

**Connection to larger flow:** With Git verified, you are ready for the next lecture where you'll start using Git for actual versioning operations — creating repositories, making commits, and working with version history.

***

***

## 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

### The Core Problem Git Solves

```
Manual versioning:
  file.sh → edit → breaks → need to revert → can't remember changes
  
  "Solution": cp file.sh file.sh.27May2025_1430.backup
    → works for 1-2 versions
    → fails at scale: hundreds of backups, no comparison, no collaboration
    → who changed what? when? why? → unknown

Git:
  → tracks EVERY change automatically
  → stores ALL versions in a special database
  → enables rollback to ANY point in time
  → tracks WHO changed WHAT, WHEN, and WHY
  → enables TEAM collaboration on same codebase
```

***

### VCS Evolution — Three Stages

```
LOCALIZED VCS
  │  All versions on local machine only
  │  ⚠️ Single point of failure: disk dies → everything lost
  ↓
CENTRALIZED VCS (SVN, CVS, Perforce)
  │  Server = complete copy + full history
  │  Clients = working copies only
  │  Checkout ↓↑ Commit
  │  ⚠️ Single point of failure: server down → no versioning
  ↓
DISTRIBUTED VCS (Git, Mercurial)
     Every clone = FULL repository + FULL history
     Local operations: commit, branch, history → no network needed
     Remote sync: push (send) / pull (receive)
     ✅ No single point of failure
     ✅ Server down → still fully functional locally
```

***

### Centralized vs Distributed — Architecture Contrast

```
CENTRALIZED (SVN):                 DISTRIBUTED (Git):
┌─────────┐                        ┌─────────┐
│  SERVER  │ ← full repo           │ REMOTE   │ ← full repo (by convention)
│  (SPOF)  │                       │  REPO    │
└────┬─────┘                       └──┬───┬───┘
     │                           push↑   ↓pull
  checkout/                     ┌────┴─┐ ┌┴─────┐
  commit                        │LOCAL │ │LOCAL  │
     │                          │REPO  │ │REPO   │ ← each is FULL copy
┌────┴────┐  ┌────────┐        │(full)│ │(full) │
│ working │  │working │        └──────┘ └───────┘
│  copy   │  │ copy   │
│ (partial)│ │(partial)│        clone = download EVERYTHING
└─────────┘  └────────┘        commit = LOCAL operation
                                push/pull = SYNC with remote
```

***

### Git Operations — Core Vocabulary

```
clone  → download entire repository (first time)
commit → save a version LOCALLY
push   → send local commits → remote repository
pull   → receive remote changes → local repository

Most operations = LOCAL (fast, always available)
Remote operations = push/pull only (need network)
```

***

### Why DevOps Needs Git — Two Axes

```
AXIS 1: Working WITH developers
  Developers write code → push to Git
  DevOps: fetch → build → test → deploy
  Git = the shared language and transport mechanism

AXIS 2: Your OWN work
  DevOps writes: scripts, automation, IaC, configs
  All text-based → all need versioning
  Git = your personal version control
```

***

### Git — Key Properties

```
Distributed       → every clone is a full repository
Fast               → most operations are local (no network)
Non-linear         → supports branching (multiple development lines)
Scalable           → handles large projects (built for Linux kernel)
Easy               → powerful yet accessible

Creator: Linus Torvalds (also created Linux kernel)
Origin:  needed better VCS for Linux kernel development → built Git
```

***

### Git Hosting Providers (Remote Repository Platforms)

```
GitHub         → most popular (used in this course)
Bitbucket      → Atlassian
CodeCommit     → AWS
Azure Repos    → Microsoft Azure
Cloud Source    → Google Cloud

These are NOT Git → they HOST Git repositories
They ADD: web UI, pull requests, access control, CI/CD
```

***

### Git Installation — Platform Map

```
Windows  → Git Bash (installed in prerequisites) = Git + Linux terminal
macOS    → brew install git (via Homebrew)
Ubuntu   → apt install git
CentOS   → yum install git

Verify:  git --version → should return version number
Error:   "command not found" → install using above commands
```

***

### Section Roadmap — What's Coming

```
This lecture: WHY versioning → VCS types → what is Git → verify install
     ↓
Next lectures:
  ├── Git repositories (create, work with)
  ├── Versioning operations (commit, log, diff, rollback)
  ├── GitHub (remote repos, push, pull, clone)
  ├── Git concepts (branches, merges, etc.)
  ├── SSH login to GitHub
  └── GitHub Copilot (setup now, use later)
```

***

### Linus Torvalds Connection — Recurring Character

```
Linux kernel (1991)  → created by Linus Torvalds → open source
Git (2005)           → created by Linus Torvalds → open source
                        (needed better VCS for kernel development)

Both tools: open source, built to solve real engineering problems,
            became industry standards, used by millions
```

***

### Recall Triggers

| If you forget...            | Remember...                                                                                                                               |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Why DevOps needs Git?       | Two reasons: work with devs (fetch/build/deploy) + version own scripts/automation                                                         |
| What is a VCS?              | A time machine — tracks every change, who/what/when/why, enables rollback                                                                 |
| Centralized vs distributed? | Centralized: server has full copy, clients have working copy, server = SPOF. Distributed: EVERYONE has full copy, most ops local, no SPOF |
| What does "clone" mean?     | Download the ENTIRE repository (all history, all files) — not just current version                                                        |
| Most Git operations are...? | LOCAL — no network needed. Only push/pull need network                                                                                    |
| Git Bash on Windows is...?  | Git itself + a Linux-like terminal, installed as one package                                                                              |
| Who created Git?            | Linus Torvalds (also created Linux kernel)                                                                                                |
| GitHub = Git?               | NO. GitHub is a HOSTING platform for Git repositories. Git is the tool                                                                    |
| Manual versioning problem?  | Hundreds of backup files, no comparison, no collaboration, no who/what/why tracking                                                       |

***

This completes the full analysis of the Introduction to Git lecture. Every concept, demonstration, historical context, and operational detail from the video has been preserved across the three complementary sections — Theory for deep understanding, Practical for execution readiness, and Mental Compression Map for rapid future recall. [\[40-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/40-introduction.txt)

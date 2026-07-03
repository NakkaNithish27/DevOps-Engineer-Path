# 📘 Introduction to Linux — Complete Deep Learning Analysis

**Source:** Video captions from *"Introduction to Linux"* lecture   with accompanying course slides [23-Linux+Quickstart+V5.pdf](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf?EntityRepresentationId=f85783c0-7711-47c6-994e-911a72adff03) [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt) [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

This is a comprehensive foundational lecture covering everything a DevOps engineer needs from Linux — from philosophy and architecture down to commands, users, permissions, software management, and services. The video narration establishes conceptual understanding while the slides provide the full command-level detail demonstrated on screen.

***

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

### 1. The Role of Linux in DevOps — Why This Section Exists

Linux is stated as **the foundation on which DevOps and the entire course stands**. This is where the learner's "real technical strength begins." The section is designed for maximum efficiency — learn a lot of Linux in a very short time, focused on what truly matters for DevOps. If you're already a Linux administrator, you can skip this section. If not, mastering it is absolutely essential. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

The four core competency areas covered are: **commands, files, software, and servers**. The learner must be strong in all four. The practical scope includes basic commands (copy, move, directories), Linux file systems and text files, file editing, file permissions, filters and redirection, users and groups, sudo, software management (RPM, Debian, yum, apt), services and processes, and server management (setting up web servers and database servers on Linux VMs). [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

***

### 2. Open Source — The Philosophy Behind Linux

The instructor addresses a common misconception head-on: **open source does not simply mean "free software."** Some open source software isn't free at all. Open source means the **source code** — the code used to create the software — is freely available for anyone to inspect, modify, enhance, and redistribute. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

The power of open source lies in **collaborative development at scale**. A proprietary software might have 5-10 brilliant engineers working on it. An open source project can have hundreds or thousands of contributors worldwide, making the software better, more secure, and more enhanced. Contributors become part of the project, and the software benefits from collective intelligence far exceeding any single company's capacity. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

The instructor credits open source as the primary reason the IT industry has progressed so much. Most popular software in use today is either open source or was once open source. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

🔍 **Deep Dive:**
The PDF slides formalize this with the Free Software Foundation's **four freedoms**: the freedom to run the program for any purpose, to study and modify the source code, to redistribute the program, and to create derivative programs. Many open-source licenses exist, each with different particulars. The GPL (General Public License) is the specific license that enforced open source principles for Linux. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### 3. Linux History — From Unix to the Linux Kernel

The history unfolds in two critical moments: [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

**1984 — The GNU Project and the Free Software Foundation** created an open source version of Unix utilities, distributed under the GPL license. This gave the world a free set of Unix-compatible tools, but they still lacked a free kernel to run them on. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt), [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**1991 — Linus Torvalds** created a Unix-like kernel and made it open source. This is described as literally changing everything in the IT industry. The kernel was similar to Unix but came with some new utilities. He released it under the GPL and solicited assistance online. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt), [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

After that, brilliant minds worldwide took this **Linux kernel** and started developing utilities around it to create complete operating systems. **Today:** Linux kernel + GNU utilities = complete, open source, Unix-like operating system, packaged for targeted audiences as **distributions** (distros). [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

So when you hear "CentOS," "Ubuntu," "Red Hat Linux," "Kali Linux," "Debian" — they are all using the Linux kernel (upgraded over time) with their own utilities, packaging systems, and configurations built around it to form a complete OS. Even your Android phone runs Linux. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

***

### 4. Linux Principles — The Design Philosophy

These principles are fundamental to understanding why Linux works the way it does, and they are especially important for DevOps: [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt), [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Everything is a file.** In Linux, everything is considered a file — including hardware devices like your mouse, keyboard, and printer. You can literally see and interact with these "files." And "file" doesn't just mean text files — it encompasses many types (regular files, directories, links, special files, sockets, pipes — as detailed in the file types table). [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt), [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Small, single-purpose programs.** Linux favors small programs that each do one thing well, rather than bulky monolithic applications. This is the Unix philosophy at its core. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

**Ability to chain programs together.** These small programs can be combined (chained) to perform complex operations. The instructor explicitly draws a parallel to **continuous delivery and continuous integration** — where you have small automations combined together to perform complex pipeline operations. This is the same principle. The mechanism for this chaining is **piping** (`|`), which feeds the output of one program as input to the next. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

**Avoid captive user interfaces.** Linux discourages graphical "next, next, next, finish" workflows. If a program opens and waits for user input, it has "captured" the user interface — the user must be present to click or type for the program to continue. This is antithetical to automation. Being a DevOps engineer, you should avoid such things because it's difficult to run things in the background or automate them if they require human interaction. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

**Configuration data stored in text files.** This is extremely valuable for DevOps. Instead of navigating through GUI settings panels and tabs, you can directly edit text configuration files. Changes are scriptable, version-controllable, and automatable. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

⚠️ **Expert Note:**
These principles aren't just historical design choices — they are the **architectural reasons** Linux dominates DevOps. Piping enables pipeline thinking. Text-based config enables infrastructure-as-code. Avoiding captive UIs enables unattended automation. Small composable programs enable modular toolchains. Understanding these principles explains *why* Linux is the DevOps platform, not just *that* it is.

***

### 5. Why Linux — The Practical Case

Beyond philosophy, there are concrete reasons Linux dominates: [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt), [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

* **Open source** — huge community support, constant updates and improvements
* **Supports wide variety of hardware** — runs on phones, laptops, servers, supercomputers, embedded devices
* **Highly customizable** — you can modify virtually anything about the OS
* **Most servers run Linux** — including some of the most popular supercomputers
* **Most DevOps tools implement on Linux only** [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)
* **Automation is much easier** on Linux compared to Windows (though Windows is catching up with PowerShell)
* **Considered more secure** than Windows (though the instructor notes this is debatable)

***

### 6. Linux Architecture — The Layered System

The architecture follows a clean layered model from inside out: [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt), [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

```
Hardware (CPU, RAM, Network — compute resources)
    ↕
Kernel (reads/understands hardware, passes signals to/from shell)
    ↕
Shell (execute commands, expect returns)
    ↕
Tools/Utilities/Applications (from simple: cd, vi, cat, ls → to graphical: browsers, PDF readers)
    ↕
Users (connect to tools, which send information to kernel)
```

The **kernel** is the core — this is what Linus Torvalds developed. It sits directly on hardware and is the only component that can communicate with hardware. The **shell** is the interface between the user and the kernel — when you execute commands, the shell interprets them and communicates with the kernel. **Tools and utilities** are built around the kernel and provide the actual functionality users interact with — from basic commands to full graphical applications. Multiple users can connect simultaneously, each interacting through the tool/shell/kernel chain. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt), [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

🔍 **Deep Dive:**
The architecture diagram from the slides shows concentric circles: Hardware at the center, then Kernel, then Shell, then Applications/Compilers at the outermost ring. Multiple users (User 1, User 2, User 3, User n) connect from outside through tools like `vi`, `cd`, `grep`, `date`, and compiled programs (`a.out`). This visualizes the multi-user, multi-tool nature of Linux — all funneling through the kernel to shared hardware. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### 7. Linux Distributions — Desktop vs Server, RPM vs Debian

Linux distributions (distros) are the many "flavors" of Linux — complete operating systems built around the Linux kernel. The instructor shows the Wikipedia list to demonstrate the enormous scale — there are many, many Linux flavors. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

**Popular Desktop Distros:** Ubuntu Linux (most popular), Linux Mint, Arch Linux, Fedora, Debian, OpenSuse. The instructor recommends doing a dual boot and using Linux as much as possible for desktop needs to become comfortable with Linux systems. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt), [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Popular Server Distros:** Red Hat Enterprise Linux (RHEL — most stable and secure, not open source, has licensing), Ubuntu Server (open source, instructor's personal favorite for ease, though some disagree on security), CentOS (similar to RHEL but open source), SUSE Enterprise Linux. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt), [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**The Two Families That Matter in IT:**
In the IT industry, you will primarily encounter two families: **RPM-based** and **Debian-based**. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

**RPM-based:** RHEL, CentOS, Oracle Linux, Amazon Linux (used on AWS EC2), Fedora, OpenSuse
**Debian-based:** Ubuntu Server, Kali Linux (used by penetration testers), and many more [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

The **major difference** between these two families starts with the **packaging method** for software — how software is packaged, distributed, and installed: [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt), [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

| Aspect                 | Debian-based                             | RPM-based                                         |
| ---------------------- | ---------------------------------------- | ------------------------------------------------- |
| Package extension      | `.deb`                                   | `.rpm`                                            |
| Manual install command | `dpkg -i package.deb`                    | `rpm -ivh package.rpm`                            |
| Package manager        | `apt`                                    | `yum` / `dnf`                                     |
| Example package        | `google-chrome-stable_current_amd64.deb` | `google-chrome-stable-57.0.2987.133-1.x86_64.rpm` |

Beyond packaging, commands, file names, and configuration paths will also differ between the families. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

**When to use which (instructor's personal preference):**

* **Red Hat-based for running servers** — stability and security-focused. RHEL tests all software thoroughly before releasing to users (compared to Apple's approach). You download only from Red Hat's repository.
* **Debian-based (Ubuntu) for DevOps/automation** — you may need latest libraries and software, easy installation, and user-friendliness. Avoids software installation headaches.
* No hard and fast rule — you can do either on any OS, but this is the general mentality. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

Being a DevOps engineer, you should be comfortable in **any** Linux operating system. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

***

### 8. Linux Directory Structure — The Filesystem Map

In Linux, "directories" are what Windows users call "folders." The filesystem has a well-defined structure where each directory serves a specific purpose: [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt), [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Home Directories:** `/root` for root user, `/home/username` for normal users (e.g., `/home/vagrant`). Every user gets their own home directory.

**User Executables:** `/bin`, `/usr/bin`, `/usr/local/bin` — commands that normal users can execute (`cat`, `pwd`, `ls`, etc.).

**System Executables:** `/sbin`, `/usr/sbin`, `/usr/local/sbin` — commands for root user (system admin commands like `rpm`, `dpkg`, `useradd`).

**External Device Mountpoints:** `/media`, `/mnt` — where USB drives, CDs are automatically mounted.

**Configuration:** `/etc` — **this is where you'll spend a lot of time**. Network configuration, server configuration, user configuration — most configuration lives here.

**Temporary Files:** `/tmp` — for temporary data. **Warning:** contents may be deleted on reboot.

**Kernel and Bootloader:** `/boot`

**Server Data:** `/var`, `/srv` — website files go in paths like `/var/html`, MySQL data in `/var/lib/mysql`. **You'll spend a lot of time here too.**

**System Information:** `/proc`, `/sys`

**Shared Libraries:** `/lib`, `/usr/lib`, `/usr/local/lib`

***

### 9. Absolute vs Relative Paths — Navigation Logic

A **path** is a unique location to a file or folder in the filesystem — a combination of `/` and alphanumeric characters. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Absolute path** specifies location from the root directory (`/`). It is a complete path from the start of the filesystem. All absolute paths start with `/`. Examples: `/home/imran/linux-practices/`, `/var/ftp/pub`, `/etc/samba.smb.conf`, `/boot/grub/grub.conf`. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Relative path** is defined relative to the present working directory (`pwd`). If you are in `/home/imran` and want to reach `/home/imran/linux-practices`, you simply use `cd linux-practices/` — no leading `/`. Relative paths **never** start with `/`. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### 10. File Types in Linux — Everything is a File, But Not All Files Are Equal

Linux has six distinct file types, each identified by the first character in `ls -l` output: [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

| Type         | Character | Description                                                      |
| ------------ | --------- | ---------------------------------------------------------------- |
| Regular file | `-`       | Normal files: text, data, executables                            |
| Directory    | `d`       | Files that are lists of other files                              |
| Link         | `l`       | A shortcut pointing to the actual file location                  |
| Special file | `c`       | Mechanism for I/O, such as files in `/dev`                       |
| Socket       | `s`       | Inter-process networking, protected by filesystem access control |
| Pipe         | `p`       | Allows processes to communicate without network socket semantics |

**Symbolic links** are like desktop shortcuts in Windows. They point to another file or directory. You can create a soft link to access a distant directory from your current location. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### 11. The VIM Editor — Three-Mode Architecture

VIM (Vi IMproved) is the most popular command-mode editor for files in Linux. Other editors exist (emacs, gedit), but vi/vim is dominant. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

VIM operates in **three modes**, and understanding this modal architecture is essential: [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Command Mode** — the **default mode** when you open vim. You navigate, copy, delete, search, but you **cannot type text**. Key operations include: `gg` (go to beginning), `G` (go to end), `w`/`b` (move word forward/backward), `yy` (copy line), `dd` (delete line), `p`/`P` (paste below/above), `u` (undo), `Ctrl+R` (redo), `/` (search).

**Insert Mode (Edit Mode)** — entered by pressing `i` from command mode. Now you can type and edit text. The status bar shows `-- INSERT --`. Press `Esc` to return to command mode.

**Extended Command Mode (Colon Mode)** — entered by pressing `Esc` then `:` from command mode. Used for save/quit operations: `:w` (save), `:q` (quit without saving), `:wq` (save and quit), `:w!` (force save), `:wq!` (force save and quit), `:x` (save and quit), `:X` (set/remove password), `:20` (go to line 20), `:se nu` (show line numbers), `:se nonu` (hide line numbers). [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

🔍 **Deep Dive:**
The three-mode design embodies the Linux principle of separating concerns. Navigation/manipulation (command mode), text entry (insert mode), and file operations (extended mode) are distinct operations with distinct interfaces. This prevents accidental edits while navigating and keeps the editor lightweight — every keystroke in command mode is a shortcut, not a character to insert.

***

### 12. Filters, Grep, and I/O Redirection — Data Flow Engineering

This is described by the instructor as a **really very important topic for DevOps**. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

**grep** is used to find text from any text input. It searches for patterns in files or piped input. Linux is **case-sensitive** — "root" and "Root" are different. Use `-i` to ignore case. Use `-v` to display everything **except** the matched word. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Filter commands** allow viewing file content in controlled ways: [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

* **`less`** — displays content page-wise or line-wise. Navigate with `Enter` (line by line), `d` (next page), `b` (previous page), `/` (search), `v` (enter vi mode for editing).
* **`more`** — similar to `less` with the same navigation keys.
* **`head`** — displays the **top 10 lines** of a file by default.
* **`tail`** — displays the **last 10 lines** of a file by default.
* **`cut`** — extracts fields from text using delimiters. Syntax: `cut -d: -f1 filename` (delimiter `:`, field 1).
* **`sed`** (stream editor) — search and replace in output. Syntax: `sed 's/searchfor/replacewith/g' filename`. **Important note:** sed only modifies the output, not the original file. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**I/O Redirection** is the process of copying command output into files: [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

* **`>`** — redirect output to file (creates new or **overwrites** existing)
* **`>>`** — **append** output to file (preserves existing content)
* **`2>>`** — redirect only **error output** (stderr) to file
* **`&>>`** — redirect **all output** (stdout + stderr) to file

**Piping (`|`)** feeds the output of one program as input to the next program. This is the mechanism that implements the Linux principle of chaining small programs for complex operations. Examples: `ls | head -3`, `ls | grep logdir`, `cat /etc/passwd | grep root`. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**`find`** command locates files by path, name, inode number, type, user, or group. Syntax: `find /path/ -name filename`. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### 13. Users and Groups — Access Control System

Users and groups exist to **control access to files and resources**. Every file is owned by a user and associated with a group. Every process has an owner and group affiliation and can only access resources its owner/group can access. Users cannot read, write, or execute each other's files without permission. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Three types of users:** [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt), [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

| Type        | Example                | UID        | GID        | Home Dir         | Shell           |
| ----------- | ---------------------- | ---------- | ---------- | ---------------- | --------------- |
| **Root**    | `root`                 | 0          | 0          | `/root`          | `/bin/bash`     |
| **Regular** | `imran`, `vagrant`     | 1000–60000 | 1000–60000 | `/home/username` | `/bin/bash`     |
| **Service** | `ftp`, `ssh`, `apache` | 1–999      | 1–999      | `/var/ftp` etc.  | `/sbin/nologin` |

**Root** is the admin, all-powerful user. **Regular users** are created by root for human users. **Service users** are automatically created when software is installed (e.g., installing Apache creates an `apache` user). Service accounts have `/sbin/nologin` as their shell — they **cannot log in interactively**. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

When a user is created, Linux automatically: creates a home directory (`/home/username`), creates a mailbox (`/var/spool/mail`), and assigns a unique UID and GID. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Critical system files for user/group management:** [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

* **`/etc/passwd`** — stores user information. Each line has 7 colon-separated fields: username, `x` (link to shadow file), UID, GID, comment, home directory, shell.
* **`/etc/shadow`** — stores encrypted passwords and password policy (last changed, min/max age, warning period, disable period).
* **`/etc/group`** — stores group information: group name, group password, GID, group members.

***

### 14. File Permissions — The Security Model

File permissions are viewed with `ls -l`. Four symbols represent permissions: **`r`** (read), **`w`** (write), **`x`** (execute), **`-`** (no permission). Permissions are displayed as three groups of three characters: **owner**, **group**, **others**. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Ownership changes:** Only root can change a file's owner. Only root or the owner can change a file's group. `chown [-R] user_name file|directory` changes ownership. `chgrp [-R] group_name file|directory` changes group. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Two methods to change permissions:** [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Symbolic method:** `chmod [options] mode file` — where mode uses `u`/`g`/`o` (user/group/other), `+`/`-`/`=` (grant/deny/set), `r`/`w`/`x`. Examples: `chmod ugo+r file` (grant read to all), `chmod o-wx dir` (deny write+execute to others). Options: `-R` (recursive), `-v` (verbose), `--reference` (copy mode from another file).

**Numeric method:** Three-digit number where each digit = sum of 4 (read) + 2 (write) + 1 (execute). First digit = owner, second = group, third = others. Example: `chmod 755 file` gives owner rwx (7), group r-x (5), others r-x (5). `chmod 640 file` gives owner rw- (6), group r-- (4), others --- (0). [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### 15. Sudo — Controlled Privilege Escalation

`sudo` gives a normal user the power to execute commands owned by the root user. If a user has full sudoers privilege, they can become root anytime using `sudo -i`. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

The sudoers configuration is edited with `visudo` (never edit the file directly). Users are added with the format `username ALL=(ALL:ALL) ALL`. Groups can also be added (prefixed with `%`): `%admin ALL=(ALL) ALL`. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

To eliminate the password prompt for sudo, add `NOPASSWD` in the sudoers entry. You can switch to any other user with `su - username`. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### 16. Software Management — The Package Ecosystem

This is one of the four core competency areas. The instructor demonstrates the **two-tier package management system** that exists in both RPM and Debian families. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt), [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Tier 1 — Low-level package tools (manual installation):**

* **RPM-based:** `rpm -ivh package.rpm` (install), `rpm -Uvh` (upgrade), `rpm -ev` (erase/remove), `rpm -qa` (query all installed)
* **Debian-based:** `dpkg -i package.deb`

The problem with low-level tools: they don't handle **dependencies**. If a package requires other packages, `rpm` will fail. "What if we have hundreds of dependencies?" [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Tier 2 — High-level package managers (automatic dependency resolution):**

* **RPM-based:** `yum` (CentOS 7) / `dnf` (CentOS 8+) — reads repository configuration files from `/etc/yum.repos.d/`, downloads software, resolves dependencies, installs required RPM packages automatically.
* **Debian-based:** `apt` — reads repository information from `/etc/apt/sources.list`.

Core operations are identical across both managers: `search`, `install`, `remove`, `update`, `reinstall`, `groupinstall`, `repolist`, `clean all`, `history`, `info`/`show`. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

🔍 **Deep Dive:**
Note the package name difference: the web server is called `httpd` on RPM-based systems and `apache2` on Debian-based systems. This naming difference extends to services and configuration paths. This is a common source of confusion when switching between distro families. The instructor uses `httpd` on CentOS and `apache2` on Ubuntu throughout.

⚠️ **Expert Note:**
The two-tier architecture (rpm/dpkg as low-level, yum/apt as high-level) is a **controller/engine pattern**. `yum`/`apt` are the controllers that orchestrate installations; `rpm`/`dpkg` are the engines that actually install individual packages. The controllers add dependency resolution, repository management, and transaction handling on top of the basic install/remove capability.

***

### 17. Services — Process Lifecycle Management

Services are managed with `systemctl` on modern Linux (both CentOS and Ubuntu): [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

| Command                          | Purpose                              |
| -------------------------------- | ------------------------------------ |
| `systemctl start <service>`      | Start the service now                |
| `systemctl stop <service>`       | Stop the service now                 |
| `systemctl restart <service>`    | Restart the service                  |
| `systemctl status <service>`     | Show current status                  |
| `systemctl reload <service>`     | Reload configuration without restart |
| `systemctl enable <service>`     | Start at boot time                   |
| `systemctl disable <service>`    | Don't start at boot time             |
| `systemctl is-active <service>`  | Check if currently active            |
| `systemctl is-enabled <service>` | Check if enabled at boot             |

**Important:** The service name differs by distro — `httpd` on CentOS, `apache2` on Ubuntu. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

### What We Are Building and Why

We are building **complete Linux operational proficiency** — the ability to navigate, manage files, edit configurations, control users/permissions, install software, and manage services on Linux systems. The final outcome: you can confidently operate any Linux server, whether RPM-based or Debian-based, for DevOps purposes. All practice happens on the Linux VMs set up in the virtualization section. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt)

***

### Step 1: Basic Navigation and File Operations

**Know your location:**

```bash
pwd
```

`pwd` = **p**rint **w**orking **d**irectory. Shows your current absolute path. For a normal user, you typically start at `/home/username`. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Create a directory:**

```bash
mkdir linux-practices
```

`mkdir` = **m**a**k**e **dir**ectory. Creates a new directory in your current location.

**Change into it:**

```bash
cd linux-practices/
```

`cd` = **c**hange **d**irectory. Your prompt changes to reflect the new location.

**Create more directories and files:**

```bash
mkdir vpdir testdir devopsdir
ls
touch file1 file2 file3 file4
ls
```

`touch` creates empty files. `ls` lists contents of current directory. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Verify your location:**

```bash
pwd
```

Always reconfirm after navigation. Expected: `/home/imran/linux-practices`. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Creating directories using absolute vs relative paths:**

```bash
mkdir devopsdir/ansible                              # relative path
mkdir /home/imran/linux-practices/devopsdir/aws       # absolute path
ls devopsdir/
```

Both create directories inside `devopsdir`, but one uses relative reference (from current location) and the other uses the full path from root. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Copying files:**

```bash
cp file1 testdir/
```

`cp` = **c**o**p**y. Copies `file1` into `testdir/` directory. Original remains.

**Copying directories (requires `-r` for recursive):**

```bash
cp -rvfp testdir/ vpdir/
```

* `-r` = recursive (copy directory and all contents)
* `-v` = verbose (show what's being copied)
* `-f` = force
* `-p` = preserve permissions/timestamps

 [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Moving files/directories:**

```bash
mv devopsdir/ vpdir/
mv file3 file4 vpdir/
```

`mv` = **m**o**v**e. Unlike `cp`, the original is removed from the source location. Also used for renaming. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Removing files and directories:**

```bash
rm file1                  # remove a single file
rm -rf testdir/           # remove directory and all contents
```

* `-r` = recursive
* `-f` = force (no confirmation prompts)

⚠️ **Expert Note:** `rm -rf` is **irreversible**. There is no recycle bin. Double-check your path before executing, especially as root. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Special navigation shortcuts:**

```bash
cd                        # go to home directory
cd -                      # go to previous directory
```

 [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### Step 2: Using VIM Editor

**Install vim (Ubuntu):**

```bash
sudo apt-get install vim
```

`sudo` runs the command as root. `apt-get install` installs the package. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Open/create a file:**

```bash
vim firstfile.txt
```

Opens the file in vim. If it doesn't exist, creates it. You start in **command mode**. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Enter insert mode → type → save and quit:**

1. Press `i` — status bar shows `-- INSERT --`
2. Type your content
3. Press `Esc` — returns to command mode
4. Type `:wq` — saves and quits
5. Press `Enter`

**Read the file:**

```bash
cat firstfile.txt
```

`cat` = con**cat**enate — displays file content to the terminal. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Verification:** The file should display exactly what you typed.

**Key command mode operations to practice:**

| Key            | Action                               |
| -------------- | ------------------------------------ |
| `gg` / `G`     | Go to beginning / end of file        |
| `w` / `b`      | Move forward / backward by word      |
| `dd` / `5dd`   | Delete current line / delete 5 lines |
| `yy` / `5yy`   | Copy current line / copy 5 lines     |
| `p` / `P`      | Paste below / above cursor           |
| `u` / `Ctrl+R` | Undo / redo                          |
| `/word`        | Search for "word"                    |

 [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### Step 3: Using Grep and Filters

**View the passwd file (all system users):**

```bash
cat /etc/passwd
```

 [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Search for "root" in passwd file:**

```bash
grep root /etc/passwd
```

Returns: `root:x:0:0:root:/root:/bin/bash`

**Case-insensitive search:**

```bash
grep -i Root /etc/passwd
```

`-i` = ignore case. Without it, `grep Root` finds nothing because Linux is case-sensitive. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Exclude matches (invert):**

```bash
grep -v root /etc/passwd
```

`-v` = display everything **except** lines containing "root". [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Display top/bottom lines:**

```bash
head /etc/passwd           # first 10 lines
tail /etc/passwd           # last 10 lines
```

 [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Extract specific fields with cut:**

```bash
cut -d: -f1 /etc/passwd
```

* `-d:` = delimiter is `:`
* `-f1` = extract field 1 (usernames only)

 [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Search and replace with sed:**

```bash
sed 's/Tech/Technologies/g' ktfile
```

* `s` = substitute
* `/Tech/` = search for
* `/Technologies/` = replace with
* `/g` = globally (all occurrences on each line)

**Critical note:** sed modifies only the **output**, not the original file. To save changes, redirect output to a new file. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### Step 4: I/O Redirection and Piping

**Redirect output to new file (overwrite):**

```bash
sed 's/tech/tools/g' devopstools > newtools.txt
```

`>` creates `newtools.txt` with the modified output. If the file exists, it is **overwritten**. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Append output to existing file:**

```bash
tail /etc/passwd >> newtools.txt
```

`>>` adds output to the **end** of the file without destroying existing content. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Redirect only errors:**

```bash
uptimer 2>> /tmp/error.log
```

`2>>` redirects **stderr** (file descriptor 2) only. The typo `uptimer` (instead of `uptime`) generates an error, which goes to the log file. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Redirect all output (stdout + stderr):**

```bash
uptime &>> /tmp/error.log
```

`&>>` captures both normal output and errors into the same file. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Piping — chain commands:**

```bash
ls | head -3                        # show first 3 items from ls
ls | grep logdir                    # filter ls output for "logdir"
cat /etc/passwd | grep root         # find root in passwd file
```

The pipe `|` takes the **output** of the left command and feeds it as **input** to the right command. This is the mechanism that enables the Linux principle of chaining small programs. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### Step 5: Creating a Symbolic Link

```bash
ln -s /var/log/ logdir
```

* `ln` = link
* `-s` = symbolic (soft link)
* `/var/log/` = target directory
* `logdir` = name of the link in current directory

Now `ls logdir` shows the contents of `/var/log/` — a shortcut. Verify with `ls -l` — the link shows `logdir -> /var/log/`. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### Step 6: User and Group Management

**Create a user and set password (CentOS):**

```bash
sudo useradd dino
sudo passwd dino
```

`useradd` creates the user. `passwd` sets/resets the password (you'll be prompted twice). [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Switch to the new user:**

```bash
su - dino
```

`su -` = **s**witch **u**ser with a login shell (loads the user's environment). Verify with `pwd` (should show `/home/dino`) and `id` (shows UID, GID, groups). [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Create a group and add user to it:**

```bash
groupadd opsadmin
usermod -G opsadmin devops
```

`usermod -G` adds a user to a supplementary group. Verify: `grep opsadmin /etc/group` and `id devops`. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Delete user and group:**

```bash
sudo userdel -r dino          # -r removes home directory too
sudo groupdel opsadmin
```

Verify deletion: `id dino` → "no such user". [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Note:** On Ubuntu, `adduser` is used instead of `useradd` — it's more interactive and user-friendly. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### Step 7: File Permission Changes

**View permissions:**

```bash
ls -l
```

 [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Symbolic method examples:**

```bash
chmod u+x newtools.txt            # add execute for owner
chmod o-r newtools.txt            # remove read for others
```

 [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Numeric method examples:**

```bash
chmod 700 newtools.txt            # rwx------ (owner only)
chmod 755 newtools.txt            # rwxr-xr-x (owner full, others read+execute)
```

Verify each change with `ls -l` to see the permission string update. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Change ownership:**

```bash
chown sam:sam devopstools         # change owner and group to sam
sudo chown sam:sam devopstools    # needs sudo if you're not root/owner
```

 [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### Step 8: Sudo Configuration

**Become root:**

```bash
sudo -i
```

Changes from normal user to root. Verify with `id` — should show `uid=0(root)`. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Add a user to sudoers:**

```bash
sudo -i
export EDITOR=vim
visudo
```

In the sudoers file, add: `sam ALL=(ALL:ALL) ALL`
Save and exit. User `sam` can now use `sudo`. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Disable sudo password prompt:**
Add `NOPASSWD` to the user's sudoers entry: `sam ALL=(ALL:ALL) NOPASSWD: ALL` [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

### Step 9: Software Installation

**RPM-based (CentOS) — Manual method:**

```bash
curl https://rpmfind.net/linux/centos/7.9.2009/os/x86_64/Packages/tree-1.6.0-10.el7.x86_64.rpm -o tree-1.6.0-10.el7.x86_64.rpm
rpm -ivh tree-1.6.0-10.el7.x86_64.rpm
```

* `curl -o` downloads the file
* `rpm -ivh` = **i**nstall, **v**erbose, **h**ash progress

**When dependencies fail:** Use the high-level package manager instead. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**RPM-based — Using yum:**

```bash
yum install httpd -y              # install with auto-yes
yum remove httpd -y               # remove
yum update                        # update all packages
```

 [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Debian-based (Ubuntu) — Manual method:**

```bash
wget http://archive.ubuntu.com/ubuntu/pool/universe/t/tree/tree_1.7.0-3_amd64.deb
dpkg -i tree_1.7.0-3_amd64.deb
```

 [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Debian-based — Using apt:**

```bash
apt update                        # update package lists first
apt search apache2                # search for a package
apt install apache2 -y            # install
apt remove apache2 -y             # remove
```

 [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Verification:** After installation, run the installed command (e.g., `tree`) or check the service status.

***

### Step 10: Service Management

**Start and manage a web server (CentOS):**

```bash
sudo systemctl start httpd
sudo systemctl status httpd        # verify it's running
sudo systemctl enable httpd        # auto-start at boot
```

 [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Same on Ubuntu:**

```bash
sudo systemctl start apache2
sudo systemctl status apache2
sudo systemctl enable apache2
```

 [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

**Key difference:** Service name is `httpd` on CentOS, `apache2` on Ubuntu.

**Verification:** `systemctl is-active httpd` returns "active" if running. `systemctl is-enabled httpd` returns "enabled" if set for boot. [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

***

***

## 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

### Linux Architecture — Core Layer Stack

```
USER → Tools/Utilities (cd, vim, grep, browsers) → Shell → Kernel → Hardware
         ↑ many users, many tools                            ↑ only kernel talks to hardware
```

***

### Four Competency Areas

```
1. COMMANDS  → navigate, manipulate files, filter data
2. FILES     → types, permissions, ownership, paths, editing
3. SOFTWARE  → packages, repos, install/remove/update
4. SERVERS   → services lifecycle, web/db server setup
```

***

### Linux Principles → DevOps Implications

```
Everything is a file       → uniform interface for all resources
Small single-purpose tools → composable, modular toolchains
Chain programs (piping)    → pipeline thinking (CI/CD analog)
Avoid captive UI           → automation-friendly, background execution
Config in text files       → scriptable, version-controllable, IaC-ready
```

***

### Two Distro Families — Decision Map

```
RPM-based (RHEL, CentOS, Amazon Linux, Fedora)
  Package: .rpm → rpm -ivh
  Manager: yum / dnf
  Repos:   /etc/yum.repos.d/
  Web server service name: httpd
  Use for: SERVERS (stability, security, tested repos)

Debian-based (Ubuntu, Kali, Debian)
  Package: .deb → dpkg -i
  Manager: apt
  Repos:   /etc/apt/sources.list
  Web server service name: apache2
  Use for: DEVOPS/AUTOMATION (latest software, ease of use)
```

***

### Package Management — Two-Tier Architecture

```
HIGH-LEVEL (controller):  yum / dnf / apt
  → resolves dependencies automatically
  → reads from repositories
  → wraps low-level tool
        ↓
LOW-LEVEL (engine):       rpm / dpkg
  → installs single packages
  → NO dependency resolution
  → fails if dependencies missing
```

**Pattern:** Controller/Engine — same as Vagrant/Hypervisor, Terraform/Cloud API

***

### Directory Structure — Function Map

```
/root, /home/user      → Home directories (user workspaces)
/bin, /usr/bin          → User commands (normal user)
/sbin, /usr/sbin        → System commands (root only)
/etc                    → ALL configuration (★ spend most time here)
/var, /srv              → Server data, logs, websites, databases (★ spend most time here)
/tmp                    → Temporary (⚠️ deleted on reboot)
/boot                   → Kernel + bootloader
/proc, /sys             → System/kernel info (virtual filesystems)
/lib, /usr/lib          → Shared libraries
/media, /mnt            → External device mount points
```

***

### User System — Type/ID/Shell Map

```
Root     → UID 0    → /root        → /bin/bash      → all-powerful
Regular  → UID 1000+ → /home/user  → /bin/bash      → human users
Service  → UID 1-999 → /var/...    → /sbin/nologin  → software accounts (can't login)

Files:
  /etc/passwd  → user info (7 colon-separated fields)
  /etc/shadow  → encrypted passwords + policy
  /etc/group   → group info (name:pw:GID:members)
```

***

### Permission System — Decode Pattern

```
-rwxr-xr-- = regular file, owner rwx, group r-x, others r--

Numeric: r=4, w=2, x=1
  rwx = 7, r-x = 5, r-- = 4 → chmod 754

Change: chmod (permissions), chown (owner), chgrp (group)
Only root changes ownership. Owner or root changes group.
```

***

### VIM — Three-Mode Flow

```
OPEN → Command Mode (default)
         │
    [i]  ↓         [Esc] ↑
         │
      Insert Mode (type text)
         │
   [Esc] ↓
         │
Command Mode → [:] → Extended Mode → :wq (save+quit)
                                    → :q! (quit no save)
                                    → :w  (save only)
```

***

### I/O Redirection — Data Flow Operators

```
command > file      → overwrite file with stdout
command >> file     → append stdout to file
command 2>> file    → append stderr only
command &>> file    → append stdout + stderr

command1 | command2 → stdout of 1 → stdin of 2 (piping)
```

***

### Filter Command Quick-Recall Chain

```
grep  → find text in input (case: -i, invert: -v)
less  → page-by-page viewing (d/b/q)
head  → first 10 lines (head -n N)
tail  → last 10 lines (tail -n N)
cut   → extract fields (-d delimiter, -f field)
sed   → search/replace in output (s/old/new/g) — doesn't change original
find  → locate files (-name, -type, -user, -group, -inum)
```

***

### Sudo — Privilege Escalation Flow

```
Normal user → sudo command → executes as root (prompts for user's own password)
            → sudo -i      → become root entirely
            → su - user    → switch to another user

Config: visudo → /etc/sudoers
  Format: username ALL=(ALL:ALL) ALL
  No password: username ALL=(ALL:ALL) NOPASSWD: ALL
  Group: %groupname ALL=(ALL) ALL
```

***

### Service Lifecycle — systemctl

```
               start ←→ stop
                 ↓
              restart (stop + start)
              reload  (re-read config, no downtime)
                 
              enable  (start at boot)
              disable (don't start at boot)
              
              status     → full status report
              is-active  → active/inactive
              is-enabled → enabled/disabled

Service names: httpd (CentOS) = apache2 (Ubuntu)
```

***

### Reusable Patterns Extracted

| Pattern                    | Instance                                                      |
| -------------------------- | ------------------------------------------------------------- |
| **Controller/Engine**      | yum→rpm, apt→dpkg, Vagrant→VirtualBox                         |
| **Small composable units** | Linux commands piped together = CI/CD pipeline stages         |
| **Text-as-interface**      | Config in `/etc`, passwd/shadow/group files = IaC foundation  |
| **Layered architecture**   | Hardware→Kernel→Shell→Tools→User                              |
| **Two-family ecosystem**   | RPM vs Debian = same concepts, different implementations      |
| **Privilege separation**   | Root/Regular/Service users + sudo = least-privilege principle |
| **Avoid captive UI**       | CLI-first = automation-first = DevOps-first                   |

***

### Recall Triggers

| If you need to remember...   | Think...                                                                                           |
| ---------------------------- | -------------------------------------------------------------------------------------------------- |
| Open source ≠ free?          | Code is freely available to inspect/modify/redistribute. Some OS software has licensing (RHEL).    |
| Why Linux dominates servers? | Open source + automation-friendly + secure + customizable + CLI principles                         |
| RPM vs DEB?                  | Package format → different install commands → different package managers → different service names |
| Everything is a file?        | Hardware, devices, processes — all represented as files in the filesystem                          |
| Why `/etc` matters?          | ALL configuration lives here — network, servers, users, software                                   |
| sed changes original file?   | **NO.** Only modifies output. Redirect to save.                                                    |
| `>` vs `>>`?                 | `>` overwrites, `>>` appends                                                                       |
| Service user vs regular?     | Service: UID 1-999, `/sbin/nologin`. Regular: UID 1000+, `/bin/bash`                               |
| `useradd` vs `adduser`?      | `useradd` = RedHat. `adduser` = Ubuntu (more interactive)                                          |
| httpd vs apache2?            | Same software. `httpd` = CentOS name. `apache2` = Ubuntu name                                      |

***

This completes the full analysis of the Introduction to Linux lecture. Both the video narration  and the course slides  have been fully processed into complementary theory, practical, and compression sections with zero redundancy between them. [\[23-introdu...n-to-linux \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-introduction-to-linux.txt) [\[23-Linux+Q...ckstart+V5 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/23-Linux+Quickstart+V5.pdf)

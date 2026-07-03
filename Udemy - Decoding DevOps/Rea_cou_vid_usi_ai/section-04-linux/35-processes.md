# 🎓 Complete Deep Learning Material — Linux Processes: Process Architecture, Monitoring, Lifecycle States, and Process Control

**Source:** [35-processes.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt?EntityRepresentationId=ca530440-0654-4c8c-8bdb-757be04bf2ad) — In-depth lecture on Linux process management covering the `top`, `ps aux`, `ps -ef` commands, process states (running, sleeping, stopped, zombie, orphan), parent-child relationships (forking), PID 1 (`systemd`/`init`), the `kill` command (graceful vs. forceful), and advanced process filtering pipelines using `grep`, `awk`, and `xargs`. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Processes Are and Why They Matter

A **process** is a running instance of a program. When you execute a command, start a service, or boot the system, the kernel creates processes to carry out that work. At any given moment, a Linux system has **many processes** — the video shows 117 tasks on a relatively idle system. Processes are the fundamental unit of execution in Linux; understanding them is essential for monitoring system health, troubleshooting performance issues, and managing services. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

The instructor draws a direct parallel: the `top` command is **"similar to like a task manager you have on Windows."** It's the Linux equivalent for observing what's running, what's consuming resources, and what state everything is in. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

## 1.2 — Process States: Running, Sleeping, Stopped, and Zombie

Every process on the system exists in one of several **states**, and understanding these states is crucial for diagnosing system behavior. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

### Running

A process actively using CPU cycles right now. On the demonstrated system, only **1 out of 117** tasks is running at any given instant. This is normal — a CPU core can only execute one process at a time (or a few with multiple cores), so most processes wait their turn.

### Sleeping

A process that is alive and loaded in memory but **not currently executing**. It is waiting for something — user input, a network response, a timer, disk I/O. The instructor notes **116 out of 117** tasks are sleeping and comments: "looks like a very lazy operating system, but that's how it works." This is not laziness; it's efficiency. Processes sleep when they have nothing to do, freeing CPU for processes that do. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

### Stopped

A process that has been **manually paused** and can be resumed by issuing specific commands. The video shows zero stopped processes. This state is typically used during debugging or job control.

### Zombie

A zombie is a process whose **execution is completely finished** (it's "dead"), but its **entry still remains in the process table**. The process has completed its work and exited, but the operating system hasn't fully cleaned up its record yet — usually because the parent process hasn't read the child's exit status. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

The instructor uses the movie analogy: "Zombie's, dead, like we see in the movies." A zombie process is **not consuming CPU or RAM** resources, but it occupies a slot in the process table. If zombie processes accumulate in large numbers, they can exhaust the process table, preventing new processes from being created. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

The recommended way to clear zombie processes is to **reboot the machine**, though there are other ways to refresh the process table. The video doesn't detail those alternative methods. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

> 🔍 **Deep Dive:** The zombie state exists because of a design contract in Unix/Linux: when a child process finishes, it must report its exit status to its parent. The kernel keeps the process table entry alive until the parent calls `wait()` to collect that status. If the parent never calls `wait()` (because it's buggy, or crashed, or is ignoring children), the dead child lingers as a zombie. This is a **resource leak** at the process table level — the process itself is dead, but the metadata record persists.

***

## 1.3 — Orphan Processes

An **orphan process** is a child process whose **parent has died** (been killed or terminated) while the child is still running. When this happens, the child doesn't disappear — it gets **adopted by PID 1** (`systemd` or `init`), the first process in the system. PID 1 becomes the new parent. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

The instructor demonstrates this directly: when `kill -9` forcefully kills the parent `httpd` process, the child `httpd` processes don't die — they become orphans and their PPID changes to `1` (adopted by `systemd`). [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

Orphan processes are problematic because they **"will not serve much purpose, but will still consume the resources."** They're doing work (or holding resources) for a parent that no longer exists. The instructor advises: "it's ideal to clear the orphan processes." Modern systems are smarter about this — the instructor notes "nowadays, the systems are smart. This orphan process will get cleared automatically." But this isn't guaranteed, and in cases with many orphans, manual cleanup is needed. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

> 🔍 **Deep Dive:** The difference between orphan and zombie is a common source of confusion. An **orphan** is a *living* process with a dead parent — it's still running and consuming resources. A **zombie** is a *dead* process with a (potentially living) parent — it has finished but its entry persists. Orphans consume CPU/RAM; zombies only consume a process table slot. Orphans can be killed normally; zombies can only be cleared by having their parent collect their exit status, or by rebooting.

***

## 1.4 — PID 1: The Root of All Processes (`systemd` / `init`)

**PID 1** is the first process started by the kernel at boot time. In modern Linux systems (like CentOS), this is **`systemd`**. In older systems and in Ubuntu, it's **`init`**. Every other process on the system descends from PID 1, either directly or through a chain of parent-child relationships. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

The `ps -ef` output shows PID 1 has a PPID (parent process ID) of **0**. But you won't find a process with PID 0 running — it's the **kernel boot process** that existed only during boot time and is now "dead." PID 1 is the surviving root of the entire process tree. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

PID 1 has a special role beyond being the first process: it **adopts orphan processes** (as covered above) and manages the lifecycle of system services. When you run `systemctl start httpd`, it's `systemd` (PID 1) that orchestrates starting the service. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

## 1.5 — Parent-Child Relationships and Forking

Processes in Linux have a **hierarchical parent-child structure**. When a process needs to create another process, it **forks** — it creates a copy of itself, which then becomes the child. The parent's PID becomes the child's PPID (parent process ID). [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

The video demonstrates this concretely with `httpd` (Apache web server). The `ps -ef` output shows: [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

* One `httpd` process with PID 1420 and PPID 1 (started by systemd)
* Multiple `httpd` child processes, each with PPID 1420 (started by the parent httpd)

The instructor reads this directly: "PID is 1420 for this process and PPID is 1, then this process, PID 1421, its parent is 1420, which is this process. Again here also 1420, 1420, 1420... So I can say that this process has started all this other child processes. Which is also called forking." [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

This parent-child tree is the fundamental structure of process management. It determines who controls whom, who inherits what, and what happens when a process dies (children become orphans, or children become zombies if they die before the parent collects their status).

### Kernel Threads

Processes displayed in **square brackets** in `ps` output (like `[kthreadd]`, `[ksoftirqd]`) are **kernel threads** — processes that run inside the kernel space, not in user space. The instructor mentions them briefly: "The process that you see in this square bracket, these are kernel threads." They are managed by the kernel directly and are distinct from normal user-space processes. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

## 1.6 — Load Average vs. CPU Utilization

The `top` command displays **load average** as three comma-separated values: the load over the **last 1 minute, 5 minutes, and 15 minutes**. The instructor makes an important conceptual distinction: load average is **CPU wait time**, which is different from CPU utilization. CPU utilization measures how busy the CPU is; load average measures how many processes are **waiting** to use the CPU. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

The relationship: "If the CPU utilization is full, then the load average will start increasing." When the CPU is 100% busy, new processes must wait in a queue, and the load average reflects the length of that queue. A system can have low CPU utilization but still show a load average (processes waiting for I/O, for example), or high CPU utilization with a low load average (CPU is busy but no queue is forming). [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

> ⚠️ **Expert Note:** Load average values should be interpreted relative to the number of CPU cores. A load average of 4.0 on a 4-core system means each core has roughly one process waiting — the system is at capacity but not overloaded. The same load average of 4.0 on a single-core system means 3 processes are waiting at all times — the system is severely overloaded. The three time windows (1m, 5m, 15m) show the trend: if 1m > 15m, load is increasing; if 1m < 15m, load is decreasing.

***

## 1.7 — Graceful Kill vs. Forceful Kill (`kill` vs. `kill -9`)

The `kill` command is how you terminate processes that don't have a `systemctl` service manager (or when `systemctl` isn't available). Despite its name, `kill` without options is actually **graceful** — the instructor explains: "when I say kill, which sounds harsh, but it's actually more of asking this process, hey, can you please close your operations?" [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

### Graceful Kill (default `kill`)

The process receives a signal (SIGTERM, signal 15 by default) that says "please shut down." The process has the opportunity to **close child operations first**, clean up resources, save state, and then terminate itself in an orderly fashion. The parent process shuts down its children, then itself. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

### Forceful Kill (`kill -9`)

When a process "becomes adamant and does not listen" to the graceful kill, you use `kill -9`. The `-9` sends **SIGKILL**, which the process **cannot catch, block, or ignore**. The kernel immediately terminates the process. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

The critical consequence: **`kill -9` on a parent does NOT close child processes.** The parent is instantly destroyed with no chance to shut down its children. Those children become **orphan processes**, adopted by PID 1. The instructor demonstrates this explicitly with httpd — after `kill -9` on the parent httpd, the child httpd processes survive as orphans with PPID changed to 1. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

The instructor's guideline: "you don't have to issue -9 every time because kill is better, but if sometimes it does not work, you give -9." Always try graceful first; use forceful only as escalation. And when you do use `-9`, be prepared to clean up orphan children. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

> 🔍 **Deep Dive:** This graceful-then-forceful pattern maps directly to how `systemctl stop` works internally. `systemctl stop httpd` sends a graceful signal first and waits for the service to shut down. If it doesn't respond within a timeout, systemd escalates to a forceful kill. The manual `kill` and `kill -9` sequence is the same pattern performed by hand — and is necessary when `systemctl` isn't available for a particular process.

***

## 1.8 — Process Filtering Pipeline: `grep`, `grep -v`, `awk`, `xargs`

The video builds a **multi-stage pipeline** for finding and killing processes, demonstrating how small Unix tools combine into powerful operations. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

### The Problem with `grep`

When you run `ps -ef | grep httpd`, you see all httpd processes — but you also see **the grep process itself** in the results (because `grep httpd` contains the word "httpd" in its own command line). This grep process is already dead by the time you see the output, but it clutters the results. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

### Filtering Out Grep: `grep -v grep`

The solution: pipe the output through `grep -v grep`. The `-v` flag **inverts** the match — it shows everything that does NOT contain "grep." This removes the self-referencing grep entry from the results. The instructor also notes you could use `grep -v color` — the principle is excluding the noise. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

### Extracting PIDs: `awk '{print $2}'`

To kill multiple processes, you need their PIDs. The `awk '{print $2}'` command extracts the **second column** from each line of output — which in `ps -ef` output is the PID column. This transforms the full process listing into a clean list of just process IDs. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

### Bulk Killing: `xargs kill -9`

The `xargs` command takes the list of PIDs from the pipe and **passes them as arguments** to `kill -9`. So if awk produced PIDs `1421 1422 1423`, xargs constructs and executes: `kill -9 1421 1422 1423`. This kills all matching processes in one operation. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

The complete pipeline: `ps -ef | grep httpd | grep -v grep | awk '{print $2}' | xargs kill -9`

The instructor presents this as the correct approach when using `kill -9`: "if you're issuing 9, then you make sure you do like this — filter it, find the process IDs, and then send it to kill -9 command." [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are learning to **monitor, inspect, and control processes** on a running Linux system. By the end, you will be able to view all running processes and their resource consumption, understand parent-child relationships between processes, gracefully and forcefully terminate processes, and efficiently filter and bulk-kill processes using pipelines. The final operational outcome is **full command-line competency for Linux process management.** [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

## Step 1 — View Dynamic Process Activity with `top`

```bash
top
```

**Breakdown:**

* **`top`** — launches a real-time, continuously updating process viewer [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**What the display shows (top to bottom):**

**Header area:**

* **Uptime:** how long the system has been running (e.g., "up 9 minutes")
* **Users:** number of logged-in users
* **Load average:** three values (1min, 5min, 15min) — CPU wait time, not utilization. If CPU is fully utilized, load average increases. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**Tasks line:**

* Total number of processes and their states: running, sleeping, stopped, zombie [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**CPU line:**

* Current CPU utilization percentage

**Memory lines:**

* RAM and swap usage (instructor notes: "better to see through `free -m`") [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**Process table:**

* Columns include: **PID** (process ID), **USER** (who runs it), **S** (status: `S`=sleeping, `R`=running), **%CPU**, **%MEM**, **COMMAND** (process name)
* Processes **dynamically re-sort** based on CPU consumption — "they're just getting sorted automatically," "dancing" [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**To exit `top`:**

```
q
```

Press `q` to quit. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**Connection to flow:** `top` gives the live, real-time view. The next commands give static snapshots for detailed analysis.

***

## Step 2 — View All Processes (Static Snapshot) with `ps aux`

```bash
ps aux
```

**Breakdown:**

* **`ps`** — process status command
* **`aux`** — combined options:
  * **`a`** — show processes from all users
  * **`u`** — display user-oriented format (shows USER, %CPU, %MEM)
  * **`x`** — include processes not attached to a terminal [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**What happens:** Displays all processes with resource utilization details, then immediately returns to the prompt (unlike `top`, which stays open). Shows similar information to `top` but as a **one-time snapshot**. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**Key observations in output:**

* **PID 1** is `systemd` (CentOS) or `init` (older/Ubuntu) — the first process
* Processes in **square brackets** (e.g., `[kthreadd]`) are kernel threads
* Service processes like `httpd`, `sshd` appear with their owning user
* Zombie processes show status `Z` in the STAT column [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**Connection to flow:** `ps aux` shows resource utilization; `ps -ef` (next) shows parent-child relationships.

***

## Step 3 — View Process Hierarchy with `ps -ef`

```bash
ps -ef
```

**Breakdown:**

* **`ps`** — process status
* **`-e`** — show every process
* **`-f`** — full-format listing (includes PPID column) [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**Key difference from `ps aux`:** Instead of CPU/RAM utilization, this shows the **PPID (parent process ID)** column — which process started which. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**Reading parent-child relationships (httpd example):**

```
UID   PID   PPID
root  1420  1       ← parent httpd, started by systemd (PID 1)
apache 1421 1420    ← child, started by parent httpd (PID 1420)
apache 1422 1420    ← child, started by parent httpd
apache 1423 1420    ← child, started by parent httpd
```

The parent httpd (PID 1420) **forked** all child httpd processes. The parent's PPID is 1 (systemd started it via `systemctl start httpd`). [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**PID 1's own PPID is 0** — the kernel boot process, which no longer exists ("it's dead. It's at the boot time"). [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

## Step 4 — Check Memory with `free -m`

```bash
free -m
```

**Breakdown:**

* **`free`** — displays memory information
* **`-m`** — show values in megabytes [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**Operational note:** The instructor recommends this over the memory lines in `top` for a clearer view of RAM and swap usage.

***

## Step 5 — Gracefully Kill a Process

### First, find the process:

```bash
ps -ef | grep httpd
```

**Problem:** The output includes the `grep httpd` process itself (already dead, but shown). [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

### Filter out the grep noise:

```bash
ps -ef | grep httpd | grep -v grep
```

* **`grep -v grep`** — `-v` inverts the match; excludes lines containing "grep" [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

### Kill the parent process gracefully:

```bash
kill 1420
```

* **`kill`** — sends SIGTERM (signal 15) to the process
* **`1420`** — the PID of the parent httpd process [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**What happens internally:** The parent httpd receives the termination signal, **closes all child processes first**, then terminates itself. All httpd processes should be gone. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**Verification:**

```bash
ps -ef | grep httpd | grep -v grep
```

Should return no results (or only unrelated lines). [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

## Step 6 — Forcefully Kill a Process (and Handle Orphans)

### Restart httpd for demonstration:

```bash
systemctl start httpd
```

### Find the parent PID again:

```bash
ps -ef | grep httpd | grep -v grep
```

 [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

### Forcefully kill the parent:

```bash
kill -9 <parent_PID>
```

* **`-9`** — sends SIGKILL; instant, uncatchable termination [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**What happens internally:** The parent is destroyed instantly. It has **no chance to shut down children**. Child processes survive as **orphans** — their PPID changes to `1` (adopted by systemd). [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**Verification:**

```bash
ps -ef | grep httpd | grep -v grep
```

You'll see the child httpd processes still running, but now with **PPID = 1** (adopted by systemd). The parent httpd is gone. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**Key lesson:** Modern systems may auto-clear orphans, but if they don't, you need to kill them manually — and there could be many. This leads to the bulk-kill pipeline.

***

## Step 7 — Bulk-Kill Processes Using the Filter Pipeline

### Extract only PIDs from the process list:

```bash
ps -ef | grep httpd | grep -v grep | awk '{print $2}'
```

**Breakdown of the pipeline:**

1. **`ps -ef`** — list all processes with full format
2. **`| grep httpd`** — filter to only httpd-related lines
3. **`| grep -v grep`** — remove the grep process itself from results
4. **`| awk '{print $2}'`** — extract only the 2nd column (PID) from each line [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**Expected output:** A clean list of PIDs, one per line. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

### Send all PIDs to kill:

```bash
ps -ef | grep httpd | grep -v grep | awk '{print $2}' | xargs kill -9
```

* **`| xargs kill -9`** — `xargs` takes each PID from stdin and passes it as an argument to `kill -9`. Effectively executes `kill -9 PID1 PID2 PID3 ...` in one shot. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**Verification:**

```bash
ps -ef | grep httpd | grep -v grep
```

Should return nothing — all httpd processes are terminated. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

**Instructor's rule:** "If you're issuing -9, then you make sure you do like this — filter it, find the process IDs, and then send it to kill -9 command." This ensures you clean up all orphans created by the forceful kill. [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

> ⚠️ **Expert Note:** This pipeline pattern (`ps | grep | grep -v | awk | xargs kill`) is a foundational operations tool. In production, always **preview** the PID list before piping to `kill` — run the pipeline without `| xargs kill -9` first to confirm you're targeting the right processes. One wrong `grep` pattern can kill unrelated processes, including critical system services.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🏗️ Process System Architecture

```
KERNEL (boot)
  └── PID 0 (dead after boot)
       └── PID 1: systemd (CentOS) / init (Ubuntu/older)
            ├── [kernel threads] (in square brackets)
            ├── sshd
            ├── httpd (parent) ──fork──→ httpd (child) × N
            ├── java (jenkins)
            └── all other processes...

EVERY PROCESS HAS:
  PID    → unique ID
  PPID   → parent's PID
  USER   → owner
  STATE  → Running | Sleeping | Stopped | Zombie
```

 [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

## 🔄 Process State Model

```
                ┌──────────┐
    Created ──→ │ RUNNING  │ ←── actively using CPU
                └────┬─────┘
                     │ waiting (I/O, timer, input)
                ┌────▼─────┐
                │ SLEEPING │ ←── alive, not executing (116/117 typical)
                └────┬─────┘
                     │ manual pause
                ┌────▼─────┐
                │ STOPPED  │ ←── paused, can resume
                └──────────┘

    Process finishes but parent doesn't collect exit status:
                ┌──────────┐
                │  ZOMBIE  │ ←── dead, entry in process table
                └──────────┘     not consuming CPU/RAM
                                 fix: reboot or refresh table

    Parent dies, child still alive:
                ┌──────────┐
                │  ORPHAN  │ ←── adopted by PID 1
                └──────────┘     still consuming resources
                                 should be cleared
```

 [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

## ⚔️ Kill Semantics

```
kill <PID>          → SIGTERM (graceful)
  └── "Hey, can you please close your operations?"
  └── Parent shuts down children first → then itself
  └── ALWAYS TRY THIS FIRST

kill -9 <PID>       → SIGKILL (forceful)
  └── Instant death, uncatchable
  └── Parent CANNOT close children → children become ORPHANS
  └── Use ONLY when graceful fails
  └── MUST clean up orphans afterward

ESCALATION RULE:
  kill → wait → still alive? → kill -9 → clean orphans
```

 [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

## 🔍 Three Monitoring Commands

```
top         → LIVE, dynamic, auto-sorting by CPU
              shows: uptime, load avg, tasks, CPU%, MEM%, per-process
              exit: q

ps aux      → SNAPSHOT, shows CPU/MEM utilization per process
              zombie status visible as 'Z' in STAT column

ps -ef      → SNAPSHOT, shows PPID (parent-child relationships)
              used for: tracing forking, finding parent PID

free -m     → RAM/swap in megabytes (cleaner than top's memory line)
```

 [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

## 📊 Load Average

```
top header: load average: X.XX, X.XX, X.XX
                          1min  5min  15min

Load average = CPU WAIT TIME (≠ CPU utilization)
CPU full → load average increases (queue builds)

Trend: 1m > 15m → load increasing
       1m < 15m → load decreasing
```

 [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

## 🔧 Process Filter Pipeline (Critical Operational Pattern)

```
FULL PIPELINE:
  ps -ef | grep <name> | grep -v grep | awk '{print $2}' | xargs kill -9

STAGE BREAKDOWN:
  ps -ef              → all processes with PPID
  | grep httpd        → filter to target process
  | grep -v grep      → remove self-referencing grep line
  | awk '{print $2}'  → extract PID column only
  | xargs kill -9     → pass PIDs as arguments to kill

SAFETY: Run WITHOUT xargs kill first to preview targets

WHEN TO USE:
  kill -9 on parent → orphans created → need bulk cleanup
  Many instances of same process → kill all at once
```

 [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

## 🔗 Parent-Child Lifecycle Chain

```
systemctl start httpd
  └── systemd (PID 1) starts httpd parent (PID X, PPID=1)
       └── httpd parent forks → child1 (PPID=X), child2 (PPID=X), ...

GRACEFUL KILL (kill X):
  parent receives SIGTERM → closes children → closes self → ALL GONE ✓

FORCEFUL KILL (kill -9 X):
  parent dies instantly → children survive → PPID changes to 1 (orphans)
  orphans adopted by systemd → may auto-clear OR need manual cleanup
  cleanup: ps -ef | grep | grep -v | awk | xargs kill -9
```

 [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

## 🧩 Reusable Patterns

| Pattern                               | Instance                                                                                                                             |                                                  |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------ |
| **Graceful-then-Forceful Escalation** | `kill` first → `kill -9` only if needed; same pattern as `systemctl stop` internally                                                 |                                                  |
| **Parent-Child Tree Control**         | Kill parent → children follow (graceful) OR orphan (forceful); applies to all process hierarchies                                    |                                                  |
| **Pipeline Composition**              | Small tools (`grep`, `awk`, `xargs`) chained via \`                                                                                  | \` to build complex operations from simple parts |
| **Preview before Destroy**            | Run filter pipeline without `xargs kill` first to verify targets; same as `ls *.txt` before `rm *.txt`                               |                                                  |
| **Adoption by Root Controller**       | PID 1 adopts orphans — the root process is the ultimate fallback parent; similar to how a master orchestrator handles failed workers |                                                  |
| **State-based Resource Model**        | Running=CPU, Sleeping=memory only, Zombie=table entry only, Orphan=full resources but purposeless                                    |                                                  |

 [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

***

## 🧭 One-Line Mental Reload

> **Processes form a parent-child tree rooted at PID 1 (`systemd`); monitor with `top` (live), `ps aux` (utilization snapshot), `ps -ef` (hierarchy/PPID); kill gracefully first (`kill PID`), escalate to `kill -9` only when needed (creates orphans); clean up orphans with the filter pipeline `ps -ef | grep X | grep -v grep | awk '{print $2}' | xargs kill -9`; zombies = dead but in table (reboot to clear); load average = CPU wait time, not utilization.** [\[35-processes \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/35-processes.txt)

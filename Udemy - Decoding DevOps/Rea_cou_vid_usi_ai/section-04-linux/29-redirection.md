# 🎓 Linux I/O Redirection, Piping & Filtering — Deep Learning Material

*Reconstructed from the video lecture on input/output redirection, piping, and file searching in Linux* [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. Standard Output — The Default Destination

Every command you run on a Linux system produces output. That output has a default destination: the **screen** (your terminal/monitor). This is the **standard output device**. When you run `uptime`, the result appears on screen. When you run `ls`, the file listing appears on screen. This is so intuitive it feels like common sense — but recognizing it as a configurable behavior is the conceptual foundation of everything in this lecture. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

The critical insight is that this default destination is **not fixed**. Linux treats output as a **stream** — a flow of data that goes *somewhere*. By default, that "somewhere" is the screen. But you can **redirect** that stream to a different destination — a file, another command, or even a black hole that discards it entirely. This ability to redirect output streams is what makes Linux so powerful for automation, logging, and scripting. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

## 2. Output Redirection to Files — `>` and `>>`

The **redirection operator `>`** changes the destination of a command's standard output from the screen to a **file**. Instead of the output appearing on your terminal, it gets written into the specified file. Two critical behaviors govern how `>` interacts with the target file: if the file **does not exist**, it is **created**; if the file **already exists**, its content is **overwritten** — completely replaced with the new output. This overwrite behavior is the single most important thing to remember about `>`, because it's destructive and irreversible. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

The **append operator `>>`** solves the overwrite problem. It works identically to `>` except that when the target file already exists, the new output is **appended** (added to the end) rather than replacing the existing content. This makes `>>` the safe choice when you want to accumulate data from multiple commands into a single file — like building a system information report by sequentially appending the output of `date`, `uptime`, `free -m`, and `df -h`. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

> 🔍 **Deep Dive**
> The distinction between `>` and `>>` maps to a fundamental data-management decision: **replace vs. accumulate**. The first write to a new file can use either operator (the file doesn't exist yet, so there's nothing to overwrite). But every subsequent write forces a choice: do you want a fresh snapshot (`>`) or a growing log (`>>`)? This decision appears constantly in bash scripting and system automation.

***

## 3. `/dev/null` — The Black Hole Device

Linux has a special file called **`/dev/null`**. It is a file that **contains nothing**, and anything you send to it **disappears permanently** — the instructor describes it as *"like a black hole in the galaxy."* It never grows, never stores anything, and always remains empty. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

`/dev/null` serves two distinct purposes:

**Purpose 1: Silencing output.** When you run a command that generates a lot of output but you don't care about seeing it (you only care that the command executes), you redirect its output to `/dev/null`. The command runs, does its work, but the output vanishes. The instructor demonstrates this with `yum install vim -y`, which normally produces extensive installation output — redirecting to `/dev/null` makes it silent. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Purpose 2: Emptying files.** If you want to wipe a file's content without deleting the file itself, you can `cat /dev/null > targetfile`. What comes out of `/dev/null`? Nothing. That "nothing" gets redirected to the target file via `>` (which overwrites), so the file's content becomes nothing. The file still exists, but it's now empty. The instructor notes this is easier than opening the file in an editor and manually deleting everything. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

> 🔍 **Deep Dive**
> `/dev/null` is a **device file** — part of Linux's "everything is a file" design (covered in the previous lecture's `/proc` discussion). Just as `/proc` exposes system information as files, `/dev` exposes devices as files. `/dev/null` is a virtual device whose only behavior is to discard all input and produce no output. This uniform file interface means you can use the same redirection operators (`>`, `>>`) to interact with devices, regular files, and virtual filesystems.

***

## 4. Standard Error — The Second Output Stream

Commands don't just produce regular output — they can also produce **errors**. Linux separates these into two distinct streams: **standard output** (stream number **1**) and **standard error** (stream number **2**). By default, both streams go to the screen, which is why you see both successful output and error messages in your terminal. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

The plain `>` operator only redirects **standard output** (stream 1). If a command produces an error, that error still appears on screen even if you've redirected standard output to a file or `/dev/null`. The instructor demonstrates this by running a deliberately misspelled command (`freeeeeeeee`) — the "command not found" error appears on screen despite output redirection, because the error travels on stream 2, which wasn't redirected. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

To redirect **standard error**, you use **`2>`** — the `2` explicitly specifies stream number 2. You can send errors to a file (like `/tmp/error.log`) for later review. To redirect **both streams** (output and errors) to the same destination, you use **`&>`** — the `&` means "all streams." [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

The number `1` for standard output is the **default** — writing `>` is equivalent to writing `1>`. You only need to write the number explicitly when redirecting standard error (`2>`) or when you want to be explicit for clarity. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

## 5. Log Files — Redirection in Production

The instructor connects output redirection directly to a real-world system concept: **log files**. The files you see in `/var/log/` are not magically generated — they are created by **processes running in the background** that redirect their standard output and standard error to files. Some processes redirect output to one file and errors to another; others combine both into a single file using `&>`. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

This is the same mechanism you've just learned, applied at scale by the operating system and its services. When you write bash scripts later, you'll run them in the background and redirect their output to log files so you can review execution results later — exactly as system processes do. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

> ⚠️ **Expert Note**
> Understanding that log files are just redirected output streams demystifies one of the most common operational tasks: log analysis. Every log file you'll ever troubleshoot in production was generated by some process using `>`, `>>`, `2>`, or `&>` (or their programmatic equivalents). Knowing this means you can also *create* structured log files from your own scripts using the same operators.

***

## 6. Piping — Connecting Commands Together

Piping is a fundamentally different concept from redirection, though both control where output goes. Redirection sends output **to a file**. Piping sends output **to another command** — specifically, the output of the command on the left side of the pipe symbol `|` becomes the **input** of the command on the right side. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

This creates a **command chain** where data flows left to right through a series of processing stages. Each command in the chain receives the previous command's output, processes it, and either displays the result or passes it to the next command in the chain. The instructor describes this as having "numerous benefits" and states it's limited only by "your imagination." [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

The power of piping comes from **composability** — each Linux command does one thing well, and piping lets you combine these single-purpose tools into complex operations without any of them needing to know about each other. `ls` lists files. `grep` searches text. `wc` counts lines. Individually, they're simple. Piped together, they become a filtering and analysis system. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

## 7. Filtering Commands — `wc`, `grep`, `head`, `tail`

These commands are the primary **filtering tools** used with piping. Each processes input and produces a subset or transformation of it: [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**`wc -l`** (word count, line mode) counts the number of lines in its input. It can take a file path directly as an argument (`wc -l /etc/passwd` → counts lines in the passwd file, yielding 25 in the demo), or it can receive input from a pipe. When piped, it counts lines from whatever the previous command produced — so `ls | wc -l` counts the number of files/directories listed by `ls` (186 in the demo). [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**`grep`** searches for a specific text pattern in its input and returns only the lines that contain that pattern. It can search within a file or within piped input. The instructor demonstrates `ls | grep host` to find all files in `/etc` whose names contain "host", `tail -20 /var/log/messages | grep vagrant` to find vagrant-related events in the last 20 lines of the system log, and `free -m | grep Mem` to extract only the physical RAM line from memory output (excluding the Swap and header lines). The key to effective grep usage is identifying something **unique** in the line you want — like `Mem` in the memory output, which only appears on the physical RAM line. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**`head`** and **`tail`** extract lines from the beginning or end of input, respectively. `tail -20 /var/log/messages` shows the last 20 lines of the messages log. These can also be piped: `ls -l | tail` shows the last 10 entries of a long listing, `ls -l | head` shows the first 10. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

> 🔍 **Deep Dive**
> The instructor notes a subtle mistake during the demo: running `ls | grep host*` didn't work as expected because the shell tried to expand `host*` as a filename glob before grep received it. Removing the `*` and using just `ls | grep host` worked correctly — grep already searches for the pattern as a substring within each line, so the wildcard was unnecessary and counterproductive. This highlights that **shell expansion happens before command execution**, a common source of errors when mixing glob patterns with text-search tools.

***

## 8. The `find` Command — Real-Time File Search

All the filtering discussed above operates on **file content** or **command output**. But sometimes you need to find **the file itself** — locate a file somewhere in the filesystem by its name. The **`find`** command does this by performing a **real-time search** — it physically traverses the directory tree, checking each file against your search criteria at the moment you run the command. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

`find` takes a starting path and search criteria. `find /etc -name host*` searches the `/etc` directory for files whose names start with "host". You can search from `/` to scan the entire filesystem, but the instructor explicitly warns against this: because `find` is a real-time search that physically walks every directory, searching from `/` on a system with large data can **slow down the operating system**. The demo system has minimal data so it works fine, but on production systems with millions of files, this becomes a performance concern. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

## 9. The `locate` Command — Database-Backed File Search

**`locate`** is an alternative to `find` that trades real-time accuracy for **speed**. Instead of searching the filesystem in real-time, `locate` searches from a **pre-built database** of filenames. This makes it dramatically faster, but introduces a critical trade-off: the results are only as current as the last database update. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

`locate` is **not installed by default** — you must install the `mlocate` package first. After installation, you must run **`updatedb`** to build/update the filename database. Only then does `locate` work. If files are created or deleted after the last `updatedb` run, `locate` will show stale results — deleted files may still appear, and new files won't be found. The instructor emphasizes: **always run `updatedb` before `locate`** to ensure accurate results. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

The fundamental trade-off between `find` and `locate` is: **real-time accuracy vs. speed**. `find` is always current but slow on large filesystems. `locate` is fast but potentially stale. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

## 10. The `echo` Command — Printing Text

**`echo`** is a simple print command — it outputs whatever text you give it. `echo "Good morning"` prints "Good morning" to the screen. Its real power emerges when combined with redirection: you can use `echo` to write arbitrary text (headers, separators, labels) into files. The instructor uses `echo "################" > /tmp/sysinfo.txt` to write visual separator lines between sections of a system info report. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

## 11. The `history` Command — Reviewing Your Command Trail

The instructor ends by recommending the **`history`** command, which shows all previously executed commands in order. This is positioned as a **practice and review tool** — you can scroll through your command history to see what you've done and re-execute commands for practice. The instructor emphasizes that proficiency in redirection, piping, and filtering is a **prerequisite for bash scripting**. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Building

We are learning to **control where command output goes** (redirection), **chain commands together** (piping), and **search for files** (find/locate). The final operational outcome is the ability to: construct multi-command data pipelines, build structured output files from multiple commands, silence unwanted output, separate errors from normal output, and locate files anywhere in the filesystem. These skills are described as **prerequisites for bash scripting**. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

## Step 1: Redirect Output to a File with `>`

**What we're doing:** Sending a command's output to a file instead of the screen.

```bash
uptime > /tmp/sysinfo.txt
```

* **`uptime`** — the command whose output we want to redirect
* **`>`** — the redirection operator: "send standard output to..."
* **`/tmp/sysinfo.txt`** — the destination file (created if it doesn't exist) [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**What happens:** The uptime information does **not** appear on screen. Instead, it's written to `/tmp/sysinfo.txt`. If the file didn't exist, it's created. If it existed, its content is **completely replaced**.

**Verify:**

```bash
cat /tmp/sysinfo.txt
```

You should see the uptime output in the file. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Demonstrating overwrite behavior:**

```bash
ls > /tmp/sysinfo.txt
cat /tmp/sysinfo.txt
```

The previous uptime content is **gone** — replaced by the `ls` output. This confirms `>` is destructive to existing content. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Common mistake:** Using `>` when you intended to append. Once overwritten, the previous content is unrecoverable.

***

## Step 2: Append Output with `>>`

**What we're doing:** Adding output to a file without destroying existing content.

```bash
uptime >> /tmp/sysinfo.txt
cat /tmp/sysinfo.txt
```

* **`>>`** — append redirection: adds to the end of the file instead of replacing [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**What happens:** The `ls` output from Step 1 remains, and the `uptime` output is added below it.

***

## Step 3: Build a Structured System Info Report

**What we're doing:** Combining `echo`, `>`, and `>>` to build a formatted multi-section file. This demonstrates the real operational use of redirection.

**Three utility commands used in this report:** [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

```bash
uptime
```

Shows system uptime, logged-in users, and load average.

```bash
free -m
```

* **`free`** — display memory usage
* **`-m`** — show values in megabytes
* Output shows: physical RAM (total 486MB, 100 used, 35 free, 369 available) and Swap (virtual memory) [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

```bash
df -h
```

* **`df`** — disk filesystem usage
* **`-h`** — human-readable sizes (GB, MB instead of raw bytes)
* Output shows: root partition `/` is 50GB total, 1.5GB used, 49GB available [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

```bash
echo "################"
```

* Prints the text — used as a visual separator between report sections [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Building the report (sequenced execution):** [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

```bash
date > /tmp/sysinfo.txt
echo "################" >> /tmp/sysinfo.txt
uptime >> /tmp/sysinfo.txt
echo "################" >> /tmp/sysinfo.txt
free -m >> /tmp/sysinfo.txt
echo "################" >> /tmp/sysinfo.txt
df -h >> /tmp/sysinfo.txt
echo "################" >> /tmp/sysinfo.txt
```

**Key operational logic:** The first command uses `>` (creates/overwrites — gives a fresh file). Every subsequent command uses `>>` (appends — accumulates sections). The `echo` commands inject separator lines between data sections. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Verify:**

```bash
cat /tmp/sysinfo.txt
```

**Expected output:** A structured report showing date, then hash separator, then uptime, separator, RAM usage, separator, disk usage, separator. The instructor calls this "fancy." [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Connection to larger flow:** This pattern — first `>` then repeated `>>` with separators — is the foundational technique for building log files and reports in bash scripts.

***

## Step 4: Silence Output with `/dev/null`

**What we're doing:** Discarding command output entirely.

```bash
yum install vim -y > /dev/null
```

* **`yum install vim -y`** — installs the vim package; `-y` auto-confirms; generates extensive output
* **`> /dev/null`** — redirects all that output to the black hole [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**What happens:** The installation executes successfully, but no output appears on screen. The output is permanently discarded.

**Verify `/dev/null` is truly empty:**

```bash
cat /dev/null
```

Nothing appears — it's always empty regardless of what you send to it. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

## Step 5: Empty a File Using `/dev/null`

**What we're doing:** Wiping a file's content without deleting the file.

```bash
cat /dev/null > /tmp/sysinfo.txt
cat /tmp/sysinfo.txt
```

* **`cat /dev/null`** — reads `/dev/null`, which produces nothing
* **`> /tmp/sysinfo.txt`** — that "nothing" overwrites the file's content [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Result:** The file exists but is now empty. All previous content is wiped.

***

## Step 6: Redirect Standard Error with `2>`

**What we're doing:** Capturing error messages separately from normal output.

**First, observe the problem:**

```bash
free -m > /dev/null
```

Normal output is silenced. But now introduce an error: [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

```bash
freeeeeeeee > /dev/null
```

**What happens:** Despite `> /dev/null`, the error "command not found" still appears on screen. This is because `>` only redirects stream 1 (standard output). The error travels on stream 2 (standard error), which was not redirected. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Redirect the error:**

```bash
freeeeeeeee 2> /tmp/error.log
```

* **`2>`** — redirect standard error (stream 2) to the specified file [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Verify:**

```bash
cat /tmp/error.log
```

The error message now appears in the file instead of on screen. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

## Step 7: Redirect Both Output and Error with `&>`

**What we're doing:** Sending ALL output (normal + errors) to a single destination.

```bash
freeeeeeeee &> /tmp/error.log
```

* **`&>`** — redirect both standard output (1) and standard error (2) [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Result:** Whether the command produces normal output, errors, or both — everything goes to the specified file. Nothing appears on screen.

**Connection to larger flow:** This is exactly how system processes create log files in `/var/log/` — they redirect all their output (both streams) to files for later review. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

## Step 8: Count Lines with `wc -l`

**What we're doing:** Using the word-count command to count lines.

**Direct file input:**

```bash
wc -l /etc/passwd
```

* **`wc`** — word count utility
* **`-l`** — count lines only
* **`/etc/passwd`** — the file to count lines in [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Output:** `25 /etc/passwd` — 25 lines in the file.

**Piped input:**

```bash
ls /etc | wc -l
```

* **`ls /etc`** — lists files in `/etc` → output becomes input to the next command
* **`|`** — pipe operator: sends left-side output as right-side input
* **`wc -l`** — counts the lines it receives [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Output:** `186` — there are 186 files/directories in `/etc`.

***

## Step 9: Filter with `grep` via Pipe

**What we're doing:** Searching for specific text patterns within command output.

**Search for filenames containing "host":**

```bash
ls /etc | grep host
```

**Output:** Only files with "host" in their name (e.g., `hostname`, `hosts`, `hosts.allow`, etc.) [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Common mistake:** Do NOT use `ls | grep host*` — the shell expands `host*` as a glob pattern before grep sees it, causing unexpected behavior. Use `ls | grep host` without the wildcard. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Search within log file output:**

```bash
tail -20 /var/log/messages | grep vagrant
```

* **`tail -20`** — show last 20 lines of the file
* **`| grep vagrant`** — from those 20 lines, show only ones containing "vagrant" [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Extract only RAM line from memory output:**

```bash
free -m | grep Mem
```

* Identifies `Mem` as the unique text on the physical RAM line
* Returns only that line, excluding Swap and the header [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Piping `ls -l` with `head`/`tail`:**

```bash
ls -l /etc | tail
ls -l /etc | head
```

Shows the last 10 or first 10 entries of a long directory listing. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

## Step 10: Find Files in Real-Time with `find`

**What we're doing:** Searching for files by name across directory trees.

```bash
find /etc -name host*
```

* **`find`** — the real-time file search command
* **`/etc`** — the directory to search within (starting point)
* **`-name`** — search criterion: match by filename
* **`host*`** — pattern: files starting with "host" [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Output:** All files under `/etc` whose names match `host*`.

**Searching from root `/`:**

```bash
find / -name host*
```

This searches the **entire filesystem**. Works but **not recommended** — it's a real-time traversal that can slow down the system on production machines with large data volumes. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

> ⚠️ **Expert Note**
> On production systems, `find /` can cause significant I/O load. Use targeted paths (like `/etc`, `/var`, `/home`) instead. Reserve root-level searches for small/test systems only.

***

## Step 11: Fast File Search with `locate`

**What we're doing:** Using a database-backed search for speed.

**Install the package:**

```bash
yum install mlocate -y
```

`locate` is not available by default — `mlocate` must be installed first. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Build the database:**

```bash
updatedb
```

This scans the entire filesystem and builds a database of all filenames. `locate` searches this database, not the live filesystem. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Search:**

```bash
locate host
```

**Output:** Every file on the system containing "host" in its name — returned almost instantly because it's a database lookup, not a filesystem traversal. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

**Critical operational rule:** Always run `updatedb` before `locate` to ensure the database reflects the current filesystem state. If files were created or deleted since the last `updatedb`, results will be stale. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

## Step 12: Review Your Command History

```bash
history
```

Shows all commands executed in the current session (and previous sessions). Use this to review, re-practice, and internalize the commands covered. The instructor emphasizes: **master redirection, piping, and filtering before moving to bash scripting**. [\[29-redirections \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/29-redirections.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## The Three Output Control Mechanisms

```
1. REDIRECTION  →  command output → FILE
2. PIPING       →  command output → ANOTHER COMMAND (as input)
3. /dev/null    →  command output → NOWHERE (discarded)
```

***

## Redirection Operator Map

```
>     Standard output → file     (OVERWRITE / CREATE)
>>    Standard output → file     (APPEND / CREATE)
2>    Standard error  → file
&>    Both streams    → file
1>    = >  (1 is default, implicit)

Stream 1 = stdout (normal output)
Stream 2 = stderr (error output)
```

***

## `/dev/null` — Dual Use

```
Silence output:    command > /dev/null          → output disappears
Empty a file:      cat /dev/null > targetfile   → file content becomes nothing

Nature: device file, always empty, accepts anything, returns nothing
```

***

## Log File Origin (System Pattern)

```
Background processes ──┬── stdout ──▶ logfile.log     (via > or >>)
                       └── stderr ──▶ error.log       (via 2>)
                       └── both   ──▶ combined.log    (via &>)

Location: /var/log/
Mechanism: same redirection operators you just learned
```

***

## Report-Building Pattern

```
date              >  /tmp/report.txt    ← first write: > (fresh file)
echo "########"   >> /tmp/report.txt    ← all subsequent: >> (append)
uptime            >> /tmp/report.txt
echo "########"   >> /tmp/report.txt
free -m           >> /tmp/report.txt
echo "########"   >> /tmp/report.txt
df -h             >> /tmp/report.txt

Rule: first > then all >>
echo used for visual separators
```

***

## Piping Flow

```
command_A  |  command_B  |  command_C
    │              │              │
    └─ produces    └─ receives    └─ receives B's output
       output         A's output     → final result
                      as input

Key: each command is independent; pipe connects output→input
```

***

## Filtering Commands Quick Reference

```
wc -l                  Count lines (from file or pipe)
grep <pattern>         Show only lines matching pattern
head [-n]              First n lines (default 10)
tail [-n]              Last n lines (default 10)
echo "<text>"          Print text (useful for labels/separators)

Piping combos:
  ls | wc -l                   → count files
  ls | grep host               → filter filenames  (NOT grep host*)
  free -m | grep Mem            → extract RAM line only
  tail -20 /var/log/messages | grep vagrant  → search recent log entries
  ls -l | head                  → first 10 entries
  ls -l | tail                  → last 10 entries
```

***

## File Search: `find` vs `locate`

```
┌─────────────┬──────────────────────┬──────────────────────┐
│             │       find           │       locate         │
├─────────────┼──────────────────────┼──────────────────────┤
│ Search type │ Real-time traversal  │ Database lookup      │
│ Speed       │ Slow on large FS     │ Fast (pre-indexed)   │
│ Accuracy    │ Always current       │ Stale until updatedb │
│ Install     │ Built-in             │ yum install mlocate  │
│ Pre-step    │ None                 │ updatedb (required)  │
│ Syntax      │ find /path -name X   │ locate X             │
│ Risk        │ find / can slow OS   │ Stale results        │
└─────────────┴──────────────────────┴──────────────────────┘

Trade-off: real-time accuracy ←→ speed
```

***

## Reusable Patterns

```
PATTERN 1: Stream Separation & Selective Routing
  stdout (1) and stderr (2) are independent streams
  Each can be routed to different destinations
  → Same pattern in logging frameworks: INFO→app.log, ERROR→error.log

PATTERN 2: Compose Small Tools via Pipes
  Each tool does ONE thing (ls=list, grep=filter, wc=count)
  Pipe connects them into processing chains
  → Unix philosophy: small, composable, single-purpose tools

PATTERN 3: Real-Time vs. Indexed Search Trade-off
  find = real-time scan (accurate, slow, resource-heavy)
  locate = indexed lookup (fast, potentially stale)
  → Same trade-off in databases: full table scan vs. indexed query

PATTERN 4: Destructive vs. Additive Write Operations
  > = overwrite (destructive, for fresh state)
  >> = append (additive, for accumulation)
  → Fundamental data-write decision in any system
```

***

## Prerequisite Chain

```
Redirection + Piping + Filtering
         │
         ▼
    Bash Scripting (next topic)
    
"You should be really very good in this filtering and 
 redirection before you step into bash scripting."
```

***

This lecture is dense with operational tools that compound massively once you reach scripting. The report-building pattern (Step 3) and the pipe-filter combinations (Steps 8–9) are the techniques you'll use most frequently going forward. Ready for the next one whenever you are! 🚀

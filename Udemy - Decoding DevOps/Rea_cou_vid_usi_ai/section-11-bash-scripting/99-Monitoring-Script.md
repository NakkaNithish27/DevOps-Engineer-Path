# 🎓 Deep Learning Material: Building a Process Monitoring Script with Cron Scheduling

*Reconstructed from video captions — [99-script-for-monitoring.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt?EntityRepresentationId=e1a70e85-79c8-419b-9a2b-90822c929c8c)* [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 Bash Operators — The Comparison Toolkit

Bash provides a set of operators for comparisons and tests inside conditional statements. The video references these from the "Decoding DEVOPS Book" and groups them into categories: [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**Negation operator:** `!` — inverts the truth value of any expression. If something evaluates to true, `!` makes it false. If something evaluates to false, `!` makes it true. This is a universal logical inversion operator.

**String operators:** `-n` checks if a string's length is **greater than zero** (true if the string is non-empty). `-z` is its opposite — true if the string is **zero length** (empty). For string equality, you can use `=` (equal) and `!=` (not equal) as alternatives to the numeric comparison operators. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**Numeric comparison operators:** `-eq` (equal), `-gt` (greater than), `-lt` (less than). These were used in prior scripts and the video confirms them here as part of the formal operator set. The `=` and `!=` operators work for string comparison; `-eq`, `-gt`, `-lt` work for numeric comparison. This distinction matters — using the wrong type can produce unexpected results when comparing numbers stored as strings or vice versa.

**File test operators (single operand):** These are particularly important for this video's script. They take a single argument — a file or directory path — and return true or false based on the filesystem state: [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

* `-d PATH` — true if the **directory** exists
* `-e PATH` — true if the **file** exists (any type)
* `-r PATH` — true if the file exists **and** has read permission
* `-f PATH` — true if the file exists and is a **regular file** (not a directory, not a device)

These operators let scripts make decisions based on what exists on the filesystem — a fundamental capability for any automation or monitoring script.

***

## 1.2 Exit Codes and the `$?` Variable — The Universal Success/Failure Signal

This is the central concept of the entire video. Every command executed in bash produces an **exit code** — a numeric value that reports whether the command succeeded or failed. This exit code is stored in the special variable `$?` (dollar-question-mark), which always holds the exit code of the **most recently executed command**. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

The convention is absolute and universal in bash: **exit code 0 means success (true). Any nonzero exit code means failure (false).** This is the opposite of what most programming languages use (where 0 typically means false), and the video explicitly highlights this: "Zero means true in Bash scripting and nonzero means false." [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

Why does this matter? Because `$?` gives you a **programmable signal** — you can run any command, check `$?`, and make decisions based on whether it succeeded or failed. You don't need to parse the command's text output or understand its specific behavior. You just check: did it return 0 or not? This transforms every system command into a boolean test that your script can act on.

The video's instructor explicitly states a personal preference: "I'm a big fan of exit codes, especially in Bash scripting, so I usually use that." This reveals a design philosophy — exit codes are the **most universal and reliable** mechanism for detecting command success/failure, because every command produces one, and the convention (0 = success) is consistent across the entire Unix/Linux ecosystem. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

> 🔍 **Deep Dive:** The `$?` variable is **volatile** — it gets overwritten after every single command. If you run command A, then command B, then check `$?`, you get B's exit code, not A's. If you need to preserve an exit code for later use, you must capture it immediately: `my_exit_code=$?` right after the command you care about, before running anything else.

***

## 1.3 PID Files — The Process-Is-Alive Indicator

When a service like `httpd` (Apache web server) is running, the system creates a **PID file** — a small file that contains the **process ID** of the running service. For httpd, this file is located at `/var/run/httpd/httpd.pid`. The PID file's existence on the filesystem serves as a **signal**: if the file exists, the process is running. If the process stops (or is stopped), the PID file is deleted — it ceases to exist. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

The video demonstrates this directly: with httpd running, `cat /var/run/httpd/httpd.pid` shows the process ID. After stopping httpd with `systemctl stop httpd`, attempting to access the same file returns "No such file or directory." And critically, that "No such file or directory" error produces a **nonzero exit code** in `$?` — which is exactly the signal the monitoring script will use. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

This creates a clean logical chain: **Process running → PID file exists → command to check file succeeds → $? = 0. Process dead → PID file gone → command to check file fails → $? ≠ 0.** The PID file acts as a filesystem-level proxy for process state — you don't need to query the process manager directly; you can simply check whether a file exists.

> ⚠️ **Expert Note:** PID files can sometimes become **stale** — if a process crashes hard (killed by the kernel, segfault, power loss), the PID file may not be cleaned up. The file still exists, but the process is actually dead. This is a known limitation of PID-file-based monitoring. The video's approach using `cat` on the PID file and checking `$?` would report "running" in this stale-PID scenario. The alternative `-f` approach shown at the end has the same limitation. Production monitoring tools like Monit (mentioned in the video) handle this by verifying the PID file's contents against actually running processes. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

***

## 1.4 Nested Conditionals — Multi-Level Decision Logic

The monitoring script requires more than a simple if/else. It needs **three possible outcomes**: (1) the process is already running — do nothing, (2) the process is not running AND we successfully restart it — report success, (3) the process is not running AND the restart fails — alert the admin. This three-outcome requirement demands a **nested conditional** — an if/else inside another if/else. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

The structure is: the outer condition checks if the process is running. If not (else block), the script attempts to start the process. Inside that else block, a second (inner) condition checks whether the start command succeeded. If yes, report success. If no, report failure and advise contacting the admin. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

The video emphasizes: "Just make sure you're closing the conditions properly." In bash, every `if` must have a matching `fi`. When you nest conditions, you have multiple `if`/`fi` pairs, and mismatching them is a common source of syntax errors. The inner `if`/`fi` must be fully contained within the outer `else` block, and the outer `fi` must come after the inner `fi`. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

***

## 1.5 Output Redirection — Controlling Where Data Goes

The script uses two forms of output redirection: [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**Redirecting to `/dev/null`:** The command whose exit code we check (like `cat` on the PID file) produces text output that we don't need to see. We only care about the exit code. So the output is redirected to `/dev/null` — a special "black hole" file that discards everything written to it. The syntax is `command > /dev/null`. This keeps the script's output clean — the user sees only the meaningful messages we write with `echo`, not the raw output of internal check commands.

**Redirecting to a log file:** When the script runs automatically via cron (unattended, no terminal), there is no screen to display output. All output must be captured to a file for later review. The cron job redirects the script's entire output to `/var/log/monit_httpd.log`. This log file becomes the **operational record** — you can review it to see when the process was running, when it went down, when the script restarted it, and whether restarts succeeded or failed. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

The `date` command is included in the script's output specifically because the log file will accumulate entries from multiple cron executions. Without timestamps, you'd see a series of status messages but wouldn't know when each one occurred. The `date` command adds the temporal context necessary to make the log file useful for tracking. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

***

## 1.6 Cron Jobs — Automated Scheduled Execution

A cron job is a **scheduled task** — a command or script that the system executes automatically at specified intervals without human intervention. The tool to manage cron jobs is `crontab`, and `crontab -e` opens the editor to add or modify scheduled tasks. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

The cron schedule uses **five fields**, each representing a time dimension: [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

| Position | Meaning      | Range                    |
| -------- | ------------ | ------------------------ |
| 1st      | Minute       | 0–59                     |
| 2nd      | Hour (24h)   | 0–23                     |
| 3rd      | Day of month | 1–31                     |
| 4th      | Month        | 1–12 (1=Jan, 12=Dec)     |
| 5th      | Day of week  | 0–6 (0=Sunday, 1=Monday) |

After these five fields, you write the command to execute. The **asterisk** (`*`) means "every" — it matches all values for that field. A **range** is specified with a hyphen (e.g., `1-5` = Monday through Friday). [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

The video gives a concrete example: to run something at **8:30 PM every weekday** (Monday–Friday), the cron expression is `30 20 * * 1-5 /path/to/command`. Breakdown: minute 30, hour 20 (8 PM in 24-hour format), every day of month (`*`), every month (`*`), days 1 through 5 (Monday–Friday).

For the monitoring script, the schedule is `* * * * *` — every minute, every hour, every day, every month, every day of the week. This means the script executes **once per minute**, continuously. Combined with the log file, this creates a persistent monitoring system that checks the httpd process every 60 seconds and logs every check. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

> 🔍 **Deep Dive:** When `crontab -e` is saved and closed, the system confirms with "installing new crontab." The cron daemon reads this file and begins executing the scheduled jobs. Cron runs in the background as a system service — you don't need to keep a terminal open. The jobs execute even if nobody is logged in. This is what transforms a manual script into an **autonomous monitoring agent**. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

***

## 1.7 The Two Approaches — Exit Code vs. File Test Operator

The video presents two logically equivalent methods to detect whether httpd is running: [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**Approach 1 (Exit code):** Run `cat /var/run/httpd/httpd.pid`, redirect output to `/dev/null`, then check `$?`. If `$? -eq 0`, the file existed and the process is running. If nonzero, the file doesn't exist and the process is dead.

**Approach 2 (File test operator):** Use `-f /var/run/httpd/httpd.pid` directly inside the `if` condition. The `-f` operator returns true if the file exists and is a regular file. No need for `cat`, no need to check `$?` manually — the test is built into the conditional syntax.

Both achieve the same result. The video frames this as a matter of **personal style and creativity**: "It's really just the matter of creativity. But at the end of the day, the result matters." The instructor prefers exit codes. Other engineers may prefer file test operators. The video also acknowledges: "There are many, many more methods to do the same thing. And this will all come with experience." [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

***

## 1.8 The Monitoring Tool Concept

The video explicitly names what we've built: a **monitoring plugin**. It draws a direct parallel to a real tool called **Monit** that does the same thing — monitors processes and takes action (like restarting) if they go down. The difference is that Monit is a mature, sophisticated tool, while our script is a simplified version that demonstrates the core concept. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

The key insight: the script we built is not just an exercise — it implements a real operational pattern used in production infrastructure. Process monitoring with automatic restart is a fundamental infrastructure management capability. The script achieves: **detect state → decide action → execute action → verify result → log everything → repeat on schedule.** [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are building a **process monitoring script** (`11_monit.sh`) that automatically checks whether the `httpd` (Apache) service is running. If it's not running, the script attempts to start it. If the start fails, it alerts the user. We then schedule this script to run **every minute** using a cron job, and redirect all output to a log file — creating a self-running monitoring system. The final outcome: an autonomous agent that keeps httpd alive and logs all activity. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

***

## Phase 1: Understanding the Detection Mechanism

### Step 1 — Observe the PID File Behavior

**What we are doing:** Verifying that the PID file exists when httpd is running and disappears when it stops.

```bash
systemctl status httpd
```

Confirm httpd is running. While it's running, check the PID file:

```bash
cat /var/run/httpd/httpd.pid
```

**Expected result:** A number (the process ID) is printed. The command succeeds. `$?` = 0. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

Now stop the process:

```bash
systemctl stop httpd
```

Check the PID file again:

```bash
cat /var/run/httpd/httpd.pid
```

**Expected result:** `No such file or directory`. The command fails. `$?` = nonzero (typically 1). [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**What this proves:** The PID file's existence directly reflects the process state. We can use `$?` after checking this file as our detection mechanism.

**Restart httpd for the next phase:**

```bash
systemctl start httpd
```

Confirm the PID file reappears:

```bash
cat /var/run/httpd/httpd.pid
```

**Connection to flow:** This PID file + exit code relationship is the foundation of the entire monitoring script.

***

## Phase 2: Writing the Monitoring Script

### Step 2 — Create the Script File

```bash
vim /opt/scripts/11_monit.sh
```

**Naming:** `11_monit.sh` — the video specifies this name. "Monit" references the real monitoring tool that does the same job in production. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

### Step 3 — Write the Script Logic

The complete script (reconstructed from the video's walkthrough): [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

```bash
#!/bin/bash

echo "############"
date

cat /var/run/httpd/httpd.pid > /dev/null

if [ $? -eq 0 ]
then
    echo "httpd process is running"
else
    echo "httpd process is not running"
    echo "starting the process"
    systemctl start httpd

    if [ $? -eq 0 ]
    then
        echo "process started successfully"
    else
        echo "process failed to start, contact the admin"
    fi
fi

echo "############"
```

**Line-by-line breakdown:**

**`#!/bin/bash`** — Shebang. Tells the OS to use the bash interpreter.

**`echo "############"` and `date`** — Output formatting. The hash line creates a visual separator between executions in the log file. `date` prints the current timestamp so each log entry is time-stamped. These exist specifically because the script will run repeatedly via cron — without them, the log file would be an unreadable stream of messages with no temporal context. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**`cat /var/run/httpd/httpd.pid > /dev/null`** — The detection command. `cat` attempts to read the PID file. The `> /dev/null` redirects the output (the process ID number) to the black hole — we don't need to see it. We only care about whether the command succeeded or failed, captured in `$?`. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**`if [ $? -eq 0 ]`** — Checks the exit code of the `cat` command. If 0 (success), the PID file exists, meaning httpd is running.

**`then echo "httpd process is running"`** — The happy path. Process is alive. Nothing to do. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**`else`** — The PID file doesn't exist. Process is down.

**`echo "httpd process is not running"` / `echo "starting the process"`** — Inform the log what's happening.

**`systemctl start httpd`** — Attempt to start the process. This command itself produces an exit code. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**`if [ $? -eq 0 ]`** — **Nested condition.** Checks whether the start command succeeded.

**`then echo "process started successfully"`** — The restart worked.

**`else echo "process failed to start, contact the admin"`** — The restart failed. This is the critical failure path — something is seriously wrong if the process can't even be started. The message directs the operator to escalate. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**Inner `fi`** — Closes the nested if/else (the start-success check).

**Outer `fi`** — Closes the outer if/else (the is-running check).

**Final `echo "############"`** — Closing separator for the log entry.

**Save and exit:** `Esc` → `:wq`

**Common mistakes:**

* Forgetting `> /dev/null` on the `cat` command — the PID number clutters the log output
* Mismatching `fi` closings — each `if` needs exactly one `fi`, and nesting order matters
* Checking `$?` after the wrong command — remember, `$?` always reflects the **most recent** command. If you accidentally insert an `echo` between `cat` and the `$?` check, you're checking the exit code of `echo` (which is always 0), not `cat`

***

### Step 4 — Test the Script Manually

**Test Case 1 — Process is running:**

```bash
systemctl start httpd
/opt/scripts/11_monit.sh
```

**Expected output:** [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

```
############
[current date and time]
httpd process is running
############
```

**Test Case 2 — Process is stopped:**

```bash
systemctl stop httpd
/opt/scripts/11_monit.sh
```

**Expected output:** [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

```
############
[current date and time]
httpd process is not running
starting the process
process started successfully
############
```

**Verification:** After test case 2, run `systemctl status httpd` to confirm the script actually restarted the service.

**Connection to flow:** Manual testing confirms the logic works. Next, we automate it.

***

## Phase 3: Scheduling with Cron

### Step 5 — Get the Script's Absolute Path

```bash
pwd
```

Or simply note: `/opt/scripts/11_monit.sh` — the absolute path is needed for the cron job because cron does not execute from the script's directory. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

### Step 6 — Create the Cron Job

```bash
crontab -e
```

**Breakdown:**

* `crontab` — the cron table management command
* `-e` — **edit** mode. Opens the crontab file in vim for editing. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**Inside the editor, add this line:**

```
* * * * * /opt/scripts/11_monit.sh &>> /var/log/monit_httpd.log
```

**Breakdown of the cron expression:** [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

| Field        | Value | Meaning             |
| ------------ | ----- | ------------------- |
| Minute       | `*`   | Every minute        |
| Hour         | `*`   | Every hour          |
| Day of month | `*`   | Every day           |
| Month        | `*`   | Every month         |
| Day of week  | `*`   | Every day (Sun–Sat) |

**`/opt/scripts/11_monit.sh`** — The absolute path of the script to execute.

**`&>> /var/log/monit_httpd.log`** — Redirects **all output** (stdout and stderr) from the script into the log file. The `&>>` ensures both standard output and error messages are captured, and `>>` appends (does not overwrite) — so each execution adds to the log rather than replacing it. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**Save and exit vim:** `Esc` → `:wq`

**Expected confirmation:** `installing new crontab` — this message confirms cron has accepted the new schedule. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**Connection to flow:** The script is now autonomous. It will run every 60 seconds without human intervention.

***

### Step 7 — Verify the Automated Monitoring

**What we are doing:** Stopping httpd and waiting for the cron job to detect and restart it.

```bash
systemctl stop httpd
```

**Wait at least one minute** for the cron job to fire. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

Then check the log file:

```bash
cat /var/log/monit_httpd.log
```

**Expected log content:** [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

```
############
[timestamp when process was found stopped]
httpd process is not running
starting the process
process started successfully
############
############
[timestamp ~1 minute later]
httpd process is running
############
```

The first entry shows the script detected the down process and restarted it. The second entry (one minute later) shows the process is now running normally. Subsequent entries will continue showing "running" every minute. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**Operational verification:** You can stop httpd multiple times and review the log to confirm the script consistently detects and recovers the service.

> ⚠️ **Expert Note:** In production, the log file at `/var/log/monit_httpd.log` will grow indefinitely since the script runs every minute. You'd need **log rotation** (via `logrotate` or similar) to prevent disk space exhaustion. The video doesn't cover this, but it's an implicit operational concern for any cron-based logging. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

***

## Phase 4: Alternative Approach — Using the `-f` File Test Operator

### Step 8 — Rewrite Detection with `-f`

**What we are doing:** Replacing the `cat` + `$?` check with a direct file existence test.

The alternative script replaces the detection block: [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

```bash
if [ -f /var/run/httpd/httpd.pid ]
then
    echo "httpd process is running"
else
    echo "httpd process is not running"
    # ... same start logic as before
fi
```

**Breakdown:**

* `[ -f /var/run/httpd/httpd.pid ]` — the `-f` operator tests if the path is a regular file that exists. Returns true (0) if the file exists, false (nonzero) if it doesn't. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

**Operational difference:** No need for `cat`, no need for `> /dev/null`, no need to check `$?` manually. The `-f` test integrates directly into the `if` condition. The rest of the script (nested condition, start logic, logging) remains identical.

**When to use which:** Both produce the same result. Exit code approach (`cat` + `$?`) is more general — it works with any command, not just file checks. File test operator (`-f`) is more concise and self-documenting for filesystem checks specifically. Choose based on personal preference and readability needs. [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## 🏗️ System Architecture

```
MONITORING SYSTEM:
  Cron Daemon (every minute)
    └── Executes: /opt/scripts/11_monit.sh
          ├── OUTPUT → &>> /var/log/monit_httpd.log
          │
          └── LOGIC:
                ├── Check: Does PID file exist?
                │     ├── YES → "running" (do nothing)
                │     └── NO  → Attempt start
                │                 ├── Start succeeds → "started successfully"
                │                 └── Start fails    → "contact admin"
                │
                └── Each entry timestamped with `date`
```

## 🔑 Exit Code System

```
$? = Exit code of MOST RECENT command (volatile — overwritten after every command)

0     = SUCCESS (true in bash)
≠ 0   = FAILURE (false in bash)

⚠️ Bash convention is OPPOSITE of most programming languages (where 0 = false)
```

## 🔗 PID File → Process State Chain

```
httpd RUNNING  → /var/run/httpd/httpd.pid EXISTS  → cat succeeds → $? = 0
httpd STOPPED  → /var/run/httpd/httpd.pid GONE    → cat fails    → $? ≠ 0
```

## 📋 Bash Operator Quick Reference

```
NUMERIC:  -eq  -gt  -lt
STRING:   =    !=   -n (non-empty)  -z (empty)
FILE:     -d (dir exists)  -e (file exists)  -f (regular file)  -r (readable)
LOGIC:    ! (negate/invert)
```

## 🔀 Nested Condition Structure

```
if [ OUTER_CONDITION ]        ← Is process running?
then
    HAPPY_PATH                ← Running — do nothing
else
    RECOVERY_ACTION           ← Start process
    if [ $? -eq 0 ]           ← Did start succeed?
    then
        SUCCESS_REPORT        ← Started OK
    else
        ESCALATION            ← Failed — contact admin
    fi                        ← Close INNER
fi                            ← Close OUTER

Rule: Every `if` needs exactly one `fi`. Nesting = multiple if/fi pairs.
```

## 🕐 Cron Schedule Format

```
┌───── Minute (0-59)
│ ┌───── Hour (0-23)
│ │ ┌───── Day of Month (1-31)
│ │ │ ┌───── Month (1-12)
│ │ │ │ ┌───── Day of Week (0-6, 0=Sun)
│ │ │ │ │
* * * * *  /path/to/command

*     = every (wildcard)
1-5   = range (Mon-Fri)
30 20 * * 1-5  = 8:30 PM weekdays
* * * * *      = every minute (monitoring)
```

## 🔄 Two Detection Approaches

```
APPROACH 1 — Exit Code:
  cat /var/run/httpd/httpd.pid > /dev/null
  if [ $? -eq 0 ]  →  General-purpose, works with ANY command

APPROACH 2 — File Test:
  if [ -f /var/run/httpd/httpd.pid ]  →  Concise, specific to file checks

SAME RESULT. Different style. Both have stale-PID limitation.
```

## 📊 Output Redirection Map

```
> /dev/null           → Discard output (only care about exit code)
&>> /var/log/file.log → Append ALL output (stdout+stderr) to log file

Script uses BOTH:
  Internal check → /dev/null (suppress noise)
  Cron output    → log file  (preserve for review)
```

## ⚡ Operational Flow (End-to-End)

```
1. Write script → /opt/scripts/11_monit.sh
2. chmod +x     → Make executable
3. Test manually → Stop httpd, run script, verify restart
4. crontab -e   → Schedule: * * * * * /path/script &>> /var/log/monit_httpd.log
5. Stop httpd   → Wait 1 min → cat log file → Verify auto-detection + restart
6. Ongoing      → Log grows with timestamped entries every minute
```

## 🔁 Reusable Engineering Patterns

| Pattern                                  | Manifestation                                                                                 |
| ---------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Detect → Decide → Act → Verify → Log** | Core monitoring loop: check state, take action if needed, verify action, record everything    |
| **Exit code as universal boolean**       | Any command's success/failure → programmable decision point via `$?`                          |
| **Filesystem as state indicator**        | PID file existence = process alive. File system reflects runtime state.                       |
| **Nested recovery with escalation**      | Try recovery → if recovery fails → escalate. Two-level failure handling.                      |
| **Suppress noise, capture signal**       | `/dev/null` for internal checks; log file for operational output. Separate signal from noise. |
| **Autonomous agent via scheduling**      | Script + cron = unattended continuous monitoring. Manual script → autonomous system.          |
| **Timestamped logging for auditability** | `date` command in output → every log entry has temporal context for post-incident review      |
| **Multiple paths to same result**        | `cat` + `$?` vs. `-f` operator — engineering offers choices; result matters, not method       |

## ⚡ Key Gotchas for Fast Recall

```
❌ Check $? after echo (not after cat)    → $? reflects echo (always 0), not the check command
✅ Check $? IMMEDIATELY after the command → Before any other command overwrites it

❌ Mismatched if/fi in nested conditions  → Syntax error, script won't run
✅ Count: every `if` needs exactly one `fi`

❌ Forget > /dev/null on internal check   → PID number clutters log output
✅ Suppress internal command output        → Log stays clean and meaningful

❌ No timestamp in cron-logged script     → Log entries have no temporal context
✅ Include `date` in output               → Every entry is time-traceable

❌ 0 = false (programming habit)          → WRONG in bash
✅ 0 = true/success in bash               → Opposite of most languages
```

***

This completes the full reconstruction of the Process Monitoring Script video.  Want me to generate Anki flashcards (CSV) from this material, or shall I process another caption file? [\[99-script-...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/99-script-for-monitoring.txt)

# 📘 Linux Filters & Redirections — Complete Deep Learning Analysis

**Source:** Video captions from *"Filters and Redirections"* lecture [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

This lecture covers one of the most operationally critical skills in Linux for DevOps: **extracting the right data from files and streams, and routing that data to files or other programs for further processing.** The instructor explicitly states: *"If you really want to be smart in Linux, you should be very good in filtering and redirection. This is also very helpful in scripting."* The video walks through grep, less, more, head, tail (including live log tailing), cut, awk, sed, vim search-and-replace, input redirection, and real-world system administration troubleshooting methodology — all demonstrated on a live Linux VM.

***

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

### 1. The Core Idea — Filtering and Redirection as a Two-Part System

The lecture frames this entire topic as two interconnected skills: **filtering** (getting the right data out of files or streams) and **redirection** (sending that data somewhere — to another file, to another program, or to the screen). These are not isolated tricks — they form the operational backbone of how system administrators and DevOps engineers interact with Linux systems daily. The instructor emphasizes this is also very helpful in **scripting**, because scripts are fundamentally chains of filter-and-redirect operations automated into repeatable flows. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

The tools covered split naturally into these categories:

* **Text search:** `grep` (find text in files)
* **File readers:** `less`, `more` (read files page-by-page)
* **Partial viewers:** `head`, `tail` (see beginning or end of files)
* **Column extraction:** `cut`, `awk` (extract specific fields from structured data)
* **Search and replace:** `sed`, `vim :%s` (find text and replace it)
* **Data routing:** Input redirection (`<`), output to commands via piping (`|`)

Each tool solves a distinct problem, but they are designed to **compose together** — the output of one can feed into another, building increasingly powerful data extraction and transformation pipelines. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

***

### 2. grep — Text Search Engine for Files

`grep` searches for a specific text pattern inside one or more files and returns every **line** that contains the match. Its basic form is: `grep <search_term> <file_path>`. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Case sensitivity** is a fundamental Linux behavior that directly affects grep. Linux treats `firewall` and `Firewall` and `FIREWALL` as completely different strings. If you search for `firewall`, lines containing `Firewall` will **not** match. The `-i` option tells grep to **ignore case**, matching regardless of capitalization. This is critical because configuration files, logs, and code often have inconsistent casing. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Searching across multiple files** extends grep from a single-file tool to a directory-wide search tool. Using `*` (wildcard) as the file argument searches all files in the current directory. However, grep will **not** enter subdirectories by default — if it encounters a directory, it throws an error: `"Is a directory"`. The `-R` option enables **recursive** searching, making grep descend into all subdirectories and search their files too. Combining both: `grep -iR <term> /path/*` performs a case-insensitive, recursive search across an entire directory tree. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

🔍 **Deep Dive — The Real-World Power of Recursive grep:**
The instructor demonstrates a critically important system administration pattern: **finding an unknown configuration file by searching for a known setting.** The example uses SELINUX (Security Enhanced Linux) — a security setting that sometimes needs to be changed from `enforcing` to `permissive` or `disabled`. The administrator knows the setting name (`SELINUX`) but **does not know which file** in `/etc` contains it. By running `grep SELINUX /etc/* -R`, every file in the entire `/etc` tree is searched, and the result reveals the exact file path. The administrator then opens that file, makes the change, and saves. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

The instructor makes a powerful statement about this: *"This is a very effective trick of system administrators. They don't need to memorize things."* The implication is profound — you don't need to memorize which configuration file holds which setting. You need to know how to **search for it**. The combination of Linux storing configuration in text files + grep's recursive search capability means the entire system is searchable. This is one of the most operationally valuable skills in Linux administration. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Inverse search** with `-v` inverts the logic: instead of showing lines that **contain** the search term, it shows every line that **does not contain** it. `grep -vi firewall filename` displays all lines except those mentioning firewall (case-insensitive). This is useful when you want to filter **out** noise from output. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

***

### 3. Input Redirection — The Invisible Default

The instructor briefly but importantly reveals a concept most beginners never notice: when you run `grep -i firewall anaconda-ks.cfg`, the file is coming in as **input** to the grep command. This is technically **input redirection**. You can make it explicit with the `<` symbol: `grep -i firewall < anaconda-ks.cfg`. Both produce identical results. The `<` is "invisible" by default — Linux automatically feeds the file as input to the command without needing the symbol. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

This matters conceptually because it establishes that **every command has an input stream and an output stream**. Understanding this is the foundation for piping and output redirection — once you see commands as processors with input and output channels, chaining them becomes intuitive.

***

### 4. less and more — File Readers vs. File Dumpers

Both `less` and `more` are **file readers** — they display file content in a controlled, navigable way. The key distinction from `cat` is explicitly stated: *"You can use cat also, but cat just displays all the content and quits."* Cat dumps everything to the screen at once. `less` and `more` let you **read** through content interactively. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**`less`** is the more capable reader. You can navigate with up/down arrows, search with `/` followed by a search term, and quit with `q`. The instructor notes it "looks like vim but it's not an editor — it's a reader." [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**`more`** is more limited — you cannot use up/down arrows, only `Enter`/`Return` keys to advance, and it shows a percentage progress indicator. The instructor states: *"I really don't use it much. I use less more than more."* You can quit with `q` or by reaching the end. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

***

### 5. head and tail — Partial File Viewing

`head` displays the **first 10 lines** of a file by default. `tail` displays the **last 10 lines**. Both accept a number flag to change the count: `head -20 file` shows the first 20 lines, `tail -2 file` shows the last 2 lines. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

The practical value is direct: *"You don't need to read the entire file."* When you just need to check the beginning or end of a file — verify a header, check recent entries, confirm a format — these commands save time.

**`tail -f` — Live Log Monitoring:**
This is one of the most operationally important capabilities covered in the lecture. The `-f` flag makes tail **follow** the file — it does not quit after showing the last 10 lines. Instead, it keeps the session open, and **any new content appended to the file appears on your screen in real time**. The cursor stays blinking, waiting for updates. You exit with `Ctrl+C`. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

The primary use case is **reading log files**. System and service logs are located in `/var/log`. On Red Hat machines, the system log file is `messages` (`/var/log/messages`), which records a wide range of system events including logins. The instructor demonstrates this live: tailing `/var/log/messages` in one terminal, then SSH-ing into the same machine from another Git Bash window. The login event appears dynamically in the tailed output. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

🔍 **Deep Dive — The Troubleshooting Methodology:**
The instructor reveals a core system administration troubleshooting pattern: *"One very important tip about troubleshooting a server: you see errors in log files. That's how you start troubleshooting."* Every service has its own log file. The workflow is: tail the log file with `-f` in one terminal session, then in another session make changes or restart the service. Watch the log for errors. If a specific action triggers an error, you've identified the cause. Then "more further you can funnel down to the problem." [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

This is a **dual-session troubleshooting pattern**: one session observes (tailing logs), another session acts (making changes). The observation session provides real-time feedback on whether actions are causing errors, which errors, and when. This is how professionals isolate problems in production systems.

***

### 6. cut — Column Extraction from Structured Data

`cut` extracts specific **fields (columns)** from files that have a consistent **delimiter** (separator character). The instructor demonstrates with `/etc/passwd`, which stores user information with fields separated by colons (`:`). [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

The command `cut -d: -f1 /etc/passwd` means: use `:` as the **d**elimiter, extract **f**ield **1** (the first column — usernames). You can extract any field by number: `-f3` for user ID, `-f4` for group ID, etc. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

The critical limitation: **cut requires proper, consistent delimiters.** If the file doesn't have clean separators (like colon, comma, tab), cut cannot reliably extract columns. For files with irregular or complex structure, the instructor introduces `awk` as the alternative. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

***

### 7. awk — Intelligent Filter Tool

`awk` is presented as the more powerful alternative to `cut` — an "intelligent filter tool" that supports regular expressions and advanced filtering techniques. The equivalent of the cut example is: `awk -F':' '{print $1}' /etc/passwd`. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

The `-F':'` sets the field separator (same as cut's `-d:`). The `'{print $1}'` is an awk program that prints the first field. The instructor acknowledges this looks more complicated than cut for simple cases, but states that *"for advanced search or intelligent search, awk is always better."* More awk examples are promised later in the course. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

***

### 8. Search and Replace — Two Methods, Two Scopes

The lecture covers two ways to search and replace text: **vim** (for editing individual files interactively) and **sed** (for command-line batch processing across one or many files). [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Vim's `:%s` command:** Inside vim, `:%s/search/replace` finds the first occurrence of "search" on each line and replaces it with "replace." The `%` means "the entire file," `s` means "substitute." However — and this is a critical behavior — **without the `g` flag, vim only replaces the first occurrence on each line.** If the same term appears multiple times on one line, only the first is replaced, then vim moves to the next line. Adding `/g` (global) at the end (`:%s/search/replace/g`) replaces **every** occurrence on every line. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

You can also replace with nothing — `:%s/covid-19//g` — which effectively **deletes** every occurrence of the search term. The `u` key undoes changes. If you quit with `:q!`, changes are discarded. If you save with `:wq`, they're permanent. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**sed (stream editor):** `sed 's/search/replace/g' filepath` performs the same search-and-replace but **from the command line**, without opening an editor. The same `/g` flag logic applies. sed also accepts wildcards: `*.txt` for all text files, or `*` for all files in the current directory. This makes sed enormously powerful for batch changes across multiple files. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**The critical safety behavior of sed:** By default, sed **only prints the modified output to the screen. It does NOT change the original file.** The instructor verifies this — after running sed, the original file still contains the old text. To actually modify the file, you must use the `-i` option (in-place editing). [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

The instructor frames this as a safety feature: *"It's like a little safer, right? First you see what you are changing, and then if you're good, use -i to actually change the content."* This establishes a **preview-then-commit pattern**: run sed without `-i` to preview changes → verify they look correct → run again with `-i` to apply. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

⚠️ **Expert Note:**
The preview-then-commit pattern with sed is essential operational discipline. In production, running `sed -i` on the wrong files or with the wrong pattern can corrupt configuration across an entire system. Always preview first. For extra safety in production, `sed -i.bak` creates a backup of the original file before modifying it (creates `filename.bak`).

***

### 9. The System Administrator's Operational Philosophy

Throughout the lecture, the instructor weaves in a consistent philosophy that transcends individual commands: [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**You don't need to memorize configuration file locations.** Linux stores configuration in text files, and grep can search recursively across entire directory trees. The skill is knowing **how to search**, not memorizing **where things are**.

**Most of your operations will follow this pattern:** Look for a file (grep/find) → make the change (vim/sed) → either manually or automatically through scripts. This is the fundamental operational loop of Linux system administration. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Log files are where troubleshooting begins.** Every service writes logs. Errors appear in logs. Tailing logs while making changes in another session is how you isolate problems. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

***

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

### What We Are Building and Why

We are building **proficiency in Linux data extraction, transformation, and routing** — the ability to find any text in any file, view files intelligently, extract specific data from structured files, search-and-replace across files, and monitor live system activity through logs. The final operational outcome: you can locate unknown configuration files, extract specific data from system files, make batch changes across multiple files, and troubleshoot running services by monitoring their logs in real time. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

All operations are performed as root user on a Linux VM.

***

### Step 1: Become Root User

```bash
sudo -i
```

`sudo` = execute as superuser. `-i` = login shell (full root environment). You need root access for unrestricted file operations across the system. Your prompt changes to `#` indicating root. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

***

### Step 2: Basic grep — Search for Text in a File

**Search for "firewall" in a file:**

```bash
grep firewall anaconda-ks.cfg
```

* `grep` = the search command
* `firewall` = the text pattern to find
* `anaconda-ks.cfg` = the file to search in

**Result:** Displays every line from the file that contains the word "firewall." [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Case-insensitive search:**

```bash
grep -i firewall anaconda-ks.cfg
```

* `-i` = ignore case

Now matches `firewall`, `Firewall`, `fireWall`, etc. Without `-i`, only exact case matches. This is essential because Linux is case-sensitive — `firewall` ≠ `Firewall`. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Verification:** The output should show all lines containing any casing variation of "firewall." Lines with uppercase F, lowercase f, or mixed case W should all appear.

***

### Step 3: Input Redirection (Explicit Form)

```bash
grep -i firewall < anaconda-ks.cfg
```

* `<` = explicit input redirection symbol

Produces the **same result** as without `<`. The `<` is invisible/implied by default. This demonstrates that the file is being fed as **input** to the grep command. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

***

### Step 4: grep Across Multiple Files and Directories

**Search all files in current directory:**

```bash
grep -i firewall *
```

* `*` = wildcard, means all files in current directory

**Result:** Shows matches with the **filename prefixed** to each matching line (e.g., `anaconda-ks.cfg:firewall --disabled`). However, if a directory exists in the current path, grep throws an error: `devopsdir: Is a directory`. grep does not enter directories by default. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Search recursively into directories:**

```bash
grep -iR firewall *
```

* `-R` = recursive (descend into subdirectories)
* Combined with `-i` as `-iR`

Now grep enters `devopsdir/` and searches files inside it too. The output includes paths like `devopsdir/mybootingfile.cfg:firewall --disabled`. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Connection to larger flow:** This is the building block for the real-world use case demonstrated next.

***

### Step 5: Real-World Use Case — Finding Unknown Configuration Files

**Scenario:** You know a setting name (`SELINUX`) but don't know which file in `/etc` contains it.

```bash
grep SELINUX /etc/* -R
```

* `SELINUX` = the configuration setting to find
* `/etc/*` = search all files in /etc
* `-R` = include all subdirectories

**Result:** Grep returns every file in the `/etc` tree that contains the text "SELINUX," showing the file path and the matching line. You identify the correct file from the results. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Then open and edit:**

```bash
vim /etc/selinux/config
```

Change the value (e.g., from `enforcing` to `disabled`), save with `:wq`. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Key insight:** The instructor emphasizes this is how system administrators actually work — *"They don't need to memorize things."* The pattern is: **search → find → edit.** This works because Linux stores all configuration in text files, making the entire system searchable with grep. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

***

### Step 6: Inverse grep — Exclude Matching Lines

```bash
grep -vi firewall anaconda-ks.cfg
```

* `-v` = invert match (show lines that do **NOT** contain the pattern)
* `-i` = case-insensitive

**Result:** Every line in the file is displayed **except** those containing any form of "firewall." Useful for filtering out known noise from output. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

***

### Step 7: Reading Files with less and more

**Using less:**

```bash
less anaconda-ks.cfg
```

* Navigate with up/down arrow keys
* Search with `/` then type search term (e.g., `/network`)
* Quit with `q`

`less` is a **reader**, not an editor — it looks like vim but you cannot modify the file. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Using more:**

```bash
more anaconda-ks.cfg
```

* Navigate with `Enter`/`Return` only (no arrow keys)
* Shows percentage progress at the bottom
* Quit with `q` or reach end of file

The instructor's preference: *"I use less more than more."* [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

***

### Step 8: Viewing File Beginnings and Endings

**First 10 lines (default):**

```bash
head anaconda-ks.cfg
```

**First N lines:**

```bash
head -20 anaconda-ks.cfg
head -2 anaconda-ks.cfg
```

* `-20` = show first 20 lines
* `-2` = show first 2 lines [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Last 10 lines (default):**

```bash
tail anaconda-ks.cfg
```

**Last N lines:**

```bash
tail -2 anaconda-ks.cfg
```

 [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

***

### Step 9: Live Log Monitoring with tail -f

This is one of the most operationally important capabilities in the entire lecture.

```bash
tail -f /var/log/messages
```

* `tail` = show end of file
* `-f` = **follow** — keep the session open and display new content as it's appended
* `/var/log/messages` = system log file on Red Hat machines

**What happens:** The last 10 lines display, then the cursor **keeps blinking** — it does not return to the prompt. Any new events written to this file appear on your screen in real time. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Live demonstration flow:**

1. In **Terminal 1**: run `tail -f /var/log/messages`
2. Open **Terminal 2** (another Git Bash window)
3. In Terminal 2: SSH into the machine (a successful login)
4. In **Terminal 1**: the login event appears dynamically in the tailed output

**Exit:** `Ctrl+C` to stop tailing and return to the prompt. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Other log file examples:**

```bash
tail -f /var/log/yum.log
```

Shows the last 10 lines of yum package manager activity, and any new installations/updates appear live. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Troubleshooting methodology (operational workflow):**

1. Identify the service's log file (usually in `/var/log/` or the service's own log directory)
2. In one terminal: `tail -f <logfile>`
3. In another terminal: make changes, restart the service, or trigger the suspected action
4. Watch the log for errors — when the error appears, you know what triggered it
5. Funnel down from there to isolate the root cause [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

⚠️ **Expert Note:**
The dual-session pattern (observe in one, act in another) is the standard troubleshooting workflow in production environments. Many engineers keep a `tail -f` running on the relevant log file **before** making any change, so they capture the exact moment something goes wrong. This is faster and more reliable than searching through logs after the fact.

***

### Step 10: Extracting Columns with cut

**View the passwd file:**

```bash
cat /etc/passwd
```

Each line represents a user. Fields are separated by colons (`:`): username:x:UID:GID:comment:home:shell. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Extract just usernames (field 1):**

```bash
cut -d: -f1 /etc/passwd
```

* `cut` = column extraction command
* `-d:` = **d**elimiter is colon
* `-f1` = extract **f**ield **1**

**Extract other fields:**

```bash
cut -d: -f3 /etc/passwd    # user IDs
cut -d: -f4 /etc/passwd    # group IDs
```

 [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Limitation:** cut only works when the file has **consistent, clean delimiters**. For irregular data, use awk instead.

***

### Step 11: Extracting Columns with awk

```bash
awk -F':' '{print $1}' /etc/passwd
```

* `awk` = advanced text processing tool
* `-F':'` = field separator is colon (same concept as cut's `-d`)
* `'{print $1}'` = awk program — print the first field
* `$1` = first field, `$2` = second field, etc.

**Result:** Same as `cut -d: -f1` — shows all usernames. awk is more complex syntactically but far more powerful for advanced filtering with regular expressions. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

***

### Step 12: Search and Replace in vim

**Open the file:**

```bash
vim sample.txt
```

**Replace first occurrence per line:**

```
:%s/coronavirus/covid-19
```

* `%` = entire file scope
* `s` = substitute
* `/coronavirus/` = search pattern
* `/covid-19` = replacement text

**Critical behavior:** This replaces only the **first match on each line**. If "coronavirus" appears twice on one line, only the first is replaced. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Replace ALL occurrences (global):**

```
:%s/coronavirus/covid-19/g
```

* `/g` = global — replace every occurrence on every line [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Replace with nothing (delete the text):**

```
:%s/covid-19//g
```

Two consecutive forward slashes with nothing between them = replace with empty string. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Undo:** Press `u` in command mode.
**Discard all changes:** `:q!` (quit forcefully without saving).
**Save changes:** `:wq` (save and quit). [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

***

### Step 13: Search and Replace with sed (Command Line)

**Basic sed — preview only (does NOT change the file):**

```bash
sed 's/coronavirus/covid19/g' sample.txt
```

* `sed` = stream editor
* `'s/coronavirus/covid19/g'` = substitute command (same syntax as vim's `:%s`)
* `sample.txt` = target file

**Result:** Modified text prints to the screen. The **original file is unchanged.** [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Verification that file is unchanged:**

```bash
cat sample.txt
```

Original content still shows `coronavirus`. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Apply changes to the file (in-place editing):**

```bash
sed -i 's/coronavirus/covid19/g' sample.txt
```

* `-i` = **i**n-place — actually modify the file

**Verification:**

```bash
cat sample.txt
```

Now shows `covid19` instead of `coronavirus`. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Batch processing across multiple files:**

```bash
sed 's/coronavirus/covid19/g' *.txt       # all .txt files (preview)
sed 's/coronavirus/covid19/g' *           # all files in current dir (preview)
sed -i 's/coronavirus/covid19/g' *.txt    # all .txt files (apply)
```

 [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Operational discipline — the preview-then-commit pattern:**

1. Run `sed 's/old/new/g' file` — preview what would change
2. Verify the output looks correct
3. Run `sed -i 's/old/new/g' file` — apply the change

This is the safe way to use sed. Never jump directly to `-i` without previewing first. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Replace with nothing:**

```bash
sed -i 's/covid19//g' sample.txt
```

Deletes every occurrence of `covid19` from the file. [\[28-filters \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/28-filters.txt)

**Connection to larger flow:** sed combined with grep forms the complete **search → find → change** operational loop. grep finds where the configuration lives, sed changes it — both from the command line, both scriptable, both automatable.

***

***

## 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

### Filter Tools — Function Map

```
SEARCH TEXT:
  grep <pattern> <file>              → find lines containing pattern
    -i                               → case-insensitive
    -R                               → recursive (enter subdirectories)
    -v                               → invert (show NON-matching lines)
    *                                → all files in current dir

READ FILES:
  less <file>                        → interactive reader (↑↓, /search, q)
  more <file>                        → basic reader (Enter only, % progress, q)
  cat <file>                         → dump entire file to screen (no navigation)

PARTIAL VIEW:
  head <file>                        → first 10 lines (head -N for N lines)
  tail <file>                        → last 10 lines (tail -N for N lines)
  tail -f <file>                     → LIVE follow (Ctrl+C to exit) ★

COLUMN EXTRACT:
  cut -d<delim> -f<N> <file>         → extract field N using delimiter
  awk -F'<delim>' '{print $N}' <file> → same but supports regex/advanced logic

SEARCH & REPLACE:
  vim:  :%s/old/new       → first per line only
        :%s/old/new/g     → global (all occurrences)
  sed:  sed 's/old/new/g' file    → preview only (no file change!)
        sed -i 's/old/new/g' file → apply change to file
        sed ... *.txt | *         → batch across multiple files
```

***

### Input/Output Flow Model

```
                    INPUT                    OUTPUT
                      ↓                       ↓
FILE → [< implicit] → COMMAND → stdout → screen (default)
                                       → > file  (overwrite)
                                       → >> file (append)
                         ↓
                      stderr → 2>> file (errors only)
                      all    → &>> file (stdout + stderr)
                         ↓
                COMMAND1 | COMMAND2  (pipe stdout → stdin)
```

***

### grep Decision Tree

```
Know exact case?
  YES → grep <term> <file>
  NO  → grep -i <term> <file>

Single file or multiple?
  SINGLE → grep <term> <file>
  ALL in dir → grep <term> *
  ALL including subdirs → grep -R <term> /path/*

Want matches or exclusions?
  MATCHES  → grep <term> (default)
  EXCLUSIONS → grep -v <term>
```

***

### sed Safety Pattern (Preview → Commit)

```
Step 1: sed 's/old/new/g' file       → PREVIEW (prints to screen, file unchanged)
Step 2: verify output visually
Step 3: sed -i 's/old/new/g' file    → COMMIT (modifies file in-place)

Without /g → replaces first match per line only
With /g    → replaces ALL matches per line
Replace with nothing: sed 's/old//g'  → deletes the pattern
```

***

### vim :%s vs sed — Scope Comparison

```
vim :%s/old/new/g
  → single file, interactive, inside editor
  → changes visible immediately, undo with u
  → save explicitly (:wq) or discard (:q!)

sed 's/old/new/g' file(s)
  → command-line, non-interactive, scriptable
  → supports wildcards (*.txt, *)
  → safe by default (preview-only)
  → -i to apply
  → batch-capable across many files
```

***

### Sysadmin Operational Loop (Core Pattern)

```
DON'T KNOW which file holds the setting?
  → grep -R <setting> /etc/*
     → find the file path in results

NEED TO CHANGE the setting?
  → vim <file>     (single file, manual)
  → sed -i         (single or batch, scriptable)

NEED TO VERIFY the change took effect?
  → grep <setting> <file>
  → restart service if needed

TROUBLESHOOTING a service?
  → Terminal 1: tail -f <logfile>     (observe)
  → Terminal 2: make changes/restart  (act)
  → Watch log for errors → identify trigger → funnel down
```

***

### Log File Locations — Quick Reference

```
/var/log/                → all system and service logs
/var/log/messages        → system log (Red Hat) ★
/var/log/yum.log         → yum package manager activity
[service-specific dirs]  → some services write logs elsewhere
```

***

### cut vs awk — When to Use Which

```
Data has CLEAN, CONSISTENT delimiters?
  YES → cut -d<delim> -f<N> file     (simple, fast)
  NO  → awk -F'<delim>' '{print $N}' (regex, intelligent)

/etc/passwd structure:
  username : x : UID : GID : comment : home : shell
  field:      1   2     3     4         5      6     7
  delimiter: colon (:)
```

***

### Key Behavioral Rules to Remember

| If you forget...                 | Remember...                                  |
| -------------------------------- | -------------------------------------------- |
| grep is case-sensitive?          | YES. Use `-i` to ignore case                 |
| grep enters subdirectories?      | NO by default. Use `-R` for recursive        |
| sed changes the file?            | NO by default. Use `-i` for in-place         |
| `:%s` replaces all occurrences?  | NO. Only first per line. Add `/g` for global |
| `tail -f` returns to prompt?     | NO. It follows live. `Ctrl+C` to exit        |
| Where are log files?             | `/var/log/` (system + services)              |
| Where are configs?               | `/etc/` (searchable with `grep -R`)          |
| How to find unknown config file? | `grep -R <setting_name> /etc/*`              |

***

### Reusable Patterns Extracted

| Pattern                          | Instance in This Lecture                                    |
| -------------------------------- | ----------------------------------------------------------- |
| **Search → Find → Edit**         | grep finds file → vim/sed edits → verify with grep          |
| **Preview → Commit**             | sed without `-i` (preview) → sed with `-i` (commit)         |
| **Dual-Session Troubleshooting** | Terminal 1: `tail -f` (observe) ↔ Terminal 2: act           |
| **Text-as-Interface**            | All config in text files → searchable, editable, scriptable |
| **Small tools composed**         | grep + cut + sed + pipe = complex data pipeline             |
| **Don't memorize, search**       | grep -R replaces memorizing file locations                  |

***

This completes the full analysis of the Filters & Redirections lecture. Every command, option, use case, and operational insight from the video has been preserved across the three complementary sections — Theory for understanding, Practical for execution, and Mental Compression Map for rapid future recall. <cite>turn4search4</cite>

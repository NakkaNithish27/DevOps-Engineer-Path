# Vim Editor — Complete Text Editing in Linux

### Creating, Editing, Navigating, and Operating Files from the Command Line

*Reconstructed from video lecture captions* [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Vim Is and Why It Matters

Vim is a **text editor** that operates entirely inside the Linux terminal. Throughout any DevOps, Linux administration, or server management workflow, you will constantly need to create and edit text files — configuration files, scripts, logs, notes. You cannot use graphical editors like Notepad or VS Code on a remote Linux server accessed via SSH. You need an editor that works inside the command line itself. Vim is that editor. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

If you already know another terminal-based text editor like **Nano**, you can continue using that. But if you have no text editor experience in Linux, vim is the one the course teaches and uses going forward. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

## 1.2 — vi vs. vim: The Relationship

Vim stands for **Vi IMproved**. `vi` is the original text editor that ships with virtually every Linux distribution. `vim` is an enhanced version of `vi` — it adds features like syntax highlighting, better navigation, and more powerful commands, but the core editing model (modes, commands, shortcuts) is the same. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

A critical installation fact: on **CentOS**, vim is **not installed by default** — only the basic `vi` editor is present. You must install vim manually. On **Ubuntu**, vim comes **pre-installed**. This means if your CentOS vim installation fails (e.g., no internet connectivity on the VM), you can switch to the Ubuntu VM where vim is already available, rather than spending time troubleshooting network issues at this stage. Networking with Vagrant is covered later, so the video explicitly advises: **do not troubleshoot installation failures now — just use the Ubuntu VM instead.** [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

## 1.3 — The Three-Mode Architecture (Core Concept)

This is the single most important concept to understand about vim. Unlike typical editors where you just type and your keystrokes appear on screen, vim operates through a **modal architecture** — the same key does completely different things depending on which **mode** you are in. There are three modes: [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

### Command Mode (Default)

When you first open a file in vim, you land in **command mode**. In this mode, your keystrokes are interpreted as **commands**, not as text input. Pressing `j` doesn't type the letter "j" — it moves the cursor down. Pressing `dd` doesn't type "dd" — it deletes a line. This is the most common source of confusion for beginners: they open vim, start typing, and nothing they expect happens because they're in command mode, not insert mode. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

Command mode is the **hub** of vim. You always return here before switching to any other mode. It is the resting state, the control center. Every navigation shortcut, every copy/paste/delete operation, every search — all of these happen in command mode. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

### Insert Mode (Editing)

To actually type text into the file — to write, edit, add content — you must enter **insert mode**. There are two ways to enter insert mode from command mode: [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

* **`i`** (as in India) — enters insert mode at the current cursor position. You start typing exactly where the cursor is.
* **`o`** (as in Oscar) — enters insert mode but first creates a **new line below** the current line and places the cursor there. This is useful when you want to add a new line of content without manually positioning the cursor at the end of the current line and pressing Enter. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

Once in insert mode, vim behaves like a normal text editor — your keystrokes produce characters on screen. To leave insert mode and return to command mode, press **`Esc`**. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

### Extended Mode (Operations)

When you need to perform file-level operations — saving, quitting, searching, setting options — you use **extended mode** (also called command-line mode or last-line mode). You enter extended mode by pressing **`:`** (colon) while in command mode. A colon prompt appears at the bottom of the screen, and you type your operation command there. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

The critical transition rule: **you cannot go directly from insert mode to extended mode.** You must first press `Esc` to return to command mode, then press `:` to enter extended mode. Command mode is always the intermediary. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

```
Mode Transition Map:

                    i or o
   Command Mode ──────────→ Insert Mode
        ↑                        │
        │         Esc            │
        ←────────────────────────┘
        │
        │    : (colon)
        ↓
   Extended Mode
   (bottom-line prompt)
```

> 🔍 **Deep Dive**
> The modal architecture exists because vim was designed for efficiency on systems where mice didn't exist and keyboards had limited keys. By separating "navigation/commands" from "text input," vim allows every letter key to serve double duty — as a powerful command in command mode and as a text character in insert mode. This is why experienced vim users can edit files extremely fast: they navigate, copy, delete, and rearrange text using single keystrokes without ever reaching for a mouse or arrow keys. The learning curve is steep precisely because of this modal design, but once internalized, it becomes the fastest text editing method available in a terminal.

***

## 1.4 — File Extensions in Linux

When creating a file like `firstfile.txt`, the `.txt` extension is purely **for human reference**. Unlike Windows, where extensions determine which application opens a file, Linux does not use extensions to determine file type or behavior. You could name the file `firstfile` with no extension at all and it would work identically. The video explicitly states: "extension is just for our reference. It doesn't matter." [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

## 1.5 — The Save/Quit Operation Model

Extended mode commands follow a consistent pattern of short mnemonics: [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

| Command | Meaning             | Behavior                                                                            |
| ------- | ------------------- | ----------------------------------------------------------------------------------- |
| `:w`    | **Write**           | Saves the file to disk. Vim confirms with line count and character count.           |
| `:q`    | **Quit**            | Exits vim. Only works if there are no unsaved changes.                              |
| `:wq`   | **Write + Quit**    | Saves and exits in one operation.                                                   |
| `:q!`   | **Quit forcefully** | Exits vim **discarding all unsaved changes**. The `!` overrides vim's safety check. |

The important behavioral rule: if you have made changes and try `:q`, vim **refuses to quit** and warns you. This is a safety mechanism. You must explicitly choose: either save first (`:wq`) or discard changes (`:q!`). Vim never silently loses your work. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

> ⚠️ **Expert Note**
> The `:q!` command is the emergency exit. In production, if you accidentally opened a critical config file and made unintended changes, `:q!` is your safety net — it guarantees you leave the file exactly as it was before you opened it. Never use `:wq` unless you are certain your changes are correct.

***

## 1.6 — Navigation Model: Moving Beyond Arrow Keys

In command mode, vim provides shortcuts for moving through files far faster than arrow keys. The video teaches a specific set of navigation commands designed for large files (hundreds or thousands of lines): [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

* **`Shift+G`** (capital G) — jumps to the **last line** of the file
* **`gg`** (small g twice) — jumps to the **first line** of the file
* **`w`** — moves cursor **one word forward**
* **`b`** — moves cursor **one word backward**
* **`nw`** (e.g., `5w`) — moves cursor **n words forward** (the `n` is replaced by a number)

The `n` prefix pattern is important: vim treats numbers before commands as **multipliers**. This is a general vim design principle — `5w` means "do `w` five times." This same multiplier logic applies to copy, delete, and other operations, creating a composable command language. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

## 1.7 — Copy, Paste, Cut, and Delete: The yy/dd/p System

Vim's clipboard operations use a different vocabulary than typical editors. The video teaches them through a practical file called `anaconda-ks.cfg` — a file found in the root user's home directory that contains information about how the OS was installed. This file is used purely as a practice playground because it has many lines of real content. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

### Copy (Yank) and Paste

* **`yy`** — **yanks** (copies) the current line. The term "yank" is vim's word for copy.
* **`nyy`** (e.g., `4yy`) — yanks **n lines** starting from the cursor position downward.
* **`p`** (small) — **pastes** the yanked content **below** the current line.
* **`P`** (capital) — **pastes** the yanked content **above** the current line. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

### Cut (Delete) and Paste

* **`dd`** — **deletes** the current line. But critically, this is not just a delete — **`dd` is actually a cut operation**. The deleted content is stored in vim's buffer and can be pasted with `p`. This is a common misunderstanding: people think `dd` destroys the content permanently, but it actually functions like "cut" in a graphical editor.
* **`ndd`** (e.g., `5dd`) — cuts **n lines** starting from the cursor position. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

The video demonstrates a powerful trick: to delete all lines in a file, go to line 1 (`gg`), then use `117dd` (where 117 is the total number of lines). This wipes the entire file content. If you save after this, the file becomes empty permanently. But if you haven't saved, `u` (undo) brings everything back. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

### Undo

* **`u`** — undoes the last change. Can be pressed repeatedly to undo multiple changes in reverse order. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

> 🔍 **Deep Dive**
> The `yy`/`dd` + `p` system is consistent with vim's multiplier-prefix design: the number before the command always means "apply this command to n lines." `4yy` = yank 4 lines. `5dd` = delete 5 lines. `3p` would paste 3 times. Once you internalize the `[count][command]` pattern, you can compose operations without memorizing individual combinations. This composability is what makes vim powerful — a small set of building blocks creates a large set of possible operations.

***

## 1.8 — Search Within a File

To find specific text in a file, vim uses **forward slash** (`/`) as the search trigger. From command mode, press `/`, type the search term, and press Enter. Vim highlights and jumps to the first occurrence. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

* **`n`** — moves to the **next** occurrence of the search term
* When the search reaches the bottom of the file, it **wraps around** to the top with the message: "Search hit bottom, continue at Top" [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**Search is case-sensitive.** The video explicitly demonstrates this: searching for lowercase `network` finds matches, but if the file contained `Network` with a capital N, a lowercase search would not find it. This ties into a broader Linux principle: **Linux is case-sensitive in nearly everything** — file names, commands, search operations, and this behavior continues throughout the course. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

## 1.9 — Line Numbers Display

The command `:se nu` (short for "set numbers") in extended mode toggles **line numbers** along the left margin. This is a display-only setting — it doesn't modify the file. Line numbers are essential when working with large files because they let you reference specific lines during copy/paste/delete operations and when communicating about file content (e.g., "the error is on line 45"). [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

## 1.10 — Alternative Copy-Paste: Using GitBash Selection

The video briefly mentions that you can also copy-paste using **GitBash's own selection mechanism** — click and drag to select text in the terminal window, right-click to copy, position cursor, enter insert mode, and paste. This is a host-level operation (GitBash feature), not a vim operation. It works but is less precise than vim's native `yy`/`p` system for line-level operations. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are installing the vim text editor, learning to create and edit files, and building operational fluency with vim's three-mode editing system — command mode, insert mode, and extended mode. By the end, you will be able to create files, write content, save, quit, navigate large files, copy/paste lines, cut/delete lines, undo changes, and search for text. These operations are used constantly throughout all subsequent Linux, DevOps, Docker, and Kubernetes work. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

## Step 1 — Install Vim on CentOS

You are logged into the CentOS VM as the `vagrant` user. Vim is not pre-installed on CentOS (only basic `vi` is available). [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

```bash
sudo yum install vim -y
```

* `sudo` — runs the command with **root (administrator) privileges**. Installing software requires elevated permissions.
* `yum` — the **package manager** for CentOS/Red Hat systems. It downloads and installs software from configured repositories.
* `install` — the yum subcommand to install a package.
* `vim` — the package name to install.
* `-y` — automatically answers **yes** to all confirmation prompts, allowing the installation to proceed without manual intervention. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**Verification:** After installation completes, you should be able to run `vim` without errors.

**Failure scenario:** If installation throws errors, the most likely cause is the VM not having internet connectivity. The video explicitly instructs: **do not troubleshoot this now.** Either recreate the VM or switch to the Ubuntu VM where vim is pre-installed. Networking troubleshooting with Vagrant is covered in a later lecture. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**Connection to system flow:** This is a one-time setup step. Once vim is installed, it's available for all future file editing on this VM.

***

## Step 2 — Create and Open a New File

Navigate to or confirm you are in your home directory (the video states "I'm in the home directory"). [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

```bash
vim firstfile.txt
```

* `vim` — launches the vim editor
* `firstfile.txt` — the filename to create/open. If the file doesn't exist, vim creates it. If it exists, vim opens it for editing. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**What happens:** A vim editing screen opens. At the bottom, you'll see **"\[New File]"** indicating this file is being created fresh. You are now in **command mode** — keystrokes are commands, not text input. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**Common mistake:** Trying to type text immediately. Nothing will appear as expected because you're in command mode. You must switch to insert mode first.

***

## Step 3 — Enter Insert Mode and Write Content

Press **`i`** (lowercase, as in India). [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

The bottom of the screen changes to show `-- INSERT --`, confirming you are now in insert mode. Type your content:

```
Welcome to Linux.
I hope you enjoy command line.
```

Every keystroke now produces text on screen, exactly like a normal editor. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**Connection to system flow:** You've transitioned from command mode → insert mode. The file now has unsaved content in memory.

***

## Step 4 — Save the File

Press **`Esc`** to return to command mode (the `-- INSERT --` indicator disappears). [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

Then type:

```
:w
```

* `:` — enters extended mode (a colon prompt appears at the bottom of the screen)
* `w` — **write** (save) the file to disk [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

Press **Enter**.

**Expected output:** Vim confirms with a message like `"firstfile.txt" 2L, 45C written` — showing the filename, number of lines (2L), and number of characters (45C). Vim counts these automatically. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**What happened internally:** The content that existed only in vim's memory buffer has now been written to the file on disk.

***

## Step 5 — Quit Vim

From command mode (press `Esc` if unsure): [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

```
:q
```

Press **Enter**. Vim exits and you return to the shell prompt.

**Verification:** Use the `cat` command to read the file and confirm your content was saved:

```bash
cat firstfile.txt
```

This prints the file content directly to the terminal. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

## Step 6 — Reopen and Add Content with `o`

```bash
vim firstfile.txt
```

This time, vim opens an **existing** file (no "\[New File]" message). The previous content is visible. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

Press **`o`** (as in Oscar) to enter insert mode. Unlike `i`, which places the cursor at the current position, `o` creates a **new blank line below** the current line and enters insert mode there. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

Type additional content:

```
It is super important for you to practice Linux before into DevOps.
```

 [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

## Step 7 — Save and Quit in One Operation

Press **`Esc`**, then type: [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

```
:wq
```

Press **Enter**. This saves the file **and** exits vim in a single command — combining the `:w` (write) and `:q` (quit) operations. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**Verification:** The file now contains all three lines.

***

## Step 8 — Force Quit Without Saving

Open the file again:

```bash
vim firstfile.txt
```

Make some changes (enter insert mode, type something, or delete text). Then realize you don't want to save these changes. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

Press **`Esc`**, then try:

```
:q
```

**What happens:** Vim **refuses to quit** and displays an error message indicating unsaved changes exist. This is vim's safety mechanism. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

To discard all changes and exit:

```
:q!
```

* `!` — the **force** operator. Overrides vim's safety check and quits without saving. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**Verification:** Check the file with `cat` — it contains only the original content. All changes made in that session are gone.

**Connection to system flow:** You now know all four extended mode operations — `:w`, `:q`, `:wq`, `:q!`. These are the complete save/quit vocabulary of vim.

***

## Step 9 — Switch to Root and Open a Practice File

To practice navigation and copy/paste on a larger file, switch to the root user: [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

```bash
su -
```

*(Or however you become root on your VM.)*

The root user's home directory contains a file called **`anaconda-ks.cfg`** — this file stores information about how the operating system was installed (what options were selected during OS installation). The video uses this purely as a large practice file. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

```bash
vim anaconda-ks.cfg
```

***

## Step 10 — Enable Line Numbers

From command mode, type: [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

```
:se nu
```

* `:` — extended mode
* `se nu` — short for **set numbers**

Line numbers appear along the left margin. This is a display setting only — it doesn't modify the file. Useful for referencing specific lines during editing operations. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

## Step 11 — Navigate Large Files

All of these work in **command mode** (press `Esc` first if needed): [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

| Keystroke             | Action                                                      |
| --------------------- | ----------------------------------------------------------- |
| `Shift+G` (capital G) | Jump to the **last line**                                   |
| `gg` (small g twice)  | Jump to the **first line**                                  |
| `5w`                  | Move cursor **5 words forward** (replace 5 with any number) |
| `w`                   | Move cursor **1 word forward**                              |
| `b`                   | Move cursor **1 word backward**                             |

 [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**When to use:** Files with hundreds or thousands of lines where arrow keys are impractical. `Shift+G` and `gg` are the most frequently used — they get you to the extremes of the file instantly.

***

## Step 12 — Copy and Paste Lines

**Copy a single line:** Position cursor on line 12 (using arrow keys or navigation). [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

```
yy
```

This **yanks** (copies) the entire current line. No visual confirmation — the operation is silent.

Navigate to the destination (e.g., `Shift+G` to go to the last line):

```
p
```

The yanked line is pasted **below** the current line. Use **`P`** (capital) to paste **above** instead. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**Copy multiple lines:** Position cursor on line 16. To copy lines 16, 17, 18, 19 (four lines): [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

```
4yy
```

Navigate to destination, then `p` to paste. All four lines appear. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

## Step 13 — Cut (Delete) and Paste Lines

**Delete/cut a single line:** [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

```
dd
```

The current line disappears. But it is **not destroyed** — it is stored in vim's buffer (this is a cut, not a permanent delete).

**Undo the delete:**

```
u
```

The line reappears. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**Delete multiple lines:** Position cursor on the target starting line. To cut 4 lines:

```
4dd
```

Navigate to destination, then `p` to paste the cut lines. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**Delete all lines in a file:** Go to line 1 (`gg`), then delete all 117 lines:

```
117dd
```

The entire file is now empty. If you save (`:wq`), the file is permanently emptied. If you undo (`u`), everything comes back. The video uses `:q!` to exit without saving, preserving the original file. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**Key insight:** `yy` + `p` = copy-paste. `dd` + `p` = cut-paste. The paste command `p` works with whatever was last yanked or deleted. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

## Step 14 — Search for Text

Open a file in vim. From command mode: [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

```
/network
```

* `/` — initiates a **forward search**
* `network` — the search term

Press **Enter**. Vim jumps to and highlights the first occurrence. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

Press **`n`** to jump to the **next** occurrence. When the search reaches the end of the file, vim wraps around to the top with the message: `"Search hit bottom, continue at Top"`. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

**Critical behavior:** Search is **case-sensitive**. Searching `/network` will NOT match `Network` or `NETWORK`. This is consistent with Linux's overall case-sensitive nature, which the video emphasizes will apply to everything from this point forward. [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

## Operations Summary

| Operation                          | Keystroke(s)     | Mode             |
| ---------------------------------- | ---------------- | ---------------- |
| Enter insert mode (at cursor)      | `i`              | Command → Insert |
| Enter insert mode (new line below) | `o`              | Command → Insert |
| Return to command mode             | `Esc`            | Any → Command    |
| Save                               | `:w` + Enter     | Extended         |
| Quit                               | `:q` + Enter     | Extended         |
| Save & quit                        | `:wq` + Enter    | Extended         |
| Force quit (discard changes)       | `:q!` + Enter    | Extended         |
| Show line numbers                  | `:se nu` + Enter | Extended         |
| Go to last line                    | `Shift+G`        | Command          |
| Go to first line                   | `gg`             | Command          |
| Copy line                          | `yy`             | Command          |
| Copy n lines                       | `nyy`            | Command          |
| Paste below                        | `p`              | Command          |
| Paste above                        | `P`              | Command          |
| Delete/cut line                    | `dd`             | Command          |
| Delete/cut n lines                 | `ndd`            | Command          |
| Undo                               | `u`              | Command          |
| Search                             | `/term` + Enter  | Command          |
| Next search result                 | `n`              | Command          |
| Move word forward                  | `w`              | Command          |
| Move word backward                 | `b`              | Command          |
| Move n words forward               | `nw`             | Command          |

 [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Architecture: Three-Mode System

```
┌─────────────────────────────────────────────────────┐
│                   VIM EDITOR                         │
│                                                     │
│   ┌──────────────┐                                  │
│   │ COMMAND MODE │ ← DEFAULT / HUB                  │
│   │              │                                  │
│   │ Navigation:  │    ┌─────────────┐               │
│   │  gg, G,      │──→ │ INSERT MODE │               │
│   │  w, b, nw    │ i  │             │               │
│   │              │ o  │ Type text   │               │
│   │ Operations:  │    │             │               │
│   │  yy, dd,     │ ←──│   Esc       │               │
│   │  p, P, u     │    └─────────────┘               │
│   │              │                                  │
│   │ Search:      │    ┌──────────────┐              │
│   │  /term, n    │──→ │ EXTENDED MODE│              │
│   │              │ :  │              │              │
│   └──────────────┘    │ :w  :q  :wq  │              │
│                       │ :q!  :se nu  │              │
│                       └──────────────┘              │
└─────────────────────────────────────────────────────┘
```

***

## Mode Transition Rules

```
Command ──i/o──→ Insert ──Esc──→ Command
Command ──:────→ Extended ─Enter→ Command
Insert  ──(X)──→ Extended   ← BLOCKED. Must go through Command.
```

**Golden rule:** Command mode is always the hub. You always return there first.

***

## Command Composability Pattern

```
[count] + [operator] = action on N items

  4yy  →  yank 4 lines
  5dd  →  delete 5 lines
  5w   →  move 5 words forward
117dd  →  delete all 117 lines

Operator vocabulary:
  yy = copy (yank)     dd = cut (delete)
  p  = paste below     P  = paste above
  u  = undo            w  = word forward
  b  = word backward
```

***

## Save/Quit Decision Tree

```
Want to save?
  ├── YES → Want to quit too?
  │          ├── YES → :wq
  │          └── NO  → :w
  └── NO  → Want to quit?
             ├── No changes made → :q (works)
             └── Changes made → :q FAILS
                                → :q! (force discard + quit)
```

***

## Copy vs. Cut Mental Model

```
COPY workflow:  yy (or nyy)  → navigate → p/P
CUT  workflow:  dd (or ndd)  → navigate → p/P

⚠️ dd is CUT, not permanent delete.
   Content lives in buffer until next yy/dd overwrites it.
   u (undo) reverses the dd itself.
```

***

## Search Behavior

```
/term → Enter → first match → n → next match → ... → wraps to top
                                                       ↑
                                    "Search hit bottom, continue at Top"

Case-sensitive: /network ≠ /Network ≠ /NETWORK
(Linux is case-sensitive in everything)
```

***

## Installation & Environment

```
CentOS:  vim NOT pre-installed → sudo yum install vim -y
Ubuntu:  vim IS pre-installed  → ready to use

Install fails? → Don't troubleshoot → Use Ubuntu VM
                  (Networking covered later)

File extensions: irrelevant in Linux (purely human reference)
```

***

## Practice File Shortcut

```
Root user home dir → anaconda-ks.cfg
   = OS installation record
   = Large multi-line file for practicing vim navigation/editing
   = Safe to experiment on (non-critical)
```

***

## Key Failure Points & Recovery

```
❌ Typing text but nothing appears     → You're in command mode → press i
❌ :q refuses to quit                  → Unsaved changes → :q! to discard, or :wq to save
❌ vim not found on CentOS             → sudo yum install vim -y (or use Ubuntu VM)
❌ Search not finding expected text     → Case mismatch (Linux is case-sensitive)
❌ dd deleted important content         → u to undo (dd is cut, not permanent delete)
❌ Pasted in wrong place               → u to undo, reposition, paste again
```

***

## Reusable Engineering Patterns

**1. Modal Interface Pattern:** A single interface (keyboard) serves multiple functions by switching between discrete modes. The same physical input produces different behaviors depending on system state. *Transferable to:* any system with operational modes (network device config mode vs. exec mode, Kubernetes context switching, terminal multiplexer modes in tmux/screen).

**2. Hub-and-Spoke State Machine:** Command mode is the central hub — all transitions route through it. No direct transitions between peripheral modes (Insert ↛ Extended). This simplifies the mental model: when lost, press `Esc` to return to the known state. *Transferable to:* state machine design in any system where a "safe default state" simplifies recovery.

**3. Count-Operator Composability:** Instead of memorizing dozens of commands, learn a small operator set (`yy`, `dd`, `w`, `p`) and compose them with numeric prefixes. A small vocabulary creates a large action space. *Transferable to:* Unix command composition (piping), API design, any system that favors composable primitives over monolithic commands.

**4. Destructive-Action Safety Net:** Vim refuses `:q` when changes exist, forcing explicit intent (`:wq` or `:q!`). Destructive operations require deliberate confirmation. *Transferable to:* production safeguards (`--dry-run`, `terraform plan`, confirmation prompts before destructive API calls). [\[26-vim-editor \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/26-vim-editor.txt)

***

*This completes the full reconstruction of the vim editor lecture. Theory explains the modal architecture and command design. Practical teaches exact execution sequences. Mental Compression Map enables rapid future recall of the entire system through structural compression.*

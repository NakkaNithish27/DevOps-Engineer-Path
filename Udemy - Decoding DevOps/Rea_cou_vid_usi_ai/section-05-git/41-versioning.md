# 🎓 Git Version Control — Local & Remote Repository Workflow — Deep Learning Material

*Reconstructed from the video lecture on Git versioning, local/remote repositories, and GitHub integration* [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. What Git Solves — The Versioning Problem

Git is a **version control system** — it tracks every change made to files over time, recording **who** made the change, **when** it was made, and **what** exactly changed. Without version control, you have no history: if someone modifies a file, the previous state is lost. Git solves this by maintaining a complete, navigable history of every modification, addition, and deletion across all files in a project. Each saved point in this history is called a **commit**, and every commit has a unique **commit ID** that acts as its permanent address in the timeline. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## 2. The Repository — Git's Unit of Tracking

A **repository** (repo) is simply a directory that Git is tracking. Any regular directory on your filesystem can become a Git repository by running `git init` inside it. This command creates a hidden subdirectory called **`.git`** within the directory. This `.git` folder is the entire brain of the repository — it stores all versions, all history, all configuration, and all branch information. The working directory looks normal to you; the `.git` folder silently maintains everything underneath. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

Once `.git` exists, your shell prompt changes to show the **branch name** (e.g., `master` or `main`), providing a constant visual indicator that you're inside a Git-tracked directory. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

A critical rule about what Git tracks: **Git tracks files, not directories**. If you create an empty directory inside your repository, Git will ignore it entirely. Directories only become visible to Git when they contain at least one file. This is why the instructor explicitly warns: "make sure the directories are not empty, otherwise git will not keep track of it." [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## 3. The Three-Stage Workflow — Working Directory → Staging Area → Commit

Git does not automatically save every change you make. Instead, it uses a deliberate **three-stage workflow** that gives you full control over what gets recorded and when: [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Stage 1: Working Directory (Untracked/Modified).** You create files, edit files, delete files — these changes exist only in your working directory. Git is aware something changed (it can detect modifications), but the changes are **untracked** — they are not yet considered for the next commit. Running `git status` at this point shows files as "untracked" (new files) or "modified" (changed files). [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Stage 2: Staging Area (Indexed).** You explicitly tell Git which changes to include in the next commit by running `git add`. This moves changes into the **staging area** — a holding zone where you assemble the set of changes that will form the next commit. This step is called **staging** or **indexing**. You can stage individual files (`git add filename`) or everything at once (`git add .` — dot means current directory and all its contents). After staging, `git status` shows these files as "changes to be committed." [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Stage 3: Commit (Permanently Recorded).** Running `git commit` takes everything in the staging area and permanently records it as a new version in the repository's history. Every commit requires a **message** (`-m "message"`) describing what changed — this is mandatory and serves as the human-readable label for that point in history. After committing, `git status` shows "nothing to commit, working tree clean" — meaning the working directory matches the latest committed state. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

> 🔍 **Deep Dive**
> The three-stage design exists because not every change you make should necessarily be committed together. You might modify five files but only want to commit changes to three of them right now. The staging area gives you this selective control — you choose what goes into each commit, rather than committing everything blindly. This enables clean, logical commit history where each commit represents a coherent, purposeful change.

***

## 4. Git Identity Configuration — Who Made the Change

Git doesn't just track *what* changed — it tracks *who* changed it. Before you can make your first commit, Git requires you to configure a **username** and **email address**. Without this, `git commit` will fail with an error message that provides the exact commands to set them up. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

Git configuration exists at two levels: [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Global** (`git config --global`) — Applies to **all repositories** on your machine. Set once, and every repository you create or work in will use these values by default. The instructor sets the global username and email address, noting that if you have a GitHub account, you should use the same email address for consistency — it makes tracking contributions across local and remote repositories easier. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Local** (`git config` without `--global`) — Applies only to the **specific repository** you're currently in. Local settings override global settings for that repository. The instructor mentions this distinction but uses global configuration for the demo. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## 5. Local vs. Remote Repositories — The Two Halves of Git

Everything described so far happens **locally** — on your own machine, with no network involved. Your commits, your history, your branches — all stored in the `.git` folder on your local disk. This is a fully functional version control system by itself. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

A **remote repository** is a copy of the repository hosted on a server accessible over the network. It serves as the **shared central point** where multiple contributors can synchronize their work. The instructor mentions three remote repository hosting services: **GitHub** (the most popular, used in this course), **Bitbucket**, and **CodeCommit** (AWS's offering, to be used later in the course). The instructor notes there's "not much difference" between them operationally. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

There are **two ways** to establish the local-remote relationship: [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Remote → Local (Clone):** If a remote repository already exists, you run `git clone <URL>` to download a complete copy to your local machine. This creates a new local directory with all files, history, and the remote connection already configured. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Local → Remote (Add Origin + Push):** If you created the repository locally first (as in the demo), you create an empty remote repository (on GitHub), then link your local repo to it using `git remote add origin <URL>`. The word **`origin`** is the conventional name for the primary remote repository — it's an alias so you don't have to type the full URL every time. After linking, you run `git push` to upload your local commits to the remote. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

> 🔍 **Deep Dive**
> When you run `git remote add origin <URL>`, the URL is stored in the `.git/config` file inside your repository. The instructor explicitly opens this file to show the new `[remote "origin"]` entry. This means the local-remote connection is just a configuration entry — it can be viewed, modified, or removed by editing this file or using git remote commands.

***

## 6. Push and Pull — Synchronization Mechanics

Once local and remote repositories are linked, two operations keep them in sync: [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**`git push origin main`** — Uploads your local commits to the remote repository on the specified branch (`main`). This is how your local changes become visible to other contributors and to the GitHub web interface. Push requires **authentication** — GitHub needs to verify you have permission to modify the remote repository. On Windows, this may open a browser window for sign-in or prompt for credentials. Once authenticated, the credentials are saved locally so you don't need to re-enter them. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**`git pull`** — Downloads changes from the remote repository to your local repository. If someone else (another contributor) pushed changes to the remote, or if you edited a file directly on GitHub's web interface, `git pull` brings those changes down to your local copy. The instructor demonstrates this by editing a file directly on GitHub (simulating another contributor's change), then running `git pull` locally to receive it. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

The operational cycle is: **make changes → `git add` → `git commit` → `git push`** (local to remote), and **`git pull`** (remote to local). [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## 7. Branches — Named Lines of Development

When you initialize a repository, Git creates a default branch. Historically this was called **`master`**; the current convention (and GitHub's default) is **`main`**. The instructor renames the branch from `master` to `main` using `git branch -M main` to match GitHub's expectation. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

The instructor mentions branches as a concept that will be explored further ("we'll see what branches are"), but in this lecture, only the default branch (`main`) is used. The branch name appears in the shell prompt and in `git log` output, and it's specified in push/pull commands (`git push origin main`). [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## 8. Commit History and Inspection — `git log` and `git show`

Every commit creates a permanent record with: a **commit ID** (a long hexadecimal hash that uniquely identifies the commit), the **author** (name and email from git config), the **date and time**, and the **commit message**. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**`git log`** displays the full commit history of the current branch, showing all of these fields for each commit, newest first. For a more compact view, **`git log --oneline`** shows each commit as a single line with a **shortened commit ID** and the commit message only. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**`git show <commit-id>`** displays the detailed **diff** (what changed) for a specific commit — which lines were added (shown with `+` and green color on GitHub) and which were removed (shown with `-` and red color). You can use either the full commit ID or the shortened one from `--oneline`. The instructor demonstrates that `git show` on the command line produces the same information visible on GitHub's web interface when you click on a commit message. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## 9. GitHub's Web Interface — Visibility and Direct Editing

GitHub provides a web interface that mirrors and extends the command-line experience. You can see all files and directories, view commit messages and timestamps, click on commit messages to see diffs, and even **edit files directly** on GitHub. When you edit a file on GitHub and commit the change there, it creates a new commit on the remote repository. This simulates what happens when another contributor pushes a change — the remote now has commits that your local repository doesn't. You must `git pull` to synchronize. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

GitHub repositories can be **public** (visible to anyone in the world) or **private** (accessible only to authenticated/authorized users). The instructor creates a private repository for the demo. An optional **README file** can be added during creation — it's displayed on the repository's GitHub page — but the instructor skips it. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

Two URL types are offered for remote access: **HTTPS** and **SSH**. The instructor uses HTTPS for now and notes that SSH will be covered at the end of the Git section. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## 10. Authentication for Push Operations

When you `git push` to a remote repository, you're modifying data on a server — this requires **authentication**. The first time you push, GitHub prompts for credentials (username/password or browser-based sign-in). On Windows, after successful authentication, the credentials are **saved locally** (in the Windows Credential Manager), so subsequent pushes don't require re-authentication. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Building

We are creating a **local Git repository**, populating it with files, committing changes, linking it to a **remote GitHub repository**, and establishing a complete **push/pull synchronization workflow**. By the end, we can track file changes locally, push them to GitHub, make remote changes, and pull them back — the full operational Git cycle. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## Step 1: Open Your Terminal

**On Windows:** Open **Git Bash** (Git must be installed already). **On macOS:** Install Git, then open the regular **Terminal**. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## Step 2: Create and Enter the Repository Directory

**What we're doing:** Creating a regular directory that will become our Git repository.

```bash
cd /f
mkdir git-repository
cd git-repository
mkdir titan-work
cd titan-work
```

* Navigate to your chosen drive/location
* Create a directory (the instructor names it `titan-work`)
* Enter that directory — this is where the repository will live [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

The name you choose here will also be the name of the remote repository on GitHub — keep them matching for clarity.

***

## Step 3: Initialize the Git Repository

**What we're doing:** Converting this regular directory into a Git-tracked repository.

```bash
git init
```

* **`git init`** — initializes Git tracking in the current directory [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**What happens internally:** A hidden `.git` directory is created. This contains all versioning infrastructure.

**Verify:**

```bash
ls -a
```

* **`-a`** — show hidden files/directories (those starting with `.`)

**Expected output:** You should see `.git` in the listing. Your shell prompt should also change to show `(master)` — the default branch name. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## Step 4: Create Files and Directories

**What we're doing:** Populating the repository with content to track.

```bash
mkdir Nebula Jupiter Pluto
touch Dutch Saturn pi
touch Jupiter/file1 Pluto/file1 Nebula/file1
```

* Creates three directories and three files in the root
* Creates one file inside each directory to ensure Git tracks them [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Critical rule:** Git tracks **files, not directories**. Empty directories are invisible to Git. Always ensure directories contain at least one file. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## Step 5: Check Repository Status

**What we're doing:** Seeing what Git knows about the current state of changes.

```bash
git status
```

**Expected output:** All files listed as **"untracked files"** in red. Git sees them but is not yet tracking their changes. They will NOT be included in any commit until staged. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## Step 6: Stage All Changes

**What we're doing:** Moving all untracked/modified files into the staging area for the next commit.

```bash
git add .
```

* **`git add`** — stage files for commit
* **`.`** — dot means the current working directory and everything inside it (all files recursively) [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Verify:**

```bash
git status
```

**Expected output:** Files now listed as **"changes to be committed"** in green. They've moved from untracked to staged. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## Step 7: Attempt the First Commit (and Handle the Identity Error)

**What we're doing:** Trying to permanently record the staged changes.

```bash
git commit -m "new files committed"
```

* **`git commit`** — create a new commit from staged changes
* **`-m`** — specify the commit message inline
* **`"new files committed"`** — the descriptive message for this commit [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**What happens:** On the first commit, this **fails with an error** because Git doesn't know who you are. The error message provides the exact commands needed to set your identity. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Fix — set global identity:**

```bash
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"
```

* **`git config`** — modify Git configuration
* **`--global`** — apply to all repositories on this machine (not just the current one)
* **`user.email`** — the email address associated with your commits
* **`user.name`** — the name associated with your commits [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Operational tip:** If you have a GitHub account, use the same email address here — it links your local commits to your GitHub identity. If you don't have one yet, use any email address for now. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Now retry the commit:**

```bash
git commit -m "new files committed"
```

**Expected output:** Success — reports number of files changed (13), insertions (0 — files are empty), deletions (0 — nothing was removed). [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Verify:**

```bash
git status
```

**Expected output:** `nothing to commit, working tree clean` — all changes are committed. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## Step 8: Create the Remote Repository on GitHub

**What we're doing:** Creating the remote counterpart on GitHub to sync with.

1. Open browser → go to **github.com** (sign up if you don't have an account, or log in at `github.com/login`)
2. Click **"New repository"** (or the `+` icon)
3. Enter repository name: **`titan-work`** (same as your local directory name)
4. Choose visibility: **Private** (only you and authorized users can see it) or Public
5. Do NOT add a README file (keep it empty so it matches your local repo state)
6. Click **"Create repository"** [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**What you see after creation:** GitHub shows an empty repository page with setup instructions, including two URLs — **HTTPS** and **SSH**. Copy the **HTTPS URL** for now. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## Step 9: Link Local to Remote and Push

**What we're doing:** Connecting your local repository to the GitHub remote and uploading all commits.

```bash
git remote add origin https://github.com/username/titan-work.git
```

* **`git remote add`** — register a new remote repository
* **`origin`** — the conventional alias name for the primary remote
* **`https://...`** — the HTTPS URL from GitHub [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Verify the remote was added:**

```bash
cat .git/config
```

You should see a new `[remote "origin"]` section with the URL. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Rename branch to match GitHub's convention:**

```bash
git branch -M main
```

* **`git branch -M`** — rename the current branch
* **`main`** — the new name (GitHub expects `main`, not `master`) [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Push everything to remote:**

```bash
git push -u origin main
```

* **`git push`** — upload local commits to the remote
* **`-u`** — set `origin main` as the default upstream (so future pushes can just use `git push`)
* **`origin`** — the remote alias
* **`main`** — the branch to push [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**What happens:** Git connects to GitHub. **Authentication is required** — a browser window or credential prompt appears. Sign in with your GitHub credentials. On Windows, credentials are saved after the first successful authentication. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Verify on GitHub:** Refresh the repository page. You should see all files, directories, the commit message, and the commit timestamp. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## Step 10: Make a Change, Stage, Commit, and Push

**What we're doing:** The standard operational cycle for ongoing work.

**Edit a file:**

```bash
vim Saturn
```

Add some text content (e.g., moon names: Mimas, Dione, Rhea, Hyperion), save and quit (`:wq`). [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Check what changed:**

```bash
git status
```

**Expected output:** The edited file shows as **"modified"**. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Stage → Commit → Push:**

```bash
git add .
git commit -m "Saturn moons"
git push origin main
```

 [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Verify on GitHub:** Refresh the page — the file shows the new commit message. Click on the commit message to see the diff: added lines shown with `+` in green. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Connection to larger flow:** This three-step cycle (`add` → `commit` → `push`) is the fundamental rhythm of all Git-based work.

***

## Step 11: Inspect Commit History and Diffs

**What we're doing:** Examining the version history from the command line.

**Full log:**

```bash
git log
```

Shows all commits: commit ID (full hash), author, date, message. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Compact log:**

```bash
git log --oneline
```

Shows each commit as one line: **short commit ID + message**. Much easier to scan. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**View a specific commit's changes:**

```bash
git show <commit-id>
```

* Use the short commit ID from `--oneline` output
* Shows the diff: lines added (`+`), lines removed (`-`) [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

This produces the same information you see on GitHub when clicking a commit message.

***

## Step 12: Make Further Changes (Add + Remove Lines)

**What we're doing:** Demonstrating that Git tracks both additions and deletions.

```bash
vim Saturn
```

Remove some lines, add new ones, save and quit. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

```bash
git add .
git commit -m "updated Saturn's moon names"
git push origin main
```

**Verify with `git show`:** The diff shows removed lines (`-`) and added lines (`+`). Same view on GitHub. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

## Step 13: Pull Remote Changes to Local

**What we're doing:** Simulating a scenario where someone else (or you via GitHub's web UI) made changes on the remote repository, and you need to sync locally.

**On GitHub:** Navigate to a file (e.g., `Saturn10.py`), click edit, make changes, add a commit message, and click "Commit changes." This creates a new commit on the remote that your local repo doesn't have yet. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**On your local terminal:**

```bash
git pull
```

**What happens:** Git downloads the new commit(s) from the remote and updates your local files. The output shows which files were changed. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

**Verify:**

```bash
cat Saturn10.py
git log
```

The file content reflects the remote changes. `git log` shows the new commit with the remote contributor's details. [\[41-versioning \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/41-versioning.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Architecture

```
LOCAL MACHINE                           REMOTE (GitHub/Bitbucket/CodeCommit)
┌─────────────────────────┐             ┌─────────────────────┐
│  Working Directory      │             │  Remote Repository  │
│  (your files)           │             │  (shared, hosted)   │
│         │               │   push →    │                     │
│         ▼  git add      │ ──────────▶ │  origin/main        │
│  Staging Area           │             │                     │
│         │               │   ← pull    │                     │
│         ▼  git commit   │ ◀────────── │                     │
│  Local Repository       │             │                     │
│  (.git/)                │             │                     │
└─────────────────────────┘             └─────────────────────┘
```

***

## Three-Stage Local Workflow

```
UNTRACKED/MODIFIED  ──git add──▶  STAGED  ──git commit -m ""──▶  COMMITTED
     (red)                        (green)                        (clean)
     
git status reveals current stage
```

***

## Command Flow Map

```
SETUP (once):
  mkdir repo → cd repo → git init → creates .git/
  git config --global user.email "..."
  git config --global user.name "..."

DAILY CYCLE:
  edit files
  git status              → see what changed
  git add .               → stage everything
  git commit -m "msg"     → local commit
  git push origin main    → upload to remote

RECEIVING:
  git pull                → download remote changes

INSPECTION:
  git log                 → full commit history
  git log --oneline       → compact (short ID + message)
  git show <commit-id>    → diff of specific commit
```

***

## Local ↔ Remote Connection

```
TWO PATHS TO CONNECT:

1. Remote already exists:
   git clone <URL>  → downloads everything, remote auto-configured

2. Local already exists:
   Create empty repo on GitHub
   git remote add origin <URL>    → link saved in .git/config
   git branch -M main             → rename master → main
   git push -u origin main        → first push (sets upstream)
```

***

## Git Config Scope

```
--global    → all repos on machine  (user.name, user.email)
(no flag)   → current repo only     (local overrides global)

Stored in: ~/.gitconfig (global) or .git/config (local)
```

***

## Commit Anatomy

```
Commit:
  ├── Commit ID (unique hash, long or short form)
  ├── Author (name + email from git config)
  ├── Date/Time
  ├── Message (-m "...")
  └── Diff (+ added lines, - removed lines)
```

***

## What .git Contains

```
.git/
  ├── all version history
  ├── all commits
  ├── all branch info
  ├── config (remotes, local settings)
  └── everything Git needs to operate

.git exists → directory is a repo
.git deleted → all history lost
```

***

## Git Tracking Rule

```
Git tracks FILES, not DIRECTORIES
Empty directory → invisible to Git
Directory with ≥1 file → tracked
```

***

## Authentication Flow (Push)

```
First git push → GitHub prompts for credentials
  → browser sign-in or username/password
  → credentials saved locally (Windows Credential Manager)
  → subsequent pushes: no prompt
```

***

## GitHub Repo Setup Decisions

```
Visibility:  Public (world-readable) vs Private (auth required)
URL type:    HTTPS (used now) vs SSH (covered later)
README:      optional (displays on repo page)
Name:        match local directory name for clarity
```

***

## Sync Direction Summary

```
LOCAL → REMOTE:   git push origin main    (requires auth)
REMOTE → LOCAL:   git pull                (downloads new commits)

Push after:  local add → commit cycle
Pull when:   remote has commits you don't have locally
```

***

## Inspection Equivalence

```
Command Line                    GitHub Web UI
─────────────────               ──────────────────
git log                    ↔    Commit history page
git log --oneline          ↔    Compact commit list
git show <id>              ↔    Click on commit message
+ lines (added)            ↔    Green highlighted lines
- lines (removed)          ↔    Red highlighted lines
```

***

## Reusable Patterns

```
PATTERN 1: Staging Gate Before Commit
  Changes must pass through an explicit staging step before recording
  Prevents accidental inclusion → enables selective, intentional commits
  → Same pattern: code review before merge, approval before deployment

PATTERN 2: Local-First, Sync-Second
  Full functionality locally (commit, log, show, branch)
  Network only needed for push/pull
  → Same pattern: offline-capable apps, local caches with sync

PATTERN 3: Identity Bound to Every Action
  Every commit permanently records who + when
  Identity configured once, applied automatically
  → Same pattern: audit logs, change management systems, DB transaction logs

PATTERN 4: Alias-Based Remote Reference
  origin = alias for remote URL (stored in .git/config)
  Human-friendly name abstracts infrastructure location
  → Same pattern: DNS names for IPs, service names for endpoints
```

***

This lecture establishes the complete Git operational cycle: init → add → commit → push → pull, plus inspection with log/show. The three-stage local workflow (untracked → staged → committed) and the two-axis sync model (local ↔ remote) are the mental models that everything else in Git builds upon. Next up will likely be **branching, merging, and conflict resolution** — the collaborative dimension of Git. Ready when you are! 🚀

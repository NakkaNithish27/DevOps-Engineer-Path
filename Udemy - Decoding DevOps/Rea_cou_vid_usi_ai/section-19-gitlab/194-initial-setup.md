# 🔧 GitLab Initial Setup — Deep Learning Material

**Source:** *Initial Setup* (GitLab Section, Video Lecture Caption File) [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 GitLab — Standalone vs. SaaS Model

GitLab comes in two deployment models: **standalone** (self-hosted, you install and manage GitLab on your own server) and **SaaS** (Software as a Service, hosted by GitLab at `gitlab.com`). In this course, we use the **SaaS model** — we simply sign up at `gitlab.com` and get a fully managed GitLab instance. No installation, no infrastructure management. We sign in using a Google account, which becomes our GitLab user identity. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

***

## 1.2 The GitLab Hierarchy — Users, Groups, and Projects

GitLab organizes everything into three layers, and understanding their relationships is essential before doing anything on the platform. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

**Users** are individual accounts — the people who log in. When you sign up with your Google account, you become a user. As the person who created the account and the initial group/project, you are the **owner** with full administrative control. You can invite other users and assign them roles: **Guest**, **Developer**, or **Maintainer**, each with increasing levels of permission. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

**Groups** are collections of users and projects. Groups exist to solve the collaboration and access control problem: when a team works together, you need a way to decide who can do what. A group defines the permission boundary. Groups can contain **subgroups**, which allows you to mirror your organizational structure — a top-level group for the entire organization, subgroups for teams, sub-subgroups for sub-teams. This creates a **permission hierarchy** where access control cascades downward. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

**Projects** are the core working unit. A project contains far more than just a code repository. Inside a project you get: the **code repository** (like GitHub), **CI/CD pipelines** (build/test/deploy automation), **issues** (tickets for bug fixes and feature requests — different code changes and testing can be tracked with an issue), **wikis** (documentation with commit history, so you can track changes to documentation the same way you track code changes), and many other tools like package registry, container registry, artifacts, releases, and project-specific settings. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

A project belongs to either a user or a group. In an organizational context, it always belongs to a group. Each project has its own **visibility**: private (only group members), public (anyone on the internet), or internal (only logged-in GitLab users). [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

🔍 **Deep Dive:**
The relationship hierarchy is: **User → logs into → Group → contains → Projects**. Everything you do in this course section (code repository, CI/CD pipelines, variables) happens inside a project. The project lives inside a group. And you, as the user, are the owner of both. This three-layer model (identity → permission boundary → work unit) is a recurring pattern across DevOps platforms — AWS has Users/Groups/Resources, Kubernetes has Users/Namespaces/Resources. The abstraction is the same: who you are → what scope you belong to → what you work on.

***

## 1.3 SSH Key Authentication — How GitLab Trusts Your Machine

When you clone a GitLab repository, GitLab needs to verify that you are who you claim to be. With SSH authentication, this works through a **key pair**: you generate a **private key** (stays on your machine, never shared) and a **public key** (uploaded to your GitLab account). When you attempt to connect, your machine presents the private key, GitLab checks it against the stored public key, and if they match, access is granted. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

The critical concept here is: **authentication is tied to the user, not the project or group**. You add the public key in your **user settings** (not in the project settings or group settings). This means once the key is configured, it authenticates you for **every** project and group your user has access to — you don't need separate keys per project. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

The instructor also mentions **key expiration** — you can set an expiration date on the SSH key in GitLab. After that date, the key becomes invalid and you must add a new one. This is a **key rotation** practice: regularly replacing authentication credentials to limit the window of exposure if a key is compromised.

***

## 1.4 The SSH Config File — Routing Keys to Hosts

When you have multiple SSH keys on your machine (for different services or accounts), the SSH client needs to know **which key to use for which host**. The `~/.ssh/config` file solves this problem. Each entry in this file maps a **host alias** to a specific private key file. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

The instructor creates an entry with a custom host alias: `gitlab.com-devops-with-gitlab`. This alias is not the actual hostname — it's a label that includes the real hostname (`gitlab.com`) with a suffix (`-devops-with-gitlab`) to make it unique. In the config entry, the `IdentityFile` directive points to the specific private key file to use when connecting to this alias. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

When cloning, you modify the SSH URL to replace `gitlab.com` with your alias (`gitlab.com-devops-with-gitlab`). SSH sees this alias, looks it up in the config file, finds the matching entry, reads the `IdentityFile` path, and uses that specific private key to authenticate. This mechanism allows you to have multiple GitLab accounts (or multiple Git services) on the same machine, each using a different key, without conflicts. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

🔍 **Deep Dive:**
The URL modification is the key linkage: the clone URL from GitLab will be something like `git@gitlab.com:HC-Group/vprofile.git`. You change `gitlab.com` to `gitlab.com-devops-with-gitlab`, making it `git@gitlab.com-devops-with-gitlab:HC-Group/vprofile.git`. SSH resolves `gitlab.com-devops-with-gitlab` by looking up the config file entry with that Host name, which tells it: "connect to `gitlab.com` but use this specific private key." The modified URL is stored in the cloned repository's `.git/config` file — so every future git operation (push, pull, fetch) automatically uses the correct key without you needing to specify it again.

***

## 1.5 The Workflow — GitLab Repository as the Destination

The operational goal of this lecture is to get the vprofile source code into a GitLab repository. The source code currently lives on **GitHub** (at `github.com/hkhcoder/vprofile-project`, on the `docker` branch). GitLab is a separate platform with its own repository. We need to **bridge** the two: download the code from GitHub and push it to GitLab. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

The approach is straightforward: clone the empty GitLab repository to your local machine, download the source code from GitHub as a ZIP file, copy the contents into the cloned GitLab repository folder, then commit and push to GitLab. This is not a repository mirror or fork — it's a one-time manual code transfer from one platform to another. After this, all future work happens exclusively in the GitLab repository. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

⚠️ **Expert Note:**
The instructor specifically says to download from the **`docker` branch** on GitHub. Branch selection matters — different branches contain different configurations of the same project (e.g., `awsliftandshift`, `docker`, `local`). The `docker` branch presumably contains Dockerfiles and configurations relevant to the GitLab CI/CD pipeline work that follows in subsequent lectures.

***

## 1.6 VS Code Integration — The Development Environment

After cloning the repository, the instructor opens it in **VS Code** using the command `code .` (which opens VS Code with the current directory as the workspace). VS Code serves as the integrated development environment for editing files and interacting with Git — it has built-in source control features that let you stage, commit, and push changes directly from the UI without using the command line. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

The instructor emphasizes: when opening in VS Code, open the **repository folder** (the cloned `vprofile` folder that contains the `.git` directory), not the parent `gitlab` folder. Opening the correct folder is important because VS Code's Git integration detects the `.git` directory to enable source control features. If you open the parent folder, VS Code won't recognize it as a Git repository.

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are setting up the **complete GitLab development workflow**: creating a GitLab account, establishing SSH-based authentication between our local machine and GitLab, cloning an empty repository, populating it with the vprofile source code from GitHub, and pushing everything to GitLab. After this, we'll have a fully functional GitLab repository with source code, connected to VS Code, ready for CI/CD pipeline work in subsequent lectures. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

***

## Step 1: Sign Up for GitLab with a Google Account

Open your browser. Sign into a Google account (create a new one if needed — the instructor created a fresh Google account for this).

Navigate to **gitlab.com**. Click **Sign in**. Select **Google**. Choose your Google account and click **Continue**. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

A verification code will be sent to your Gmail inbox. Enter the code.

**Complete the onboarding form:**

* Role: `DevOps Engineer`
* Reason: `I want to learn the basics of Git`
* What would you like to do: `Create a new project`
* Who will be using GitLab: `Just me`

Click **Continue**. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

***

## Step 2: Create a Group and Project

GitLab prompts you to create a group and a project during the initial setup.

**Group name:** `HC-Group` (or any name you choose — the instructor changes from the default to `HC-Group`)
**Project name:** `vprofile`

Check the option to **include a getting started README** (this creates an initial README.md file in the repository — we'll replace it later). [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

Click **Create project**.

**What was created:** A user (your Google account) who is the owner of a group (`HC-Group`) containing a project (`vprofile`) with an empty repository (just a README.md). [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

**Verification:** Click the GitLab logo (home page). You should see your group listed. Inside the group, you should see the `vprofile` project. Click on the project — you'll land on the code repository page showing the README.md file.

**Explore (optional):** The instructor recommends pausing to browse the left sidebar: Build (pipelines, jobs, pipeline editor, artifacts), Deploy (releases, package registry, container registry), Settings (general, CI/CD, monitoring, quota limits). No need to understand them now — just note what's available. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

***

## Step 3: Generate SSH Keys on Your Local Machine

Open **Git Bash** (Windows) or **Terminal** (macOS/Linux).

```bash
cd
```

This takes you to your home directory.

```bash
cd .ssh
```

Navigate to the hidden `.ssh` folder (this is where SSH keys and config are stored). [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

```bash
ssh-keygen
```

When prompted for the **file name**, enter a descriptive name:

```
devops-with-gitlab
```

The instructor uses the same name as his Google account for easy identification. You can use any name. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

Press **Enter** through the remaining prompts (passphrase — leave empty for simplicity).

**What was created:** Two files in `~/.ssh/`:

* `devops-with-gitlab` — the **private key** (never share this)
* `devops-with-gitlab.pub` — the **public key** (this goes to GitLab)

***

## Step 4: Configure the SSH Config File

Still in the `~/.ssh/` directory, open the config file:

```bash
vim config
```

(or use any text editor)

Go to the **end of the file** and add this entry:

```
Host gitlab.com-devops-with-gitlab
    HostName gitlab.com
    IdentityFile ~/.ssh/devops-with-gitlab
```

* **`Host gitlab.com-devops-with-gitlab`** — a custom alias. When SSH sees this string as the hostname in a URL, it looks up this config entry. The name includes `gitlab.com` as a base with a suffix for uniqueness. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)
* **`HostName gitlab.com`** — the actual server to connect to (implied from the config structure in the lecture).
* **`IdentityFile ~/.ssh/devops-with-gitlab`** — the path to the private key file to use for this connection.

Save and close the file.

**Why this matters:** When you clone with a URL containing `gitlab.com-devops-with-gitlab`, SSH matches it to this config entry and uses the specified private key. This is the mechanism that links your local machine to your specific GitLab account. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

***

## Step 5: Add the Public Key to GitLab

**Copy the public key content:**

```bash
cat ~/.ssh/devops-with-gitlab.pub
```

Select and copy the entire output (it starts with `ssh-rsa` or `ssh-ed25519` and ends with your identifier). [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

**In GitLab:** Click your **user avatar** (top-left or top-right) → **Preferences** (this is user-level settings, not project settings). In the left sidebar, click **SSH Keys**. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

* Paste the public key content into the key field
* **Title:** `devops-with-gitlab` (or any descriptive name)
* **Expiration date:** Set if desired (good practice for key rotation — after this date, the key becomes invalid and you must add a new one) [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

Click **Add key**.

**Why user settings, not project settings?** Authentication is per-user, not per-project. One key authenticates you for all projects your user can access.

***

## Step 6: Clone the GitLab Repository via SSH

Navigate to your project: **GitLab home → Groups → HC-Group → vprofile project**.

Click the **Clone** dropdown. Select **Clone with SSH**. Copy the SSH URL. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

It will look like: `git@gitlab.com:HC-Group/vprofile.git`

**Before cloning, modify the URL:** Replace `gitlab.com` with the alias from your config file:

```
git@gitlab.com-devops-with-gitlab:HC-Group/vprofile.git
```

**In your terminal, navigate to your chosen location:**

```bash
cd /f/                   # or any drive/location of your choice
mkdir gitlab             # create a working folder
cd gitlab
```

**Clone:**

```bash
git clone git@gitlab.com-devops-with-gitlab:HC-Group/vprofile.git
```

SSH reads the alias `gitlab.com-devops-with-gitlab` → looks up `~/.ssh/config` → finds the matching Host entry → uses the specified private key → authenticates with GitLab → clones the repository. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

**Enter the cloned repository:**

```bash
cd vprofile
```

**Verify the clone:**

```bash
ls -a
```

You should see a `.git` folder — this confirms it's a valid Git repository.

```bash
cat .git/config
```

You should see the remote URL containing your alias (`gitlab.com-devops-with-gitlab`). This URL is stored permanently — every future `git push` and `git pull` uses it automatically. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

**Common mistake:** If the config entry name doesn't match the URL alias exactly, SSH won't find the right key, and authentication will fail with a "Permission denied (publickey)" error. Ensure the `Host` value in `~/.ssh/config` matches exactly what you put in the clone URL.

***

## Step 7: Open the Repository in VS Code

From inside the `vprofile` repository folder:

```bash
code .
```

* `code` — the VS Code command-line launcher
* `.` — opens the current directory as the workspace

Alternatively: Open VS Code manually → **File → Open Folder** → navigate to the `vprofile` repository folder. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

⚠️ **Important:** Open the **repository folder** (`vprofile`), NOT the parent folder (`gitlab`). VS Code needs to see the `.git` directory to enable Git integration features (source control panel, commit/push buttons, branch indicators). [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

***

## Step 8: Download the vprofile Source Code from GitHub

Go to **github.com/hkhcoder/vprofile-project** in your browser. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

**Switch to the `docker` branch** (use the branch dropdown on GitHub).

Click **Code → Download ZIP**. This downloads the entire repository content of the `docker` branch as a ZIP file. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

**Extract the ZIP file.** Open the extracted folder. **Copy all the contents** (files and folders inside the extracted folder).

**Paste into your GitLab repository folder** (the `vprofile` folder you cloned in Step 6). When prompted about `README.md`, choose **Replace** — the GitHub version replaces the GitLab-generated one. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

***

## Step 9: Commit and Push to GitLab

In VS Code, go to the **Source Control** panel (the branch icon in the left sidebar).

You should see all the new files listed as changes. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

1. Click **Commit** (or the checkmark icon)
2. Enter a **commit message** (e.g., "Initial commit")
3. VS Code will first commit all files to the **local repository** — this takes longer than usual because it's committing many files at once
4. Then click **Push** (or VS Code may offer "Commit and Push" as a combined action) [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

**What happens:** The commit creates a snapshot of all files in your local Git repository. The push uploads that snapshot to the remote GitLab repository using the SSH URL stored in `.git/config`, authenticating with the private key via the SSH config entry.

**Verification:** Go to your GitLab project page in the browser. **Refresh the page.** You should see all the vprofile source code in the **main branch** of the GitLab repository. [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

**Connection to the larger flow:** The initial setup is complete. The GitLab repository now contains the vprofile source code. All subsequent lectures will work with this repository — CI/CD pipelines, build automation, and deployments will all originate from this GitLab project.

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## GitLab Hierarchy

```
User (Google account login)
  └─ Owner of →
     Group (HC-Group) ← permission boundary, team container
       └─ Contains →
          Project (vprofile) ← code repo + CI/CD + issues + wikis + settings
```

## User Roles (within a Group)

```
Owner > Maintainer > Developer > Guest
Set by admin/owner per user per group
```

## Project ≠ Repository

```
Project = repository + CI/CD pipelines + issues + wikis
        + package registry + container registry
        + artifacts + releases + settings

Visibility: private | public | internal
```

## Groups → Subgroups (Hierarchy)

```
Organization Group
  ├─ Team A Subgroup
  │    ├─ Sub-team A1
  │    └─ Sub-team A2
  └─ Team B Subgroup

Permissions cascade downward
```

## SSH Authentication Flow

```
LOCAL MACHINE                         GITLAB
─────────────                         ──────
ssh-keygen
  → private key (stays local)
  → public key ──────upload──────→ User Settings → SSH Keys
                                      ↓
git clone/push/pull                   Matches private key
  → SSH reads ~/.ssh/config           against stored public key
  → finds IdentityFile                → access granted ✓
  → presents private key ──────→
```

## SSH Config File Mechanism

```
~/.ssh/config:
  Host gitlab.com-devops-with-gitlab     ← custom alias
    HostName gitlab.com                   ← actual server
    IdentityFile ~/.ssh/devops-with-gitlab ← which private key

Clone URL: git@HC-Group/vprofile.git
                ↑
SSH resolves alias → finds config entry → uses specified key

Multiple accounts? → different aliases + different keys + different config entries
```

## URL Modification Pattern

```
Original (from GitLab):  git@gitlab.com:HC-Group/vprofile.git
Modified (for config):   git@gitlab.com-devops-with-gitlab:HC-Group/vprofile.git
                              ↑ replaced with config alias

Stored in: .git/config → used for ALL future git operations
```

## Key Expiration

```
Set in GitLab when adding public key
After expiry → key invalid → must add new key
Purpose: key rotation (limits compromise window)
```

## Complete Setup Sequence

```
1. Sign up GitLab (Google account) → User created
2. Create Group + Project → empty repo with README
3. Generate SSH keys locally (ssh-keygen → private + public)
4. Configure ~/.ssh/config (alias → key mapping)
5. Add public key to GitLab (User Settings → SSH Keys)
6. Clone GitLab repo (SSH, with modified URL alias)
7. Open in VS Code (code . from repo folder, NOT parent)
8. Download vprofile source from GitHub (docker branch → ZIP)
9. Copy contents into cloned GitLab repo folder
10. Commit + Push from VS Code → code now in GitLab
```

## Source Code Transfer Path

```
GitHub (hkhcoder/vprofile-project, docker branch)
  → Download ZIP
    → Extract → Copy contents
      → Paste into cloned GitLab repo folder
        → Commit + Push
          → GitLab (HC-Group/vprofile, main branch)

One-time transfer, NOT a mirror/fork
All future work → GitLab only
```

## Verification Checkpoints

```
After clone:    ls -a → .git folder exists ✓
                cat .git/config → URL has correct alias ✓

After push:     GitLab browser → refresh → source code visible ✓
                Branch: main ✓

VS Code:        Open REPO folder (with .git), not parent folder
                Source Control panel shows Git integration ✓
```

## Gotchas

```
SSH auth fails ("Permission denied")?
  → Config Host alias ≠ URL alias (must match exactly)
  → Wrong key path in IdentityFile
  → Public key not added to GitLab user settings

VS Code Git not working?
  → Opened parent folder instead of repo folder
  → .git directory not in current workspace root

Wrong source code?
  → Didn't switch to 'docker' branch on GitHub before download
  → Downloaded from wrong branch
```

## Reusable Engineering Patterns

**1. Identity → Scope → Work Unit Hierarchy**

```
GitLab:     User → Group → Project
AWS:        User → Account/OU → Resources
Kubernetes: User → Namespace → Resources
Pattern: who you are → what boundary you're in → what you work on
```

**2. Alias-Based Credential Routing**

```
Multiple identities on one machine?
  → Create unique alias per identity in config
  → Modify connection URL to use alias
  → Config maps alias → specific credential
Same pattern: SSH config, AWS profiles (~/.aws/config), kubeconfig contexts
```

**3. Platform Transfer via Manual Bridge**

```
Source platform (GitHub) → Download artifact
  → Local machine (staging area)
    → Push to destination platform (GitLab)
When no native migration/fork path exists between platforms
```

***

*This completes the full reconstruction. Theory explains the GitLab hierarchy and SSH authentication model. Practical walks through every step from signup to push. The Compression Map enables rapid recall of the setup sequence, the SSH config mechanism, and the identity-routing pattern that applies beyond just GitLab.* [\[194-initial-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/194-initial-setup.txt)

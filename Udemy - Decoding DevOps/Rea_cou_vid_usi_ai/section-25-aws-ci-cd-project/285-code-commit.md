# Bitbucket Repository Setup & Git-to-Git Migration with SSH Authentication

**Source:** Video caption file — *"Code Commit / Bitbucket Repository Setup"* (from an AWS CI/CD course) [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Is Bitbucket and How It Relates to the CI/CD Pipeline

Bitbucket is a **Git repository hosting platform**, functionally equivalent to GitHub. It stores source code in Git repositories with all standard Git capabilities — branches, commits, push, pull, clone, tags, history. The video states explicitly: "This is, again, it's a Git repository, same like GitHub." The underlying Git operations are identical; only the hosting platform differs. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

In the context of this course's AWS CI/CD pipeline, Bitbucket serves as the **source code repository** from which AWS services (specifically AWS CodeBuild, introduced in the next lecture) will fetch source code and build it into an artifact. The choice of Bitbucket over GitHub for this project is a practical decision for the CI/CD pipeline being built — but the concepts apply to any Git hosting platform. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## 1.2 — Bitbucket Organization: Workspaces, Projects, and Repositories

Bitbucket has a three-level organizational hierarchy: [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**Workspace** — The top-level container, similar to a GitHub organization. It holds all your projects and repositories. When you create a Bitbucket account, you must create a workspace first. The workspace name must be **globally unique** — no two Bitbucket users can have the same workspace name. If the name is taken, you get an error and must choose a different one.

**Project** — A grouping within a workspace that organizes related repositories. The video creates a project called `vprofile`.

**Repository** — The actual Git repository that holds source code. The video creates a repository called `vproapp` inside the `vprofile` project. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

The repository is created as **private** — only authenticated users with explicit access can see or interact with it. The video also creates it **completely empty** — no README, no .gitignore — because the plan is to push existing code from GitHub into it. If you include a README or .gitignore during creation, the repository would have an initial commit, which can cause conflicts when pushing existing code with its own history. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## 1.3 — SSH Key-Based Authentication: Why and How

To push code to or pull code from a private Bitbucket repository, you need to **authenticate** — prove that you are authorized to access it. Bitbucket supports multiple authentication methods; this lecture uses **SSH key-based authentication**. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

SSH key authentication uses a **key pair** — a mathematically linked public key and private key:

* The **public key** is stored on the remote platform (Bitbucket, in your account settings).
* The **private key** stays on your local machine and is never shared.

When you try to connect to Bitbucket via SSH, your local machine presents the private key. Bitbucket checks it against the stored public key. If they match (cryptographically), authentication succeeds without any password. This is the same SSH key mechanism used throughout the course for EC2 access, Ansible connectivity, and other SSH-based operations. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

The key pair is generated using the `ssh-keygen` command — the same tool used in previous AWS lectures for creating EC2 key pairs. The difference here is the keys are used for Git authentication to Bitbucket rather than for SSH access to a server. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## 1.4 — The SSH Config File: Routing Authentication Automatically

After generating the key pair and uploading the public key to Bitbucket, there's still a gap: when you run `git push` or `git clone` for a Bitbucket repository, how does your local Git know **which private key to use**? You might have multiple key pairs for different services (one for GitHub, one for Bitbucket, one for AWS). [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

The **SSH config file** (`~/.ssh/config`) solves this by mapping hostnames to authentication settings. The config entry says: "When connecting to `bitbucket.org`, use public key authentication and use this specific private key file." This is automatic routing — once configured, every SSH connection to `bitbucket.org` automatically uses the correct key without you specifying it on each command. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

🔍 **Deep Dive:**
The SSH config file is a general-purpose SSH routing mechanism, not Bitbucket-specific. You can have multiple entries — one for `bitbucket.org`, one for `github.com`, one for your internal servers — each pointing to a different private key. This is how professionals manage authentication across multiple platforms without conflicts. The config file entries consist of: `Host` (the hostname to match), `PreferredAuthentications` (the auth method — `publickey`), and `IdentityFile` (the path to the private key). [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## 1.5 — The Known Hosts File and SSH Fingerprint Verification

When you connect to a remote SSH server for the first time, SSH asks you to verify the server's fingerprint: "Are you sure you want to continue connecting? (yes/no)." When you say yes, the server's fingerprint is saved in `~/.ssh/known_hosts`. On subsequent connections, SSH checks the fingerprint against the stored one — if it matches, the connection proceeds silently; if it doesn't match, SSH warns you of a potential security issue. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

The video encounters a practical problem with this: when running `git clone` for the Bitbucket repository, the command was "stuck at one point" because the fingerprint verification prompt wasn't appearing. The solution is to run `ssh -T git@bitbucket.org` first — this explicitly triggers the prompt, stores the fingerprint, and also serves as a **connectivity test**: "This is also a test to check whether our keys are authenticating or not." The output confirms: "You can use Git to connect to Bitbucket, but the shell access is disabled." Shell access is disabled because Bitbucket only allows Git operations, not interactive shell sessions. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## 1.6 — Git-to-Git Migration: Moving Code Between Hosting Platforms

The core operation of this lecture is **migrating a Git repository from GitHub to Bitbucket** while preserving all history. This is not a file copy — it's a Git-level operation that transfers commits, branches, and tags from one remote to another. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

The conceptual flow: [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

1. **Clone** the source repository (from GitHub) — this brings the entire history to your local machine.
2. **Checkout** every branch you want to migrate — Git only transfers branches that have been checked out locally. Branches that exist only on the remote and haven't been checked out locally will not be pushed.
3. **Fetch tags** — tags are not automatically included in a clone's push; they must be explicitly fetched.
4. **Remove** the old remote URL (GitHub) — disconnect from the source.
5. **Add** the new remote URL (Bitbucket) — point to the target.
6. **Push all branches** — send everything to the new remote.

The critical insight about branch selection: "Whatever branches you want to migrate, you need to do this checkout. You need to check out to those branches, and those branches only will be moved." The video runs `git branch -a` to show all available branches but only checks out `main` and `aws-ci` — only these two are migrated. This is **selective migration** — you choose exactly what goes to the target repository. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## 1.7 — Git Remotes: The `origin` Concept

A Git **remote** is a reference to a remote repository — a name that maps to a URL. By convention, the default remote is called `origin`. When you clone a repository, Git automatically creates a remote named `origin` pointing to the URL you cloned from. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

The `.git/config` file inside any Git repository stores this remote configuration. The video shows this file multiple times:

* After cloning from GitHub: `.git/config` shows `origin` pointing to `github.com/...`
* After `git remote rm origin`: the remote section is gone completely.
* After `git remote add origin <bitbucket-url>`: `.git/config` shows `origin` pointing to `bitbucket.org/...` [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

This demonstrates that `origin` is just a label — it can be changed, removed, and re-added. The migration process is essentially: remove the old origin, add a new origin, and push. The code and history stay intact on your local machine throughout; only the remote pointer changes. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up a Bitbucket repository, configuring SSH key-based authentication from our local machine to Bitbucket, and migrating the vProfile project source code from GitHub to this Bitbucket repository — preserving all commit history, selected branches, and tags. The final outcome: the vProfile source code exists in a private Bitbucket repository (with `main` and `aws-ci` branches), authenticated via SSH keys, ready for AWS CodeBuild to use in the next lecture. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## Execution Flow Overview

```
Phase 1: Bitbucket Account & Repository Setup
Phase 2: SSH Key Generation & Authentication Setup
Phase 3: Connectivity Test
Phase 4: Clone Test (empty repo)
Phase 5: Migration — GitHub → Bitbucket
```

***

### Phase 1: Bitbucket Account & Repository Setup

***

#### Step 1: Create Bitbucket Account

1. Sign into your Google account in a browser.
2. In another tab, open **bitbucket.org**.
3. Click **Log In** (or **Get It Free**).
4. Select **Google** as the sign-in method → select your Google account.
5. Bitbucket presents a window to create an account → click **Create Account**. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

#### Step 2: Create a Workspace

1. You'll be prompted to create a **workspace**.
2. Give it a **unique name** (e.g., `AWSCICD45`). The name must be globally unique — if it's taken, you'll get an error. Try a different name until one is accepted. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)
3. Click **Agree and Create Workspace**.

**Common mistake:** Using a generic name like `devops` — likely already taken. Add numbers or unique identifiers to ensure uniqueness. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

#### Step 3: Create a Repository

1. Click **Create Repository**.
2. **Project name:** `vprofile`.
3. **Repository name:** `vproapp`.
4. **Access level:** **Private** repository.
5. **Include a README file:** **No**.
6. **Include a .gitignore:** **No**. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)
7. Click **Create Repository**.

**Why empty:** We're pushing existing code from GitHub. An initial commit (from a README or .gitignore) would conflict with the existing history we're migrating. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**Expected result:** An empty repository with a `main` branch. The page displays the command to add this as a remote URL — note this for later.

***

### Phase 2: SSH Key Generation & Authentication Setup

***

#### Step 4: Generate SSH Key Pair

**Open:** Git Bash (Windows) or Terminal (macOS/Linux).

```bash
ls ~/.ssh/
```

Check for existing keys. If none exist, proceed. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

```bash
cd ~/.ssh/
ssh-keygen
```

**When prompted for the file name/path:** Enter `vprobit_rsa`. Since you're already in `~/.ssh/`, this creates the keys in the correct location. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**When prompted for passphrase:** Press Enter (no passphrase) twice. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

```bash
ls
```

**Expected output:** Two new files — `vprobit_rsa` (private key) and `vprobit_rsa.pub` (public key). [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

#### Step 5: Copy Public Key to Bitbucket

```bash
cat vprobit_rsa.pub
```

**Copy the entire output** (starts with `ssh-rsa`, ends with your email or hostname). [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**In Bitbucket:**

1. Click the **gear/cog icon** (settings) in the bottom-left.
2. Go to **Personal Bitbucket Settings**.
3. Click **SSH Keys** in the left sidebar.
4. Click **Add Key**.
5. **Label:** Give a descriptive name (e.g., "laptop key").
6. **Key:** Paste the public key content.
7. Click **Add Key**. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**How to verify:** The key appears in the SSH Keys list.

***

#### Step 6: Create SSH Config File

**What we are doing:** Creating a file that tells SSH which private key to use when connecting to `bitbucket.org`.

```bash
vim ~/.ssh/config
```

**File content:**

```
Host bitbucket.org
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/vprobit_rsa
```

 [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**Breakdown:**

* `Host bitbucket.org` — this rule applies only when SSH connects to `bitbucket.org`.
* `PreferredAuthentications publickey` — use key-based auth (not password).
* `IdentityFile ~/.ssh/vprobit_rsa` — path to the **private** key (not `.pub`). SSH uses the private key locally; Bitbucket verifies it against the stored public key.

**Save and exit:** `:wq` in vim. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**The instructor notes this content will be available in the lecture resources** for copy-pasting.

***

### Phase 3: Connectivity Test

***

#### Step 7: Test SSH Authentication to Bitbucket

**What we are doing:** Verifying that SSH key authentication works and storing Bitbucket's host fingerprint.

```bash
ssh -T git@bitbucket.org
```

**Breakdown:**

* `ssh` — the SSH client.
* `-T` — disable pseudo-terminal allocation (we don't need an interactive shell, just a test).
* `git@bitbucket.org` — connect as user `git` to `bitbucket.org`. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**First-time prompt:** "Are you sure you want to continue connecting? (yes/no)" → type `yes`. This stores Bitbucket's fingerprint in `~/.ssh/known_hosts`. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**Expected output:** A message confirming you can use Git to connect, but shell access is disabled. This is correct — Bitbucket doesn't allow interactive SSH sessions, only Git operations.

**Why this step matters:** The video explains that without this, `git clone` via SSH can get "stuck at one point" because the fingerprint prompt doesn't appear properly during Git operations. Running this command first resolves the issue. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**Failure scenario:** If you see "Permission denied" → the SSH key isn't configured correctly. Check: (1) the public key is correctly pasted in Bitbucket, (2) the config file points to the correct private key path, (3) the private key file has the right permissions.

***

### Phase 4: Clone Test (Empty Repository)

***

#### Step 8: Test-Clone the Empty Bitbucket Repository

**What we are doing:** Verifying that we can clone the Bitbucket repository via SSH.

1. In Bitbucket, navigate to your repository.
2. Click the **Clone** button. Make sure **SSH** is selected (not HTTPS). [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)
3. Copy the clone command.

```bash
cd /tmp
git clone git@bitbucket.org:AWSCICD45/vproapp.git
```

**Expected output:** "Cloning into 'vproapp'... You appear to have cloned an empty repository." This confirms SSH authentication works and the repository is accessible. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**Verification:**

```bash
ls -ltr
```

You should see the `vproapp` directory. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

```bash
cat vproapp/.git/config
```

This shows the remote URL pointing to `bitbucket.org`. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**This was just a test.** The actual migration happens next from a different location.

***

### Phase 5: Migration — GitHub → Bitbucket

***

#### Step 9: Clone the Source Repository from GitHub

**What we are doing:** Getting the vProfile source code from GitHub onto our local machine.

```bash
mkdir -p /d/aws-cicd
cd /d/aws-cicd
```

Choose any location you prefer. The video uses `D:\aws-cicd`. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

Get the HTTPS URL from `github.com/hkhcoder/vprofile-project`:

```bash
git clone https://github.com/hkhcoder/vprofile-project.git
```

```bash
cd vprofile-project
```

 [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**Verify the current remote:**

```bash
cat .git/config
```

The `[remote "origin"]` section shows `github.com`. This is what we'll replace. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

#### Step 10: Checkout Target Branches

**What we are doing:** Making the branches we want to migrate available locally. Only checked-out branches will be pushed to Bitbucket.

```bash
git checkout aws-ci
```

This checks out the `aws-ci` branch. The `main` branch is already checked out by default (it's the default branch). [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**See all available branches:**

```bash
git branch -a
```

This shows many remote branches, but we're only migrating `main` and `aws-ci`. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**Fetch tags (if any):**

```bash
git fetch --tags
```

This ensures any tags in the repository are also available for pushing. The video notes: "We don't have any tags in our repository, but if you have, we can do fetch the tags." [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

#### Step 11: Remove the GitHub Remote

```bash
git remote rm origin
```

**Breakdown:**

* `git remote rm` — removes a remote reference.
* `origin` — the name of the remote to remove (which currently points to GitHub). [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**Verify:**

```bash
cat .git/config
```

The `[remote "origin"]` section should be **completely gone**. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

#### Step 12: Add the Bitbucket Remote

```bash
git remote add origin git@bitbucket.org:AWSCICD45/vproapp.git
```

**Breakdown:**

* `git remote add` — adds a new remote reference.
* `origin` — the name for the remote (convention).
* `git@bitbucket.org:AWSCICD45/vproapp.git` — the SSH URL of your Bitbucket repository. Copy **only the URL** from Bitbucket, not the full `git clone` command. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**Verify:**

```bash
cat .git/config
```

The `[remote "origin"]` section should now show the **Bitbucket URL**. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

#### Step 13: Push All Branches to Bitbucket

```bash
git push origin --all
```

**Breakdown:**

* `git push` — sends local commits to the remote.
* `origin` — the remote to push to (now Bitbucket).
* `--all` — push **all local branches** (both `main` and `aws-ci`). [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**Expected output:** Git shows the push progress for each branch.

**Verify in Bitbucket:** Refresh the repository page. You should see:

* Source code visible on the main page.
* Both branches available: `main` and `aws-ci`. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

**Connection to flow:** The Bitbucket repository now contains the vProfile source code with full history. In the next lecture, AWS CodeBuild will fetch this source code and build it into a deployable artifact. [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    Bitbucket Repository Setup + Git Migration
PURPOSE:  Create private repo on Bitbucket, migrate vProfile code from GitHub
CONTEXT:  Source code setup for AWS CI/CD pipeline (CodeBuild uses this repo next)
```

 [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## Overall Execution Sequence

```
1. Create Bitbucket account (Google sign-in)
2. Create workspace (globally unique name)
3. Create private empty repository (no README, no .gitignore)
4. Generate SSH key pair (ssh-keygen → vprobit_rsa)
5. Upload public key to Bitbucket (Settings → SSH Keys)
6. Create ~/.ssh/config (map bitbucket.org → private key)
7. Test SSH: ssh -T git@bitbucket.org (stores fingerprint + verifies auth)
8. Test clone empty repo from /tmp (verify SSH clone works)
9. Clone vProfile from GitHub (HTTPS)
10. Checkout target branches (main + aws-ci)
11. Fetch tags (git fetch --tags)
12. Remove GitHub remote (git remote rm origin)
13. Add Bitbucket remote (git remote add origin <SSH URL>)
14. Push all branches (git push origin --all)
15. Verify in Bitbucket UI (code + both branches visible)
```

 [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## SSH Authentication Architecture

```
LOCAL MACHINE                          BITBUCKET
─────────────                          ─────────
~/.ssh/vprobit_rsa     (private key)
~/.ssh/vprobit_rsa.pub (public key) ──→ SSH Keys (account settings)
~/.ssh/config          (routing)
~/.ssh/known_hosts     (fingerprint)

FLOW:
  git push origin → SSH connects to bitbucket.org
    → config file says: use vprobit_rsa as identity
      → private key presented → matched against public key on Bitbucket
        → AUTH SUCCESS → Git operation proceeds
```

 [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## SSH Config File

```
~/.ssh/config

Host bitbucket.org
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/vprobit_rsa

EFFECT: Any SSH connection to bitbucket.org auto-uses this private key
PATTERN: One Host block per platform (bitbucket, github, internal servers)
```

 [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## Git Migration Flow (GitHub → Bitbucket)

```
SOURCE: github.com/hkhcoder/vprofile-project
TARGET: bitbucket.org:AWSCICD45/vproapp.git

git clone <GitHub HTTPS URL>           ← get code locally
cd vprofile-project
git checkout aws-ci                    ← select branches to migrate
git fetch --tags                       ← capture tags
git remote rm origin                   ← disconnect from GitHub
git remote add origin <Bitbucket SSH>  ← connect to Bitbucket
git push origin --all                  ← push selected branches

RESULT: Code + history + branches in Bitbucket
```

 [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## Branch Selection Rule

```
git branch -a  → shows ALL remote branches (many)

ONLY branches you git checkout locally will be pushed by --all

CHECKED OUT:     main, aws-ci     → MIGRATED ✅
NOT CHECKED OUT: all others       → NOT MIGRATED ❌

RULE: checkout = select for migration
```

 [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## Remote URL Lifecycle (in .git/config)

```
AFTER CLONE FROM GITHUB:
  [remote "origin"]
    url = https://github.com/hkhcoder/vprofile-project.git

AFTER git remote rm origin:
  (remote section GONE)

AFTER git remote add origin <bitbucket>:
  [remote "origin"]
    url = git@bitbucket.org:AWSCICD45/vproapp.git

VERIFY AT EACH STEP: cat .git/config
```

 [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## Bitbucket Organization Hierarchy

```
Account
  └── Workspace (globally unique name)
        └── Project (e.g., vprofile)
              └── Repository (e.g., vproapp)
                    ├── Branch: main
                    └── Branch: aws-ci

REPOSITORY SETTINGS:
  Access: Private
  Initial content: EMPTY (no README, no .gitignore)
  Why empty: Avoids conflicts when pushing existing code with history
```

 [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## SSH Fingerprint Problem & Solution

```
PROBLEM:
  git clone via SSH gets "stuck" on first connection
  → fingerprint verification prompt not appearing

SOLUTION:
  ssh -T git@bitbucket.org      ← run BEFORE any git clone
  → prompts "Are you sure?" → type yes
  → stores fingerprint in ~/.ssh/known_hosts
  → also verifies: "You can use Git to connect to Bitbucket"

MUST DO: Run this ONCE before first Git SSH operation to Bitbucket
```

 [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## Key Commands Quick Reference

```
COMMAND                              PURPOSE
───────                              ───────
ssh-keygen                           Generate key pair
cat ~/.ssh/vprobit_rsa.pub           View public key (for Bitbucket)
ssh -T git@bitbucket.org             Test auth + store fingerprint
git clone <URL>                      Clone repository
git checkout <branch>                Select branch for migration
git fetch --tags                     Fetch all tags
git branch -a                        List all branches (local + remote)
git remote rm origin                 Remove current remote URL
git remote add origin <URL>          Add new remote URL
git push origin --all                Push all local branches to remote
cat .git/config                      Verify remote URL configuration
```

 [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## Reusable Engineering Patterns

| Pattern                              | Manifestation                                                                               |
| ------------------------------------ | ------------------------------------------------------------------------------------------- |
| **Key-Based Authentication**         | SSH key pair (public on server, private local) — same pattern for EC2, Ansible, Git         |
| **Config-Based Routing**             | `~/.ssh/config` maps hosts to keys — automatic auth routing without per-command flags       |
| **Selective Migration**              | `git checkout` determines which branches migrate — explicit selection, not blanket transfer |
| **Remote Pointer Swap**              | `git remote rm` + `git remote add` = change where code pushes without touching code/history |
| **Pre-Flight Verification**          | `ssh -T` test before real operations — verify auth before attempting data transfer          |
| **Empty Target for Clean Migration** | Create repo without README/.gitignore — prevents merge conflicts with incoming history      |
| **Verification at Each Step**        | `cat .git/config` after each remote change — confirm state before proceeding                |
| **Platform-Agnostic Git**            | Same Git commands work across GitHub, Bitbucket, GitLab — only the remote URL changes       |

 [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## CI/CD Pipeline Position

```
THIS LECTURE                    NEXT LECTURE
───────────                     ────────────
Bitbucket repo created    →    AWS CodeBuild fetches source code
Code migrated from GitHub →    Builds it into artifact
SSH auth configured       →    (AWS uses its own auth to Bitbucket)

PIPELINE FLOW:
  Bitbucket (source) → CodeBuild (build) → [Deploy] → ...
```

 [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

## One-Line System Reconstruction

> **Create a private empty Bitbucket repository (workspace → project → repo, no README), generate SSH keys (`ssh-keygen` → `vprobit_rsa`), upload the public key to Bitbucket account settings, create `~/.ssh/config` mapping `bitbucket.org` to the private key, test with `ssh -T git@bitbucket.org` (stores fingerprint + verifies auth), then migrate code by cloning from GitHub, checking out target branches (`main` + `aws-ci`), removing the GitHub remote (`git remote rm origin`), adding the Bitbucket remote (`git remote add origin <SSH URL>`), and pushing all branches (`git push origin --all`) — setting up the source code repository for the AWS CI/CD pipeline.** [\[285-code-commit \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/285-code-commit.txt)

***

This completes the full reconstruction of the Bitbucket Repository Setup & Git Migration lecture. It establishes the source code repository that feeds the AWS CI/CD pipeline — the next lecture introduces AWS CodeBuild, which fetches code from this Bitbucket repository and builds it into a deployable artifact. Let me know if you'd like any section expanded or adjusted! 🚀

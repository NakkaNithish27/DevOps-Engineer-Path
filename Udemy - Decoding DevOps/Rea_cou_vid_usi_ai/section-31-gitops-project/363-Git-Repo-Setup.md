# 🔐 Git Repository Setup — GitHub SSH Authentication & Multi-Repo Project Structure — Deep Learning Material

**Source:** *Git Repository Setup* (Video Lecture Caption File) + SSH Config Reference File [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt), [\[363.SSHconfig \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363.SSHconfig.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Project Structure — Three Repositories, Three Concerns

This lecture sets up the foundational repository structure for a GitOps-based Kubernetes project. The instructor creates **three separate GitHub repositories**, each with a distinct responsibility: [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

**1. `vprofile-infra`** — contains **Terraform source code** to manage the EKS (Elastic Kubernetes Service) cluster on AWS. This is the infrastructure layer — it defines what the cluster looks like, how many nodes it has, what networking is configured, what IAM roles are needed.

**2. `vprofile-helm`** — contains **Helm charts** for the vprofile application. Helm charts are Kubernetes deployment templates that package all the definition files (Deployments, Services, ConfigMaps, Secrets, Ingress) into a reusable, parameterized format. This is the application deployment layer.

**3. `vprofile-app`** — contains the **application source code** itself. This is the application code layer — the Java source, build files, and everything needed to produce the container image.

This three-repository separation is a deliberate architectural decision. Each repository evolves at its own pace, is managed by different teams (or the same person wearing different hats), and has different deployment triggers. Infrastructure changes don't require application rebuilds. Helm chart changes don't require infrastructure reprovisioning. Application code changes don't require Terraform runs. Each concern is isolated, versioned, and deployable independently. [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

🔍 **Deep Dive:**
This three-repo pattern is a standard GitOps architecture. In a real organization: the platform/infra team owns `vprofile-infra`, the DevOps team owns `vprofile-helm`, and the development team owns `vprofile-app`. CI/CD pipelines on each repo trigger different actions — a push to `vprofile-app` triggers a build and image push, a push to `vprofile-helm` triggers a deployment update, a push to `vprofile-infra` triggers Terraform apply. The repos are coupled by references (the Helm chart references the image tag from `vprofile-app`, the Helm deployment targets the cluster from `vprofile-infra`), not by containing each other's code.

***

## 1.2 SSH Authentication to GitHub — Why and How

All three repositories are created as **Private** repositories. Private repos require authentication for any operation (clone, push, pull). The instructor sets up **SSH key-based authentication** rather than HTTPS with passwords or tokens. [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

SSH authentication uses a **public/private key pair**:

* The **private key** stays on your local machine (never shared, never uploaded)
* The **public key** is uploaded to your GitHub account

When you perform a Git operation (clone, push, pull), Git uses SSH to connect to GitHub. GitHub checks if the connecting machine's private key matches any public key stored in the account. If it matches, access is granted — no username/password prompt needed. [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

The instructor uses a clear analogy (implicit): the public key is like a **lock** you put on your GitHub account ("This is the lock we are putting in our GitHub account"), and the private key is the key that opens that lock. Anyone can see the lock (public key), but only the person with the matching key (private key) can open it.

***

## 1.3 The SSH Config File — Multi-Account and Multi-Key Management

The SSH config file (`~/.ssh/config`) is a configuration file that tells SSH **which private key to use** for which connection. This is important when you have multiple GitHub accounts, multiple keys, or need different authentication for different hosts. [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt), [\[363.SSHconfig \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363.SSHconfig.txt)

The config entry created in this lecture:

```
Host github.com-devops4sure
    HostName github.com
    User git
    IdentityFile ~/.ssh/devops4sure
    IdentitiesOnly yes
```

**Line-by-line meaning:**

* **`Host github.com-devops4sure`** — a custom alias for this connection. This is **not** a real hostname — it's a label you define. When you use `github.com-devops4sure` in a Git URL, SSH matches it to this config block and applies the settings below. [\[363.SSHconfig \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363.SSHconfig.txt)

* **`HostName github.com`** — the actual server to connect to. Regardless of what you put in the `Host` line, SSH connects to `github.com`.

* **`User git`** — the SSH username. For GitHub, this is always `git` (GitHub identifies you by your key, not by a username).

* **`IdentityFile ~/.ssh/devops4sure`** — the path to the **private key** file to use for this connection. This is the key generated by `ssh-keygen`.

* **`IdentitiesOnly yes`** — tells SSH to **only** use the specified identity file, not try other keys from the SSH agent. This prevents authentication confusion when multiple keys are loaded. [\[363.SSHconfig \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363.SSHconfig.txt)

The key mechanism: when you clone a repository, the standard GitHub SSH URL looks like `git@github.com:devops4sure/vprofile-infra.git`. To use the config entry, you modify the URL to `git@github.com-devops4sure:devops4sure/vprofile-infra.git`. SSH sees `github.com-devops4sure`, matches it to the `Host` entry, and uses the specified private key. [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

This is how you handle **multiple GitHub accounts** on the same machine. Each account gets its own key pair and its own config entry with a unique Host alias. Without this, SSH would try the same default key for all GitHub connections, which fails when you have multiple accounts.

***

## 1.4 The Toolchain Prerequisites

The instructor lists the tools needed before starting: [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

* **GitHub account** — to host the repositories
* **VS Code** — the code editor for developing Helm charts and Terraform code
* **Amazon Q extension in VS Code** — an AI coding assistant (signed in with AWS account) for code generation help
* **Git Bash (Windows)** or **Terminal with Git (macOS)** — for command-line Git operations

VS Code with the Amazon Q extension will be used in subsequent lectures to develop the Helm charts with AI-assisted code generation. This lecture only sets up the repositories and authentication — the actual code development comes next. [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

***

## 1.5 Repository Visibility — Why Private

All three repositories are set to **Private**. The instructor makes this choice deliberately (changing visibility each time from the default). In a real project: [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

* Infrastructure code (`vprofile-infra`) should be private because it contains cloud architecture details, IAM configurations, and potentially sensitive infrastructure patterns.
* Helm charts (`vprofile-helm`) should be private because they contain deployment configurations, service names, and internal architecture.
* Application source code (`vprofile-app`) should be private because it's proprietary business logic.

Public repositories are appropriate for open-source projects and learning examples, but production project repositories should always be private.

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are creating three private GitHub repositories for a GitOps project, generating an SSH key pair for authentication, configuring the SSH config file for automatic key selection, uploading the public key to GitHub, and cloning all three repositories to a local working directory. After this, the repositories are ready for Helm chart development in the next lecture. [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

***

## Step 1: Create the Three GitHub Repositories

Log into your GitHub account. For each repository:

Click **New** (or the `+` icon → New repository). [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

**Repository 1:**

| Setting    | Value                                          |
| ---------- | ---------------------------------------------- |
| Name       | `vprofile-infra`                               |
| Visibility | **Private**                                    |
| README     | Don't add (will be generated with source code) |
| .gitignore | Don't add                                      |

Click **Create repository**.

**Repository 2:**

| Setting    | Value           |
| ---------- | --------------- |
| Name       | `vprofile-helm` |
| Visibility | **Private**     |

Click **Create repository**.

**Repository 3:**

| Setting    | Value          |
| ---------- | -------------- |
| Name       | `vprofile-app` |
| Visibility | **Private**    |

Click **Create repository**. [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

**After this step:** Three empty private repositories exist on GitHub.

***

## Step 2: Generate an SSH Key Pair

Open **Git Bash** (Windows) or **Terminal** (macOS).

Navigate to the SSH directory:

```bash
cd
cd .ssh/
```

* `cd` alone → takes you to your home folder (`~`)
* `cd .ssh/` → enters the SSH configuration directory

Generate the key pair: [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

```bash
ssh-keygen
```

When prompted for the filename, enter **your GitHub account name** (e.g., `devops4sure`). This creates a key pair specific to this account.

Press **Enter** twice to skip the passphrase (no passphrase for convenience).

**Verify:**

```bash
ls
```

You should see two files: [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

* `devops4sure` — the **private key** (stays on your machine, never shared)
* `devops4sure.pub` — the **public key** (will be uploaded to GitHub)

***

## Step 3: Configure the SSH Config File

```bash
vim config
```

Add the following entry (available in lecture resources): [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt), [\[363.SSHconfig \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363.SSHconfig.txt)

```
Host github.com-devops4sure
    HostName github.com
    User git
    IdentityFile ~/.ssh/devops4sure
    IdentitiesOnly yes
```

**Replace `devops4sure` with your GitHub account name** in three places:

1. The `Host` line after the hyphen: `github.com-<your-account>`
2. The `IdentityFile` path: `~/.ssh/<your-account>`

Save and exit (`:wq`).

**Verify the config:**

```bash
cat ~/.ssh/config
```

Confirm the `Host` line matches `github.com-<your-account>` and the `IdentityFile` points to the correct private key path. [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

**Common mistake:** The `Host` alias must **exactly match** what you use in the Git clone URL later. If the config says `github.com-devops4sure` but you type `github.com-devops` in the URL, SSH won't match the entry and authentication will fail.

***

## Step 4: Upload the Public Key to GitHub

**Display the public key:**

```bash
cat devops4sure.pub
```

**Copy the entire output** — it starts with `ssh-rsa` (or `ssh-ed25519`) and ends with your identifier. [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

**In GitHub:**

1. Go to **Settings** (click your avatar → Settings)
2. Click **SSH and GPG keys** in the left sidebar
3. Click **New SSH key**
4. **Title:** Give a descriptive name (e.g., `my workstation`) — this name is just for your identification, it can be anything
5. **Key:** Paste the public key content
6. Click **Add SSH key**

**⚠️ Critical:** Make sure you paste the **public key** (`.pub` file), not the private key. The instructor warns: "Make sure this is the public key and not the private key." Public keys look like a long single line starting with `ssh-rsa`. Private keys look like multi-line content starting with `-----BEGIN`. [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

***

## Step 5: Clone the Repositories

Navigate to your desired working directory:

```bash
cd
cd ~/Desktop/
mkdir gitops
cd gitops
```

The instructor creates a `gitops` folder on the Desktop as the parent directory for all three repos. [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

**Clone each repository:**

Go to each GitHub repository → click **Code** → select **SSH** (not HTTPS) → copy the URL.

The URL looks like: `git@github.com:devops4sure/vprofile-infra.git`

**Modify the URL** to use the SSH config alias — change `github.com` to `github.com-devops4sure`:

```bash
git clone git@github.com-devops4sure:devops4sure/vprofile-infra.git
```

* `git clone` — copies the remote repository to your local machine
* `git@github.com-devops4sure:` — SSH connection using the config alias (SSH matches `github.com-devops4sure` to the Host entry → uses the correct private key → connects to `github.com`)
* `devops4sure/vprofile-infra.git` — your account name and repository name [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

**Repeat for the other two repositories:**

```bash
git clone git@github.com-devops4sure:devops4sure/vprofile-helm.git
git clone git@github.com-devops4sure:devops4sure/vprofile-app.git
```

**Expected result:** Each clone succeeds without prompting for a password. The SSH key authentication handles it automatically. [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

**If clone fails — troubleshooting:**

```bash
cat ~/.ssh/config
```

Check that the `Host` value in the config matches what you used in the clone URL (after `github.com`). The instructor says: "This should match github.com-, the name you have given should match with this. If that matches, then it is going to use your key." [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

***

## Step 6: Open in VS Code

Navigate into one of the repositories and open it in VS Code:

```bash
cd vprofile-helm
code .
```

* `code .` — opens the current directory in VS Code

Click **"I trust this author"** when prompted. [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt)

**Connection to the flow:** The repositories are now cloned, authenticated, and open in VS Code. The next lecture begins developing Helm charts for the vprofile application inside the `vprofile-helm` repository.

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Three-Repository Architecture

```
vprofile-infra  → Terraform code    → manages EKS cluster (infrastructure)
vprofile-helm   → Helm charts       → K8s deployment templates (deployment)
vprofile-app    → Application source → Java code + Dockerfiles (application)

All PRIVATE repositories
Each evolves independently
Each triggers different CI/CD actions
```

## Separation of Concerns

```
INFRA repo changes  → terraform apply → cluster updated
HELM repo changes   → helm upgrade    → deployment updated
APP repo changes    → docker build    → new image pushed

No cross-contamination between layers
Same pattern as: logic/data separation in Ansible, Terraform, K8s
```

## SSH Authentication Flow

```
ssh-keygen → generates key pair
  ├─ private key: ~/.ssh/devops4sure     (stays local, NEVER shared)
  └─ public key:  ~/.ssh/devops4sure.pub (uploaded to GitHub)

GitHub stores PUBLIC key (the lock)
Your machine uses PRIVATE key (the key)
SSH matches them → access granted (no password needed)
```

## SSH Config File (\~/.ssh/config)

```
Host github.com-devops4sure          ← custom alias (used in clone URL)
    HostName github.com              ← actual server
    User git                         ← always "git" for GitHub
    IdentityFile ~/.ssh/devops4sure  ← which private key to use
    IdentitiesOnly yes               ← don't try other keys

PURPOSE: maps alias → key
  Clone URL uses alias → SSH finds matching Host → uses correct key
```

## URL Transformation for Clone

```
STANDARD GitHub SSH URL:
  git@github.com:devops4sure/vprofile-infra.git

MODIFIED for config alias:
  git@github.com-devops4sure:devops4sure/vprofile-infra.git
       └──────────┬─────────┘
         matches Host in config
         → uses IdentityFile specified

MUST MATCH EXACTLY:
  config Host: github.com-devops4sure
  clone URL:   github.com-devops4sure
  Mismatch → authentication fails
```

## Setup Sequence

```
1. Create 3 repos on GitHub (all Private)
2. cd ~/.ssh/
3. ssh-keygen → name: <github-account-name>
4. vim config → add Host entry
5. cat <name>.pub → copy public key
6. GitHub → Settings → SSH keys → paste public key
7. mkdir ~/Desktop/gitops && cd gitops
8. git clone (3 repos, URL with alias)
9. cd vprofile-helm && code .
```

## Troubleshooting Clone Failure

```
git clone fails → check:
  1. cat ~/.ssh/config → Host alias matches URL?
  2. ls ~/.ssh/ → key files exist?
  3. GitHub → SSH keys → public key added?
  4. Public key (not private key) was uploaded?

Public key: starts with ssh-rsa (one line)
Private key: starts with -----BEGIN (multi-line)
⚠️ NEVER upload private key to GitHub
```

## Prerequisites

```
GitHub account         → host repositories
VS Code               → code editor
Amazon Q extension     → AI coding assistant (signed in with AWS)
Git Bash (Windows)     → command line Git
  or Terminal (macOS)
```

## What Comes Next

```
This lecture: repos + auth + clone       (foundation)
Next lecture: develop Helm charts        (in vprofile-helm)
Later:        Terraform for EKS          (in vprofile-infra)
Later:        CI/CD pipeline             (connecting all three)
```

## Reusable Engineering Patterns

**1. Repository-Per-Concern (GitOps Pattern)**

```
Infrastructure code → separate repo
Deployment config   → separate repo
Application code    → separate repo

Each repo:
  - has its own lifecycle
  - has its own CI/CD pipeline
  - is owned by the relevant team
  - can be versioned independently

Same pattern in:
  Monorepo vs. polyrepo debate
  Microservices (service-per-repo)
  Terraform modules in separate repos
```

**2. SSH Config as Connection Router**

```
Multiple accounts/keys → SSH config maps alias → key

Pattern: configuration-based routing of credentials
  Instead of remembering which key for which service,
  define it once in config → automatic selection

Same concept as:
  AWS CLI profiles (~/.aws/config)
  Kubernetes contexts (~/.kube/config)
  Database connection configs
```

**3. Public Key Infrastructure (Asymmetric Trust)**

```
Generate key pair locally
Upload PUBLIC key to remote service
PRIVATE key authenticates locally

Remote trusts you because:
  your private key matches their stored public key

Same pattern:
  SSH to EC2 (key pair uploaded to AWS)
  SSH to bastion host (key pair in GCP)
  TLS certificates (public/private key pairs)
  GPG signing (commit signing)
```

***

*This completes the full reconstruction. Theory explains the three-repository GitOps architecture and the SSH key authentication mechanism. Practical walks through every step from repository creation to SSH config to cloning. The Compression Map enables instant recall of the URL transformation pattern, the SSH config structure, the troubleshooting flow, and the repository-per-concern architectural pattern that underpins the entire GitOps project.* [\[363-git-re...tory-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363-git-repository-setup.txt), [\[363.SSHconfig \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/363.SSHconfig.txt)

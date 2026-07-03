# 🎓 Build Triggers Introduction (Lecture 182)

**Video Title:** Build Triggers Intro
**Context:** This lecture marks a turning point in the Jenkins series. Up to this point, every pipeline was executed **manually** — by clicking the "Build Now" button. This lecture introduces the concept of **automatic job triggers** — mechanisms that make Jenkins execute jobs without human intervention. It covers the theory of five popular trigger types and then walks through a complete setup of prerequisites (Git repository, SSH authentication, Jenkinsfile, Jenkins pipeline job) that will be used in subsequent lectures to test each trigger. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

***

## 🧠 SECTION 1: THEORY — Deep Learning Mode

***

### 1. The Problem — Manual Execution Doesn't Scale

The instructor opens with a direct framing: **"So far we are running Jenkins job or the pipeline manually. We click on Build Now button, but Jenkins jobs can also execute automatically and there are various triggers which you can use. So you don't need to manually click on a Build Now button."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

This is the foundational problem this entire lecture addresses. In a real CI/CD environment, pipelines must run **without human intervention**. A developer pushes code, and within minutes the pipeline should automatically fetch, build, test, analyze, containerize, and deploy — all triggered by that single push. If someone had to manually log into Jenkins and click "Build Now" every time, it would defeat the entire purpose of automation. Build triggers are the mechanism that makes this possible.

***

### 2. Git Webhooks — The Most Popular Trigger

The instructor calls this **"the most famous one."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**What it is:** A Git webhook is a mechanism where the **Git repository** (e.g., GitHub) actively notifies Jenkins whenever an event occurs — most commonly, a new commit is pushed. GitHub sends an HTTP POST request (called a "JSON payload") to a pre-configured Jenkins URL. When Jenkins receives this request, it triggers the corresponding job.

**How it works internally:** You configure a webhook in your GitHub repository settings by providing Jenkins' URL (typically `http://<jenkins-ip>:8080/github-webhook/`). Whenever a developer pushes a commit, GitHub's servers immediately send a JSON payload to that URL. Jenkins has a listener that receives this payload, identifies which job is associated with that repository, and starts the build. The flow is: **Developer pushes → GitHub detects commit → GitHub sends HTTP POST to Jenkins → Jenkins triggers the job.** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**Why it's the most popular:** It provides **near-instant** feedback. The moment code is pushed, the pipeline starts. There's no delay, no polling interval, no wasted resources checking for changes that don't exist. It's event-driven — Jenkins only runs when there's actually something new to build.

**Where it connects:** This is the trigger mechanism used in most production CI/CD setups. It's the standard way to connect a Git repository to a Jenkins pipeline for automatic execution.

> 🔍 **Deep Dive (Optional):**
> The term "JSON payload" refers to the data GitHub sends in the HTTP POST body. This payload contains details about the commit — who pushed it, which branch, what changed, the commit message, etc. Jenkins can parse this payload to make decisions, such as only triggering for specific branches or ignoring commits that only change documentation files.

***

### 3. Poll SCM — The Opposite of Webhooks

The instructor describes this as **"just the opposite of Git Webhook."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**What it is:** Instead of the Git repository notifying Jenkins (push model), Jenkins itself **periodically checks** the Git repository for new commits (pull model). You configure a polling interval (e.g., every 5 minutes, every minute), and Jenkins checks the repository at that frequency. If it detects a new commit since the last check, it triggers the job.

**How it works internally:** Jenkins stores the last commit hash it processed. At each polling interval, it connects to the Git repository, checks the latest commit hash, and compares it with the stored one. If they differ, there's a new commit, and the job is triggered. If they're the same, Jenkins does nothing and waits for the next interval. The flow is: **Jenkins checks on schedule → Compares commit hashes → If different, triggers job → Stores new hash.** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**The key difference from webhooks:** With webhooks, GitHub tells Jenkins ("Hey, there's a new commit!"). With Poll SCM, Jenkins asks GitHub ("Is there a new commit?") repeatedly. Webhooks are more efficient because they only trigger when needed. Poll SCM wastes resources by checking even when nothing has changed, and it introduces a delay equal to the polling interval.

**Why it still exists:** Not all environments allow incoming webhooks. If Jenkins is behind a strict firewall or on a private network that GitHub cannot reach, webhooks won't work. Poll SCM is the fallback — Jenkins can always make outbound connections to check GitHub, even if GitHub can't reach Jenkins.

> ⚠️ **Expert Note (Optional):**
> Poll SCM at aggressive intervals (e.g., every minute) on many jobs can put significant load on both Jenkins and the Git server. In large organizations with hundreds of jobs, this can cause performance issues. Webhooks are almost always preferred when network architecture allows them.

***

### 4. Scheduled Jobs — The Alarm Clock

The instructor uses a clear analogy: **"Pretty simple. You mention date and time like an alarm clock in cron job format and Jenkins will make sure your job runs at that particular time or in some intervals that you specified."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**What it is:** A scheduled trigger runs a Jenkins job at a **fixed time or interval**, regardless of whether there are any code changes. It's based on a **cron expression** — a standard Unix format for specifying schedules.

**How it works internally:** You configure a cron expression in the job's trigger settings. Jenkins' internal scheduler evaluates this expression and triggers the job when the current time matches. This is completely independent of Git — no commits are checked, no webhooks are received. The job simply runs because the clock says it's time.

**Where it's used:** Scheduled triggers are common for tasks that aren't tied to code changes — nightly builds, periodic integration tests, database backups, cleanup jobs, report generation, security scans, or any recurring maintenance task. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

> 🔍 **Deep Dive (Optional):**
> Jenkins uses a cron-like syntax with five fields: `MINUTE HOUR DAY_OF_MONTH MONTH DAY_OF_WEEK`. For example, `H/15 * * * *` means "every 15 minutes" (the `H` is a Jenkins-specific hash that spreads load across minutes to avoid all jobs firing at exactly the same time). `0 2 * * *` means "every day at 2:00 AM." The cron format is the same concept used in Linux crontab, which is why the instructor calls it "cron job format."

***

### 5. Remote Triggers — The Architect's Tool

The instructor gives this trigger special attention: **"Now this is slightly complicated and most of the people will skip this one, but I think this is one very helpful trigger for DevOps engineer or architect."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**What it is:** A remote trigger allows you to start a Jenkins job by making an **API call** (an HTTP request) to a specific Jenkins URL. This means you can trigger a Jenkins job from **anywhere** — from a shell script, from an Ansible playbook, from another CI/CD system, from a monitoring tool, from a custom application, or from any system that can make HTTP requests. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**How it works internally:** Jenkins provides a URL for each job that can be called with an authentication token. The URL typically looks like `http://<jenkins>/job/<job-name>/build?token=<secret-token>`. You configure the token in the job settings, and anyone (or any system) that knows the URL and the token can trigger the job by making an HTTP GET or POST request to it. The instructor mentions: **"There are tokens and secrets and URL — multiple things go into that, and you get an API call which you can use to trigger your Jenkins job."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**Why it's powerful:** This trigger turns Jenkins into a **callable service**. Instead of Jenkins reacting to Git events or running on a schedule, external systems can orchestrate Jenkins jobs on demand. For example, an Ansible playbook that provisions infrastructure could trigger a Jenkins deployment job after the infrastructure is ready. A monitoring system could trigger a rollback job when it detects an error spike. The possibilities are limitless.

The instructor also reassures: **"Do not worry, I have a piece of document for this one. We'll go through it and we'll set up the trigger."** — indicating this will be covered in detail in a subsequent lecture. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

### 6. Build After Other Projects Are Built — Job Chaining

**What it is:** This trigger links jobs together in a chain. You configure a job to trigger **automatically after another specific job completes**. The instructor explains: **"You just select that after this job is completed, run this particular job. So here trigger is completion of a previous job."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**How it works internally:** In the job's trigger configuration, you specify the name of an upstream job. When that upstream job finishes (successfully, or optionally even on failure/instability), Jenkins automatically starts the downstream job. This creates a dependency chain: Job A finishes → Job B starts → Job B finishes → Job C starts, and so on.

**Where it's used:** This is useful when you have **separate but sequential** jobs — for example, a build job that produces an artifact, followed by a deployment job that takes that artifact and deploys it. Rather than combining everything into one massive pipeline, you keep them as independent jobs and chain them together.

> 🔍 **Deep Dive (Optional):**
> This trigger type can be configured with conditions: trigger only on **stable** (successful) completion, trigger on **unstable** (tests failed but build succeeded), or trigger even on **failure**. This gives you control over whether downstream jobs should proceed when upstream jobs have issues.

***

### 7. The Instructor's Scope Statement

The instructor explicitly sets expectations: **"Now these are some popular triggers, but not all. And of course we cannot cover all the triggers, but I'm sure these triggers are more than enough to set up a proper and successful pipeline."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

This is important context. Jenkins has many more trigger types (e.g., trigger on pull request, trigger from another Jenkins instance, trigger on file system changes), but these five cover the vast majority of real-world use cases. The instructor is being practical — teaching what matters most rather than trying to be exhaustive.

***

### 8. SSH Authentication to GitHub — Why and How It Works

A significant portion of this lecture covers **SSH authentication** between the local machine (and later Jenkins) and GitHub. This is not a trigger concept itself, but it's a **prerequisite** for all the trigger exercises. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**What it is:** SSH (Secure Shell) key-based authentication is a method where you prove your identity using a **key pair** — a private key (kept secret on your machine) and a public key (shared with the server you want to connect to). Instead of typing a username and password every time you interact with GitHub, your SSH client automatically presents the private key, GitHub verifies it against the stored public key, and access is granted.

**How the key pair works:** The `ssh-keygen` command generates two files:

*   **Private key** (`~/.ssh/id_rsa`) — this is your secret. It never leaves your machine. It's long and must never be shared.
*   **Public key** (`~/.ssh/id_rsa.pub`) — this is what you give to servers (GitHub, Jenkins, etc.). It's shorter than the private key.

The instructor emphasizes this distinction multiple times: **"We will take the content of the public key... public key again, and not the private key. Private key is a very long one."** And later, when setting up Jenkins: **"Private key in Jenkins, public key in GitHub."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**The authentication flow:** When you `git clone` (or Jenkins fetches code from) a GitHub repository using an SSH URL, the following happens:

1.  Your SSH client presents the private key.
2.  GitHub checks if the corresponding public key is registered in your account.
3.  If it matches, access is granted without a password.

This is why the public key must be added to your **GitHub account settings** (not repository settings) — it authenticates **you as a user**, not a specific repository. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

### 9. Host Key Verification — The "First Connection" Problem

The instructor introduces a specific error and its solution: **"You may get this error: host key verification failed."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**What this error means:** When any SSH client connects to a server for the first time, it receives the server's **host key** (a fingerprint that uniquely identifies the server). The client asks: "I've never seen this server before. Do you trust this fingerprint? Yes/No?" If you say yes, the fingerprint is stored in `~/.ssh/known_hosts`, and future connections proceed without asking. If the client is configured with **strict host key checking** and there's no stored fingerprint, it **rejects** the connection outright — no prompt, just failure.

**Why this affects Jenkins:** When Jenkins tries to clone a Git repository via SSH, the Jenkins process (running as the `jenkins` user) makes an SSH connection to GitHub's servers. If this is the first time the Jenkins server has connected to GitHub via SSH, and strict host key checking is enabled, the connection fails silently with "host key verification failed." There's no interactive prompt for Jenkins to answer "yes." [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**The solution:** Go to **Manage Jenkins → Security → Configure Global Security → Git Host Key Verification Configuration** and select **"Accept first connection."** This tells Jenkins to automatically accept the host key the first time it connects to a new Git server, just like typing "yes" at an interactive prompt. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

The instructor frames this as a precautionary step: **"This step is a precautionary measure for an error that you may get."** — meaning you might not always see this error (if the host key was already accepted), but configuring this setting prevents it from ever occurring. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

> ⚠️ **Expert Note (Optional):**
> "Accept first connection" is a pragmatic setting for lab and most enterprise environments. It's equivalent to the SSH `StrictHostKeyChecking=accept-new` option — accept on first contact, but alert if the key changes later (which could indicate a man-in-the-middle attack). In highly secure environments, you might instead manually pre-populate the `known_hosts` file with GitHub's official host keys.

***

### 10. Pipeline Script from SCM — The Production-Standard Pattern

The instructor introduces a critical Jenkins concept when creating the job: **"Pipeline script from SCM, source code manager."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

In previous lectures, pipeline code was pasted directly into the Jenkins UI ("Pipeline script" option). This is convenient for learning but **not production-grade**. In real environments, the Jenkinsfile is stored **in the Git repository alongside the application code**. This is the "Pipeline script from SCM" approach.

**Why this matters:** When the Jenkinsfile lives in the repository, it's version-controlled just like the application code. Changes to the pipeline go through the same review process (pull requests, code reviews) as application changes. You can see the pipeline's history, revert changes, and ensure that the pipeline definition matches the code it's building. The instructor explicitly states: **"The point is, we are using Jenkinsfile from our repository. And we are using SSH authentication. Now this is very safe and now very popular method."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**Script Path:** When configuring "Pipeline script from SCM," Jenkins asks for the **Script path** — the location of the Jenkinsfile within the repository. If the Jenkinsfile is in the root directory (top level) of the repository, you simply provide the filename: `Jenkinsfile`. If it were in a subdirectory (e.g., `ci/Jenkinsfile`), you'd provide the relative path. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

***

## ⚙️ SECTION 2: PRACTICAL — Guided Execution Mode

***

### What We Are Building

We are setting up the **complete prerequisite environment** needed to learn and test Jenkins build triggers. This involves four things:

1.  Creating a **private GitHub repository** to hold our Jenkinsfile.
2.  Setting up **SSH authentication** between our local machine and GitHub (and later between Jenkins and GitHub).
3.  Creating a **simple Jenkinsfile**, committing it to the repository.
4.  Creating a **Jenkins pipeline job** that fetches and executes this Jenkinsfile from GitHub using SSH.

**Why it matters:** All trigger types (webhooks, poll SCM, scheduled, remote, job chaining) need a working Jenkins job connected to a Git repository. Without this setup, there's nothing to trigger. This is the foundation that all subsequent trigger lectures will build upon.

**Final outcome:** A Jenkins pipeline job named `build` that successfully clones a private GitHub repository via SSH, reads the Jenkinsfile, and executes a simple echo statement. Once this works, we can attach any trigger to it. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

### Step 1: Create a GitHub Repository

Log into your **GitHub account** and create a new repository. Click the **New** button (typically on the repositories page or the `+` icon in the top-right corner). [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

| Setting             | Value             | Reasoning                                                                                                                                                                       |
| ------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Repository name** | `jenkinstriggers` | Descriptive name for the exercise                                                                                                                                               |
| **Visibility**      | Private           | The instructor chooses private, but notes: "You can use private or public because we are not going to store anything that is really private for us. Just a simple Jenkinsfile." |

Click **Create repository**. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

After creation, GitHub shows the repository page with setup instructions. The key thing to note here is the **SSH URL** — it will look like `git@github.com:<your-username>/jenkinstriggers.git`. The instructor specifically says: **"We will be using the SSH link."** Not HTTPS. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**Connection to overall setup:** This repository will hold the Jenkinsfile that Jenkins fetches and executes. It's also the repository that triggers will monitor for changes.

***

### Step 2: Generate SSH Keys (If Not Already Done)

If you already have SSH keys from a previous section of the course, skip this step. If not, generate them now. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

Open **Git Bash** (on Windows) or **Terminal** (on Mac/Linux) and run:

```bash
ssh-keygen
```

This command generates an SSH key pair. It will ask:

*   **File location** — press Enter to accept the default (`~/.ssh/id_rsa`)
*   **Passphrase** — press Enter for no passphrase (or set one for extra security)

**What it produces:**

*   `~/.ssh/id_rsa` — the **private key** (keep this secret, never share it)
*   `~/.ssh/id_rsa.pub` — the **public key** (this is what you share with GitHub and Jenkins)

The instructor already has keys, so he says: **"I already have the key, so I'm not going to overwrite. I'm just going to say no."** If you don't have keys, just press Enter through all prompts until the keys are generated. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**Verify the keys exist:**

```bash
ls ~/.ssh/
```

You should see `id_rsa` (private) and `id_rsa.pub` (public). [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

### Step 3: Add the Public Key to GitHub

We need to copy the **public** key content and add it to GitHub so that GitHub trusts connections from our machine. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**Copy the public key content:**

```bash
cat ~/.ssh/id_rsa.pub
```

This displays the public key content in the terminal. Select and copy it. The instructor emphasizes: **"Copy the public key... public key again, and not the private key. Private key is a very long one. This is the public key."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**Add it to GitHub:**

1.  Go to your **GitHub account** (not a specific repository).
2.  Click on your **profile icon** → **Settings**. The instructor warns: **"This is the account settings, not the repository settings. So you need to click over here and come to the settings."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)
3.  In the left sidebar, click **SSH and GPG keys**.
4.  Click **New SSH key**.
5.  **Title**: Give it a descriptive name (instructor uses `my laptop`).
6.  **Key**: Paste the public key content.
7.  Click **Add SSH key**. Enter your GitHub password if prompted.

**Expected result:** The public key appears in your SSH keys list. Your machine can now authenticate to GitHub via SSH without a password. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

### Step 4: Clone the Repository Using SSH

Go back to the GitHub repository page. Click the **Code** button and select **SSH** (not HTTPS). Copy the SSH URL. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

In Git Bash or terminal:

```bash
mkdir F:\Gitrepos
cd F:\Gitrepos
git clone git@github.com:<your-username>/jenkinstriggers.git
```

The instructor creates a directory in `F:` drive — you can use any location. When you run `git clone` with an SSH URL for the first time, it may ask: **"Are you sure you want to continue connecting?"** — type `yes` and press Enter. This is the same host key verification concept discussed in the theory section — your SSH client is seeing GitHub's server for the first time. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**Expected result:** The repository is cloned into a local `jenkinstriggers` folder. It's currently empty (except for the hidden `.git` directory).

***

### Step 5: Create the Jenkinsfile

Open any text editor (the instructor uses Sublime Text — you can use VS Code, Vim, Notepad++, or any editor). Create a file with the following content: [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'This message is from the Jenkinsfile'
            }
        }
    }
}
```

This is an intentionally **simple** Jenkinsfile. It defines a pipeline with one stage (`Build`) that does nothing but print a message. The instructor explains: **"We are really not doing any build part over here, we are just using the simple Jenkinsfile."** The purpose is to have a minimal working pipeline so we can focus entirely on **triggers**, not on pipeline logic. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**Save the file** in the cloned repository directory (e.g., `F:\Gitrepos\jenkinstriggers\`) with the exact name:

    Jenkinsfile

**Important:** The filename must be `Jenkinsfile` with a **capital J** and **no file extension**. The instructor encounters a problem where his editor automatically appends `.groovy` — he renames it: **"For some reason it named it as jenkinsfiles.groovy. I'm gonna rename it to just Jenkinsfile."** Make sure to set "File type" to "All files" in the save dialog to prevent your editor from adding an unwanted extension. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

### Step 6: Commit and Push the Jenkinsfile

In Git Bash, navigate to the repository directory and run: [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

```bash
git add .
```

`git add .` stages **all** new and modified files in the current directory for the next commit. The `.` means "everything in the current directory." In our case, this stages the `Jenkinsfile`.

```bash
git commit -m "first commit"
```

`git commit` creates a new commit (a snapshot of the staged changes). `-m "first commit"` provides the commit message inline. Without `-m`, Git would open an editor for you to type the message.

```bash
git push origin master
```

`git push` uploads your local commits to the remote repository (GitHub). `origin` is the default name for the remote repository (GitHub). `master` is the branch name.

**Verify on GitHub:** Go to your GitHub repository page and refresh. You should see the `Jenkinsfile` listed in the repository contents. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

### Step 7: Configure Git Host Key Verification in Jenkins

Before creating the Jenkins job, the instructor takes a **precautionary step** to prevent the "host key verification failed" error. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

In the Jenkins UI:

1.  Go to **Manage Jenkins**.
2.  Under **Security**, click **Configure Global Security** (or just find the security settings).
3.  Scroll down to find **Git Host Key Verification Configuration**.
4.  Select **"Accept first connection"**.
5.  Click **Save** (or **Apply** then **Save**). [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**What this does:** It tells Jenkins to automatically accept the SSH host key from any Git server the first time it connects. This prevents the "host key verification failed" error that would otherwise occur because Jenkins can't interactively answer "yes" to the SSH fingerprint prompt.

The instructor says: **"Remember, whenever you see this error, host key verification, this is the step that you need to take."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

### Step 8: Create the Jenkins Pipeline Job

Go to the Jenkins dashboard. Click **New Item** (or **Create Job**). [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

| Setting  | Value    |
| -------- | -------- |
| **Name** | `build`  |
| **Type** | Pipeline |

Click **OK**. Scroll down to the **Pipeline** section. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

This time, instead of "Pipeline script" (inline code), select **"Pipeline script from SCM"**. This tells Jenkins to fetch the Jenkinsfile from a source code repository rather than reading it from the job configuration.

| Setting            | Value                                                | Explanation                                |
| ------------------ | ---------------------------------------------------- | ------------------------------------------ |
| **SCM**            | Git                                                  | We're using a Git repository               |
| **Repository URL** | `git@github.com:<your-username>/jenkinstriggers.git` | The SSH URL (not HTTPS) copied from GitHub |
| **Branch**         | `*/master`                                           | The branch where our Jenkinsfile lives     |
| **Script Path**    | `Jenkinsfile`                                        | The file name/path within the repository   |

 [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

### Step 9: Add SSH Credentials in Jenkins

When you paste the SSH repository URL, Jenkins will show an error (it can't authenticate yet). Click **Add** → **Jenkins** next to the credentials dropdown. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

A credential form appears:

| Field           | Value                           | Explanation                                                             |
| --------------- | ------------------------------- | ----------------------------------------------------------------------- |
| **Kind**        | `SSH Username with private key` | Because we're using SSH key-based authentication, not username/password |
| **ID**          | `gitsshkey`                     | A unique identifier for this credential in Jenkins                      |
| **Username**    | *(your GitHub username)*        | The GitHub account that owns the repository                             |
| **Private Key** | Enter directly → Add            | We'll paste the private key content directly                            |

**Get the private key content:**

In Git Bash or terminal:

```bash
cat ~/.ssh/id_rsa
```

This displays the **private** key. Copy the entire content — from `-----BEGIN OPENSSH PRIVATE KEY-----` to `-----END OPENSSH PRIVATE KEY-----` (inclusive). The instructor warns: **"Make sure you copied properly. Do not copy any extra characters."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

Paste it into the **Private Key** field in Jenkins and click **Add**.

**The key placement pattern is:**

*   **Public key** → stored in **GitHub** (account settings)
*   **Private key** → stored in **Jenkins** (credentials)

The instructor reiterates this: **"Once again, private key in Jenkins, public key in GitHub."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

Now, back in the job configuration, select the newly created credential (`gitsshkey`) from the **Credentials** dropdown. The instructor notes: **"You see the error just goes away. That means we are authenticated to our repository."** When the error disappears, it confirms Jenkins can successfully connect to the GitHub repository using the SSH key. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

Click **Save**.

***

### Step 10: Test the Pipeline

Click **Build Now** to manually trigger the job. [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

**What happens internally:**

1.  Jenkins uses the stored SSH private key to authenticate with GitHub.
2.  Jenkins clones the `jenkinstriggers` repository (master branch).
3.  Jenkins finds the `Jenkinsfile` at the script path specified (`Jenkinsfile` in the root).
4.  Jenkins parses and executes the pipeline defined in the Jenkinsfile.
5.  The single `Build` stage runs, executing `echo 'This message is from the Jenkinsfile'`.
6.  The job completes successfully.

**Expected result:** A successful build (green checkmark). If you look at the console output, you should see the echo message printed.

The instructor acknowledges: **"That got completed because it's pretty simple. But the code of the pipeline script — that's not the point here. The point is, we are using Jenkinsfile from our repository. And we are using SSH authentication. Now this is very safe and now very popular method."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

### Step 11: Setup Complete — Summary of What Was Accomplished

The instructor recaps the complete setup before closing: [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

1.  ✅ Created a Git repository on GitHub (`jenkinstriggers`, private).
2.  ✅ Set up SSH authentication (public key in GitHub, private key in Jenkins).
3.  ✅ Created and committed a simple Jenkinsfile.
4.  ✅ Created a Jenkins pipeline job (`build`) that fetches the Jenkinsfile from GitHub via SSH.
5.  ✅ Verified the job runs successfully.

**"Now in the next video, we will test our triggers — we'll learn all the different kinds of triggers. So complete this setup and join me in the next lecture."** [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

***

## 🧭 Trigger Types — Quick Reference Map

| Trigger                  | Direction          | Mechanism                 | Best For                         |
| ------------------------ | ------------------ | ------------------------- | -------------------------------- |
| **Git Webhooks**         | GitHub → Jenkins   | HTTP POST on commit       | Real-time CI on every push       |
| **Poll SCM**             | Jenkins → GitHub   | Periodic Git check (cron) | When webhooks aren't possible    |
| **Scheduled Jobs**       | Internal (clock)   | Cron-based timer          | Nightly builds, periodic tasks   |
| **Remote Triggers**      | External → Jenkins | API call with token       | Orchestration from scripts/tools |
| **Build After Projects** | Jenkins → Jenkins  | Job completion event      | Chaining sequential jobs         |

 [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

## 🧭 Authentication Key Placement Map

    ┌────────────────────┐         ┌────────────────────┐
    │     YOUR MACHINE   │         │      GITHUB        │
    │                    │         │                    │
    │  Private Key       │         │  Public Key        │
    │  (~/.ssh/id_rsa)   │───SSH──→│  (Account Settings)│
    │                    │         │                    │
    └────────────────────┘         └────────────────────┘

    ┌────────────────────┐         ┌────────────────────┐
    │     JENKINS        │         │      GITHUB        │
    │                    │         │                    │
    │  Private Key       │         │  Public Key        │
    │  (Credentials:     │───SSH──→│  (Account Settings)│
    │   gitsshkey)       │         │                    │
    └────────────────────┘         └────────────────────┘

The same public key in GitHub serves both connections. The private key exists in two places — on your local machine (for your Git operations) and in Jenkins (for Jenkins' Git operations). [\[182.-Build...gers-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/182.-Build-Triggers-Intro.txt)

***

Would you like me to save this as a downloadable markdown file?

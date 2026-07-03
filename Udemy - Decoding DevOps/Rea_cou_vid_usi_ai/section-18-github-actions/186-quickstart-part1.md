# 🎓 GitHub Actions Quickstart — Part 1 (Lecture 186)

**Video Title:** Quickstart Part 1 — GitHub Actions
**Resource File:** [186. workflow-main-1.yaml](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186.%20workflow-main-1.yaml?EntityRepresentationId=315af583-0cdb-44e9-bcde-ab39c11987f2) (Workflow YAML)
**Context:** This is the first hands-on lecture after the GitHub Actions introduction (Lecture 185). It bridges theory to practice — creating a real repository, setting up SSH authentication, downloading source code, understanding the workflow YAML syntax in detail, writing a two-job workflow, and executing it. This lecture transforms the abstract hierarchy (Workflow → Job → Step → Action) into a concrete, running pipeline. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

***

## 🧠 SECTION 1: THEORY — Deep Learning Mode

***

### 1. The SSH Configuration File — Multi-Key Identity Management

When you have **multiple SSH keys** on one machine (each for a different purpose — one for a personal GitHub account, one for a work account, one for a specific project), SSH doesn't know which key to use for which connection. They all connect to the same host (`github.com`), but each needs a different private key. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

The solution is the **SSH config file** (`~/.ssh/config`). This file lets you create **aliases** for hosts with specific settings. In this lecture, the instructor creates an entry like:

    Host github.com-actions-profile
        HostName github.com
        IdentityFile ~/.ssh/actions-profile

This says: "When I connect to the alias `github.com-actions-profile`, actually connect to `github.com`, but use the specific private key `actions-profile` for authentication." This is why, when cloning, the instructor modifies the SSH URL from `git@github.com:user/repo.git` to `git@github.com-actions-profile:user/repo.git` — the hyphenated alias triggers the config rule to use the correct key. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

> 🔍 **Deep Dive (Optional):**
> Without the config file, SSH defaults to `~/.ssh/id_rsa` for all connections. If you have a key named `actions-profile` instead of `id_rsa`, SSH won't find it automatically. The config file acts as a **routing table for SSH identities** — matching connection destinations to specific keys. The `HostName` field is the actual server address, while `Host` is the alias you use in your commands. SSH resolves the alias through the config file before connecting.

***

### 2. Why Source Code Must Be Cloned Inside the Runner

The instructor addresses a question learners naturally have: **"If you are thinking — here's the source code, and why do I need to clone it? Well, that is because it's not going to be executing here. It's going to create a runner. A runner is like a VM or a container that gets created. And in that, all the steps get executed. So in the runner, it is going to clone the source code."** [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

This is a critical architectural concept. Your GitHub repository **stores** the code, but the code doesn't execute on GitHub's storage servers. When a workflow triggers, GitHub spins up a **runner** — a fresh virtual machine (or container) — in a completely separate environment. This runner starts empty. It has an operating system and some pre-installed tools, but it does **not** have your source code. The very first step in almost every workflow is to **clone the source code into the runner** using the `actions/checkout` action.

This is fundamentally different from Jenkins, where the Jenkins server itself had a persistent workspace, and the code remained there between builds. In GitHub Actions, the runner is **ephemeral** — it's created fresh for each job and destroyed afterward. Nothing persists.

***

### 3. The Workflow YAML Structure — Syntax and Hierarchy

The instructor spends significant time explaining the YAML structure, because getting the indentation wrong is the most common source of errors. The hierarchy is: [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

```yaml
name:          # Workflow name (top level)
on:            # Trigger configuration (same column as name)
  push:        # Trigger type (indented under on)
    branches:  # Branch filter (indented under push)
      - main   # Branch name (list item under branches)
jobs:          # Job definitions (same column as on)
  Build:       # Job name (indented under jobs)
    runs-on:   # Runner selection (indented under job name)
    steps:     # Step list (same column as runs-on)
      - name:  # Step name (list item under steps)
        uses:  # Action reference (same column as name within the step)
```

The instructor repeatedly emphasizes **column alignment**: `on` and `jobs` must be in the **same column**. Within a job, `runs-on` and `steps` must be in the **same column**. Within steps, each step item (prefixed with `-`) must be in the **same column**. The instructor says: **"Please keep in mind this is a YAML format. So everything needs to be structured into the YAML syntax."** [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

> ⚠️ **Expert Note (Optional):**
> YAML uses **spaces only** (never tabs) for indentation. A single misaligned space can cause the entire workflow to fail with a cryptic parse error. Most code editors (like VSCode) have YAML extensions that highlight syntax issues. Always use consistent 2-space indentation for GitHub Actions workflows — this is the community convention.

***

### 4. Triggers (`on:`) — The Three Types Shown

The instructor examines a sample workflow in the GitHub UI and explains three trigger types: [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

**`push`** — The workflow runs whenever a commit is pushed to the specified branches. The `branches` key accepts a **list** (YAML list format with `-` or inline with `[branch1, branch2]`). The instructor demonstrates: **"The square bracket represents a list. You can have multiple branch names also, separated by comma and double quotes."** He shows an example with both `main` and `feature` branches.

**`pull_request`** — The workflow runs when a pull request is opened, updated, or merged targeting the specified branches. The instructor connects this to real-world practice: **"For branches like main, there won't be a direct push. It will be through a pull request. And if the request is approved, then the code will be merged into the main branch."** This is the standard branch protection workflow in professional teams.

**`workflow_dispatch`** — The workflow can be triggered manually from the GitHub UI. The instructor explains: **"Dispatch is for manual. If you want to manually trigger the job, that means you want to just run the workflow."** [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

The instructor notes: **"You might have one or multiple triggers based on your requirement."** — meaning a single workflow can respond to multiple trigger types simultaneously.

***

### 5. `run` vs. `uses` — Two Types of Steps

Within a job's `steps`, there are **two fundamentally different ways** to define what a step does: [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

**`run:`** — Executes a **shell command** directly on the runner. The instructor explains: **"Run means just run the command. So run means echo 'Hello World'. That is going to just run a bash command on the GitHub runner."** This is equivalent to the `sh` step in Jenkins — it runs any command the runner's shell supports.

**`uses:`** — Invokes a **pre-built action** from the GitHub Marketplace. The instructor explains: **"You will be doing many more things apart from just running the command. Like you need to clone the source code. In such cases you have predefined actions in GitHub."** Actions are referenced in the format `owner/action-name@version` — for example, `actions/checkout@v4`. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

This maps to Jenkins:

| GitHub Actions              | Jenkins Equivalent      |
| --------------------------- | ----------------------- |
| `run: mvn install`          | `sh 'mvn install'`      |
| `uses: actions/checkout@v4` | Git plugin / `git` step |

The instructor explicitly draws the parallel: **"Like in Jenkins you have plugins. You can call this as extensions. These are the actions."** [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### 6. `actions/checkout@v4` — The Most Fundamental Action

The instructor navigates to the GitHub Marketplace to show the `checkout` action: **"If you come to github.com/marketplace, you can go to actions, all actions, and you will see here many actions like Super-Linter which is used to do code analysis. You have checkout."** [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

The `checkout` action clones the repository's source code into the runner. The basic usage is simply:

```yaml
- name: Code checkout
  uses: actions/checkout@v4
```

The instructor notes it can accept additional configuration via a `with` block (repository, reference, token, etc.), but: **"Mostly it will be simple like this, because the source code will be in the same place where you're running the GitHub Actions."** — meaning when the workflow is in the same repository as the code, the action automatically knows which repo and branch to check out. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### 7. Default Parallel Execution and the `needs` Keyword

This is one of the most important behavioral differences between GitHub Actions and Jenkins. The instructor states clearly: **"In GitHub Actions, all the jobs run parallelly by default. So if you want it one by one, one at a time, then you need to give this `needs` and you need to give the previous job that you want to run before the current job."** [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

In Jenkins, pipeline stages execute **sequentially** by default — stage 1 finishes, then stage 2 starts. In GitHub Actions, jobs run **in parallel** by default — Build and Testing would start simultaneously. To enforce sequential execution, you use the `needs` keyword:

```yaml
Testing:
    runs-on: ubuntu-latest
    needs: Build
```

This tells GitHub Actions: "Do not start the `Testing` job until the `Build` job completes successfully." The instructor emphasizes: **"Make sure the name matches."** — the value of `needs` must exactly match the job name as defined under `jobs:`. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

> 🔍 **Deep Dive (Optional):**
> Because each job runs on its **own separate runner**, the Testing job does not have access to anything the Build job produced. This is why the Testing job must **also** run `actions/checkout@v4` — it's a fresh machine with no source code. In Jenkins, all stages shared a single workspace, so code checked out in the first stage was available in all subsequent stages. In GitHub Actions, if you need to pass build artifacts between jobs, you must explicitly use artifact upload/download actions.

***

### 8. Pre-Installed Tools on Runners

When writing the `mvn install` command, the instructor makes a notable comment: **"Now this is predefined in this runner, so we don't need to install Maven. But yes, there are GitHub Marketplace actions which you can use to run Maven commands also, but really not required."** [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

GitHub-hosted runners come with a **substantial set of pre-installed software** — Java, Maven, Node.js, Python, Docker, Git, AWS CLI, Azure CLI, and many more. This means for common build tools, you don't need a setup step — you can directly use the tool. This is a significant operational advantage over Jenkins, where you had to manually install every tool on the Jenkins server (or use tool installer plugins).

***

### 9. The Workflow File Location — Convention Enforced by GitHub

The instructor creates the directory structure manually in VSCode: **"Click on new folder and give folder a name `.github`. Make sure the dot comes first. And in that `.github`, create new folder. Name it as `workflows`. And inside the workflows you need to create the file."** [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

The path `.github/workflows/main.yml` is not arbitrary — GitHub **only recognizes** workflow files in the `.github/workflows/` directory. The file can have any name (`main.yml`, `ci.yml`, `deploy.yml`, etc.) as long as it's a valid YAML file in that specific directory. The instructor names it `main.yml` and explains: **"That represents this is the main workflow. By default this will get executed."** [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

***

## ⚙️ SECTION 2: PRACTICAL — Guided Execution Mode

***

### What We Are Building

We are creating a **complete GitHub Actions environment from scratch**: a GitHub repository, SSH authentication, source code, and a two-job workflow that builds and tests a Java application. By the end, pushing a commit to the `main` branch will automatically trigger a workflow that clones the code, runs `mvn install`, then runs `mvn test` and `mvn checkstyle:checkstyle` — all on GitHub-hosted Ubuntu runners.

**Final outcome:** A workflow run visible in the repository's Actions tab, triggered by our commit, executing Build and Testing jobs sequentially. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Step 1: Create a GitHub Repository

Log into GitHub. Click **New** (create repository). [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

| Setting        | Value            |
| -------------- | ---------------- |
| **Name**       | `action-profile` |
| **Visibility** | Private          |

Click **Create repository**. The repository is created empty. Note the **SSH URL** shown on the setup page — you will need it shortly.

***

### Step 2: Generate SSH Keys

Open your terminal (or Git Bash on Windows): [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

```bash
cd ~/.ssh
ssh-keygen
```

When prompted for a filename, the instructor gives a **custom name**: `actions-profile` (not the default `id_rsa`). This is important — naming the key after the project avoids overwriting existing keys for other purposes.

Press Enter through all prompts (no passphrase). Two files are created:

*   `actions-profile` — private key
*   `actions-profile.pub` — public key

***

### Step 3: Configure SSH to Use the Correct Key

Because the key has a custom name (not `id_rsa`), SSH won't automatically find it. We need to tell SSH which key to use for this specific GitHub connection: [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

```bash
vi config
```

Add this block at the end of the file:

    Host github.com-actions-profile
        HostName github.com
        IdentityFile ~/.ssh/actions-profile

Save and quit (`:wq`).

**What this does:** It creates an SSH alias. When you connect to `github.com-actions-profile`, SSH actually connects to `github.com` but uses the `actions-profile` private key for authentication. This is the routing mechanism explained in the Theory section. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Step 4: Add the Public Key to GitHub

Display and copy the public key: [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

```bash
cat actions-profile.pub
```

Copy the output. Then in GitHub:

1.  Click your **profile icon** → **Settings** (account settings, not repository settings — the instructor warns about this).
2.  Go to **SSH and GPG keys**.
3.  Click **New SSH key**.
4.  **Title**: `action-profile`
5.  **Key**: Paste the public key content.
6.  Click **Add SSH key**. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Step 5: Clone the Repository with the Modified SSH URL

Navigate out of the `.ssh` folder and to your desired working directory: [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

```bash
cd ~
cd /f  # or wherever you want to work
```

Now clone — but with a **modified URL**. The standard SSH URL from GitHub looks like:

    git@github.com:username/action-profile.git

You must change it to match the config alias:

```bash
git clone git@github.com-actions-profile:username/action-profile.git
```

The change is inserting `-actions-profile` after `github.com`. This makes SSH match the config entry and use the correct private key. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

```bash
cd action-profile
```

You're now inside the cloned repository. The instructor confirms: **"Now we have successfully cloned and authenticated with our GitHub account."** [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Step 6: Open in VSCode

```bash
code .
```

This opens the current directory in Visual Studio Code. If `code .` doesn't work, open VSCode manually and use File → Open Folder to navigate to the repository directory. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Step 7: Download and Add the vprofile Source Code

The workflow needs actual source code to build. The instructor uses the existing **vprofile-project** from earlier in the course: [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

1.  Open a browser and go to `github.com/hkhcoder/vprofile-project`.
2.  Switch to the **`docker`** branch.
3.  Click the green **Code** dropdown → **Download ZIP**.
4.  Extract the ZIP contents.
5.  Copy **all** the extracted files into your `action-profile` repository folder.

**Verify in VSCode:** You should see the full project structure (source code, `pom.xml`, Docker files, etc.) in the VSCode file explorer. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Step 8: Explore the GitHub Actions UI (Orientation)

Before writing the workflow, the instructor navigates to the **Actions** tab in the GitHub repository to show the UI: [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

*   The Actions tab says **"Build, test, deploy your code"** — confirming its CI/CD purpose.
*   GitHub offers **sample workflows** as starting points.
*   Clicking **Simple Workflow → Configure** shows the file path: `action-profile/.github/workflows/main.yml` — confirming the required directory structure.
*   The sample workflow in the UI demonstrates the YAML syntax with `name`, `on`, `jobs`, `runs-on`, `steps`, `run`, and `uses`.

The instructor uses this UI exploration purely for understanding — we will write our own workflow manually in VSCode. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Step 9: Create the Workflow Directory Structure

In VSCode, at the **top level** of the repository: [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

1.  Create folder: `.github` (dot first)
2.  Inside `.github`, create folder: `workflows`
3.  Inside `workflows`, create file: `main.yml`

The full path is: `.github/workflows/main.yml`

***

### Step 10: Write the Workflow YAML

The instructor writes the workflow step by step. Based on the video content and the resource file ([186. workflow-main-1.yaml](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186.%20workflow-main-1.yaml?EntityRepresentationId=315af583-0cdb-44e9-bcde-ab39c11987f2)), the workflow is: [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186.%20workflow-main-1.yaml)

```yaml
name: Build WF
on:
  push:
    branches:
      - main
jobs:
  Build:
    runs-on: ubuntu-latest
    steps:
      - name: Code checkout
        uses: actions/checkout@v4
      - name: Maven build
        run: mvn install
  Testing:
    runs-on: ubuntu-latest
    needs: Build
    steps:
      - name: Code checkout
        uses: actions/checkout@v4
      - name: Maven test
        run: mvn test
      - name: Checkstyle
        run: mvn checkstyle:checkstyle
```

Let's break down each section:

**`name: Build WF`** — The display name of the workflow. This appears in the Actions tab UI. "WF" is short for "workflow." [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

**`on: push: branches: - main`** — The trigger. This workflow runs when a push (commit) happens on the `main` branch. Only one trigger is used for now. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

**`jobs:`** — Contains two jobs: `Build` and `Testing`.

**Job 1 — `Build`:**

*   `runs-on: ubuntu-latest` — Executes on a GitHub-hosted Ubuntu runner.
*   Step 1: `uses: actions/checkout@v4` — Clones the source code into the runner (because the runner starts empty, as explained in Theory).
*   Step 2: `run: mvn install` — Runs the Maven build command. Maven is pre-installed on the runner. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

**Job 2 — `Testing`:**

*   `runs-on: ubuntu-latest` — Its own separate Ubuntu runner (different machine from Build).
*   `needs: Build` — Waits for the Build job to complete before starting. Without this, it would run in parallel.
*   Step 1: `uses: actions/checkout@v4` — Must clone the source code again (fresh runner, no shared state with Build).
*   Step 2: `run: mvn test` — Runs unit tests.
*   Step 3: `run: mvn checkstyle:checkstyle` — Runs Checkstyle code analysis. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

The instructor summarizes: **"In short, I cloned the source code, I run `mvn install` in the first job. In the second job, I again clone the source code. I run `mvn test` command and I run `mvn checkstyle:checkstyle`."** [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

> ⚠️ **Expert Note (Optional):**
> Notice that `mvn install` is run with no flags (like `-DskipTests`). This means Maven will also run tests during the Build job. Then the Testing job runs `mvn test` again separately. In a real production workflow, you'd typically skip tests in the build stage (`mvn install -DskipTests`) and run them only in the test stage, to avoid duplicate work. The instructor is keeping things simple for this quickstart.

***

### Step 11: Commit and Push to Trigger the Workflow

Save the file (`Ctrl+S`). In VSCode, go to the **Source Control** panel (left sidebar, branch icon). [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

1.  Click the dropdown arrow and select **Commit and Push**.
2.  Enter a commit message: `first test on actions`
3.  Confirm.

This commits all files (source code + workflow YAML) and pushes to the `main` branch on GitHub. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

**What happens immediately:** Because the workflow is triggered `on: push: branches: - main`, and we just pushed to `main`, GitHub automatically detects the workflow file and starts executing it. The instructor confirms: **"As soon as that happens, this will trigger the workflow."** [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Step 12: Verify in the GitHub Actions Tab

Go to the GitHub repository in your browser. Click the **Actions** tab. [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

You should see a workflow run named **"first test on actions"** (the commit message). Click on it to see the jobs (`Build` and `Testing`) and their status. The Build job runs first, and once it completes, the Testing job starts (because of `needs: Build`).

The instructor says: **"Let it complete. And then once this is done, join me in the next lecture."** [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

**Common failure scenarios:**

*   **YAML syntax error** — Incorrect indentation will cause the workflow to fail immediately with a parse error. Check that all indentation uses spaces (not tabs) and alignment is correct.
*   **Branch name mismatch** — If your default branch is `master` instead of `main`, the trigger won't fire. Update the YAML to match your actual branch name.
*   **Maven build failure** — If the source code wasn't copied correctly, `mvn install` will fail because `pom.xml` is missing or incomplete.

***

***

## 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

### Setup Flow

    GitHub Repo (action-profile, private)
        ↓
    SSH Key Pair: ssh-keygen → actions-profile / actions-profile.pub
        ↓
    SSH Config: Host github.com-actions-profile → IdentityFile ~/.ssh/actions-profile
        ↓
    Public key → GitHub account settings → SSH keys
        ↓
    Clone: git@github.com-actions-profile:user/repo.git  (alias triggers config)
        ↓
    VSCode: code .
        ↓
    Source code: vprofile-project (docker branch) → download ZIP → paste into repo

 [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### SSH Multi-Key Routing Pattern

    ~/.ssh/config acts as IDENTITY ROUTER:

      Connection attempt → match Host alias → resolve HostName + IdentityFile
      
      git@github.com-actions-profile:...
           ↓ matches
      Host github.com-actions-profile
           ↓ resolves to
      HostName github.com + IdentityFile ~/.ssh/actions-profile

 [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Workflow File Location (Non-Negotiable)

    <repo-root>/
      └── .github/
            └── workflows/
                  └── main.yml   ← GitHub scans ONLY this path

 [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Workflow Structure — YAML Column Alignment

    name:                          ← col 0
    on:                            ← col 0 (same as name)
      push:                        ← col 2
        branches:                  ← col 4
          - main                   ← col 6 (list item)
    jobs:                          ← col 0 (same as on)
      Build:                       ← col 2
        runs-on: ubuntu-latest     ← col 4
        steps:                     ← col 4 (same as runs-on)
          - name: Step Name        ← col 6 (list item)
            uses: action@version   ← col 8 (within step item)
          - name: Another Step     ← col 6 (same column as first step)
            run: shell command     ← col 8

 [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Step Type Decision

    Need to run a shell command?     → run: <command>
    Need reusable/complex behavior?  → uses: owner/action@version

 [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Job Execution Model

    DEFAULT:  Job A ──┬──→ runs in PARALLEL
              Job B ──┘

    WITH needs:  Job A ──→ Job B (sequential)
                 needs: A

    CRITICAL: Each job = SEPARATE runner = SEPARATE machine
              → No shared filesystem
              → Must re-checkout code in each job
              → Must re-create any state needed

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186.%20workflow-main-1.yaml), [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Runner State Model (vs Jenkins)

    JENKINS:   [Stage 1] → [Stage 2] → [Stage 3]
               ────── same workspace, same machine ──────

    GITHUB ACTIONS:  [Job 1: own runner] ─needs→ [Job 2: own runner]
                      fresh VM              fresh VM
                      no shared files       must checkout again

 [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Actual Workflow Execution Flow

    PUSH to main
      ↓ trigger
    WORKFLOW: Build WF
      │
      ├── JOB: Build [ubuntu-latest]
      │     ├── checkout@v4 (clone source)
      │     └── run: mvn install
      │
      │ ← needs: Build (waits for completion)
      │
      └── JOB: Testing [ubuntu-latest]  (separate runner)
            ├── checkout@v4 (clone source AGAIN)
            ├── run: mvn test
            └── run: mvn checkstyle:checkstyle

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186.%20workflow-main-1.yaml), [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Trigger → Execution Chain

    Developer: git commit + git push (to main)
      ↓
    GitHub: detects push event on main branch
      ↓
    GitHub: finds .github/workflows/main.yml
      ↓
    GitHub: matches on.push.branches includes "main"
      ↓
    GitHub: spins up runner for Build job
      ↓
    Runner: executes steps sequentially
      ↓
    Build completes → needs satisfied → Testing job starts
      ↓
    GitHub: spins up NEW runner for Testing job
      ↓
    Runner: executes steps sequentially
      ↓
    Workflow complete → visible in Actions tab

 [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Pre-Installed Tools Pattern

    GitHub-hosted runner (ubuntu-latest) comes with:
      Maven ✓  Java ✓  Docker ✓  Git ✓  Node ✓  Python ✓  AWS CLI ✓ ...

    → No tool installation steps needed for common tools
    → Unlike Jenkins where every tool was manually installed

 [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Key Verification Checkpoint

    ✅ Repo created (private, action-profile)
    ✅ SSH keys generated (custom name: actions-profile)
    ✅ SSH config maps alias → key
    ✅ Public key in GitHub account settings
    ✅ Clone via modified SSH URL (github.com-actions-profile)
    ✅ Source code (vprofile-project, docker branch) in repo
    ✅ .github/workflows/main.yml created with correct YAML
    ✅ Two jobs: Build (mvn install) → Testing (mvn test, checkstyle)
    ✅ needs: Build enforces sequential execution
    ✅ Commit + push triggers workflow automatically
    ✅ Actions tab shows running/completed workflow

 [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

### Reusable Pattern: Ephemeral Isolated Execution

    PATTERN: Each unit of work gets a clean, isolated, disposable environment

    Applies to:
      - GitHub Actions runners (each job = fresh VM)
      - Docker containers (each container = fresh filesystem)
      - AWS Lambda (each invocation = fresh instance)
      - Kubernetes pods (each pod = fresh container)

    Consequence: NEVER assume state carries over between units
    Solution: Explicitly provision state at the start of each unit
    Example: actions/checkout in EVERY job, not just the first one

 [\[186-quicks...art-part-1 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/186-quickstart-part-1.txt)

***

Would you like me to save this as a downloadable markdown file?

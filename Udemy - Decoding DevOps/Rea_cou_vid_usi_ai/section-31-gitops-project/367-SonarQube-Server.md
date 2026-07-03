# 🎓 GitOps Pipeline: SonarQube Server Setup & Source Code Initialization — Deep Learning Material

**Source:** Video caption file — *SonarQube Server Setup* + `sonar-project.properties` configuration file [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt), [\[367.sonar-...properties \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367.sonar-project.properties.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Where SonarQube Fits in the GitOps Pipeline

In the GitOps pipeline architecture (covered in the previous lecture), the **CI/CD pipeline** is responsible for testing, building, and packaging the application before updating the Helm repository. **SonarQube** is the **code quality and static analysis gate** that sits within the CI pipeline — between the developer's code commit and the Docker image build. Before the application code is packaged into a Docker image and deployed, it must pass quality and security checks. SonarQube performs this analysis. [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

This is the same SonarQube server concept from the Jenkins CI/CD lectures earlier in the course. The difference now: instead of Jenkins triggering the analysis, **GitHub Actions** will upload the analysis results to the SonarQube server. The SonarQube server is a **standalone service** running on its own EC2 instance — external to the Kubernetes cluster. [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

***

## 1.2 — SonarQube Server Architecture: EC2 + User Data

The SonarQube server is deployed on an **EC2 instance** using the same **User Data automation pattern** seen throughout the course. A shell script (`sonar-setup.sh`) is pasted into the EC2 instance's User Data field. When the instance boots, it automatically executes the script, which installs and configures SonarQube without any manual SSH login required. [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

The script comes from the **hkhcoder repository, electron branch** — the same branch used in the Jenkins lectures. This is direct reuse of previously created automation code.

### Instance Sizing Decision

SonarQube requires at least **4 GB of RAM** to run effectively. The instructor explicitly selects **`t2.medium`** instead of the free-tier `t2.micro` for this reason: "Instance type will be bigger, t2.medium. Needs at least four GB of RAM." [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

> ⚠️ **Expert Note:** `t2.medium` is **not free tier** — it incurs charges. The SonarQube server should be terminated after the project is complete to avoid ongoing costs. The instructor also creates a key pair ("it will mostly not be required to log in SSH to the sonar server, but anyways, let's just create it") — showing the defensive practice of always having SSH access even if you don't plan to use it.

***

## 1.3 — SonarQube Security Model: Token Authentication

SonarQube listens on **port 80** (HTTP). The security group allows port 80 from **anywhere** because the GitHub Actions pipeline (which runs on GitHub's infrastructure, not on your AWS network) needs to reach the SonarQube server over the public Internet. [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

The instructor anticipates the security concern: "Don't worry, we have the authentication for SonarQube server with the token. So it's not going to be like anonymous login. It will be with authentication." [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

The authentication mechanism is a **User Token** — a secret string generated inside SonarQube that authenticates API requests. The CI pipeline includes this token when uploading analysis results. Without the token, the SonarQube server rejects the request. The token is stored as a **GitHub Secret** (covered in the next lecture), keeping it out of the source code.

### Token Configuration

The instructor creates the token with:

* **Name:** `actions` (identifies the purpose — GitHub Actions pipeline)
* **Type:** User Token (personal token tied to the admin user)
* **Expiration:** 30 days (after which it must be regenerated) [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

***

## 1.4 — The `sonar-project.properties` File: Externalized Scanner Configuration

In the Jenkins CI/CD lectures, SonarQube scanner configuration was embedded **inside the pipeline itself** (the Jenkinsfile). The instructor explicitly highlights the architectural change: "In previous lectures, we have put all this information in the pipeline itself. This time, we are separating it." [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

The `sonar-project.properties` file is placed at the **root of the application source code repository**. When the SonarQube scanner runs (triggered by the CI pipeline), it automatically reads this file to know what to scan and where to find the analysis inputs.

### Configuration Fields Explained

| Field                                  | Value                           | Purpose                                         |
| -------------------------------------- | ------------------------------- | ----------------------------------------------- |
| `sonar.projectKey`                     | `vprofile-java99`               | Unique identifier for this project in SonarQube |
| `sonar.projectName`                    | `vprofile-java99`               | Display name in SonarQube dashboard             |
| `sonar.projectVersion`                 | `1.0`                           | Version label for the analysis                  |
| `sonar.sources`                        | `src/`                          | Directory containing source code to scan        |
| `sonar.java.binaries`                  | `target/classes`                | Compiled Java classes (produced by Maven build) |
| `sonar.junit.reportsPath`              | `target/surefire-reports/`      | JUnit test results location                     |
| `sonar.coverage.jacoco.xmlReportPaths` | `target/site/jacoco/jacoco.xml` | Code coverage report location                   |
| `sonar.java.checkstyle.reportPaths`    | `target/checkstyle-result.xml`  | Checkstyle analysis report location             |

 [\[367.sonar-...properties \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367.sonar-project.properties.txt)

All `target/` paths are generated by the **Maven build** (`mvn install`). The source code is scanned from `src/`. The scanner combines source analysis with build artifacts and test reports to produce a comprehensive quality report.

> 🔍 **Deep Dive:** Externalizing scanner configuration into `sonar-project.properties` (rather than embedding it in the pipeline) follows the **separation of concerns** principle. The pipeline defines *how* to run the analysis (which commands, which tools). The properties file defines *what* to analyze (which project, which paths, which reports). If the project structure changes (different source path, different report location), only the properties file changes — not the pipeline. If the pipeline technology changes (Jenkins → GitHub Actions → GitLab CI), the properties file remains the same. [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

***

## 1.5 — Application Source Code Initialization

The V-Profile application source code for this GitOps project is initialized by copying files from a previously downloaded repository branch (`vprofile-project-kubeapp`). The files copied are: [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

* **`src/`** — Java application source code
* **`pom.xml`** — Maven build configuration (dependencies, plugins, build lifecycle)
* **`Dockerfile`** — Container image definition (for the CI pipeline to build Docker images later)

These files are placed into the **`vprofile-app`** folder — the application source code repository in the three-repo GitOps architecture. The `sonar-project.properties` file is added at the root level of this same repository.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Building

We're setting up two things: (1) a **SonarQube server** on an EC2 instance for code quality analysis, and (2) **initializing the application source code repository** (`vprofile-app`) with the source code, Dockerfile, Maven config, and SonarQube properties file. The final outcome: a running SonarQube server with an authentication token, and a Git repository ready for the CI pipeline. [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

***

## Phase 1: Initialize the Application Source Code

### Step 1: Open the vprofile-app Folder in VS Code

Open VS Code → **Open Folder** → navigate to `Desktop/gitops/vprofile-app` (or wherever your GitOps project folder is). [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

### Step 2: Copy Source Files from the kubeapp Branch

From the previously downloaded `vprofile-project` repository (branch: `kubeapp`), copy these files/folders into `vprofile-app`: [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

* `src/` — Application source code
* `pom.xml` — Maven build file
* `Dockerfile` — Container image definition

### Verify in VS Code

You should see `src/`, `pom.xml`, and `Dockerfile` in the file explorer. Don't commit yet — we'll add one more file first. [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

***

## Phase 2: Launch the SonarQube EC2 Instance

### Step 3: Get the User Data Script Ready

In a separate browser tab, go to the **hkhcoder repository** on GitHub → switch to the **`electron` branch** → navigate to `userdata/` → open **`sonar-setup.sh`**. Keep this tab open. [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

### Step 4: Launch the EC2 Instance

AWS Console → EC2 → **Launch Instance:**

| Setting        | Value                                           |
| -------------- | ----------------------------------------------- |
| Name           | `SonarServer`                                   |
| AMI            | **Ubuntu** (Ubuntu Server 26, HVM, SSD)         |
| Instance type  | **t2.medium** (⚠️ NOT t2.micro — needs 4GB RAM) |
| Key pair       | Create new: `SonarKey` (.pem)                   |
| Security group | Create new: `sonar-sg`                          |
| Inbound Rule 1 | SSH (22) from **My IP**                         |
| Inbound Rule 2 | HTTP (80) from **Anywhere** (0.0.0.0/0)         |
| User Data      | Paste contents of `sonar-setup.sh`              |

 [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

Click **Launch Instance.**

### Why Port 80 from Anywhere

GitHub Actions runs on GitHub's cloud infrastructure — its IP addresses are dynamic and not in your AWS network. The CI pipeline needs to reach SonarQube over the public Internet on port 80. Token authentication prevents unauthorized access despite the open port. [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

### Wait for Setup

The User Data script installs and configures SonarQube. **Wait approximately 5–10 minutes** for the instance to boot and the script to complete. [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

***

## Phase 3: Configure the SonarQube Server

### Step 5: Access SonarQube

Copy the instance's **Public IP** → open in browser: `http://<PUBLIC_IP>` [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

### Step 6: Log In and Reset Password

| Field    | Value             |
| -------- | ----------------- |
| Username | `admin`           |
| Password | `admin` (default) |

SonarQube forces a **password reset** on first login. Enter old password (`admin`), set a new password. [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

### Step 7: Generate an Authentication Token

1. Click your **Account** icon (top-right) → **My Account**
2. Go to the **Security** tab
3. Under **Tokens**, create a new token:

| Setting    | Value          |
| ---------- | -------------- |
| Name       | `actions`      |
| Type       | **User Token** |
| Expires in | **30 days**    |

 [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

4. Click **Generate**
5. **Copy the token immediately** — it's shown only once
6. Save it in a **sticky note, text editor, or password manager**

### Critical Warning

The token is displayed **once**. If you close or navigate away without copying it, you must generate a new one. This token will be stored as a **GitHub Secret** in the next lecture. [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

***

## Phase 4: Create the sonar-project.properties File

### Step 8: Create the Properties File

In VS Code, create a new file at the **root level** of `vprofile-app/`:

**Filename:** `sonar-project.properties`

### Content:

```properties
sonar.projectKey=vprofile-java99
sonar.projectName=vprofile-java99
sonar.projectVersion=1.0
sonar.sources=src/
sonar.java.binaries=target/classes
sonar.junit.reportsPath=target/surefire-reports/
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
sonar.java.checkstyle.reportPaths=target/checkstyle-result.xml
```

 [\[367.sonar-...properties \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367.sonar-project.properties.txt)

Save the file.

### What Each Line Does (Quick Reference)

* **`projectKey` / `projectName`** — Identifies the project in SonarQube's dashboard
* **`sources=src/`** — Points to the Java source code directory
* **`java.binaries=target/classes`** — Points to compiled classes (Maven produces this)
* **`junit.reportsPath`** — Location of test results (Surefire plugin output)
* **`jacoco.xmlReportPaths`** — Location of code coverage report
* **`checkstyle.reportPaths`** — Location of code style analysis report [\[367.sonar-...properties \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367.sonar-project.properties.txt)

***

## Phase 5: Commit and Push to Git

### Step 9: Commit Everything

Open **Git Bash** or **Terminal** in VS Code. Navigate to the `vprofile-app` folder:

```bash
cd vprofile-app
```

```bash
git add .
```

**Breakdown:** Stage all new and modified files (src/, pom.xml, Dockerfile, sonar-project.properties). [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

```bash
git commit -m "init"
```

**Breakdown:** Create an initial commit with the message "init". [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

```bash
git push origin main
```

**Breakdown:** Push the commit to the `main` branch on the remote repository (GitHub). [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

### Verify

Go to your GitHub repository → you should see all files: `src/`, `pom.xml`, `Dockerfile`, `sonar-project.properties`.

### What We Have Now

| Asset                      | Status      | Location                              |
| -------------------------- | ----------- | ------------------------------------- |
| Application source code    | ✅ Committed | GitHub (vprofile-app repo)            |
| Maven build file (pom.xml) | ✅ Committed | GitHub (vprofile-app repo)            |
| Dockerfile                 | ✅ Committed | GitHub (vprofile-app repo)            |
| SonarQube properties       | ✅ Committed | GitHub (vprofile-app repo)            |
| SonarQube server           | ✅ Running   | EC2 (t2.medium, port 80)              |
| SonarQube token            | ✅ Generated | Saved locally (→ GitHub Secrets next) |

 [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

### Connection to Next Lecture

The next lecture creates the **ECR (Elastic Container Registry) repository** for storing Docker images and sets up **access keys** for authentication. The SonarQube token and ECR credentials will all be stored as **GitHub Secrets** — making them available to the GitHub Actions pipeline without exposing them in the source code. [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 📐 Where SonarQube Fits in the GitOps Pipeline

```
Developer commits code → APPLICATION GIT REPO
       │
       ▼
GitHub Actions CI Pipeline:
  ├── 1. Checkout code
  ├── 2. Maven build (produces target/)
  ├── 3. SONARQUBE ANALYSIS ◄── THIS LECTURE
  │        ├── Reads sonar-project.properties
  │        ├── Sends results to SonarQube server (EC2, port 80)
  │        └── Authenticates with token (GitHub Secret)
  ├── 4. Docker build + push to ECR (next lecture)
  └── 5. Update Helm values in Helm repo
              │
              ▼
       Argo CD syncs to K8s cluster
```

 [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

***

## 🏗️ SonarQube Server Setup

```
EC2 Instance:
  ├── AMI: Ubuntu 26
  ├── Type: t2.medium (4GB RAM minimum)
  ├── Key pair: SonarKey
  ├── Security Group: sonar-sg
  │     ├── SSH (22) from My IP
  │     └── HTTP (80) from Anywhere ← GitHub Actions needs public access
  ├── User Data: sonar-setup.sh (from hkhcoder repo, electron branch)
  └── Boot time: ~5-10 minutes

POST-BOOT:
  http://<PUBLIC_IP>
  ├── Login: admin / admin → reset password
  └── Generate token: Account → Security → Token
        ├── Name: actions
        ├── Type: User Token
        ├── Expires: 30 days
        └── ⚠️ Copy immediately — shown ONCE
```

 [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

***

## 📦 sonar-project.properties Structure

```
sonar.projectKey=vprofile-java99          ← Project identifier
sonar.projectName=vprofile-java99         ← Display name
sonar.projectVersion=1.0                  ← Version label
sonar.sources=src/                        ← Source code location
sonar.java.binaries=target/classes        ← Compiled classes (from mvn)
sonar.junit.reportsPath=target/surefire-reports/        ← Test results
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml  ← Coverage
sonar.java.checkstyle.reportPaths=target/checkstyle-result.xml      ← Style

ALL target/ PATHS = produced by Maven build (mvn install)
FILE LOCATION = root of application repo (vprofile-app/)
```

 [\[367.sonar-...properties \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367.sonar-project.properties.txt)

***

## 🔗 Configuration Separation (Jenkins vs. GitOps)

```
JENKINS CI/CD (previous):
  SonarQube config → INSIDE Jenkinsfile (embedded in pipeline)
  → Pipeline change needed if project structure changes
  → Coupled: pipeline logic + scan config

GITOPS (this project):
  SonarQube config → sonar-project.properties (separate file in repo)
  → Only properties file changes if project structure changes
  → Decoupled: pipeline logic ≠ scan config

PRINCIPLE: Separate WHAT to analyze from HOW to run analysis
```

 [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

***

## ⚡ Complete Execution Sequence

```
 1. Copy src/, pom.xml, Dockerfile → vprofile-app/ folder
 2. Open hkhcoder repo → electron branch → userdata/sonar-setup.sh
 3. EC2 → Launch (Ubuntu, t2.medium, sonar-sg: 22+80, User Data: script)
 4. Wait 5-10 minutes for SonarQube setup
 5. Browser → http://<PUBLIC_IP> → login admin/admin → reset password
 6. Account → Security → Generate token (actions, User Token, 30 days)
 7. ⚠️ COPY TOKEN IMMEDIATELY (shown once)
 8. VS Code → create sonar-project.properties at repo root
 9. git add . → git commit -m "init" → git push origin main
10. NEXT: Create ECR repo + store tokens as GitHub Secrets
```

 [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

***

## 📦 Repository State After This Lecture

```
vprofile-app/ (GitHub, main branch)
  ├── src/                          ← Java source code
  ├── pom.xml                       ← Maven build config
  ├── Dockerfile                    ← Container image definition
  └── sonar-project.properties      ← SonarQube scanner config

EXTERNAL:
  ├── SonarQube server (EC2, t2.medium, port 80)
  ├── SonarQube token (saved locally → GitHub Secrets next)
  └── SonarKey.pem (SSH key, backup access)
```

***

## 🛡️ Security Model

```
SONARQUBE ACCESS:
  Port 80 open to anywhere (GitHub Actions needs it)
  BUT: Token authentication required
  → No token = no access (not anonymous)
  → Token stored as GitHub Secret (not in source code)
  → Token expires in 30 days (must regenerate)

PATTERN: Open port + token auth = accessible by CI + secure
  → Same as: Docker Hub (public API + token),
    API Gateway (public endpoint + API key),
    SaaS webhooks (public URL + shared secret)
```

 [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

***

## 🔄 Reuse from Previous Lectures

```
REUSED COMPONENT             FROM LECTURE            REUSED HOW
──────────────────           ────────────            ──────────
sonar-setup.sh               Jenkins CI/CD           User Data script (identical)
SonarQube config concept     Jenkins CI/CD           Same fields, different location
EC2 + User Data pattern      AWS lectures            Same automation pattern
Security Group setup         AWS lectures            Same SG creation flow
Token authentication         Jenkins CI/CD           Same SonarQube token flow
Source code (src, pom.xml)   V-Profile projects      Same application

NEW IN THIS LECTURE:
  → sonar-project.properties as SEPARATE FILE (not in pipeline)
  → GitHub Actions as CI tool (not Jenkins)
  → GitOps context (SonarQube = quality gate before image build)
```

***

## 🧩 Reusable Engineering Patterns

```
PATTERN 1: EXTERNALIZED CONFIGURATION (Properties File)
  Scanner config IN the repo, not IN the pipeline
  → Pipeline-agnostic: works with Jenkins, GitHub Actions, GitLab CI
  → Same as: application.properties (Spring), .env files (Docker),
    terraform.tfvars (Terraform), values.yaml (Helm)
  → PRINCIPLE: Configuration that describes the PROJECT belongs with the project

PATTERN 2: OPEN PORT + TOKEN AUTHENTICATION
  Public access needed (CI from Internet) + security required
  → Open the port, authenticate with token/secret
  → Same as: API endpoints + API keys, webhook URLs + signatures,
    Docker Hub + access tokens
  → PRINCIPLE: Network openness ≠ security weakness (when auth exists)

PATTERN 3: USER DATA AUTOMATION (Infrastructure Bootstrapping)
  Script in User Data → instance self-configures on boot
  → No SSH needed, no manual setup, repeatable
  → Same pattern used: AWS EC2, GCP startup scripts,
    cloud-init, Vagrant provisioning
  → PRINCIPLE: Servers should configure themselves
```

 [\[367-sonar-...ube-server \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/367-sonar-qube-server.txt)

***

## 🧭 Course Flow Context

```
PREVIOUS  → GitOps Pipeline Introduction (3-layer architecture, Argo CD concept)
THIS      → SonarQube server setup + application source code initialization
NEXT      → ECR repository creation + GitHub Secrets setup
LATER     → GitHub Actions pipeline → Docker build → Helm update → Argo CD deploy

GITOPS PROJECT PROGRESS:
  ✅ Architecture understood (previous lecture)
  ✅ SonarQube server running (this lecture)
  ✅ Application source code committed (this lecture)
  ✅ SonarQube token generated (this lecture)
  ⬜ ECR repository (next lecture)
  ⬜ GitHub Secrets (next lecture)
  ⬜ GitHub Actions pipeline
  ⬜ Helm charts + Argo CD
  ⬜ EKS cluster (Terraform)
```

***

Your SonarQube Server + Source Code Initialization deep learning material is fully reconstructed — covering the SonarQube server setup, the externalized properties file architecture, the token authentication model, and the complete repository initialization workflow. Ready for the next lecture (ECR + GitHub Secrets) or want me to generate **AnkiDeck flashcards (.csv)** from this or the full series? 🃏

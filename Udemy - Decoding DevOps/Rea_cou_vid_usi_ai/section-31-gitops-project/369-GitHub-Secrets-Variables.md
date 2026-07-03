# 🔐 GitHub Secrets and Variables for CI/CD Pipeline — Deep Learning Material

**Source:** Video caption files — [369-github-secrets-and-variables.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt?EntityRepresentationId=c02504a2-55e3-41b8-a48b-0fda132b8991) and [369.SecretsAndVariablesAppRepo.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369.SecretsAndVariablesAppRepo.txt?EntityRepresentationId=8c9ae9d6-4cf0-4644-8210-03502433d953) [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt), [\[369.Secret...lesAppRepo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369.SecretsAndVariablesAppRepo.txt)

**Video Context:** The instructor configures all the **secrets and variables** that the GitHub Actions CI pipeline in the `vprofile-app` repository will need to function. This includes creating a GitHub Personal Access Token (PAT) for cross-repository commits, storing sensitive credentials (AWS keys, Sonar token, Helm repo user, PAT, Slack webhook) as GitHub Secrets, and storing non-sensitive configuration values (AWS region, ECR repository name, Helm repository name) as GitHub Variables. One variable (SonarQube URL) is deferred until the SonarQube server is powered on. This lecture is pure pipeline preparation — no pipeline code is written yet.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Cross-Repository Commit Problem — Why a PAT Is Needed

The instructor opens with a critical architectural point: "At the end of this continuous integration pipeline, it is going to update the `values.yaml` file in another repository, `vprofile-helm` repository." [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

This is the **GitOps bridge**: the CI pipeline runs in the `vprofile-app` repository (triggered by application code changes), but at its final step, it needs to reach into a **different** repository (`vprofile-helm`) and update the Helm chart's `values.yaml` — typically to change the image tag to the newly built version. This cross-repository commit requires **authentication** because the pipeline running in one repository doesn't automatically have write access to another repository.

The solution is a **Personal Access Token (PAT)**: "We are going to create a GitHub token and the username, that is our GitHub account username. These two things it will use to authenticate to this repository and then make a commit." [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

The instructor makes an important distinction about token scope: "For us, both the repository are in the same account, so we can just go to our account and generate a token. But in your case, if you have in your project you're working, and your Helm repository is in a different account, then you need to go to that account and generate the token. Keep in mind, it will be the account where you have the Helm repository." [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

The token must come from the **account that owns the target repository** — the one being written to. This is a common real-world scenario: the application team and the platform/DevOps team may use different GitHub accounts or organizations, and the PAT must be generated from the platform account.

***

## 1.2 Personal Access Token (PAT) — What It Is

A **PAT (Personal Access Token)** is a GitHub-generated credential that acts as a substitute for your password in API and Git operations. It has configurable scopes (permissions) and an expiration date. The instructor creates one with: [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

* **Note:** `gitops-pipeline` (descriptive label for what the token is used for)
* **Expiration:** 30 days
* **Scope:** `Repository` — "because we're going to make commit to the repository"

The Repository scope grants the token permission to read and write to repositories in the account. The instructor navigates: **Settings → Developer Settings → Personal Access Tokens → Tokens (Classic) → Generate New Token (Classic)**. [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

Once generated, the token is shown **only once**: "Keep it in your sticky note or in your text pad, wherever you're saving all these details." If you lose it, you must generate a new one.

***

## 1.3 GitHub Secrets vs. Variables — The Security Boundary

The instructor stores pipeline configuration in two distinct mechanisms, and the distinction is the core teaching point of this lecture: [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

### GitHub Secrets (for sensitive data)

Secrets are **encrypted** values stored in the repository settings that are **never visible** after creation. The instructor demonstrates: "If you click on Edit, then there is no option to see it still. You have to just enter a new value." [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

Secrets are used for credentials that must never be exposed: AWS access keys, tokens, passwords, webhooks. Even if someone has repository access, they cannot view the secret values — they can only replace them.

The instructor warns about accuracy: "Copy everything very carefully because later you cannot view this. You need to just delete it and recreate again if you make any mistakes." [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

### GitHub Variables (for non-sensitive configuration)

Variables are **plaintext** values — visible to anyone with repository access. The instructor shows: "Here, you can see the value of the variable, but if you go to Secrets, you cannot see it." [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

Variables are used for non-sensitive configuration that changes between environments but isn't confidential: region names, repository names, URLs. Exposing these values doesn't create a security risk.

### The Decision Criteria

The instructor applies a clear mental model: **"These are the information that needs to be secret. That's why we store it in Secrets. You cannot accidentally expose it."** For everything else — region, repository names — **"These we can add as variables."** [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

***

## 1.4 The Complete Secrets and Variables Inventory

The lecture defines the full set of credentials and configuration the CI pipeline needs. From the reference file: [\[369.Secret...lesAppRepo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369.SecretsAndVariablesAppRepo.txt)

### Secrets (6 total):

| Secret Name             | What It Holds                             | Why It's Needed                                             |
| ----------------------- | ----------------------------------------- | ----------------------------------------------------------- |
| `AWS_ACCESS_KEY_ID`     | AWS IAM access key                        | Authenticate to AWS for ECR push, EKS access                |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key                        | Paired with access key for AWS authentication               |
| `SONAR_TOKEN`           | SonarQube authentication token            | Authenticate to SonarQube for code quality analysis         |
| `HELM_REPO_USER`        | GitHub account name (e.g., `devops4sure`) | Username for authenticating to the Helm repository          |
| `GITOPS_PAT`            | GitHub Personal Access Token              | Authenticate to `vprofile-helm` repo for cross-repo commits |
| `SLACK_WEBHOOK`         | Slack incoming webhook URL                | Send pipeline notifications to a Slack channel              |

### Variables (4 total):

| Variable Name    | What It Holds                          | Why It's Needed                                           |
| ---------------- | -------------------------------------- | --------------------------------------------------------- |
| `AWS_REGION`     | AWS region (e.g., `us-east-1`)         | Specify which AWS region to operate in                    |
| `ECR_REPOSITORY` | ECR repo name (e.g., `vprofileappimg`) | Identify where to push Docker images                      |
| `HELM_REPO_NAME` | Helm repo name (e.g., `vprofile-helm`) | Identify which repo to update with new image tags         |
| `SONAR_HOST_URL` | SonarQube server URL                   | **Deferred** — will be added when SonarQube server starts |

The instructor notes about the SonarQube URL: "There's also one more variable, but this we are going to define later when we power on our SonarQube server. Because when we power on, we get a new public IP, and that's when we are going to store this into this variable." [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

***

## 1.5 The Naming Contract — Secret/Variable Names Must Match Pipeline Code

The instructor emphasizes naming precision: "It should be exactly this because same we are going to give in our pipeline, `AWS_ACCESS_KEY_ID`." He also states: "I'll put all these names in the lecture resource so you don't make any typos." [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

This is a **name contract** — identical to the Kubernetes Service naming pattern from lecture 353. The GitHub Actions pipeline code will reference secrets using `${{ secrets.AWS_ACCESS_KEY_ID }}` and variables using `${{ vars.AWS_REGION }}`. If the name in the repository settings doesn't exactly match what the pipeline code expects, the value will be empty and the pipeline step will fail. There's no partial matching or fallback — it's an exact string match.

***

## 1.6 Where Secrets and Variables Live — Repository Scope

All secrets and variables are created under the **`vprofile-app` repository** specifically — not at the account level or organization level. The path is: **Repository → Settings → Secrets and Variables → Actions**. [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

The instructor navigates there explicitly: "Go to your repository, app repository, `vprofile-app` repository. We are going to create a continuous integration pipeline on this one. So here, you need to store all these secrets." [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

These secrets are scoped to GitHub Actions workflows in this specific repository. Other repositories cannot access them. This is security-by-scope — each repository only has access to the credentials it needs for its own pipelines.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Setting Up

We are storing all the **credentials and configuration values** that the GitHub Actions CI pipeline (in the `vprofile-app` repository) will need to authenticate to external services (AWS, SonarQube, Slack) and make cross-repository commits (to `vprofile-helm`). The final outcome: 6 secrets and 3 variables (plus 1 deferred) configured and ready for the pipeline to consume. [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

***

## Phase A: Create the GitHub Personal Access Token

### Step A1: Navigate to Token Settings

Go to your **GitHub account** → click your profile icon → **Settings** → scroll to the bottom → **Developer Settings** → **Personal Access Tokens** → **Tokens (Classic)** → **Generate New Token** → **Generate New Token (Classic)**. [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

GitHub may prompt for your password/2FA again for security.

### Step A2: Configure the Token

* **Note:** `gitops-pipeline` (describes the token's purpose)
* **Expiration:** `30 days`
* **Scopes:** Check **`repo`** (Full control of private repositories) [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

Scroll to the bottom → click **Generate Token**.

### Step A3: Save the Token

**Copy the token immediately** and save it somewhere secure (text file, password manager, sticky note). [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

⚠️ **You will never see this token again.** If you navigate away without copying it, you must generate a new one.

Also note down your **GitHub account name** (e.g., `devops4sure`). Both the token and username will be stored as secrets.

***

## Phase B: Store Secrets in the Repository

Navigate to: **`vprofile-app` repository → Settings → Secrets and Variables → Actions → Secrets tab**. [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

### Secret 1: AWS Access Key ID

Click **New Repository Secret**. [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

* **Name:** `AWS_ACCESS_KEY_ID`
* **Value:** Paste your AWS IAM access key ID

Click **Add Secret**.

### Secret 2: AWS Secret Access Key

Click **New Repository Secret**.

* **Name:** `AWS_SECRET_ACCESS_KEY`
* **Value:** Paste your AWS IAM secret access key [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

Click **Add Secret**.

⚠️ **Copy carefully** — you cannot view the value after saving. If you paste incorrectly, you must delete the secret and recreate it.

### Secret 3: SonarQube Token

Click **New Repository Secret**.

* **Name:** `SONAR_TOKEN`
* **Value:** Paste the SonarQube authentication token (generated from SonarQube server in a previous lecture) [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

Click **Add Secret**.

### Secret 4: Helm Repository Username

Click **New Repository Secret**.

* **Name:** `HELM_REPO_USER`
* **Value:** Your GitHub account name (e.g., `devops4sure`) [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

Click **Add Secret**.

**Why this is a secret:** Although a GitHub username is semi-public, storing it as a secret prevents it from appearing in pipeline logs and keeps the authentication pair (user + token) consistently managed.

### Secret 5: GitOps Personal Access Token

Click **New Repository Secret**.

* **Name:** `GITOPS_PAT`
* **Value:** Paste the PAT created in Phase A [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

Click **Add Secret**.

### Secret 6: Slack Webhook

Click **New Repository Secret**.

* **Name:** `SLACK_WEBHOOK`
* **Value:** Paste the Slack incoming webhook URL (set up in a previous lecture) [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

Click **Add Secret**.

### Verification:

You should now see **6 secrets** listed. For each one, the name is visible but the value shows only "Updated X minutes ago" — **you cannot see the actual values**. [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

If you click **Edit** on any secret, there's no way to view the current value — only replace it. This is by design.

***

## Phase C: Store Variables in the Repository

Navigate to: **`vprofile-app` repository → Settings → Secrets and Variables → Actions → Variables tab**. [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

### Variable 1: AWS Region

Click **New Repository Variable**.

* **Name:** `AWS_REGION`
* **Value:** `us-east-1` (or your chosen AWS region) [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

Click **Add Variable**.

### Variable 2: ECR Repository Name

Click **New Repository Variable**.

* **Name:** `ECR_REPOSITORY`
* **Value:** `vprofileappimg` (the ECR repository name — the instructor says "I told you to keep the same") [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

Click **Add Variable**.

### Variable 3: Helm Repository Name

Click **New Repository Variable**.

* **Name:** `HELM_REPO_NAME`
* **Value:** `vprofile-helm` [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

Click **Add Variable**.

### Variable 4: SonarQube Host URL (DEFERRED)

**Do NOT create this now.** This variable (`SONAR_HOST_URL`) will be added later when the SonarQube server is powered on and its public IP is known. [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

### Verification:

You should see **3 variables** listed. Unlike secrets, the **values are visible** — you can see `us-east-1`, `vprofileappimg`, `vprofile-helm` in plain text. [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt)

**Observe the difference:** "Here, you can see the value of the variable, but if you go to Secrets, you cannot see it." This visual confirmation helps verify correctness for variables — you can check them anytime. For secrets, you must be right on the first entry.

***

## Phase D: Verify the Complete Inventory

Navigate between the Secrets and Variables tabs to confirm: [\[369.Secret...lesAppRepo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369.SecretsAndVariablesAppRepo.txt)

**Secrets (6):**

* ✅ `AWS_ACCESS_KEY_ID`
* ✅ `AWS_SECRET_ACCESS_KEY`
* ✅ `SONAR_TOKEN`
* ✅ `HELM_REPO_USER`
* ✅ `GITOPS_PAT`
* ✅ `SLACK_WEBHOOK`

**Variables (3 now, 4 later):**

* ✅ `AWS_REGION`
* ✅ `ECR_REPOSITORY`
* ✅ `HELM_REPO_NAME`
* ⏳ `SONAR_HOST_URL` (to be added when SonarQube server starts)

**Connection to flow:** The pipeline code (created in the next lecture via AI prompt) will reference these exact names. The prompt for generating the pipeline will include these names, ensuring the generated code matches the stored secrets and variables.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ GitOps Pipeline Data Flow — Why These Credentials Exist

```
PIPELINE (runs in vprofile-app repo)
│
├──→ AWS (ECR + EKS)
│    Auth: AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY
│    Config: AWS_REGION, ECR_REPOSITORY
│
├──→ SonarQube (code quality)
│    Auth: SONAR_TOKEN
│    Config: SONAR_HOST_URL (deferred)
│
├──→ vprofile-helm repo (update values.yaml)
│    Auth: HELM_REPO_USER + GITOPS_PAT
│    Config: HELM_REPO_NAME
│
└──→ Slack (notifications)
     Auth: SLACK_WEBHOOK
```

***

## ⚡ Secrets vs. Variables — Decision Map

```
SENSITIVE (credentials, tokens, keys)?
  YES → GitHub SECRET
    ├── Encrypted at rest
    ├── Never visible after creation
    ├── Cannot be viewed, only replaced
    └── Pipeline: ${{ secrets.NAME }}

  NO → GitHub VARIABLE
    ├── Plaintext, visible to repo users
    ├── Editable and viewable
    └── Pipeline: ${{ vars.NAME }}

RULE: "If exposing it would be a security risk → Secret"
      "If it's just configuration → Variable"
```

***

## 📦 Complete Inventory — Quick Reference

```
SECRETS (6):
  AWS_ACCESS_KEY_ID          ← AWS IAM key ID
  AWS_SECRET_ACCESS_KEY      ← AWS IAM secret
  SONAR_TOKEN                ← SonarQube auth token
  HELM_REPO_USER             ← GitHub account name (devops4sure)
  GITOPS_PAT                 ← GitHub PAT (repo scope, 30-day expiry)
  SLACK_WEBHOOK              ← Slack incoming webhook URL

VARIABLES (3 + 1 deferred):
  AWS_REGION                 ← us-east-1
  ECR_REPOSITORY             ← vprofileappimg
  HELM_REPO_NAME             ← vprofile-helm
  SONAR_HOST_URL             ← (added later when SonarQube starts)
```

***

## 🔗 PAT (Personal Access Token) — Creation and Scope

```
LOCATION: GitHub → Settings → Developer Settings → PAT → Tokens Classic

CONFIGURATION:
  Note:       gitops-pipeline
  Expiry:     30 days
  Scope:      repo (read/write to repositories)

PURPOSE:
  CI pipeline (vprofile-app) → commits to vprofile-helm
  Auth: HELM_REPO_USER (username) + GITOPS_PAT (token)

ACCOUNT RULE:
  Token MUST come from the account that OWNS the target repo
  Same account → generate from your own account
  Different account → generate from the Helm repo owner's account

⚠️ Token shown ONCE at generation → save immediately
```

***

## 🔄 Cross-Repository Commit Flow

```
vprofile-app repo (CI pipeline runs here)
    │
    │ Pipeline builds new Docker image → pushes to ECR
    │ New image tag generated (e.g., v1.2.3)
    │
    │ FINAL STEP: Update values.yaml in vprofile-helm
    │ Auth: HELM_REPO_USER + GITOPS_PAT
    │ Target: HELM_REPO_NAME (vprofile-helm)
    │
    ▼
vprofile-helm repo (values.yaml updated with new image tag)
    │
    ▼
ArgoCD / CD pipeline detects change → deploys to K8s
```

***

## ⚠️ Operational Gotchas

```
SECRET VALUE WRONG?
  → Cannot view current value
  → Must delete and recreate (or overwrite with new value)
  → "Copy everything very carefully"

NAME TYPO?
  → Pipeline references ${{ secrets.AWS_ACCESS_KEY_ID }}
  → If stored as AWS_ACESS_KEY_ID (typo) → empty value → pipeline fails
  → Names in lecture resource file to prevent typos

PAT EXPIRED?
  → 30-day expiry → pipeline stops working after 30 days
  → Must regenerate and update GITOPS_PAT secret

SONAR_HOST_URL NOT SET YET?
  → Will be added later when SonarQube server starts
  → Pipeline will fail on SonarQube step until this is set
```

***

## 🔒 Security Architecture

```
REPOSITORY SCOPE:
  Secrets/Variables stored in vprofile-app repo
  Only accessible by GitHub Actions in THIS repo
  Other repos (vprofile-helm, vprofile-infra) cannot access

VISIBILITY:
  Secrets → encrypted, invisible even to repo admins
  Variables → plaintext, visible to anyone with repo access

PIPELINE LOGS:
  Secrets are MASKED in logs (shown as ***)
  Variables may appear in logs (non-sensitive, acceptable)
```

***

## 📍 Navigation Path

```
SECRETS:   Repo → Settings → Secrets and Variables → Actions → Secrets
VARIABLES: Repo → Settings → Secrets and Variables → Actions → Variables
PAT:       Profile → Settings → Developer Settings → PAT → Tokens Classic
```

***

## 🏗️ Reusable Engineering Patterns

**Pattern 1: Secret/Config Separation**
Sensitive values (credentials, tokens) and non-sensitive configuration (regions, names) are stored through different mechanisms with different security properties. Secrets are encrypted, write-only, and masked in logs. Variables are plaintext and readable. This separation appears identically in Kubernetes (Secrets vs. ConfigMaps), AWS (Secrets Manager vs. Parameter Store), Docker (secrets vs. environment variables), and Terraform (sensitive vs. non-sensitive variables). The principle: **classify data by sensitivity, then use the appropriate storage mechanism**.

**Pattern 2: Cross-System Authentication via Token + Username**
The pipeline authenticates to a different repository using a token (GITOPS\_PAT) paired with a username (HELM\_REPO\_USER). This token-plus-identity pattern is the standard for service-to-service authentication across systems: API keys + account IDs, service accounts + tokens, OAuth client credentials. The token proves authorization; the username identifies the account.

**Pattern 3: Name-as-Contract Between Config and Code**
Secret and variable names (`AWS_ACCESS_KEY_ID`, `ECR_REPOSITORY`) are contracts — the pipeline code references these exact strings. Changing a name in settings without changing the pipeline code (or vice versa) breaks the connection silently (empty value, no error at config time, failure at runtime). This is the same name-contract pattern seen in Kubernetes Service names, Helm template variables, and application.properties hostnames.

***

## 🎯 One-Line System Summary

> **The `vprofile-app` repository's GitHub Actions pipeline requires 6 secrets (AWS keys, SonarQube token, GitHub PAT for cross-repo Helm commits, Slack webhook) and 4 variables (AWS region, ECR repo name, Helm repo name, SonarQube URL — deferred), all stored under Settings → Secrets and Variables → Actions, with the PAT generated from the account owning the Helm repository (repo scope, 30-day expiry), secret names forming an exact-match contract with pipeline code, and the fundamental distinction being: secrets are encrypted/invisible (credentials), variables are plaintext/visible (configuration).** [\[369-github...-variables \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369-github-secrets-and-variables.txt), [\[369.Secret...lesAppRepo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/369.SecretsAndVariablesAppRepo.txt)

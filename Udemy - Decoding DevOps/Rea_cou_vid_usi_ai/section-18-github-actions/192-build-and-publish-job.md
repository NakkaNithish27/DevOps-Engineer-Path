# 📘 Deep Learning Material — Lecture 192: GitHub Actions — Build & Publish Job (Docker Image to Amazon ECR)

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

### 1.1 The BUILD\_AND\_PUBLISH Job — Role in the Workflow Architecture

The workflow being built throughout this course follows a **sequential pipeline architecture**: Build → Testing → Security Scan → **Build & Publish**. The `BUILD_AND_PUBLISH` job is the **final stage** — the culmination of the entire CI/CD pipeline. Its purpose is to take the validated, tested, scanned source code and produce a **deployable artifact**: a Docker image, tagged with the commit ID, and pushed to a container registry (Amazon ECR). [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192.%20workflow-main-5.yaml)

This job only runs after *all three* preceding jobs complete successfully, and only on the `main` branch. This makes it the **gated release step** — the point where validated code transforms into a shippable container image. Everything before it is validation; this job is production.

***

### 1.2 Job Dependencies with `needs` — Multi-Job Gating

The `needs` keyword defines **execution dependencies** between jobs. When a job declares `needs: [Build, Testing, Security_Scan]`, it tells the GitHub Actions scheduler: "Do not start this job until all three listed jobs have completed successfully." [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192.%20workflow-main-5.yaml)

In prior lectures, `needs` was used with a single dependency (e.g., `needs: Build`). Here, the instructor introduces the **list format** — square brackets containing multiple job names. This creates a **fan-in dependency**: three parallel jobs converge into one.

```yaml
needs: [Build, Testing, Security_Scan]
```

The scheduler evaluates all three. If any one fails, `BUILD_AND_PUBLISH` never starts. This is the **quality gate** — the final job inherits the collective validation of all prior stages.

🔍 **Deep Dive**
This fan-in pattern creates an implicit parallelism: Build, Testing, and Security\_Scan can run concurrently (assuming their own dependencies allow it — in this workflow, Testing and Security\_Scan both `need: Build`, so they start after Build completes, then run in parallel, and BUILD\_AND\_PUBLISH starts after both finish). The dependency graph is: `Build → [Testing ∥ Security_Scan] → BUILD_AND_PUBLISH`.

***

### 1.3 Branch-Conditional Execution with `if`

Not every workflow trigger should execute every job. The `BUILD_AND_PUBLISH` job must only run when code is pushed to the `main` branch — you don't want Docker images built and published from pull request test runs or feature branches. The `if` keyword provides **conditional execution** at the job level. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192.%20workflow-main-5.yaml)

```yaml
if: github.ref == 'refs/heads/main'
```

`github.ref` is a **context variable** provided by GitHub Actions at runtime. It contains the full Git reference that triggered the workflow. For a push to the `main` branch, this value is `refs/heads/main`. The `if` expression evaluates this at runtime — if the condition is `true`, the job runs; if `false`, the job is **skipped entirely** (not failed, just skipped).

**Why this matters:** The workflow's `on:` block allows triggers from pushes, pull requests, manual dispatch, and schedules. Without the `if` condition, a pull request trigger would also run the publish job, which would push an untested, unmerged image to ECR. The `if` condition acts as a **second-level filter** — the `on:` block decides *whether the workflow runs*, and the `if` condition decides *whether a specific job within the workflow runs*. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

***

### 1.4 GitHub Environments — Scoped Secret Access

When the instructor stored AWS credentials (in a previous lecture), they were saved inside a GitHub **Environment** named `production`. Environments are isolation boundaries for secrets and configuration variables — secrets stored in the `production` environment are *only* accessible to jobs that explicitly declare `environment: production`. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192.%20workflow-main-5.yaml)

```yaml
environment: production
```

This single line grants the job access to all secrets and variables stored in that environment. Without it, `${{ secrets.AWS_ACCESS_KEY_ID }}` would resolve to nothing — the job simply cannot see those secrets.

**Why environments exist:** They enforce the principle that **sensitive credentials should be scoped, not global**. A testing job shouldn't have access to production AWS keys. By tying secrets to environments and requiring jobs to declare which environment they use, GitHub Actions creates an **access-control boundary** around credentials.

🔍 **Deep Dive**
Environments can also have **protection rules** — required reviewers, wait timers, and branch restrictions. For example, you could configure the `production` environment to require manual approval before any job using it can proceed. This turns `environment: production` into both a secrets-access mechanism and a deployment gate.

***

### 1.5 The Secrets and Variables Access Model

GitHub Actions provides three scopes for storing and accessing configuration: [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

**Secrets** (sensitive, encrypted, write-once-read-never by humans):

```yaml
${{ secrets.AWS_ACCESS_KEY_ID }}
${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

**Environment variables (stored in GitHub Vars)** (non-sensitive, visible):

```yaml
${{ vars.AWS_REGION }}
```

**Workflow-level `env` variables** (defined inline in the YAML):

```yaml
env:
  ECR_REPOSITORY: 'vprofile-appimage'
```

Accessed as:

```yaml
${{ env.ECR_REPOSITORY }}
```

The access syntax follows a consistent pattern: `${{ SCOPE.KEY }}`. The scope determines *where* the value comes from (`secrets`, `vars`, `env`, `github`, `steps`), and the key identifies the specific value.

The instructor explicitly notes that defining variables in the workflow-level `env` block is **not the recommended practice** — it's better to store them in GitHub Secrets/Vars. The inline `env` is used here as a teaching demonstration to show that this mechanism exists. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

⚠️ **Expert Note**
Secrets are masked in logs — if a secret value accidentally appears in command output, GitHub replaces it with `***`. However, this masking is not foolproof (e.g., if you base64-encode a secret, the encoded form won't be masked). Never echo or print secrets intentionally.

***

### 1.6 The AWS Authentication Flow — Configure Credentials Action

Before you can interact with any AWS service (like ECR), you must **authenticate** to the AWS account. The workflow uses a predefined GitHub Action for this: [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v1
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: ${{ vars.AWS_REGION }}
```

This action takes three inputs — the access key ID, the secret access key, and the AWS region — and configures the runner's environment so that all subsequent AWS CLI commands and AWS-related actions are authenticated. It essentially sets up the `~/.aws/credentials` and `~/.aws/config` equivalents within the runner's session. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

The inputs are pulled from the GitHub environment's secrets and variables. The access key is a secret (sensitive), the secret key is a secret (sensitive), and the region is a variable (non-sensitive — it's just a region name like `us-east-1`).

**Key relationship:** This step is a **prerequisite for all subsequent AWS interactions**. The ECR login step and the Docker push step both depend on this authentication being in place. Without it, every AWS operation fails with an authentication error.

***

### 1.7 Amazon ECR Login — The `amazon-ecr-login` Action and Step Outputs

After authenticating to AWS, the next step is to **log into Amazon ECR** specifically. ECR is a Docker-compatible container registry — to push images to it, you need a Docker login session with ECR's endpoint. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

```yaml
- name: Login to Amazon ECR
  id: login-ecr
  uses: aws-actions/amazon-ecr-login@v1
```

This action leverages the credentials configured in the previous step to perform a `docker login` against the ECR registry endpoint. After this step, the runner's Docker daemon is authorized to push and pull images from your ECR repositories.

**Step IDs and Outputs — a critical concept:** Notice the `id: login-ecr` attribute. This assigns a **referenceable identifier** to the step. The reason: this action produces **outputs** — specifically, it outputs the ECR **registry URI** (the base URL of your ECR, something like `123456789012.dkr.ecr.us-east-1.amazonaws.com`). Later steps can access this output using the expression: [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

```yaml
${{ steps.login-ecr.outputs.registry }}
```

This is the **step output access pattern**: `steps.<STEP_ID>.outputs.<OUTPUT_KEY>`. It allows data to flow *between steps* within the same job — a step produces data, assigns it to an output key, and downstream steps consume it by referencing the step's ID.

🔍 **Deep Dive**
The `outputs.registry` value from the ECR login action returns everything *except* the repository name. It gives you the registry base URI: `<account_id>.dkr.ecr.<region>.amazonaws.com`. You then append your specific repository name (e.g., `/vprofile-appimage`) to form the complete image URI. This separation of registry (stable infrastructure) from repository (project-specific) is a deliberate design — the login action doesn't know or care which repository you'll push to.

***

### 1.8 Docker Image Naming Convention — Registry / Repository : Tag

Docker images follow a strict naming structure that directly maps to where the image is stored and how it's versioned: [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

    <registry>/<repository>:<tag>

| Component  | Example                                        | Source in Workflow                 |
| ---------- | ---------------------------------------------- | ---------------------------------- |
| Registry   | `123456789012.dkr.ecr.us-east-1.amazonaws.com` | `steps.login-ecr.outputs.registry` |
| Repository | `vprofile-appimage`                            | `env.ECR_REPOSITORY`               |
| Tag        | `3b7a2f9c...` (commit SHA)                     | `github.sha`                       |

The **registry** identifies *which container service* hosts the image (ECR, Docker Hub, Google Container Registry, etc.). The **repository** identifies the *specific image collection* within that registry. The **tag** identifies the *specific version* of the image.

The instructor emphasizes that this structure is **universal** — if you switch from ECR to Docker Hub, only the registry portion changes. The repository and tag concepts remain identical. This is the **portable image addressing model**. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

***

### 1.9 Using `github.sha` as the Image Tag

Instead of manually versioning images (v1, v2, v3...), the workflow uses `github.sha` — a context variable that contains the **full 40-character SHA hash of the commit that triggered the workflow**. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

```yaml
IMAGE_TAG: ${{ github.sha }}
```

**Why this is powerful:** Every commit has a unique SHA. By tagging the Docker image with the commit SHA, you create an **immutable, traceable link** between the container image and the exact source code state that produced it. Given any running container, you can inspect its tag, look up that commit in Git, and know *exactly* which code version is inside it.

The instructor verifies this at the end by comparing the image tag in ECR with the commit ID on GitHub — they match exactly, confirming the traceability chain. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

***

### 1.10 The `run` Keyword with Pipe (`|`) — Multi-Line Shell Commands

When you need to execute raw shell commands (not a predefined action), you use the `run` keyword. For a single command, `run: echo "hello"` suffices. But when you need **multiple commands in sequence**, you use the **YAML pipe (`|`) for a multi-line block scalar**: [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

```yaml
run: |
  docker build -f docker-files/app/multistage -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
  docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
```

The `|` tells YAML: "Everything that follows (indented) is a literal block of text — preserve the newlines." Each line becomes a separate shell command executed sequentially in the runner's shell. If any command fails (non-zero exit code), the step fails.

**`run` vs `uses`:** `uses` invokes a predefined, packaged GitHub Action. `run` executes arbitrary shell commands directly on the runner. The instructor deliberately uses `run` for the Docker build/push step to demonstrate that **not everything requires a GitHub Action** — sometimes a direct shell command is simpler and more transparent. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

***

### 1.11 The `docker build` Command — Anatomy

```bash
docker build -f docker-files/app/multistage -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
```

 [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

| Flag/Argument                                 | Meaning                                                                            |
| --------------------------------------------- | ---------------------------------------------------------------------------------- |
| `docker build`                                | Build a Docker image from a Dockerfile                                             |
| `-f docker-files/app/multistage`              | Path to the Dockerfile (not the default `./Dockerfile`)                            |
| `-t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG` | Tag the resulting image with the full registry/repo:tag name                       |
| `.` (dot at the end)                          | The **build context** — the directory whose contents are sent to the Docker daemon |

**The dot (`.`) — build context — is critically important.** The instructor explains this explicitly: the `.` means "current working directory" (the repository root). The Dockerfile contains a `COPY` instruction that copies application files into the container. If the build context were the Dockerfile's own directory (`docker-files/app/`), it would only see files in that subdirectory. By setting the context to `.` (root), Docker can access *all* repository files — source code, configurations, everything — which is necessary for the `COPY` instruction to work correctly. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

Without the `.`, Docker would default to the Dockerfile's directory as the context, and the build would fail or produce an incomplete image because the source code files wouldn't be available.

***

### 1.12 The `docker push` Command

```bash
docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
```

This pushes the locally built image to the remote registry. It uses the exact same image name (registry/repository:tag) that was assigned during `docker build -t`. The push succeeds because the runner is already authenticated to ECR (from the login step). [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

The relationship is linear: **authenticate → login to ECR → build image → push image**. Each step depends on the previous one's success.

***

### 1.13 Runtime Environment Variables in a Step (`env` block inside a step)

The `BUILD_AND_PUBLISH` job's build step defines **step-scoped environment variables** using an `env` block *inside* the step: [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

```yaml
env:
  ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
  IMAGE_TAG: ${{ github.sha }}
```

These variables exist only during this step's execution. They are assigned values dynamically at runtime — `ECR_REGISTRY` gets its value from the ECR login step's output, and `IMAGE_TAG` gets the commit SHA. Inside the `run` block, these are accessed as standard shell variables (`$ECR_REGISTRY`, `$IMAGE_TAG`).

**This is a variable-scoping hierarchy:**

*   **Workflow-level `env`**: accessible to all jobs and steps (e.g., `ECR_REPOSITORY`)
*   **Job-level `env`**: accessible to all steps within the job
*   **Step-level `env`**: accessible only within that step (e.g., `ECR_REGISTRY`, `IMAGE_TAG`)

The instructor uses step-level `env` to demonstrate how to **capture runtime outputs into variables** and use them in shell commands — a technique for bridging the gap between GitHub Actions expressions (`${{ }}`) and shell variable syntax (`$VAR`). [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

***

### 1.14 Workflow-Level `env` — Defining Shared Variables

At the top of the workflow file, before the `jobs` block:

```yaml
env:
  ECR_REPOSITORY: 'vprofile-appimage'
```

This defines a variable accessible to every job and step in the workflow. It's referenced using `${{ env.ECR_REPOSITORY }}` in action inputs or `$ECR_REPOSITORY` in shell `run` blocks. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192.%20workflow-main-5.yaml)

The instructor explicitly warns: **storing variables in the workflow file is not the recommended practice for production**. It's better to use GitHub Secrets (for sensitive values) or GitHub Variables/Vars (for non-sensitive values). The inline `env` is demonstrated as a teaching tool so learners know this capability exists. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

***

### 1.15 The `permissions` Block — Principle of Least Privilege

```yaml
permissions:
  contents: read
```

This block restricts the workflow's **GITHUB\_TOKEN permissions**. By default, the token has broad permissions. Setting `contents: read` limits the token to **read-only access** to repository contents — it cannot push code, create releases, or modify the repository. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192.%20workflow-main-5.yaml)

This follows the **principle of least privilege**: grant only the minimum permissions necessary. Since this workflow reads source code but never writes back to the repository, `contents: read` is sufficient.

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

### What We Are Building

We are adding the **final job** to the `vprofile-action` CI/CD workflow: `BUILD_AND_PUBLISH`. This job takes the source code (already validated by Build, Testing, and Security Scan jobs), builds a Docker image from it using a multi-stage Dockerfile, tags the image with the Git commit SHA, and pushes it to Amazon ECR. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

**Why it matters:** This transforms validated source code into a **deployable container image** stored in a production registry — the bridge between CI (code validation) and CD (deployment).

**Final outcome:** A complete GitHub Actions workflow that, on every push to `main`, runs build, test, and security scan jobs, then builds and publishes a Docker image to ECR tagged with the exact commit ID. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192.%20workflow-main-5.yaml)

***

### Step 1: Define the Workflow-Level Environment Variable

**What we are doing:** Adding a workflow-level `env` block to define the ECR repository name as a reusable variable.

**Where:** In `main.yml`, just before the `permissions` block (after the `on:` triggers).

```yaml
env:
  ECR_REPOSITORY: 'vprofile-appimage'
```

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192.%20workflow-main-5.yaml), [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

**Breakdown:**

*   `env:` — Opens the workflow-level environment variable block
*   `ECR_REPOSITORY` — Variable name (your choice, but must match all references)
*   `'vprofile-appimage'` — The name of the ECR repository you created in a previous lecture

**Where to get the value:** Go to AWS Console → ECR → Repositories → copy the repository name. It must exactly match.

**How to verify:** This variable is used later in the `docker build` and `docker push` commands. If misspelled, those commands will fail with a "repository not found" error.

**Connection to larger flow:** This variable is referenced in the build step using `$ECR_REPOSITORY`, avoiding hardcoding the repository name in multiple places.

⚠️ **Expert Note**
The instructor explicitly notes this is not recommended for production. In real systems, store this value in GitHub Variables (`vars.ECR_REPOSITORY`) instead. Inline `env` is fragile — it lives in the YAML file, is visible to anyone with repo access, and requires a commit to change.

***

### Step 2: Create the BUILD\_AND\_PUBLISH Job Skeleton

**What we are doing:** Adding a new job at the same indentation level as `Security_Scan`, with all necessary metadata.

```yaml
BUILD_AND_PUBLISH:
  name: BUILD_AND_PUBLISH
  runs-on: ubuntu-latest
  environment: production
  needs: [Build, Testing, Security_Scan]
  if: github.ref == 'refs/heads/main'
  steps:
```

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192.%20workflow-main-5.yaml), [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

**Breakdown:**

| Line                                     | Purpose                                                                                    |
| ---------------------------------------- | ------------------------------------------------------------------------------------------ |
| `BUILD_AND_PUBLISH:`                     | Job identifier (used in `needs` references from other jobs)                                |
| `name: BUILD_AND_PUBLISH`                | Display name shown in the GitHub Actions UI                                                |
| `runs-on: ubuntu-latest`                 | Runner image — standard Ubuntu VM                                                          |
| `environment: production`                | Links this job to the `production` GitHub Environment, granting access to its secrets/vars |
| `needs: [Build, Testing, Security_Scan]` | Wait for all three jobs to complete before starting                                        |
| `if: github.ref == 'refs/heads/main'`    | Only execute for pushes to `main` (skip for PRs, other branches)                           |

**Common mistake:** Forgetting `environment: production`. Without it, `${{ secrets.AWS_ACCESS_KEY_ID }}` resolves to empty, and the AWS authentication step silently fails or throws a credentials error.

**Common mistake:** Misspelling job names in `needs`. The names must exactly match the job identifiers defined above (`Build`, `Testing`, `Security_Scan` — case-sensitive).

***

### Step 3: Add the Code Checkout Step

```yaml
steps:
  - name: Code checkout
    uses: actions/checkout@v4
    with:
      fetch-depth: 0
```

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192.%20workflow-main-5.yaml)

**What we are doing:** Cloning the repository source code into the runner's workspace. As covered in earlier lectures, `fetch-depth: 0` fetches full history.

**Why it's needed here:** The Docker build command requires the source code files to be present on the runner. Without checkout, the runner's workspace is empty.

***

### Step 4: Configure AWS Credentials

**What we are doing:** Authenticating the runner to the AWS account using the `configure-aws-credentials` action.

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v1
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: ${{ vars.AWS_REGION }}
```

 [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

**Breakdown:**

*   `uses: aws-actions/configure-aws-credentials@v1` — Official AWS action from the `aws-actions` organization
*   `aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}` — Reads the access key from the `production` environment's secrets
*   `aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}` — Reads the secret key from secrets
*   `aws-region: ${{ vars.AWS_REGION }}` — Reads the region from environment variables (non-secret)

**What happens internally:** The action sets AWS environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`) in the runner's session. All subsequent steps inherit these, enabling seamless AWS CLI and SDK operations.

**How to verify success:** In the workflow run log, this step should complete with a green checkmark. If it fails, check: (1) the secret names match exactly what was stored, (2) `environment: production` is declared on the job, (3) the IAM user has the necessary permissions.

**Connection to larger flow:** This is a **prerequisite** for both the ECR login and the Docker push. Without valid credentials, neither can succeed.

***

### Step 5: Login to Amazon ECR

**What we are doing:** Authenticating the runner's Docker daemon to Amazon ECR so it can push images.

```yaml
- name: Login to Amazon ECR
  id: login-ecr
  uses: aws-actions/amazon-ecr-login@v1
```

 [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

**Breakdown:**

*   `id: login-ecr` — Assigns a referenceable ID to this step. **Critical:** the build step references `steps.login-ecr.outputs.registry` to get the ECR registry URI.
*   `uses: aws-actions/amazon-ecr-login@v1` — Official AWS action that performs `docker login` against ECR
*   No `with` inputs needed — it uses the credentials configured in the previous step automatically.

**What happens internally:** The action calls the ECR API to obtain a Docker login token, then runs `docker login` with that token against the ECR endpoint. It also outputs the registry URI.

**How to verify:** Green checkmark in the log. If it fails, the AWS credentials step likely failed or the IAM user lacks ECR permissions (`ecr:GetAuthorizationToken`, `ecr:BatchGetImage`, `ecr:PutImage`, etc.).

**Common mistake:** Forgetting the `id: login-ecr` line. Without it, the next step cannot reference this step's outputs, and the `ECR_REGISTRY` variable will be empty.

***

### Step 6: Build, Tag, and Push the Docker Image

**What we are doing:** Building the Docker image from the multi-stage Dockerfile, tagging it with the ECR URI and commit SHA, and pushing it to ECR. All in one step using shell commands.

```yaml
- name: Build, tag, and push image to Amazon ECR
  id: build-image
  env:
    ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
    IMAGE_TAG: ${{ github.sha }}
  run: |
    docker build -f docker-files/app/multistage -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
    docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
```

 [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

**Detailed breakdown of the `env` block:**

*   `ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}` — Captures the ECR login step's output (the registry base URI, e.g., `123456789012.dkr.ecr.us-east-1.amazonaws.com`) into a shell variable.
*   `IMAGE_TAG: ${{ github.sha }}` — Captures the full 40-character commit SHA into a shell variable.

**Detailed breakdown of `docker build`:**

```bash
docker build -f docker-files/app/multistage -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
```

| Part                                          | Meaning                                                                                                                                                                              |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `docker build`                                | Invoke the Docker build engine                                                                                                                                                       |
| `-f docker-files/app/multistage`              | Path to the Dockerfile (relative to the build context). The `-f` flag is needed because the Dockerfile is not in the default location (`./Dockerfile`)                               |
| `-t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG` | Tag the image. Expands to something like `123456789012.dkr.ecr.us-east-1.amazonaws.com/vprofile-appimage:3b7a2f9c...`                                                                |
| `.`                                           | **Build context** = current directory (repo root). Docker sends this entire directory to the daemon. The Dockerfile's `COPY` instruction copies from this context into the container |

**Why the `.` matters (instructor's explicit explanation):** The Dockerfile contains a `COPY` instruction that copies all application files into `/app` inside the container. If you omit the `.`, Docker would use the Dockerfile's directory (`docker-files/app/`) as context, and the `COPY` would only see files in that subdirectory — missing the actual source code at the repo root. The `.` ensures Docker has access to the entire repository. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

**Detailed breakdown of `docker push`:**

```bash
docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
```

Pushes the locally built image to the remote ECR registry. The image name must exactly match the tag used in `docker build -t`. The push works because the ECR login step already authenticated Docker to ECR.

**How to verify success:**

1.  In the workflow log, the build step shows Docker layer-by-layer output (pulling base images, running build stages, exporting layers) followed by push progress.
2.  In AWS Console → ECR → your repository → you should see the new image with the commit SHA as its tag. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)
3.  On GitHub → click the commit → the short commit ID visible there should match the image tag in ECR. The instructor verifies this explicitly by copying the full commit SHA from GitHub and finding it matches the ECR image tag exactly. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

**Common mistakes:**

*   Misspelling the Dockerfile path in `-f` → "file not found" error
*   Missing the `.` at the end → build context wrong → `COPY` fails
*   `ECR_REPOSITORY` value doesn't match the actual ECR repository name → push fails with "repository not found"
*   ECR login step missing `id` → `$ECR_REGISTRY` is empty → malformed image URI

🔍 **Deep Dive**
The `id: build-image` on this step would allow later steps to reference its outputs (e.g., the built image URI). The instructor mentions this is useful if you later add a deployment step (e.g., deploying to ECS), where you'd need to reference the exact image URI that was just pushed. Since there's no deployment step in this workflow, the `id` isn't strictly necessary here but is included as good practice. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

***

### Step 7: Commit, Push, and Verify the Complete Workflow

**What we are doing:** Saving the final workflow file and triggering the pipeline.

1.  **Save** the file (`Ctrl+S`).
2.  **Compare** your YAML with the lecture resource file — check for typographical errors. The instructor emphasizes this explicitly. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)
3.  **Commit and push:**
    *   In VS Code: Source Control → Stage → Commit message: "Build and publish job added" → Commit & Push
4.  **Observe the workflow:**
    *   Go to GitHub → Actions tab → the workflow triggers automatically (push to main).
    *   Wait for all four jobs to complete: Build → Testing → Security\_Scan → BUILD\_AND\_PUBLISH. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

**Verification checklist:**

*   ✅ All four jobs show green checkmarks
*   ✅ BUILD\_AND\_PUBLISH log shows: Configure AWS credentials ✓ → Login to ECR ✓ → Build/tag/push ✓
*   ✅ In ECR console: new image appears with the commit SHA as tag
*   ✅ The SHA in ECR matches the commit ID on GitHub [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

**Additional verification:** You can manually trigger the workflow via `workflow_dispatch` — go to Actions → select the workflow → "Run workflow" button → Run. This confirms the manual trigger also works end-to-end. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

⚠️ **Expert Note**
The instructor closes with important practical advice: you now understand the foundational building blocks (environments, secrets, variables, conditions, needs, run, uses, step outputs). With this knowledge, you can leverage AI coding assistants (GitHub Copilot, Amazon Q, ChatGPT) to generate more complex workflows — but the ability to *understand, debug, and validate* those generated workflows comes from knowing these fundamentals. The projects section of the course will integrate additional continuous delivery tools. [\[192-build-...ublish-job \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/192-build-and-publish-job.txt)

***

## 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

### Workflow Architecture — Complete Pipeline

    on: push/PR/dispatch/schedule
      │
      ├── env: ECR_REPOSITORY (workflow-level)
      ├── permissions: contents: read
      │
      └── jobs:
            ├── Build (ubuntu-latest)
            │     └── checkout@v4
            │
            ├── Testing (ubuntu-latest, needs: Build)
            │     └── checkout@v4
            │
            ├── Security_Scan (ubuntu-latest, needs: Build)
            │     └── checkout@v4
            │
            └── BUILD_AND_PUBLISH (ubuntu-latest)
                  ├── environment: production     ← secrets access gate
                  ├── needs: [Build, Testing, Security_Scan]  ← fan-in
                  ├── if: github.ref == 'refs/heads/main'     ← branch gate
                  └── steps:
                        1. checkout
                        2. configure-aws-credentials  ← secrets → AWS auth
                        3. amazon-ecr-login (id: login-ecr)  ← Docker auth + outputs registry URI
                        4. docker build + push (uses step output + github.sha)

***

### Job Dependency Graph (Execution Order)

    Build ──┬──→ Testing ────────┐
            │                    ├──→ BUILD_AND_PUBLISH
            └──→ Security_Scan ──┘

    Parallel:  Testing ∥ Security_Scan
    Gated by:  needs + if (main branch only)

***

### Authentication Chain — Dependency Flow

    secrets (production env)
      ├── AWS_ACCESS_KEY_ID ──┐
      ├── AWS_SECRET_ACCESS_KEY──┤──→ configure-aws-credentials ──→ AWS session active
      └── vars.AWS_REGION ────┘                                          │
                                                                         ▼
                                                             amazon-ecr-login ──→ Docker authenticated to ECR
                                                                  │                        │
                                                        outputs.registry                   ▼
                                                                  │              docker push succeeds
                                                                  ▼
                                                        ECR_REGISTRY variable
                                                                  │
                                                                  ▼
                                                        docker build -t <full_uri>

***

### Variable Scope Hierarchy

    Workflow-level env:     ECR_REPOSITORY = 'vprofile-appimage'     → all jobs/steps
    GitHub Vars:            vars.AWS_REGION                          → via environment
    GitHub Secrets:         secrets.AWS_ACCESS_KEY_ID                → via environment
                            secrets.AWS_SECRET_ACCESS_KEY             → via environment
    Step-level env:         ECR_REGISTRY (from step output)          → this step only
                            IMAGE_TAG (from github.sha)              → this step only

***

### Docker Image URI Construction

    $ECR_REGISTRY          /  $ECR_REPOSITORY    :  $IMAGE_TAG
    ────────────────────      ─────────────────     ──────────────────
    steps.login-ecr           env.ECR_REPOSITORY    github.sha
    .outputs.registry         (workflow env)         (commit SHA)
    ────────────────────      ─────────────────     ──────────────────
    123456789012.dkr.         vprofile-appimage      3b7a2f9c4e...
    ecr.us-east-1.
    amazonaws.com

    UNIVERSAL PATTERN: <registry>/<repository>:<tag>
      ECR:        account.dkr.ecr.region.amazonaws.com/repo:tag
      Docker Hub: docker.io/username/repo:tag
      GCR:        gcr.io/project/repo:tag

***

### Docker Build Command — Anatomy

    docker build  -f <dockerfile_path>  -t <full_image_name>  <build_context>
                  │                     │                      │
                  └ docker-files/       └ registry/repo:tag    └ . (repo root)
                    app/multistage                               COPY needs repo root files

**Critical:** `.` = build context = where COPY sources files from. Without it → wrong context → missing files.

***

### Step Output Access Pattern

    Producer step:  id: login-ecr  →  outputs: { registry: "..." }
    Consumer step:  ${{ steps.login-ecr.outputs.registry }}

    Generic:        ${{ steps.<STEP_ID>.outputs.<KEY> }}

***

### Conditional Execution — Two-Level Filtering

    Level 1 (Workflow):  on: push/PR/dispatch/schedule  → "Should the workflow run?"
    Level 2 (Job):       if: github.ref == 'refs/heads/main'  → "Should this job run?"

    Result: PR trigger → workflow runs → BUILD_AND_PUBLISH SKIPPED (ref ≠ main)
            Push to main → workflow runs → BUILD_AND_PUBLISH RUNS

***

### Access Scopes — Expression Syntax Map

    ${{ secrets.KEY }}              → GitHub Secrets (encrypted, environment-scoped)
    ${{ vars.KEY }}                 → GitHub Variables (visible, environment-scoped)
    ${{ env.KEY }}                  → Workflow/job/step inline env
    ${{ github.sha }}               → Commit SHA (context)
    ${{ github.ref }}               → Git ref (context)
    ${{ steps.ID.outputs.KEY }}     → Step output (inter-step data flow)

***

### `run` vs `uses` Decision

    uses:  → Predefined GitHub Action (packaged, versioned, marketplace)
             e.g., aws-actions/configure-aws-credentials@v1
    run:   → Raw shell commands (direct, transparent, flexible)
             e.g., docker build ... | docker push ...
      |    → pipe = multi-line block = multiple sequential commands

***

### Reusable Engineering Patterns

| Pattern                        | Instance                                                              |
| ------------------------------ | --------------------------------------------------------------------- |
| **Fan-In Dependency**          | `needs: [Build, Testing, Security_Scan]` — parallel jobs converge     |
| **Gated Release**              | `if` condition + `needs` = only publish after full validation on main |
| **Scoped Secret Access**       | `environment: production` gates credential visibility                 |
| **Step Output Chaining**       | ECR login outputs registry → build step consumes it                   |
| **Immutable Artifact Tagging** | `github.sha` as image tag = code↔artifact traceability                |
| **Authentication Cascade**     | credentials → ECR login → Docker push (each depends on prior)         |
| **Interface Portability**      | `registry/repo:tag` pattern works across ECR/DockerHub/GCR            |
| **Least Privilege**            | `permissions: contents: read` — minimal token scope                   |
| **Separation of Concerns**     | Validate (3 jobs) → Publish (1 job) — distinct responsibilities       |

***

### Verification Sequence

    1. Actions tab → all 4 jobs green ✓
    2. BUILD_AND_PUBLISH logs → each step green ✓
    3. AWS ECR console → image exists with commit SHA tag
    4. GitHub commit page → SHA matches ECR tag exactly
    5. (Optional) Manual trigger via workflow_dispatch → full pipeline re-runs ✓

***

Want me to generate a downloadable `.md` file for this material? 📄

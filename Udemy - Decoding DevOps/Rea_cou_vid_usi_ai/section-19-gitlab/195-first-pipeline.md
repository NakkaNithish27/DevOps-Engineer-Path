# 🧠 GitLab CI — First Pipeline: Build & Test with YAML, Runners, and Docker Executors

**Source**: [195-first-pipeline.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt?EntityRepresentationId=ec1c041a-7ddc-43ab-9bdb-043e690b5cb3) (caption file) + [195.FirstPipeline.yml](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195.FirstPipeline.yml?EntityRepresentationId=020fb35a-a864-4f3b-9a27-a0bbed5cdff6) (pipeline file) [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195.FirstPipeline.yml)

***

# 🧠 SECTION 1: THEORY (DEEP LEARNING MODE)

## 1.1 What a GitLab Pipeline Is and Where It Lives

A GitLab CI/CD pipeline is a set of automated jobs that execute against your source code whenever certain events occur (like a commit). The pipeline is **defined inside the same repository** it operates on — specifically in a file named **`.gitlab-ci.yml`** placed at the root of the repository. This is a YAML-format file. When GitLab detects this file in a repository, the pipeline becomes visible under **Build → Pipelines** in the project's GitLab interface. Without this file, the Pipelines section shows nothing. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

This is the same foundational model as GitHub Actions (workflow files in `.github/workflows/`), but in GitLab the convention is a single file at the repository root with a fixed name. The file name is not arbitrary — it must be exactly `.gitlab-ci.yml` for GitLab to recognize it. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

The underlying repository is a standard Git repository — it has branches, tags, commits, and behaves identically to any other Git repo. The pipeline file is simply another file tracked by Git. When you commit and push changes (including changes to `.gitlab-ci.yml` itself), GitLab detects the push event and triggers the pipeline. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

## 1.2 Pipeline Structure — Stages and Jobs

A pipeline is organized into **stages**, and each stage contains one or more **jobs**. Stages execute sequentially (build runs before test, test runs before deploy). Jobs within the same stage can run in parallel.

The stages are declared at the top of `.gitlab-ci.yml` using the `stages:` keyword, followed by a YAML list:

```yaml
stages:
  - build
  - test
```

Each item in the list is a stage name. The order in the list defines the execution order — `build` runs first, then `test`. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195.FirstPipeline.yml)

A **job** is defined as a top-level YAML key with a name you choose (e.g., `build-job`, `test-job`). Inside the job, the `stage:` keyword **must reference one of the stage names declared in the `stages:` list**. If the stage name in the job does not match any declared stage, GitLab will throw an error: *"stage \[name] is not in the stages."* This is a strict validation — the names must match exactly. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

The job name (e.g., `build-job`) is for **your identification** — it appears in the GitLab UI as the label for that pipeline step. The `stage:` value inside the job is what links the job to the pipeline's execution order. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

## 1.3 Variables — Pipeline-Level Configuration

Variables are defined under the `variables:` keyword at the top level of the YAML file. They act as reusable configuration values accessible throughout the pipeline:

```yaml
variables:
  PROJECT_NAME: "Vprofile-App"
```

Variables defined here are available in all jobs via the `$VARIABLE_NAME` syntax (e.g., `$PROJECT_NAME` in script commands). The instructor uses a variable to store the project name and references it in an echo command during the build job. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195.FirstPipeline.yml)

The instructor notes that you can also **store variables and secrets in GitLab itself** (through the UI, under project settings) — this is covered in a later lecture. Inline YAML variables are suitable for non-sensitive configuration; sensitive values (passwords, tokens) should use GitLab's secret storage. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

## 1.4 The `script:` Block — What the Job Actually Executes

The `script:` keyword inside a job defines the **list of commands** that will be executed. It accepts a YAML list of strings, each being a shell command:

```yaml
script:
  - echo "Building project => $PROJECT_NAME"
  - mvn install
```

Commands execute sequentially, top to bottom. If any command fails (returns a non-zero exit code), the job fails. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195.FirstPipeline.yml)

***

## 1.5 Runners — Where Jobs Actually Execute

When a pipeline is triggered, the jobs need to execute *somewhere* — on some compute resource. That resource is called a **runner**. GitLab provides two options:

1. **GitLab's built-in (shared) runners** — pre-configured runners managed by GitLab. These are available immediately with no setup. When you see "Running with GitLab Runner" in the job logs, this is the built-in runner.
2. **Self-hosted runners** — you add your own machine (EC2 instance, on-premises server, etc.) as a runner and specify it in the pipeline. You can mention the runner name in the job configuration.

For this lecture, the built-in GitLab runners are used. Self-hosted runners and their configuration are covered later. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

## 1.6 Executors — How the Runner Runs Your Commands

The runner itself is just a machine. The **executor** determines *how* commands are executed on that machine. GitLab supports several executor types:

| Executor                   | How It Works                                                                |
| -------------------------- | --------------------------------------------------------------------------- |
| **Docker**                 | Pulls a container image, creates a container, runs commands inside it       |
| **Shell**                  | Executes commands directly on the runner's OS (e.g., on an EC2 instance)    |
| **SSH**                    | SSHes into a remote machine and executes commands there                     |
| **Kubernetes**             | Creates pods in a Kubernetes cluster to run jobs                            |
| **Parallels / VirtualBox** | Runs jobs inside virtual machines                                           |
| **Docker+Machine**         | Auto-provisions Docker hosts on-demand (what GitLab's built-in runners use) |

The instructor states: **"Majority of the time it's going to be Docker."** When you add your own runner, you choose the executor type. The built-in GitLab runners use the **Docker+Machine** executor, which is visible in the job logs as "Preparing docker+machine executor." [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

## 1.7 The `image:` Keyword — Container-Based Execution

When using Docker executors, the `image:` keyword specifies which **Docker Hub image** to pull and run the job inside:

```yaml
image: maven:3.9.9-eclipse-temurin-17
```

This tells the runner: pull the `maven:3.9.9-eclipse-temurin-17` image from Docker Hub, create a container from it, and execute the `script:` commands inside that container. This image contains Maven 3.9.9 and JDK 17 (Eclipse Temurin distribution) — everything needed to build a Java project without installing anything manually. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195.FirstPipeline.yml)

**Each stage creates its own container, runs the commands, and then closes the container when done.** The build job runs in one container, the test job runs in a separate container — even if they use the same image. They are independent execution environments. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

🔍 **Deep Dive**: This is the key difference from running builds on bare metal or a persistent VM. In the container-based model, every job starts with a clean, reproducible environment defined by the Docker image. There is no state leakage between jobs (unless you explicitly use artifacts or caches to pass data). This is why you don't need to worry about tool version conflicts between jobs — each container has exactly the tools its image provides.

***

## 1.8 Automatic Source Code Cloning

A critical convenience in GitLab CI: **you do not need to write any instruction to clone the source code**. The runner automatically clones the repository (at the correct branch and commit) into the container before executing your script commands. In the job logs, you can see the "Cloning repository" step happening before "Executing step script." [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

This is different from some other CI systems where you must explicitly add a checkout step. In GitLab, it is built-in and automatic.

***

## 1.9 The `only:` Keyword — Branch Filtering

The `only:` keyword restricts which branches trigger the job:

```yaml
only:
  - main
```

This means the job **only runs when commits are pushed to the `main` branch**. Commits to any other branch will not trigger this job. Both the build and test jobs in this pipeline use `only: main`. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195.FirstPipeline.yml)

The instructor notes: **"There are better ways to do this which we're going to see in the next lecture."** The `only:` keyword is the simple/legacy approach. More modern GitLab pipelines use `rules:` for conditional execution. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

## 1.10 The `needs:` Keyword — Explicit Job Dependencies

In the test job:

```yaml
needs:
  - build-job
```

This creates an explicit dependency: the test job will not start until `build-job` has completed successfully. The instructor's YAML comment compares it to GitHub Actions: `# equivalent to 'needs: Build' in GitHub Actions`. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195.FirstPipeline.yml)

🔍 **Deep Dive**: Without `needs:`, jobs in different stages already run sequentially (build stage finishes before test stage starts). However, `needs:` becomes important when you have multiple jobs in the same stage or when you want to create a dependency graph that differs from the simple stage ordering. It makes the dependency explicit and visible in the pipeline graph.

***

## 1.11 Pipeline Triggering — Commit-Driven Automation

The pipeline triggers automatically **when a commit is pushed** to the repository. This is the fundamental CI mechanism: code change → automatic pipeline execution. In the lecture, the instructor commits and pushes the `.gitlab-ci.yml` file, which triggers the pipeline for the first time. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

In the GitLab UI (Build → Pipelines), each pipeline run shows:

* The **commit message** that triggered it
* The **commit ID**
* **What changed** (the diff)
* **Which branch** it ran for
* The **status** of each job (running, passed, failed)

You can click into individual jobs to see the full execution log, and you can **rerun a job** if needed. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

## 1.12 Account Verification Requirement

The instructor encounters a real failure: the first pipeline fails with the error *"Before you can run pipelines, we need to verify your account."* GitLab requires phone verification (SMS + puzzle) before allowing pipelines to execute. After verification, the pipeline does **not automatically rerun** — you must trigger it again by making another commit. The instructor does this by making a trivial change to `README.md` and pushing. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

⚠️ **Expert Note**: This is a one-time setup issue that can catch first-time GitLab users off guard. The pipeline will show as "failed," but the failure is not a code or YAML problem — it is an account-level gate. After verification, subsequent pipelines trigger normally. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

## 1.13 GitLab Templates — Learning the Syntax

GitLab provides built-in pipeline templates (visible when you click "Try Test template" in the Pipelines section). The instructor briefly shows the "Hello World" template, which demonstrates basic syntax and structure. However, the instructor chooses to create the pipeline manually in VSCode instead of using the template — the template is referenced only as a learning resource for understanding syntax. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (GUIDED EXECUTION MODE)

## What We Are Building

We are creating a two-stage GitLab CI pipeline (build + test) for the vprofile Java application. The pipeline will run inside Docker containers using a Maven image, triggered automatically on commits to the `main` branch. The final outcome: every push to `main` automatically builds the project with `mvn install` and runs tests with `mvn test` + `mvn checkstyle:checkstyle`. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195.FirstPipeline.yml)

***

## Step 1: Create the Pipeline File

In VSCode, with your repository open (already cloned and linked to GitLab from the previous lecture), click **New File** at the repository root. Name it exactly:

```
.gitlab-ci.yml
```

This name is mandatory — GitLab only recognizes this specific filename for pipeline definitions. The leading dot makes it a hidden file on Linux/macOS. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

## Step 2: Define the Stages

At the top of the file, declare the pipeline's stages:

```yaml
stages:
  - build
  - test
```

* **`stages:`** — top-level keyword that declares the ordered list of stages
* **`- build`** — first stage; runs first
* **`- test`** — second stage; runs after build completes

The order in this list defines the execution sequence. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195.FirstPipeline.yml)

***

## Step 3: Define Variables

```yaml
variables:
  PROJECT_NAME: "Vprofile-App"
```

* **`variables:`** — top-level keyword for pipeline-wide variables
* **`PROJECT_NAME:`** — variable name (convention: uppercase with underscores)
* **`"Vprofile-App"`** — value, accessible as `$PROJECT_NAME` in scripts

This variable is used in the build job's echo command. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195.FirstPipeline.yml)

***

## Step 4: Define the Build Job

```yaml
build-job:
  stage: build
  image: maven:3.9.9-eclipse-temurin-17
  only:
    - main
  script:
    - echo "Building project => $PROJECT_NAME"
    - mvn install
```

Breaking down each line:

* **`build-job:`** — job name (your label, appears in GitLab UI)
* **`stage: build`** — links this job to the `build` stage declared above. **Must match exactly** — a mismatch causes the error: *"stage build is not in the stages"*
* **`image: maven:3.9.9-eclipse-temurin-17`** — Docker Hub image to pull. Contains Maven 3.9.9 + JDK 17. The runner creates a container from this image and runs the script inside it
* **`only: - main`** — only triggers on commits to the `main` branch
* **`script:`** — list of shell commands to execute:
  * `echo "Building project => $PROJECT_NAME"` — prints the project name (using the variable)
  * `mvn install` — runs the full Maven build lifecycle [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195.FirstPipeline.yml)

**What happens internally when this job runs**:

1. GitLab's built-in runner receives the job
2. Runner pulls the `maven:3.9.9-eclipse-temurin-17` image
3. Runner creates a container from that image
4. Runner **automatically clones the repository** (correct branch, correct commit) into the container
5. Runner executes the `script` commands inside the container
6. Container is destroyed after the job completes [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

## Step 5: Define the Test Job

```yaml
test-job:
  stage: test
  image: maven:3.9.9-eclipse-temurin-17
  only:
    - main
  needs:
    - build-job
  script:
    - echo "Running tests on main branch..."
    - mvn test
    - mvn checkstyle:checkstyle
```

* **`test-job:`** — job name
* **`stage: test`** — links to the `test` stage. **Must match** the stage name declared in `stages:`
* **`image:`** — same Maven image (a new, separate container is created for this job)
* **`only: - main`** — same branch restriction
* **`needs: - build-job`** — explicit dependency: waits for `build-job` to succeed before starting
* **`script:`** — three commands:
  * `echo` — informational message
  * `mvn test` — runs unit tests
  * `mvn checkstyle:checkstyle` — runs Checkstyle code quality analysis [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195.FirstPipeline.yml)

**Connection to system flow**: This is a separate container from the build job. The source code is cloned fresh into this container. Each stage is fully independent in terms of environment. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

## Step 6: Save, Commit, and Push

Save the file (**Ctrl + S**).

In VSCode's Source Control panel: **Commit and Push**. Enter a commit message (e.g., "first build and test pipeline"). [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

**What happens next**: The commit push to GitLab triggers the pipeline automatically. Go to **GitLab → your project → Build → Pipelines** to see the pipeline status.

***

## Step 7: Handle Account Verification (First-Time Only)

If this is your first pipeline on a new GitLab account, you may see the pipeline status as **failed** with the message: *"Before you can run pipelines, we need to verify your account."* [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

1. Click **Verify My Account**
2. Enter your phone number
3. Receive SMS verification code
4. Solve the puzzle/captcha

After verification, the failed pipeline **will not automatically rerun**. You must trigger a new pipeline — see Step 8. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

## Step 8: Trigger a New Pipeline (After Verification)

Make any small change to trigger a new commit. The instructor edits `README.md` (adds an extra `#` character), saves, commits, and pushes. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

Go to **Build → Pipelines**. You should now see the pipeline in **running** status.

***

## Step 9: Monitor and Verify the Pipeline

### Pipeline Overview

Click on the **running** status badge. You'll see:

* The **commit message** that triggered the pipeline
* The **commit ID**
* The **diff** (what changed)
* The **branch** (main)
* The **job statuses** (build-job, test-job) [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

### Job Log Inspection

Click on **build-job** to see the full execution log. Key sections in the log:

1. **"Running with GitLab Runner"** — confirms the built-in runner is being used
2. **"Preparing docker+machine executor"** — confirms Docker executor type
3. **"Using Docker executor with image maven:3.9.9-eclipse-temurin-17"** — confirms the correct image was pulled
4. **"Running on \[runner name] via \[host]"** — shows which runner and host
5. **"Cloning repository"** — automatic source code clone (no instruction needed)
6. **"Executing step script"** — your `echo` and `mvn install` commands running
7. **Job status: succeeded** [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

### Pipeline Result

Return to the Pipelines view. Both jobs should show **passed** (green). The pipeline status shows as **passed**. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

### Rerunning Jobs

If needed, you can **rerun a job** directly from the pipeline UI without making a new commit. [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

## Common Mistakes and Failure Scenarios

| Mistake                                           | Symptom                               | Fix                                              |
| ------------------------------------------------- | ------------------------------------- | ------------------------------------------------ |
| Stage name mismatch (`stage: Build` vs `- build`) | Error: "stage X is not in the stages" | Match stage names exactly (case-sensitive)       |
| File named incorrectly (not `.gitlab-ci.yml`)     | No pipeline appears in GitLab UI      | Rename to exactly `.gitlab-ci.yml`               |
| Account not verified                              | Pipeline fails immediately            | Verify account → make a new commit               |
| Wrong Docker image name/tag                       | Job fails at image pull step          | Verify the image exists on Docker Hub            |
| Pushing to a non-main branch with `only: main`    | Pipeline does not trigger             | Push to `main` or remove the `only:` restriction |

 [\[195-first-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/195-first-pipeline.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Pipeline File Identity

```
File:     .gitlab-ci.yml (exact name, root of repo)
Format:   YAML
Trigger:  Commit push to repo → automatic pipeline execution
```

## Pipeline Structure Hierarchy

```
.gitlab-ci.yml
├── stages:          ← ordered list of stage names
│   ├── - build
│   └── - test
├── variables:       ← pipeline-wide key-value pairs
│   └── PROJECT_NAME: "Vprofile-App"
├── build-job:       ← job definition (name = UI label)
│   ├── stage: build     ← MUST match stages list exactly
│   ├── image: maven:... ← Docker Hub image for container
│   ├── only: - main     ← branch filter
│   └── script:          ← commands to execute
│       ├── - echo ...
│       └── - mvn install
└── test-job:
    ├── stage: test
    ├── image: maven:...
    ├── only: - main
    ├── needs: - build-job  ← explicit dependency
    └── script:
        ├── - echo ...
        ├── - mvn test
        └── - mvn checkstyle:checkstyle
```

## Execution Flow — What Happens on Commit Push

```
Developer commits + pushes to main
  → GitLab detects .gitlab-ci.yml
  → Pipeline triggered
  → Stage 1 (build):
  │   → Built-in runner receives job
  │   → Pulls maven:3.9.9-eclipse-temurin-17 image
  │   → Creates container
  │   → Auto-clones repo (correct branch + commit)
  │   → Executes script (echo + mvn install)
  │   → Container destroyed
  │   → Job: passed ✓
  → Stage 2 (test):
      → New container from same image
      → Auto-clones repo again
      → Executes script (echo + mvn test + mvn checkstyle)
      → Container destroyed
      → Job: passed ✓
  → Pipeline: passed ✓
```

## Runner + Executor Relationship

```
RUNNER = WHERE the job runs (machine/host)
  ├── Built-in (GitLab shared runners) ← used in this lecture
  └── Self-hosted (your EC2, VM, etc.) ← later lecture

EXECUTOR = HOW the job runs on the runner
  ├── Docker        ← majority of the time (container-based)
  ├── Shell         ← direct OS commands
  ├── SSH           ← remote execution
  ├── Kubernetes    ← pods in K8s cluster
  └── Parallels/VBox← VM-based

This lecture: Built-in runner + Docker+Machine executor
```

## Container Execution Model

```
image: keyword → Docker Hub image
  → Runner pulls image
  → Creates container
  → Auto-clones repo INTO container
  → Runs script commands IN container
  → Destroys container after job

Key property: Each job = fresh container = clean environment
              No state leakage between jobs
```

## Key YAML Keywords

```
stages:    → Declare ordered stage list
variables: → Define pipeline-wide variables ($VAR_NAME to use)
stage:     → Link job to a declared stage (MUST match exactly)
image:     → Docker image for container execution
script:    → List of shell commands to run
only:      → Branch filter (legacy; rules: is modern alternative)
needs:     → Explicit job dependency (wait for named job to complete)
```

## Naming Relationships (Strict Match)

```
stages:
  - build       ←──── MUST match exactly ────→ stage: build (in job)
  - test        ←──── MUST match exactly ────→ stage: test  (in job)

Mismatch → Error: "stage X is not in the stages"
Job name (build-job) = UI label only, no matching requirement
```

## Branch Filtering

```
only:
  - main

Effect: Job runs ONLY on main branch commits
        Other branches → job skipped
        
Note: "Better ways in next lecture" (rules: keyword)
```

## Auto-Clone Behavior

```
GitLab CI auto-clones the repo before running script
  → No checkout step needed (unlike some other CI systems)
  → Clones at correct branch + commit
  → Visible in job log as "Cloning repository"
```

## First-Time Gotcha

```
New GitLab account → First pipeline fails
  → "Before you can run pipelines, verify your account"
  → Phone verification (SMS + puzzle)
  → After verification: pipeline does NOT auto-retry
  → Must make a new commit to trigger pipeline again
```

## GitLab UI Navigation

```
Project → Build → Pipelines → [pipeline list]
  Click status → Pipeline details (commit, branch, jobs)
    Click job → Full execution log
      → Runner info
      → Executor type
      → Image pull
      → Repo clone
      → Script execution
      → Job result

Rerun: Available per-job from UI (no new commit needed)
```

## Job Log Reading Order

```
1. "Running with GitLab Runner"         → which runner
2. "Preparing docker+machine executor"  → which executor
3. "Using Docker executor with image…"  → which image
4. "Running on [runner] via [host]"     → where exactly
5. "Cloning repository"                 → auto source code fetch
6. "Executing step script"              → YOUR commands run here
7. Job status: succeeded/failed         → result
```

## GitHub Actions ↔ GitLab CI Mapping

```
GitHub Actions          GitLab CI
─────────────           ─────────
.github/workflows/*.yml → .gitlab-ci.yml (single file, repo root)
jobs:                   → stages: + job definitions
runs-on:                → runner (built-in or self-hosted)
uses: actions/checkout  → automatic (no step needed)
needs:                  → needs: (same keyword, same concept)
on: push: branches:     → only: - main (or rules:)
env:                    → variables:
container: image:       → image:
```

## Reusable Engineering Patterns

```
1. PIPELINE-AS-CODE
   Pipeline definition lives in the repo alongside the source code
   Versioned with Git → changes to pipeline are tracked like code changes
   Pattern: Infrastructure/automation config co-located with application code

2. EPHEMERAL EXECUTION ENVIRONMENT
   Each job → fresh container → destroyed after
   No state leakage, reproducible builds
   Pattern: Disposable compute for each unit of work

3. DECLARATIVE STAGE ORDERING
   stages: list declares execution order
   Jobs link to stages via stage: keyword
   Pattern: Declare structure, let the system enforce execution order

4. IMAGE-AS-TOOLCHAIN
   Docker image encapsulates all build tools (Maven, JDK)
   No manual installation → image = pre-packaged environment
   Pattern: Package tool dependencies as container images

5. COMMIT-DRIVEN AUTOMATION
   Push → pipeline triggers automatically
   Code change = automation trigger (no manual "run" needed)
   Pattern: Event-driven automation tied to version control events
```

## What's Next

```
This lecture: Basic pipeline (stages, jobs, image, script, only)
Next lecture: More variables, conditions, artifacts, advanced features
Later:        Self-hosted runners, runner configuration, executor selection
```

***

That completes the full reconstruction of the first GitLab CI pipeline lecture. The pipeline is now running automatically on every push to `main`, building and testing the vprofile application inside Docker containers. Would you like me to generate Anki flashcards from this material, or run a fill-in-the-blank recall test? 🚀

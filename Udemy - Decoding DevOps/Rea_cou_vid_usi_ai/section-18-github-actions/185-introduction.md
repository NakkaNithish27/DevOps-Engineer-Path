# 🎓 Introduction to GitHub Actions (Lecture 185)

**Video Title:** Introduction — GitHub Actions
**Context:** This lecture marks the beginning of a new section in the course — transitioning from Jenkins-based CI/CD to **GitHub Actions**, a CI/CD platform built directly into GitHub. This is a pure theory/overview lecture with no hands-on execution. It establishes what GitHub Actions is, why it exists, how its architecture works, its core terminology, and what it can do — setting the foundation for all subsequent hands-on lectures. [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

***

***

## 🧠 SECTION 1: THEORY — Deep Learning Mode

***

### 1. What GitHub Actions Is — A CI/CD Platform Built Into GitHub

The instructor opens with a direct definition: **"GitHub Actions is a CI/CD platform built into GitHub."** This is the single most important sentence of the lecture because it establishes a fundamental architectural difference from everything covered previously in the course. [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

With Jenkins, CI/CD required a **separate server** — you provisioned an EC2 instance, installed Jenkins, configured plugins, set up credentials, opened security group ports, and then connected Jenkins to your Git repository through webhooks or polling. The CI/CD platform (Jenkins) and the code repository (GitHub) were two independent systems that had to be integrated.

GitHub Actions eliminates that separation entirely. The CI/CD platform **lives inside** GitHub. When you log into your GitHub account and navigate to any repository, there is an **Actions** tab. That tab is where you configure, run, monitor, and manage your CI/CD pipelines. There is no separate server to set up, no software to install, no plugins to manage, no network rules to configure between two systems. The instructor reinforces this: **"When you log into GitHub account you can see a tab called Actions. That's where you can configure your entire CI/CD pipeline."** [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

This "built-in" nature is not merely a convenience — it represents a different architectural philosophy. Jenkins is a **general-purpose automation server** that can be connected to any Git provider. GitHub Actions is a **platform-native CI/CD system** that is tightly coupled with GitHub's own features (repositories, pull requests, issues, releases, packages, etc.). This tight coupling is both its greatest strength (seamless integration, zero setup overhead) and its constraint (it works only with GitHub repositories).

***

### 2. Why People Are Shifting to GitHub Actions — The Native Ecosystem Argument

The instructor makes a strategic observation: **"GitHub has become now an ecosystem where we not only have the GitHub repository, we have many other things. And GitHub Actions fits into this entire ecosystem. It can leverage this entire ecosystem. So that means it will be very easy to get started with GitHub Actions. And that is one of the main reasons why people are shifting to GitHub Actions, because it's just native."** [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

This is an important engineering insight. GitHub is no longer just a place to store code. It offers package registries (GitHub Packages), container registries (GitHub Container Registry), security scanning (Dependabot, code scanning), project management (Issues, Projects), documentation (GitHub Pages, Wikis), and identity/access management (GitHub Apps, OAuth). GitHub Actions can interact with **all** of these natively — without plugins, without API tokens for external services, without complex integration setups.

The word **"native"** is key. When a CI/CD tool is native to the platform where your code lives, it inherits all the context: it knows which repository triggered the build, which branch, which pull request, who the author is, what changed, and what permissions apply — all without configuration. In Jenkins, you had to manually set up every one of these connections.

The instructor's reasoning for the industry shift: **"You use GitHub, you can get started with GitHub workflows or GitHub Actions."** — the barrier to entry is essentially zero for anyone already using GitHub. [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

***

### 3. Workflows — The GitHub Actions Term for Pipelines

The instructor establishes terminology early: **"Just keep in mind, the pipelines — the CI/CD pipeline in GitHub Actions are called as workflows."** [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

This is a direct mapping:

| Jenkins Term | GitHub Actions Term |
| ------------ | ------------------- |
| Pipeline     | Workflow            |
| Jenkinsfile  | Workflow YAML file  |

A **workflow** in GitHub Actions is the complete definition of an automated process — what triggers it, what jobs it runs, in what order, on what machines, and with what steps. It is the equivalent of a Jenkins pipeline, but defined differently and executed differently.

***

### 4. Workflow Files — YAML Format and File Location

**"This workflow will be written in a text file and that will have the YAML format."** The instructor then specifies the required file location: **".github/workflows/main.yml — that will be your main workflow file."** [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

This is an architectural design choice with significant implications:

**YAML format:** Unlike Jenkins, which uses Groovy (a full programming language) for its Jenkinsfile, GitHub Actions uses **YAML** — a declarative data serialization format. YAML is simpler and more readable than Groovy, but it's also less flexible. You declare *what* you want to happen, not *how* to implement it programmatically. This makes workflows easier to write and read for most engineers, but limits complex conditional logic compared to Groovy-based Jenkinsfiles.

**File location (`.github/workflows/`):** The workflow file must exist inside a specific directory structure within the repository: `.github/workflows/`. This is a **convention enforced by GitHub** — GitHub automatically scans this directory for YAML files and treats them as workflow definitions. You can have multiple workflow files (not just `main.yml`) — each one defines an independent workflow. The instructor uses `main.yml` as the example, but the filename can be anything as long as it's a `.yml` or `.yaml` file in the correct directory. [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

**The key implication:** The workflow definition is **version-controlled alongside the application code**. This is the same principle as Jenkins' "Pipeline script from SCM" approach (covered in Lecture 182), but in GitHub Actions, it's the **only** way — there is no equivalent of pasting a pipeline script into a UI. The workflow always lives in the repository.

> 🔍 **Deep Dive (Optional):**
> The `.github/` directory is a special directory in GitHub repositories. Beyond workflows, it can contain issue templates (`ISSUE_TEMPLATE/`), pull request templates (`PULL_REQUEST_TEMPLATE.md`), funding configuration (`FUNDING.yml`), and other GitHub-specific configurations. The `workflows/` subdirectory within it is specifically for GitHub Actions.

***

### 5. What You Can Do in a Workflow — Capabilities

The instructor lists the capabilities: **"You can automate your tasks for building, testing, deploying your artifacts, sending notifications, or you can think of any command that you want to run in your pipeline. You can put that in the workflows."** [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

This is functionally equivalent to what Jenkins does. The key insight is that GitHub Actions is **not limited to CI/CD** — it's a general-purpose automation platform. Anything you can express as a sequence of commands can be a workflow: generating documentation, running database migrations, publishing packages, sending Slack messages, labeling issues, enforcing code review policies, and more.

***

### 6. Language and Platform Support

**"Any language of code you are going to build or deploy — Java, Python, Ruby, Node.js — or any platform that you have specific — Windows or Linux or macOS."** [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

This establishes that GitHub Actions is language-agnostic and platform-agnostic. It doesn't care what language your project uses — the workflow simply runs whatever commands you specify. And because runners (the machines that execute workflows) are available in Linux, Windows, and macOS flavors, you can build and test on any platform.

***

### 7. Actions and the GitHub Marketplace — The Extension System

The instructor introduces **Actions** as the extension mechanism: **"Pre-built actions available in GitHub Marketplace, which you can use to perform various tasks in your workflow."** He then lists examples: clone source code, build Docker images, deploy to GCP/AWS/Azure/Kubernetes, lint code, do code analysis, SSH, code quality, code review, CI, deployment. [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

An **Action** in GitHub Actions is a **reusable, pre-packaged unit of automation** — analogous to a Jenkins plugin, but more granular. While a Jenkins plugin is installed server-wide and adds broad capabilities, a GitHub Action is referenced per-step in a workflow and performs a specific task.

The **GitHub Marketplace** is the public catalog of these actions. Anyone can publish an action, and anyone can use it in their workflows by referencing it. For example, instead of writing complex shell commands to check out code, set up Java, or deploy to AWS, you reference community or official actions that encapsulate that logic.

The instructor emphasizes the breadth: **"There are many, many available actions that you can use in your workflows."** This ecosystem is one of GitHub Actions' strongest advantages — most common CI/CD tasks have well-maintained, ready-to-use actions. [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

> 🔍 **Deep Dive (Optional):**
> The relationship between Actions and workflows mirrors a plugin/framework relationship. The workflow is the framework (it defines structure, order, triggers, and environment), and actions are the plugins (they provide specific capabilities). But unlike Jenkins plugins which are installed globally, actions are declared per-workflow, per-step — making workflows self-contained and portable. Two different workflows in the same repository can use completely different actions without any global installation or conflict.

***

### 8. Runners — Where Workflows Actually Execute

The instructor introduces the concept of runners: **"By default this runs on the predefined runners. In your workflow jobs, you can select where do you want to run all the steps from the job."** [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

A **runner** is the **machine** (physical or virtual) that executes the steps in a workflow job. It is the equivalent of the Jenkins server (or Jenkins agent/node) — the actual compute environment where commands run.

**Predefined (GitHub-hosted) runners:** GitHub provides runners out of the box. You simply specify the platform in your workflow: [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

```yaml
runs-on: ubuntu-latest
```

This tells GitHub Actions to execute the job on a fresh Ubuntu virtual machine that GitHub manages. You don't need to provision, configure, or maintain this machine. GitHub provides Ubuntu, Windows, and macOS runners. The instructor explicitly mentions: **"You can mention you want to run this job on Linux platform or Windows or macOS. You can select Ubuntu specifically."** [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

**Self-hosted (custom) runners:** You can also register your own machines as runners. The instructor gives an example: **"Let's say you want to add an EC2 instance as a runner in your workflow. You can mention that."** This is useful when you need specific hardware, software, or network access that GitHub's predefined runners don't provide. [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

**The architectural parallel with Jenkins:** In Jenkins, the Jenkins server itself (or its agents) is the runner. You had to provision an EC2 instance, install Jenkins, install all tools (Java, Maven, Docker, AWS CLI), and manage it yourself. With GitHub-hosted runners, all of that management disappears — the runner is ephemeral, pre-configured, and managed by GitHub. With self-hosted runners, you return to the Jenkins-like model of managing your own infrastructure, but you gain the flexibility to use specialized environments.

> ⚠️ **Expert Note (Optional):**
> GitHub-hosted runners are ephemeral — they're created fresh for each job and destroyed afterward. This means every job starts with a clean environment (no leftover files, no cached state from previous runs). This is both an advantage (clean, reproducible builds) and a limitation (no persistent cache by default, though caching actions exist). Self-hosted runners persist, so they can accumulate state — which is both useful (faster builds via caching) and risky (dirty environments causing inconsistent results).

***

### 9. Triggers — What Causes a Workflow to Run

**"You can trigger your workflow on various events like a commit on your branch, a pull request. You can schedule a workflow. And there are many other events that happen in your GitHub account. You can use those events as a trigger to run your workflows."** [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

This maps directly to the Jenkins trigger concepts from Lecture 182:

| Jenkins Trigger       | GitHub Actions Equivalent                           |
| --------------------- | --------------------------------------------------- |
| Git Webhook (on push) | `on: push` event                                    |
| Poll SCM              | Not needed (native, so push events are direct)      |
| Scheduled job (cron)  | `on: schedule` with cron expression                 |
| Remote trigger (API)  | `on: workflow_dispatch` (manual/API)                |
| Build after project   | `on: workflow_run` (trigger after another workflow) |

The critical difference: in Jenkins, triggers required **external configuration** (setting up webhooks in GitHub, configuring poll intervals, creating API tokens). In GitHub Actions, triggers are **declarative** — you simply write `on: push` in your YAML file, and GitHub internally handles the event routing because the workflow lives inside the same platform as the repository. There's no webhook URL to configure, no network connectivity to establish, no poll interval to tune. [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

The instructor also hints at a much broader event model: **"There are many other events that happen in your GitHub account."** This refers to the fact that GitHub Actions can trigger on dozens of event types beyond just push and pull request — issue creation, release publication, label changes, wiki edits, discussion posts, package publications, and more. This is a capability Jenkins doesn't have natively.

***

### 10. Core Concepts — The Hierarchical Architecture

The instructor concludes the theory with a formal definition of core terminology: **"Workflow. These are defined in the YAML file. In general terminology you can also call it as a CI/CD pipeline. Workflow is a CI/CD pipeline written in YAML format. In workflow, you have various jobs that you can mention like build job, test job, deploy job. And you can define on which runner you want to run the job. Job consists of multiple steps or a single step. Each step means a task. You could be running a script, could be running a command, or you could be using predefined actions available in GitHub Marketplace. Mostly your workflow steps will consist of various actions and the runner of course."** [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

This defines a clear **four-level hierarchy**:

**Workflow** → The top-level container. One YAML file = one workflow. Equivalent to a Jenkins pipeline. Defines what triggers it and what jobs it contains.

**Job** → A named unit of work within a workflow (e.g., `build`, `test`, `deploy`). Each job runs on a **specific runner**. Jobs can run in parallel (by default) or sequentially (if dependencies are defined). Each job gets its own fresh runner environment.

**Step** → A single task within a job. Steps execute **sequentially** within a job (they always run in order). A step can be a shell command, a script, or a reference to a pre-built action.

**Action** → A reusable, pre-packaged automation unit used within a step. Actions come from the GitHub Marketplace or can be custom-built. They encapsulate complex logic into a single step reference.

**Runner** → The machine where a job executes. Defined per-job, not per-step. All steps in a job share the same runner.

The instructor lists the five terms to remember: **"Workflow. Job. Step. Action. Runner."** [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

> 🔍 **Deep Dive (Optional):**
> The relationship between jobs and runners is one-to-one per execution: each job gets its own runner instance. This means if you have a `build` job and a `test` job, they run on **different machines** (even if both specify `ubuntu-latest`). Files created in the `build` job are **not automatically available** in the `test` job — you must explicitly pass data between jobs using **artifacts** or **outputs**. This is fundamentally different from Jenkins, where all stages in a pipeline typically share the same workspace on the same server.

***

### 11. Use Cases — What GitHub Actions Is Used For

The instructor summarizes: **"You can use it to set up continuous integration pipeline or continuous delivery pipeline. You can build your code, test your code. You can do code quality checks, you can do security scans and any other kind of automation or command or scripts that you want to run from your workflow."** [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

This confirms that GitHub Actions covers the same ground as the Jenkins CI/CD pipeline built throughout the course — fetch, build, test, analyze, containerize, deploy — plus any additional automation you need. The transition from Jenkins to GitHub Actions is not about gaining new capabilities; it's about **reducing operational overhead** and leveraging native platform integration.

***

***

## ⚙️ SECTION 2: PRACTICAL — Guided Execution Mode

***

### What We Are Building

This lecture is a **pure introduction** — there are no hands-on commands to execute. The instructor explicitly closes with: **"Okay, that was enough talking. Now let's get into action with GitHub actions. So join me in the next lecture."** [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

However, the lecture does establish several **operational reference points** that will be used in all subsequent practical lectures. These are worth documenting now because they form the foundation of every hands-on exercise that follows.

***

### Operational Reference 1: Where to Find GitHub Actions in the UI

When you log into GitHub and navigate to any repository, you will see a tab labeled **Actions** in the top navigation bar (alongside Code, Issues, Pull requests, etc.). Clicking this tab takes you to the GitHub Actions dashboard for that repository, where you can view workflow runs, configure new workflows, and monitor pipeline status. [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

***

### Operational Reference 2: Where to Place Workflow Files

Every workflow file must be placed in a specific directory within your repository: [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

    .github/workflows/

The instructor uses `main.yml` as the example filename, giving the full path:

    .github/workflows/main.yml

This directory must exist in the repository for GitHub to detect and execute workflows. If the directory doesn't exist, you create it. If a YAML file is placed anywhere else, GitHub will not recognize it as a workflow.

***

### Operational Reference 3: Selecting a Runner

In the workflow YAML file, each job specifies its runner using the `runs-on` key. The instructor gives one concrete example: [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

```yaml
runs-on: ubuntu-latest
```

This tells GitHub Actions to execute the job on the latest available Ubuntu runner. Other options include `windows-latest` and `macos-latest` for GitHub-hosted runners, or a custom label for self-hosted runners.

***

### Operational Reference 4: Workflow File Format

The workflow file uses **YAML syntax**. The instructor shows (by reference) that all configuration — triggers, jobs, runners, steps, actions — is declared within this single YAML file. No external UI configuration is needed for the pipeline definition itself. Everything is code. [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

***

### What to Prepare for the Next Lecture

The instructor signals that hands-on work begins immediately in the next lecture: **"Let's get into action with GitHub Actions."** Based on the concepts covered, you should ensure:

1.  You have a **GitHub account** with access to repository creation.
2.  You are familiar with the **Actions tab** in the GitHub UI.
3.  You understand that workflow files go in `.github/workflows/`.
4.  You understand the hierarchy: Workflow → Jobs → Steps → Actions.

No servers to provision, no software to install, no security groups to configure — this is the operational simplicity the instructor was describing. [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

***

***

## 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

### Core Identity

    GitHub Actions = CI/CD platform INSIDE GitHub (not external like Jenkins)
    Workflow       = Pipeline (YAML, not Groovy)
    Location       = .github/workflows/<name>.yml

 [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

***

### Architectural Hierarchy

    WORKFLOW (YAML file)
      ├── triggered by: EVENT (push, PR, schedule, manual, other GitHub events)
      │
      ├── JOB: build
      │     ├── runs-on: RUNNER (ubuntu-latest / windows / macOS / self-hosted)
      │     ├── step 1: ACTION (from Marketplace) or COMMAND (shell)
      │     ├── step 2: ...
      │     └── step N: ...
      │
      ├── JOB: test
      │     ├── runs-on: RUNNER
      │     └── steps...
      │
      └── JOB: deploy
            ├── runs-on: RUNNER
            └── steps...

 [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

***

### Jenkins → GitHub Actions Translation Map

    Jenkins Server        →  GitHub Platform (no server needed)
    Jenkinsfile (Groovy)  →  .github/workflows/*.yml (YAML)
    Pipeline              →  Workflow
    Stage                 →  Job
    Step                  →  Step
    Plugin                →  Action (from Marketplace)
    Jenkins Agent/Node    →  Runner (GitHub-hosted or self-hosted)
    Webhook config (ext)  →  on: push (declarative, internal)
    Poll SCM              →  Not needed (events are native)
    Manage Jenkins UI     →  Actions tab in repository
    Plugin installation   →  Action reference in YAML (per-workflow, no install)
    Credential store      →  GitHub Secrets (repository/org level)

 [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

***

### Runner Model

    GITHUB-HOSTED (predefined):
      ├── ubuntu-latest   ── ephemeral, fresh each run, managed by GitHub
      ├── windows-latest  ── same
      └── macos-latest    ── same

    SELF-HOSTED (custom):
      └── Your own machine (e.g., EC2) ── persistent, you manage it

Key difference from Jenkins: Each **job** gets its own runner. Steps share a runner. Jobs do **not** share runners. [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

***

### Trigger Model

    EVENT                    →  WORKFLOW EXECUTION
    ─────────────────────────────────────────────
    push (commit)            →  instant (native, no webhook setup)
    pull_request             →  instant
    schedule (cron)          →  time-based
    workflow_dispatch        →  manual / API
    workflow_run             →  after another workflow completes
    issues / releases / etc  →  any GitHub platform event

 [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

***

### Why GitHub Actions Exists — Decision Chain

    Problem: Jenkins requires separate infrastructure → setup overhead → integration complexity
        ↓
    Insight: Code already lives in GitHub → CI/CD should too
        ↓
    Solution: CI/CD platform native to GitHub → zero external infrastructure
        ↓
    Result: Workflow = YAML in repo → triggers = native events → runners = managed
        ↓
    Advantage: No servers, no plugins to install, no webhooks to configure, instant start
        ↓
    Tradeoff: Only works with GitHub (not GitLab, Bitbucket, etc.)

 [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

***

### Core Engineering Pattern: Platform-Native Automation

    PATTERN: Instead of connecting external tools to a platform,
             embed the automation inside the platform itself.

    Jenkins model:  [GitHub] ──webhook──→ [Jenkins Server] ──API──→ [Nexus/ECR/SonarQube]
                    (3 separate systems, manual integration)

    Actions model:  [GitHub + Actions + Marketplace + Runners]
                    (1 ecosystem, declarative configuration)

    Tradeoff:       Flexibility (Jenkins) vs. Simplicity (Actions)
                    Vendor-neutral vs. Vendor-locked

 [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

***

### Five Terms — Instant Recall

    WORKFLOW  = the pipeline (YAML file, one per file)
    JOB       = a unit of work within a workflow (runs on one runner)
    STEP      = a single task within a job (sequential)
    ACTION    = a reusable automation package (Marketplace or custom)
    RUNNER    = the machine executing a job (GitHub-hosted or self-hosted)

 [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

***

### Operational Quick-Start Checklist (for next lectures)

    ✅ GitHub account
    ✅ Repository with .github/workflows/ directory
    ✅ YAML workflow file in that directory
    ✅ runs-on: specified per job
    ✅ on: trigger event declared
    ✅ Steps using actions or shell commands
    → No servers, no installs, no plugins, no webhooks to configure

 [\[185-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/185-introduction.txt)

***

This lecture is purely foundational — no commands to execute, no infrastructure to build. Its entire value is in establishing the **mental model** and **terminology** that all subsequent GitHub Actions lectures depend on. The next lecture begins hands-on work. Shall I save this as a downloadable markdown file?

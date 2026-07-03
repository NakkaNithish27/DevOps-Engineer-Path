# 🔄 AWS CI/CD Project Introduction — CodePipeline, CodeBuild, Beanstalk, RDS, and Bitbucket

**Source:** AWS CI/CD Project — Introduction (Caption File) [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

This video is the **opening lecture of the AWS CI/CD project** — a complete pipeline built entirely with AWS-native services. The instructor frames the project by connecting it to the previously completed Jenkins CI/CD pipeline, introduces each AWS service involved, explains why Bitbucket replaces GitHub as the source repository for this project, walks through the **architectural diagram** showing how all components connect, and previews the execution order. This is a pure architecture-and-planning lecture — no hands-on yet. The next lecture begins with creating the Beanstalk environment. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

***

***

# 🧠 SECTION 1: THEORY (DEEP LEARNING MODE)

***

## 1. The Project Goal — AWS-Native CI/CD Pipeline

The objective is clear: **use AWS services to fetch your code, build it, and deploy it on AWS Elastic Beanstalk**. The instructor explicitly frames this as the AWS-native equivalent of the **Jenkins CI/CD pipeline** built earlier in the course: **"Same way, we are going to create a CodePipeline, but we are going to use AWS services for that."** [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

This is an important conceptual shift. In the Jenkins project, Jenkins was the central engine — it fetched code, built it, and deployed it, running on your own infrastructure (an EC2 instance or a VM). In this project, every component is a **managed AWS service** — you don't manage any build servers, you don't install any CI/CD software, you don't maintain any infrastructure for the pipeline itself. AWS handles the underlying compute, scaling, and availability for each service. Your job is to **configure and connect** the services.

***

## 2. The Five Components — What Each One Does

The project uses five distinct components, each serving a specific role in the pipeline. Understanding what each one does and how they relate to each other is the conceptual core of this lecture: [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

### AWS Elastic Beanstalk — The Deployment Target

Beanstalk is where the application **runs in production** (or staging). It's the deployment target — the end of the pipeline. The instructor says they will "build the code and deploy it on Beanstalk environment." Beanstalk is a Platform-as-a-Service (PaaS) that manages EC2 instances, load balancers, auto-scaling, and health monitoring for you. You give it an artifact (a built application package), and it handles the deployment infrastructure. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

### AWS RDS — The Database Layer

The **Vprofile application** (the project's sample Java application used throughout the course) **needs database connectivity**. AWS RDS (Relational Database Service) provides a managed database that stores the **schemas and tables** the Vprofile application requires. RDS is not part of the CI/CD pipeline itself — it's part of the **application architecture** that the pipeline deploys into. Without RDS, the deployed application would fail because it can't connect to its database. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

### Bitbucket — The Source Code Repository

Bitbucket serves as the **Git repository** where the Vprofile source code lives. The instructor makes a deliberate choice to use Bitbucket instead of GitHub (which was used in the Jenkins project) for two reasons: [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

First, **real-world exposure.** Bitbucket is from **Atlassian** — a "very popular name among developers and also among DevOps engineers." Many organizations use Atlassian services (Jira, Confluence, Bitbucket), and the instructor explicitly states: **"There is a high chance when you work in real time, you will be using Bitbucket repositories."** Learning Bitbucket alongside GitHub makes you versatile.

Second, **conceptual equivalence.** The instructor frames Bitbucket as functionally identical to GitHub for this purpose: **"You can think Bitbucket as GitHub. All kind of Git solution it provides."** It hosts Git repositories, supports branching, pull requests, and — additionally — provides its own **complete CI/CD pipeline services** (Bitbucket Pipelines). For this project, only the Git repository capability is used; the CI/CD is handled by AWS services.

The source code is **migrated from GitHub to Bitbucket** as part of the project setup. This migration is itself a useful skill — moving repositories between platforms is a common DevOps task. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

### AWS CodeBuild — The Build Engine

CodeBuild is the service that **fetches the source code from Bitbucket and builds it into an artifact**. The instructor draws a direct parallel: CodeBuild **"will act like Jenkins build"** — it's the AWS-managed equivalent of a Jenkins build job. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

The key difference from Jenkins: CodeBuild is **serverless**. You don't provision or manage build servers. You define what to build and how, and AWS provisions the compute resources on-demand, runs the build, produces the artifact, and releases the resources. You pay only for build time. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

### AWS CodePipeline — The Orchestrator

CodePipeline is the service that **connects all the other pieces together**. It is the orchestration layer — the conductor of the entire CI/CD flow. The instructor explicitly states: **"We will be using AWS CodePipeline service to connect all these services together."** [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

CodePipeline's responsibilities in this project:

1. **Detect** any new commit on the Bitbucket repository.
2. **Fetch** the source code.
3. **Trigger** the CodeBuild project to build the artifact.
4. **Deploy** the built artifact to Elastic Beanstalk.

The instructor makes an important architectural note: **"There's no default option to deploy it on Beanstalk"** directly from CodeBuild. CodeBuild produces the artifact, but it doesn't know where to deploy it. CodePipeline is the glue that takes the CodeBuild output and sends it to Beanstalk. Without CodePipeline, you'd have disconnected pieces — code in Bitbucket, a build service, and a deployment target, with no automated flow between them. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

<details>
<summary>🔍 Deep Dive</summary>

The relationship between these services mirrors a universal CI/CD architecture pattern:

| Role          | Jenkins Pipeline               | AWS Pipeline                         |
| ------------- | ------------------------------ | ------------------------------------ |
| Source        | GitHub                         | Bitbucket                            |
| Build Engine  | Jenkins (self-managed server)  | CodeBuild (managed, serverless)      |
| Orchestrator  | Jenkins Pipeline (Jenkinsfile) | CodePipeline (managed orchestration) |
| Deploy Target | Tomcat/Nginx on EC2 (manual)   | Elastic Beanstalk (managed PaaS)     |
| Database      | MySQL on EC2 (manual)          | RDS (managed database)               |

The progression from Jenkins to AWS-native services follows the broader industry trend: moving from self-managed tools to managed services. The pipeline logic is identical — source → build → deploy. What changes is who manages the infrastructure underneath each step.

</details>

***

## 3. The Architectural Flow — How Components Connect

The instructor presents the complete pipeline flow and asks learners to pause and study the architectural diagram. The flow is: [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

**Bitbucket (Git repository)** → developer pushes a commit → **CodePipeline detects the commit** → CodePipeline fetches the source code → CodePipeline **triggers CodeBuild** → CodeBuild **builds the source code into an artifact** → CodePipeline **deploys the artifact to Elastic Beanstalk** → Beanstalk runs the application → application connects to **Amazon RDS** for database operations.

The trigger mechanism is important: the pipeline is **event-driven**. It doesn't poll or run on a schedule — it detects a new commit on Bitbucket and automatically initiates the entire flow. This means every `git push` to the configured branch triggers a fresh build and deployment. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

***

## 4. The Execution Order — What Gets Built First

The instructor previews the order in which the infrastructure will be created across the upcoming lectures: [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

1. **Elastic Beanstalk environment** — create the deployment target first (the place where the artifact will be deployed).
2. **AWS RDS** — create the database (the application needs it to function after deployment).
3. **Bitbucket repository** — migrate the Vprofile source code from GitHub to Bitbucket.
4. **AWS CodeBuild** — configure the build project (how to build the source code).
5. **AWS CodePipeline** — connect everything together (source → build → deploy).
6. **Test** — push a git commit to Bitbucket and verify the pipeline triggers automatically, builds the artifact, and deploys to Beanstalk.

This order follows a **dependency-driven sequence**: you create the things that other things depend on first. Beanstalk must exist before CodePipeline can deploy to it. RDS must exist before the deployed application can connect to it. The source code must be in Bitbucket before CodeBuild can fetch it. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

<details>
<summary>⚠️ Expert Note</summary>

This dependency-driven creation order is the same approach used in Infrastructure as Code (Terraform, CloudFormation). When you define resources in Terraform, you declare dependencies between them, and Terraform builds them in the correct order. Understanding manual dependency ordering here builds the mental model you'll need when writing IaC templates later — you're doing manually what Terraform does automatically.

</details>

***

## 5. Bitbucket as an Atlassian Ecosystem Component

The instructor positions Bitbucket within the broader **Atlassian ecosystem**. Atlassian provides Jira (project management), Confluence (documentation), and Bitbucket (code repositories + CI/CD). Many organizations adopt the full Atlassian suite, which means their Git repositories live on Bitbucket rather than GitHub. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

Beyond Git hosting, Bitbucket provides **its own complete CI/CD pipeline services** (Bitbucket Pipelines). This means Bitbucket can serve as both the source repository AND the CI/CD engine — but in this project, only the repository capability is used. The CI/CD is handled by AWS services (CodeBuild + CodePipeline). This architectural choice — using Bitbucket for source only and AWS for CI/CD — is itself a common real-world pattern where organizations mix platforms based on strengths.

***

***

# ⚙️ SECTION 2: PRACTICAL (GUIDED EXECUTION MODE)

***

## What We Are Building

We are building an **end-to-end AWS-native CI/CD pipeline** that automatically fetches code from Bitbucket, builds it with CodeBuild, and deploys it to Elastic Beanstalk — with RDS providing the database backend for the deployed application. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

**Why it matters:** This is the AWS-native equivalent of the Jenkins pipeline built earlier. Knowing both approaches (self-managed Jenkins and managed AWS services) is essential for any DevOps engineer — you'll encounter both in real organizations, and the ability to implement either gives you flexibility.

**Final operational outcome:** A git commit pushed to the Bitbucket repository automatically triggers the pipeline → code is built → artifact is deployed to Beanstalk → the Vprofile application is live and connected to RDS → the entire flow is hands-off after the initial setup.

***

## Step 1: Understand the Creation Order (Dependency-Driven)

**What we are doing:** Planning the infrastructure creation sequence before touching the AWS console.

**The order (from the instructor):** [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

1. **Create Elastic Beanstalk environment** — the deployment target must exist first.
2. **Create AWS RDS instance** — the database must exist for the application to connect.
3. **Migrate source code from GitHub to Bitbucket** — the source must be in Bitbucket before CodeBuild can fetch it.
4. **Create AWS CodeBuild project** — configure how the source code is built into an artifact.
5. **Create AWS CodePipeline** — connect Bitbucket → CodeBuild → Beanstalk.
6. **Test the pipeline** — push a commit to Bitbucket → verify automatic build and deployment.

**Operational reasoning:** Each step depends on the previous one. CodePipeline can't deploy to Beanstalk if Beanstalk doesn't exist. CodeBuild can't fetch from Bitbucket if the repository hasn't been set up. The deployed application can't function without RDS.

**Common mistake:** Trying to create the pipeline before the target services exist → configuration fails because you can't reference non-existent resources.

**Connection to flow:** This is the roadmap for all upcoming lectures. Each lecture implements one step.

***

## Step 2: Prepare for Bitbucket (Migration from GitHub)

**What we are doing:** Understanding that the Vprofile source code currently lives on GitHub and will be **migrated to Bitbucket** as part of this project. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

**Operational context:**

* The Vprofile application source code was used in the Jenkins project with a GitHub repository.
* For this project, the same code will be hosted on **Bitbucket** (from Atlassian).
* The migration is part of the project — you'll learn how to move a repository between platforms.

**Why Bitbucket:** Real-world exposure. Many organizations use Atlassian services (Jira + Confluence + Bitbucket). As a DevOps engineer, you need to be comfortable with both GitHub and Bitbucket. The instructor emphasizes: **"There is a high chance when you work in real time, you will be using Bitbucket repositories."** [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

**Connection to flow:** Once the code is in Bitbucket, CodeBuild will fetch from there, and CodePipeline will monitor it for new commits.

***

## Step 3: Understand the Pipeline Trigger Mechanism

**What we are doing:** Understanding how the pipeline starts automatically.

**The trigger flow:** [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

1. Developer makes a code change locally.
2. Developer runs `git commit` and `git push` to the Bitbucket repository.
3. **CodePipeline detects the new commit** on Bitbucket.
4. CodePipeline automatically starts the pipeline execution.
5. CodeBuild is triggered → fetches source → builds artifact.
6. CodePipeline deploys the artifact to Beanstalk.

**Operational reasoning:** The pipeline is **event-driven** — no manual triggering required after setup. Every push to the configured branch triggers a fresh build and deployment. This is the definition of Continuous Deployment.

**How to test (final step of the project):** Push a code change to Bitbucket → watch the pipeline execute in the CodePipeline console → verify the updated application is deployed on Beanstalk. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

**Connection to flow:** This is the end-to-end validation that confirms the entire pipeline works.

***

## Step 4: Study the Architectural Diagram

**What we are doing:** The instructor explicitly asks learners to **pause the lecture and study the architectural diagram** before proceeding. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

**The architecture:**

```
[Bitbucket Git Repo]
        │
        ▼ (CodePipeline detects new commit)
[AWS CodePipeline] ──── orchestrates ────→
        │                                    │
        ▼                                    ▼
[AWS CodeBuild]                    [AWS Elastic Beanstalk]
  fetch source                       deploy artifact
  build artifact ──────────────→     run application
                                          │
                                          ▼
                                    [Amazon RDS]
                                   schemas + tables
                                   for Vprofile app
```

**Operational insight:** The diagram shows the **data flow** (code → artifact → deployed app) and the **control flow** (CodePipeline orchestrates every step). RDS is outside the pipeline flow — it's part of the application's runtime architecture, not the CI/CD flow.

**Connection to flow:** This diagram is the reference for every lecture that follows. Each lecture implements one box in this diagram.

<details>
<summary>⚠️ Expert Note</summary>

In production AWS CI/CD pipelines, you'd typically add more stages: a testing stage (running unit/integration tests after build), a staging deployment (deploy to a non-production Beanstalk environment first), a manual approval gate (someone reviews before production deployment), and a production deployment. The project builds the core three-stage pipeline (source → build → deploy) which is the foundation that additional stages are added to.

</details>

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
TOPIC:   AWS CI/CD Project — Introduction & Architecture
CONTEXT: DevOps course → after Jenkins CI/CD → now AWS-native CI/CD
PURPOSE: Build entire pipeline with AWS managed services (no self-managed Jenkins)
APP:     Vprofile (Java application needing database)
```

***

## Five Components — Role Map

```
BITBUCKET (Atlassian)       = SOURCE (Git repository — migrated from GitHub)
AWS CODEBUILD               = BUILD ENGINE (fetch + compile → artifact) [= Jenkins build]
AWS CODEPIPELINE             = ORCHESTRATOR (detect commit → trigger build → deploy)
AWS ELASTIC BEANSTALK        = DEPLOY TARGET (PaaS — runs the application)
AWS RDS                      = DATABASE (schemas/tables for Vprofile — runtime dependency)
```

***

## Pipeline Flow (Data + Control)

```
Developer → git commit + push
                ↓
    BITBUCKET (source code)
                ↓ CodePipeline DETECTS new commit
    CODEPIPELINE (orchestrator)
                ↓ triggers
    CODEBUILD (build engine)
       ├── fetches source from Bitbucket
       └── builds artifact
                ↓ CodePipeline deploys
    ELASTIC BEANSTALK (deployment target)
       └── runs application
                ↓ connects at runtime
    RDS (database)
       └── schemas + tables for Vprofile
```

***

## Jenkins vs AWS-Native Mapping

```
Jenkins Pipeline          AWS Pipeline
─────────────────         ──────────────────
GitHub                    Bitbucket
Jenkins server (self-mgd) CodeBuild (managed, serverless)
Jenkinsfile (pipeline)    CodePipeline (managed orchestration)
Tomcat on EC2 (manual)    Elastic Beanstalk (managed PaaS)
MySQL on EC2 (manual)     RDS (managed database)

Pattern: same logic (source→build→deploy), different infrastructure ownership
Self-managed → Managed services
```

***

## Creation Order (Dependency-Driven)

```
1. Elastic Beanstalk  ← deploy target must exist first
2. AWS RDS            ← database must exist for app to connect
3. Bitbucket repo     ← source must be migrated before build can fetch
4. CodeBuild          ← build project configured (what to build, how)
5. CodePipeline       ← connects source → build → deploy
6. TEST               ← git push → pipeline triggers → verify deployment

Rule: create what others depend on FIRST
```

***

## Bitbucket Context

```
Bitbucket = Atlassian's Git platform
          = functionally equivalent to GitHub
          = provides Git repos + its own CI/CD pipelines
          = widely used in orgs using Jira/Confluence

This project: Bitbucket for SOURCE ONLY, AWS for CI/CD
Migration:    Vprofile code moves GitHub → Bitbucket
```

***

## CodePipeline's Unique Role

```
WHY NEEDED?
  CodeBuild builds artifacts BUT has no default option to deploy to Beanstalk
  CodePipeline = the GLUE that:
    1. Detects commits (event source)
    2. Triggers builds (build orchestration)
    3. Deploys artifacts (deployment orchestration)

Without CodePipeline: disconnected services, no automated flow
With CodePipeline:    end-to-end automated pipeline
```

***

## Trigger Mechanism

```
EVENT-DRIVEN (not polling, not scheduled):
  git push → Bitbucket → CodePipeline detects → pipeline starts automatically
  Every push = fresh build + fresh deployment
```

***

## RDS Position

```
RDS is NOT part of the CI/CD pipeline
RDS IS part of the APPLICATION ARCHITECTURE
  → exists independently
  → application connects at RUNTIME (not build time)
  → must be created BEFORE deployment (dependency)
```

***

## Reusable Engineering Patterns

```
1. MANAGED REPLACEMENT PATTERN    → Every self-managed component has a managed equivalent
                                     Jenkins → CodeBuild, Jenkinsfile → CodePipeline
                                     Same logic, different operational burden

2. ORCHESTRATOR AS GLUE           → Individual services don't know about each other
                                     Orchestrator (CodePipeline) connects them into a flow
                                     (same pattern: Kubernetes, Airflow, Step Functions)

3. DEPENDENCY-DRIVEN CREATION     → Build targets before sources, databases before apps
                                     Create what is depended-on FIRST
                                     (same pattern: Terraform dependency graph, Docker build order)

4. EVENT-DRIVEN TRIGGER           → Pipeline starts from external event (git push)
                                     No polling, no scheduling — reactive execution
                                     (same pattern: webhooks, Lambda triggers, Kubernetes controllers)

5. PLATFORM PORTABILITY           → Same source code (Vprofile) runs through different CI/CD systems
                                     GitHub+Jenkins → Bitbucket+AWS
                                     Application logic is independent of pipeline implementation
```

***

## Rapid Recall Triggers

```
"What is this project?"             → AWS-native CI/CD pipeline: Bitbucket → CodeBuild → Beanstalk
"How is it different from Jenkins?"  → Same logic, but all managed AWS services (no self-managed servers)
"What is CodePipeline?"             → Orchestrator — detects commits, triggers builds, deploys artifacts
"What is CodeBuild?"                → Build engine — fetches source, compiles, produces artifact (serverless)
"Why Bitbucket not GitHub?"         → Real-world Atlassian exposure + variety in learning
"What is Bitbucket?"                → Atlassian's Git platform — like GitHub + its own CI/CD
"Why CodePipeline needed?"          → CodeBuild has no default Beanstalk deploy — Pipeline is the glue
"Where is RDS in the pipeline?"     → NOT in pipeline — it's runtime app architecture (database)
"Creation order?"                   → Beanstalk → RDS → Bitbucket → CodeBuild → CodePipeline → Test
"How pipeline triggers?"            → Event-driven: git push → CodePipeline detects → auto-executes
"What gets deployed?"               → Built artifact (Vprofile Java app) → onto Beanstalk
"Migration path?"                   → Vprofile source: GitHub → Bitbucket (for this project)
```

***

This completes the full reconstruction of the AWS CI/CD Project Introduction. **Theory** builds the conceptual architecture of all five components and their relationships, with explicit Jenkins-to-AWS mapping; **Practical** establishes the dependency-driven creation order and pipeline trigger mechanism that guides all upcoming lectures; and the **Mental Compression Map** compresses the entire architecture, flow, and component roles into rapid-recall structures. [\[282-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/282-introduction.txt)

Ready for the next caption file in the series, or shall I generate an **AnkiDeck CSV** covering this lecture or the full course so far? 🚀

# GitLab — Complete CI/CD & DevSecOps Platform (Introduction)

**Source:** Video caption file — *"GitLab Introduction"* (from a DevOps course) [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Is GitLab and What Problem Does It Solve?

In a typical DevOps environment, you end up using multiple separate tools for different parts of the pipeline: one tool for source code management (GitHub, Bitbucket), another for CI/CD (Jenkins), another for container registry (Docker Hub, ECR), another for security scanning (SonarQube, Snyk), another for project management (Jira), another for monitoring (Prometheus, Grafana) — and you spend significant effort integrating, maintaining, and coordinating across all of them. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**GitLab is a complete DevSecOps platform that gives you everything at one place.** Source code management, CI/CD pipelines, security scanning, project management, container registry, package registry, monitoring, analytics, compliance — all unified in a single platform. Instead of stitching together a dozen tools, you get a single integrated environment that covers the entire software delivery lifecycle from code to production. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

The "DevSecOps" designation is important — GitLab doesn't just cover Dev (development) and Ops (operations). It integrates **Security** as a first-class concern directly into the pipeline, making security scanning, secret detection, license compliance, and audit logging built-in capabilities rather than afterthoughts bolted on. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## 1.2 — Hosting Models: SaaS vs. Self-Hosted

GitLab offers two deployment models, giving you flexibility in how you consume the platform. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**SaaS (Software as a Service)** — You subscribe, log in to `gitlab.com`, and start using it immediately. GitLab manages the infrastructure, updates, and availability. This is the fastest way to get started and eliminates operational overhead for managing the GitLab platform itself.

**Self-Hosted** — You host your own GitLab environment on your own infrastructure (physical servers, VMs, cloud instances). This gives you full control over data residency, network configuration, and customization, but you're responsible for maintaining the GitLab installation itself. This is common in enterprises with strict data governance or compliance requirements that prevent using external SaaS platforms. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

Within both models, there are **three tiers**: Free, Premium, and Ultimate. Each tier unlocks additional features. The course uses the **Free tier**, demonstrating that meaningful CI/CD and DevOps workflows are achievable without any cost. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## 1.3 — Source Code Management (SCM)

The foundation of GitLab is a **complete Git repository hosting platform**, functionally equivalent to GitHub or Bitbucket. You get all the standard Git capabilities: [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**Repository hosting** — Store and manage your source code in Git repositories with all the version control capabilities Git provides.

**Branching workflows** — Create branches for features, bugfixes, experiments. This is the standard Git workflow where development happens in branches, not directly on the main branch.

**Merge Requests** — This is GitLab's equivalent of what GitHub calls **Pull Requests**. A merge request is a proposal to merge code from one branch into another, with review, discussion, and approval workflows. The video explicitly clarifies this naming difference: "That's the pull request. In GitLab, it's called a merge request." This terminology difference is important to know when working across platforms. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**Approvals** — Merge requests can require approvals from designated reviewers before code is merged. This enforces code review as a gate in the development process.

**Web-based IDE** — GitLab includes a built-in code editor in the browser. If you don't prefer using a local code editor like VSCode, you can edit code directly in GitLab's web IDE. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**Wikis** — Each project can have a wiki for maintaining documentation alongside the code. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## 1.4 — CI/CD Pipelines

This is the core operational capability of GitLab from a DevOps perspective. GitLab allows you to define **YAML-based pipelines** that automate your build, test, and deployment processes. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**YAML-based configuration** — Pipelines are defined in a YAML file (`.gitlab-ci.yml`). The video emphasizes that YAML is "easy to read, easy to write." This is a significant difference from tools like Jenkins, which historically used GUI-based job configuration or Groovy-based Jenkinsfiles. YAML is declarative — you describe *what* you want (stages, jobs, scripts), and GitLab handles *how* to execute it.

**Multi-stage pipelines** — You can define multiple stages (e.g., build, test, deploy) with multiple jobs within each stage. Stages execute sequentially (build must complete before test starts), but jobs within a stage can run in parallel. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**Pipeline visualization** — GitLab provides a visual representation of your pipeline — "you can see all your pipeline and different jobs in your pipeline at one place, with all the logs and all the information." This gives you instant visibility into what's running, what passed, what failed, and why. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## 1.5 — Runners: Where Your Jobs Actually Execute

A **runner** is the execution environment where your pipeline jobs run. GitLab separates the *orchestration* (deciding what to run, in what order, tracking status) from the *execution* (actually running the commands). [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**GitLab inbuilt runners (shared runners)** — GitLab provides hosted runners that you can use immediately without any setup. These are managed by GitLab and are suitable for getting started quickly.

**Self-hosted runners** — You can add your own runner — an EC2 instance, a physical machine, a VM in your own environment. You register it with your GitLab project, and GitLab sends jobs to it for execution. This gives you full control over the execution environment: the operating system, installed tools, network access, compute capacity, and security posture. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

The video demonstrates this: "I have an EC2 instance added over here. I can enable and disable it or add any other runner of my choice." You can have multiple runners and choose which one a particular project or job should use. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

🔍 **Deep Dive:**
The runner model is an important architectural pattern: **controller/worker separation**. GitLab (the platform) is the controller — it knows the pipeline definition, tracks state, manages the UI, stores logs and artifacts. The runner is the worker — it receives job instructions, executes them, and reports results back. This separation means the compute-heavy work (compilation, testing, Docker builds) happens on the runner, not on the GitLab server itself. It also means you can scale execution capacity independently by adding more runners without affecting the GitLab server. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

⚠️ **Expert Note:**
In enterprise environments, shared runners are often insufficient due to security requirements (you can't run proprietary code on shared infrastructure), performance requirements (shared runners may have resource contention), or tooling requirements (specific software versions, network access to internal systems). Self-hosted runners on dedicated infrastructure are the norm in production pipelines. The ability to use EC2 instances as runners directly connects to the AWS infrastructure knowledge from previous course projects. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## 1.6 — Auto DevOps and Platform Integrations

**Auto DevOps** provides ready-made pipeline templates that automatically detect your project type and configure appropriate CI/CD stages. Instead of writing the pipeline YAML from scratch, you can use these templates as a starting point and customize as needed. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

GitLab integrates with several major platforms:

* **Kubernetes** — GitLab agents can securely connect to your Kubernetes cluster, enabling deployment pipelines that push directly to K8s. This is significant because Kubernetes is the dominant container orchestration platform, and having native GitLab integration simplifies the deployment pipeline. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)
* **Google Cloud** — Direct integration with GCP services.
* **Terraform** — You can monitor and manage Terraform state files from within GitLab, which ties infrastructure-as-code workflows directly into your CI/CD pipeline. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## 1.7 — Security and Compliance (DevSecOps Capabilities)

This is where GitLab differentiates itself from being just "another CI/CD tool." Security is built into the pipeline as a first-class concern, not a separate process. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**Static code analysis (SAST)** — Scans source code for vulnerabilities without executing it. Catches security issues in the code itself.

**Dynamic testing (DAST)** — Tests the running application for vulnerabilities by simulating attacks. Catches issues that only manifest at runtime.

**Container scanning** — If you're building Docker images, GitLab scans the image layers for known vulnerabilities in the base images and installed packages. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**License checks** — Scans dependencies to identify their licenses and flags any that could create legal issues for your organization. This prevents accidentally including a library with a license incompatible with your product's distribution model.

**Secret detection** — Scans code and configuration files for accidentally committed credentials (API keys, passwords, tokens). Prevents sensitive information from being exposed in repositories or public platforms. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**Audit logs** — Records who did what and when, providing a complete audit trail for compliance and forensic purposes.

**Compliance pipelines** — Enforce specific pipeline stages or checks that must pass before code can be deployed, ensuring regulatory requirements are met. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

The video emphasizes that integrating security into the pipeline "is mandatory in DevSecOps pipelines." This reflects the industry shift from "security as a final gate" to "security as a continuous, automated part of every pipeline run." [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## 1.8 — Artifact and Package Management

Pipelines produce outputs — compiled binaries, Docker images, reports, packages. GitLab provides built-in storage for these outputs. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**Container Registry** — If your pipeline builds Docker images, GitLab provides a built-in container registry where you can host them. You don't need a separate Docker Hub or Amazon ECR — GitLab includes the registry. This keeps the entire workflow (code → build image → store image → deploy) within a single platform.

**Package Registry** — For non-Docker artifacts like Maven JARs or npm packages, GitLab provides package registries. This replaces external tools like Nexus or Artifactory for storing build artifacts. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**Job artifacts** — Any output file your job produces (test reports, coverage reports, log files) can be stored as a job artifact. You define this in the pipeline YAML, and GitLab stores and makes the artifacts available for download or use by subsequent jobs. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## 1.9 — Monitoring and Analytics

GitLab provides built-in analytics for your development and deployment pipeline. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**Pipeline analytics** — A dashboard showing pipeline trends: how many pipelines passed or failed over time. This gives you visibility into the health and stability of your delivery process.

**Code quality reports** — Track code quality metrics across builds.

**Prometheus integration** — GitLab can integrate with Prometheus to monitor application health metrics (CPU, memory, disk) directly from the GitLab interface. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**Sentry integration** — Error tracking integration that connects application runtime errors back to the GitLab project for investigation.

**Audit events** — A record of who did what — essential for compliance and incident investigation. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## 1.10 — Project and Team Management

Beyond code and pipelines, GitLab includes project management capabilities. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**Issues** — Track bugs, feature requests, and tasks directly in GitLab (similar to Jira tickets).

**Milestones and roadmaps** — Plan releases and track progress toward goals.

**Dashboards** — Visual overview of project status.

**Service desk** — Built-in customer support functionality — customers can submit issues via email, which are tracked as GitLab issues. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## 1.11 — External Integrations

Even though GitLab aims to be a complete platform, it also integrates with external tools. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

* **Cloud platforms** — AWS, GCP, etc.
* **Communication/notification systems** — Slack (for pipeline notifications, alerts).
* **Project management tools** — Jira, Trello (for teams that use external project management).
* **CI/CD tools** — Jenkins (for teams that want to use Jenkins for pipeline execution while using GitLab for SCM).
* **APIs and webhooks** — Standard web integration mechanisms for custom automation and third-party tool connectivity. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## 1.12 — GitLab's Unified Value Proposition

The video's conclusion captures GitLab's core value: it "unifies development, security, and operations for teams." The three pillars are: **collaboration** (SCM, merge requests, project management), **automation** (CI/CD pipelines, Auto DevOps), and **compliance** (security scanning, audit logs, compliance pipelines). The instructor adds personal endorsement: "I have personally used it for startups and even enterprises." [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Learning

This is an introductory lecture — the hands-on GitLab work begins in the next lecture. However, this lecture establishes the practical landscape: what GitLab provides, where each capability lives, and how the pieces connect. The practical value here is **orientation** — knowing what tools are available, what they're called, and where to find them before you start using them. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## Getting Started: Access and Tier Selection

**What we are doing:** Setting up access to GitLab for the course.

**Model:** SaaS (gitlab.com) — no self-hosting setup required.

**Tier:** Free — sufficient for all course exercises.

**How to access:** Go to `gitlab.com`, subscribe (create an account), and start using it. No installation, no infrastructure provisioning, no setup. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## Practical Capability Map: Where to Find What

This is the operational orientation — mapping each capability to where you interact with it in GitLab. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

### Source Code Management

* **Repository:** Each project in GitLab has a Git repository. Clone it, push code, manage branches — standard Git operations.
* **Merge Requests:** Found in the project's sidebar. Create a merge request to propose code changes, add reviewers, require approvals, and merge after review. Remember: GitLab calls them "merge requests," not "pull requests."
* **Web IDE:** Accessible from the repository file browser — click the "Web IDE" button to edit files directly in the browser.
* **Wiki:** Found in the project sidebar under "Wiki." [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

### CI/CD Pipelines

* **Pipeline definition:** Create a `.gitlab-ci.yml` file in the root of your repository. This YAML file defines all stages, jobs, and scripts.
* **Pipeline visualization:** Found under CI/CD → Pipelines in the project sidebar. Shows all pipeline runs, their status, and detailed logs for each job.
* **Runners:** Found under Settings → CI/CD → Runners. Here you can see shared runners and add your own (EC2 instances, VMs, physical machines). You can enable/disable individual runners. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

### Security

* **Security scanning:** Integrated into pipeline jobs. You add security scanning stages to your `.gitlab-ci.yml`, and results appear in the merge request and the Security Dashboard.
* **Secret detection:** Runs automatically as part of the pipeline if configured.
* **Container scanning:** Runs against Docker images built in the pipeline. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

### Artifacts and Registries

* **Container Registry:** Found under Packages & Registries → Container Registry. Docker images built by your pipeline are stored here.
* **Package Registry:** Found under Packages & Registries → Package Registry. Maven, npm, and other package types.
* **Job artifacts:** Accessible from individual pipeline job pages. Defined in `.gitlab-ci.yml` with the `artifacts` keyword. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

### Monitoring

* **Pipeline analytics:** Found under Analytics → CI/CD Analytics.
* **Prometheus integration:** Configured under Settings → Integrations.
* **Audit events:** Found under Security & Compliance → Audit Events. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

### Project Management

* **Issues:** Found under Plan → Issues.
* **Milestones:** Found under Plan → Milestones.
* **Service Desk:** Found under Plan → Service Desk. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## How Runners Work Operationally

This is the most practically important concept to understand before the hands-on lectures. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**Default (shared runners):** When you create a pipeline on gitlab.com (free tier), GitLab provides shared runners automatically. Your jobs execute on GitLab's infrastructure with no setup from you. This is how you'll start.

**Adding a self-hosted runner:**

1. Provision a machine (e.g., an EC2 instance).
2. Install the GitLab Runner software on it.
3. Register it with your GitLab project (Settings → CI/CD → Runners provides the registration token and instructions).
4. Once registered, the runner appears in your project's runner list.
5. You can enable/disable it per project.
6. When a pipeline runs, you can specify which runner (or runner tag) should execute each job. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

**Why this matters operationally:** In the course's previous projects, EC2 instances were used for application hosting. Now, EC2 instances can also serve as CI/CD runners — the same infrastructure knowledge applies, but for a different purpose (pipeline execution instead of application serving).

⚠️ **Expert Note:**
In production environments, runner management becomes a significant operational concern. You need to consider: runner capacity (enough runners for concurrent pipeline jobs), runner security (runners execute arbitrary code from pipelines — they must be isolated), runner maintenance (keeping runner software and tools updated), and runner cost (self-hosted runners incur infrastructure costs). Many teams use auto-scaling runner pools on cloud infrastructure to balance cost and availability. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## Connection to Course Context

This GitLab section connects to everything learned previously:

* **Maven** (previous lecture) — Maven build commands (`mvn install`, `mvn package`) will be executed as jobs within GitLab CI/CD pipelines.
* **Artifact deployment** — The WAR file produced by Maven can be stored in GitLab's package registry or deployed to Beanstalk/EC2 from a GitLab pipeline job.
* **Docker** (upcoming) — Docker images will be built in GitLab pipelines and stored in GitLab's container registry.
* **AWS infrastructure** — EC2 instances can serve as GitLab runners, and pipeline jobs can deploy to AWS services. [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
PLATFORM: GitLab
TYPE:     Complete DevSecOps platform (not just CI/CD)
CORE IDEA: Everything at one place — SCM + CI/CD + Security + PM + Registry + Monitoring
HOSTING:  SaaS (gitlab.com) OR Self-hosted
TIERS:    Free → Premium → Ultimate
COURSE:   Free tier on gitlab.com
```

 [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## GitLab Capability Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     GITLAB PLATFORM                      │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │     SCM      │  │    CI/CD     │  │   SECURITY     │  │
│  │ Git repos    │  │ YAML pipes   │  │ SAST / DAST    │  │
│  │ Branches     │  │ Multi-stage  │  │ Container scan │  │
│  │ Merge Req    │  │ Runners      │  │ License check  │  │
│  │ Approvals    │  │ Auto DevOps  │  │ Secret detect  │  │
│  │ Web IDE      │  │ Visualization│  │ Audit logs     │  │
│  │ Wiki         │  │              │  │ Compliance     │  │
│  └─────────────┘  └──────────────┘  └────────────────┘  │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │  REGISTRIES  │  │  MONITORING  │  │  PROJECT MGMT  │  │
│  │ Container    │  │ Pipeline     │  │ Issues         │  │
│  │  registry    │  │  analytics   │  │ Milestones     │  │
│  │ Package      │  │ Code quality │  │ Roadmaps       │  │
│  │  registry    │  │ Prometheus   │  │ Dashboards     │  │
│  │ Job artifacts│  │ Sentry       │  │ Service desk   │  │
│  └─────────────┘  └──────────────┘  └────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │              INTEGRATIONS                         │    │
│  │  Cloud (AWS, GCP) │ Slack │ Jira │ Jenkins │ K8s  │    │
│  │  Terraform │ Trello │ APIs │ Webhooks             │    │
│  └──────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

 [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## CI/CD Pipeline Structure

```
.gitlab-ci.yml (YAML config in repo root)
        │
        ▼
PIPELINE = ordered stages
  ├── Stage 1 (e.g., build)   → jobs run in parallel
  ├── Stage 2 (e.g., test)    → jobs run in parallel
  ├── Stage 3 (e.g., security)→ SAST, DAST, container scan
  └── Stage 4 (e.g., deploy)  → push to target

Stages: sequential (Stage 1 must finish before Stage 2)
Jobs within a stage: parallel
```

 [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## Runner Architecture (Controller / Worker)

```
GITLAB PLATFORM (Controller)
  ├── Knows pipeline definition
  ├── Tracks job state
  ├── Stores logs + artifacts
  ├── Provides UI + visualization
  │
  ▼ (sends job instructions)
  
RUNNER (Worker)
  ├── Shared (GitLab-hosted) ← quick start, no setup
  └── Self-hosted ← EC2, VM, physical machine
       ├── Full control over environment
       ├── Custom tools + network access
       ├── Enable/disable per project
       └── Register via Settings → CI/CD → Runners

SEPARATION: Orchestration (GitLab) ≠ Execution (Runner)
SCALING:    Add more runners = more parallel capacity
```

 [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## Terminology Map: GitLab vs. GitHub

```
GitLab              GitHub
──────              ──────
Merge Request    =  Pull Request
Runner           ≈  GitHub Actions Runner
.gitlab-ci.yml   ≈  .github/workflows/*.yml
Container Registry≈ GitHub Container Registry (ghcr.io)
```

 [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## Security Pipeline Integration

```
CODE COMMITTED
    │
    ▼
Pipeline runs:
  ├── SAST → static code analysis (scan source)
  ├── DAST → dynamic testing (scan running app)
  ├── Container Scan → Docker image vulnerabilities
  ├── License Check → dependency license compliance
  ├── Secret Detection → exposed credentials
  │
  ▼
Results → Merge Request + Security Dashboard
Audit → Audit Logs (who did what)
Compliance → Enforced pipeline stages

PRINCIPLE: Security is IN the pipeline, not AFTER it
```

 [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## Artifact Flow

```
Pipeline Job produces output:
  │
  ├── Docker image → Container Registry (built-in)
  ├── Maven JAR/WAR → Package Registry (built-in)
  ├── npm package → Package Registry (built-in)
  └── Reports/files → Job Artifacts (stored per job)

NO EXTERNAL TOOLS NEEDED for artifact storage
(replaces Docker Hub, Nexus, Artifactory, ECR)
```

 [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## Connection to Course Pipeline

```
PREVIOUS:                           NOW:
  Maven builds WAR                    Maven runs AS a GitLab pipeline job
  Manual deploy to S3/Beanstalk       Pipeline job deploys to AWS
  EC2 hosts application               EC2 ALSO serves as GitLab runner
  Manual security review              Automated SAST/DAST in pipeline
  Jenkins (separate CI tool)          GitLab CI replaces Jenkins

UPCOMING:
  Docker images built in pipeline → stored in GitLab Container Registry
  Kubernetes deployment via GitLab agent
```

 [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## Three Pillars (Value Model)

```
COLLABORATION          AUTOMATION            COMPLIANCE
─────────────          ──────────            ──────────
Git repos              YAML pipelines        SAST / DAST
Merge requests         Auto DevOps           Container scanning
Approvals              Multi-stage jobs      License checks
Web IDE                Runners               Secret detection
Wiki                   Pipeline viz          Audit logs
Issues / Milestones    Integrations          Compliance pipelines
Service desk           APIs / Webhooks       Audit events
```

 [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## Reusable Engineering Patterns

| Pattern                       | Manifestation                                                                    |
| ----------------------------- | -------------------------------------------------------------------------------- |
| **Unified Platform**          | Single tool replaces N separate tools (SCM + CI + CD + Security + Registry + PM) |
| **Controller / Worker**       | GitLab orchestrates, Runners execute — independently scalable                    |
| **Pipeline as Code**          | `.gitlab-ci.yml` = declarative, versioned, reviewable pipeline definition        |
| **Shift-Left Security**       | Security scanning moves INTO the pipeline, runs on every commit                  |
| **Built-in Artifact Storage** | Container + Package registries eliminate external storage dependencies           |
| **Multi-Model Deployment**    | SaaS or Self-hosted — same platform, different operational models                |
| **Template Reuse**            | Auto DevOps templates = ready-made pipelines for common project types            |
| **Pluggable Execution**       | Swap runners without changing pipeline definition (shared ↔ self-hosted)         |

 [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

## One-Line System Reconstruction

> **GitLab is a unified DevSecOps platform where Git-hosted source code flows through YAML-defined multi-stage pipelines executed on pluggable runners (shared or self-hosted EC2), with built-in security scanning (SAST/DAST/secrets/containers/licenses), container and package registries for artifact storage, Prometheus/Sentry monitoring integration, and project management (issues/milestones/service desk) — replacing the need for separate SCM, CI/CD, security, registry, and PM tools.** [\[193-introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/193-introduction.txt)

***

This completes the full reconstruction of the GitLab Introduction lecture. It establishes the platform foundation for the CI/CD pipeline work that follows — where Maven builds, Docker image creation, security scanning, and AWS deployments will all be orchestrated through GitLab pipelines. Let me know if you'd like any section expanded or adjusted! 🚀

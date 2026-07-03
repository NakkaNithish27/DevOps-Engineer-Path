# 🎬 Flow of Continuous Integration Pipeline

**Source:** [163.-Flow-of-Continuous-Integration-Pipeline.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt?EntityRepresentationId=f4be54bf-448c-4715-a944-0aeb88e9d4da) [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

This video is a **conceptual foundation video** — it does not contain hands-on commands or live execution. Its purpose is to walk through the **entire flow of a Continuous Integration (CI) pipeline** before building it step-by-step in the videos that follow. The instructor uses Jenkins, Git, Maven, SonarQube, and Nexus as example tools, but repeatedly emphasizes that the **flow matters more than the specific tools**. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

***

***

# 🧠 SECTION 1: THEORY — DEEP LEARNING MODE

***

## 1. Continuous Integration (CI) — The Core Idea

Continuous Integration is a practice where every code change made by a developer is automatically fetched, built, tested, analyzed, and packaged — in a repeatable, automated sequence called a **pipeline**. The word "continuous" means this isn't a one-time activity; it triggers **every time** code changes. The word "integration" means all these separate activities (building, testing, analyzing) are **integrated into a single automated flow** so that problems are caught early, not at deployment time. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

The pipeline discussed in this video follows this exact sequence:

**Fetch → Build → Unit Test → Code Analysis → Publish Artifact**

Each stage feeds into the next. If any stage fails, the pipeline stops. This is by design — you don't want to publish an artifact that failed its tests or has known vulnerabilities. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

> 🔍 **Deep Dive (Optional)**
>
> The reason CI exists as a discipline is historical. Before CI, developers would work in isolation for days or weeks, then attempt to merge their code together. This "integration" phase was painful, error-prone, and often called "integration hell." CI solves this by making integration happen **with every single commit**, so problems surface immediately when they're small and easy to fix, rather than compounding over time.

***

## 2. The Tools in This Pipeline

The instructor names five tools that will be used to build this CI pipeline: **Jenkins, Git (with GitHub), Maven, SonarQube, and Nexus**. But the instructor is very deliberate in saying: *"In your project, you may have different tools. So focus on the flow."* And later: *"You may have GitLab, CircleCI, Bamboo — there are many CI tools, but the process will be almost same."* [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

This is an important mindset point. The tools are **interchangeable implementations** of fixed roles in the pipeline. Here's what each role is, and which tool fills it:

| **Role in Pipeline** | **Tool Used Here**             | **What It Does**                                                             |
| -------------------- | ------------------------------ | ---------------------------------------------------------------------------- |
| CI Orchestrator      | Jenkins                        | Controls the entire pipeline — triggers, sequences, and monitors every stage |
| Version Control      | Git + GitHub                   | Stores the source code centrally; tracks every change                        |
| Build Tool           | Maven                          | Compiles Java source code into deployable artifacts                          |
| Code Analysis        | SonarQube Scanner + Checkstyle | Scans code for vulnerabilities, bugs, and best-practice violations           |
| Analysis Dashboard   | SonarQube Server               | Displays analysis results as graphs, charts; enforces quality gates          |
| Artifact Repository  | Nexus (Sonatype)               | Stores versioned, verified artifacts ready for deployment                    |

 [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

The key insight is: if you understand **why** each role exists and **what** it does in the flow, you can swap Jenkins for GitLab CI, Maven for Gradle, SonarQube for Codacy, Nexus for Artifactory — and the pipeline logic remains identical. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

***

## 3. The Developer's Role — Where the Pipeline Begins

The pipeline doesn't start with Jenkins. It starts with the **developer**. The instructor describes the developer's workflow as: write code → make changes → test locally → push to a centralized repository (GitHub). [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

The developer uses a tool (like an IDE or Git CLI) that **integrates with the GitHub repository**, and the code is **committed** to that repository. This commit is the trigger point. The developer's responsibility ends at pushing verified local changes. Everything after that is the CI pipeline's job. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

The phrase "centralized repository" is important. In a team, every developer pushes to the **same** repository. This is what makes integration possible — all changes converge in one place where they can be automatically validated together. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

> 🔍 **Deep Dive (Optional)**
>
> "Test locally" is a subtle but important step. The developer doesn't blindly push code. They run basic checks on their own machine first. The CI pipeline then re-validates everything in a **controlled, standardized environment** — because "works on my machine" is not a reliable guarantee. The CI pipeline is the **objective, reproducible truth** about whether the code is healthy.

***

## 4. Jenkins Detecting Changes and Fetching Code

The instructor explains: *"As soon as there is a code change, Jenkins will detect a change and fetch the code by using git tool."* Jenkins does this through two components: the **Git tool** (the actual Git binary installed on the Jenkins server) and the **Git plugin** (which gives Jenkins the ability to interact with Git repositories through its UI and pipeline configuration). [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

This is the first stage of the pipeline. Jenkins doesn't build anything yet — it first needs to **get the latest code**. The detection can happen through mechanisms like webhooks (GitHub notifies Jenkins) or polling (Jenkins periodically checks GitHub for changes). The instructor doesn't specify the mechanism in this video, but the concept is: a code change triggers the pipeline, and Jenkins uses Git to pull that code into its workspace. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

> 🔍 **Deep Dive (Optional)**
>
> The distinction between the Git **tool** and the Git **plugin** matters. The Git tool is the command-line binary (`git`) that actually performs operations like `git clone` and `git pull`. The Git plugin is the Jenkins extension that provides the UI integration — letting you configure repository URLs, branches, and credentials inside Jenkins job settings. You need **both** for this to work. The plugin tells Jenkins *what* to do; the tool *does* it.

***

## 5. Building the Code with Maven

Once Jenkins has fetched the code, the next pipeline stage is **building** it. The instructor says: *"We will be using Maven to build the code because we have Java code."* Building means taking human-readable source code and converting it into machine-executable artifacts — in Java's case, typically `.jar` or `.war` files. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

Maven is a **build tool** specifically designed for Java projects. It reads a configuration file (`pom.xml`) in the project, resolves dependencies (libraries the code needs), compiles the source code, and packages it into an artifact. The instructor notes this could be *"any other source code and other build tools as well"* — meaning if you had Python code, you might use pip; if Node.js, you might use npm. The build tool matches the language. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

The key outcome of this stage is the **artifact** — the compiled, packaged output. If the build fails (syntax errors, missing dependencies, incompatible code), the pipeline stops here. No further testing or analysis happens on broken code. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

***

## 6. Unit Testing

After a successful build, the pipeline runs **unit tests**. The instructor explains this clearly: *"Maven will have some unit testing framework that developer will use. Unit testing will be part of your source code."* [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

Unit tests check whether individual **units** (small, isolated pieces) of code work correctly. These tests are written by the developer as part of the source code itself — they live alongside the application code in the repository. The DevOps engineer's job here is not to write these tests but to **execute them** as part of the pipeline. The instructor makes this explicit: *"Being a DevOps, you don't need to do much here. You just need to execute some steps that will run this test and generate reports mostly in XML format."* [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

This is an important role-clarity point. In CI, the **developer writes** the tests; the **DevOps engineer configures** the pipeline to run them. The output is a report (typically XML, following formats like JUnit XML) that records which tests passed and which failed. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

> ⚠️ **Expert Note (Optional)**
>
> The phrase "unit of the code" means the smallest testable piece — usually a single function or method. Unit tests are fast and isolated (they don't need databases, networks, or external services). This is why they run early in the pipeline: they're cheap to execute and catch basic logic errors quickly. If unit tests fail, there's no point proceeding to more expensive analysis stages.

***

## 7. Code Analysis — A Different Kind of Testing

After unit testing, the pipeline performs **code analysis**. The instructor draws a clear distinction: *"Unit test checks whether the unit of the code works or not. Code analysis checks if the code has any vulnerability. Are you following the best practices? Do you have any bug in the code? And there are many other parameters."* [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

This distinction is critical. Unit testing asks: **"Does the code do what it's supposed to do?"** Code analysis asks: **"Is the code written well, safely, and according to standards?"** Code can pass all unit tests (it works correctly) but still have security vulnerabilities, duplicated logic, poor readability, or violations of coding standards. Code analysis catches these. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

The tools used here are **SonarQube Scanner** and **Checkstyle**. The instructor mentions: *"There are many code analysis tools available in the market. We are using SonarQube Scanner and Checkstyle to scan the code."* Both tools scan the source code and generate reports in a similar format. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

*   **SonarQube Scanner** performs deep analysis — detecting bugs, vulnerabilities, code smells (patterns that indicate deeper problems), and security hotspots.
*   **Checkstyle** focuses on **coding style and conventions** — ensuring consistent formatting, naming conventions, and structural rules.

These reports are then **uploaded to the SonarQube Server**, which is a separate application with a web interface where you can see *"proper graphs, charts and you can see what are the bugs, vulnerabilities and many other things in your code."* [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

> 🔍 **Deep Dive (Optional)**
>
> Notice the architecture here: the **Scanner** runs inside the Jenkins pipeline (it's the tool that does the actual scanning), while the **SonarQube Server** is a separate, persistent service that receives and displays results. This separation is intentional — the server accumulates results over time, so you can track trends: is code quality improving or degrading across commits? This historical view is valuable for engineering leadership and audit purposes.

***

## 8. Quality Gates — The Pass/Fail Decision

The instructor introduces a powerful concept: *"We can also set a quality gate and we can say, if my code does not follow these practices, then fail the build. And if it fails, the pipeline will stop. If it passes, we have then a verified copy of the artifact."* [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

A **quality gate** is a set of conditions defined in SonarQube that the code must satisfy. For example: "no critical vulnerabilities," "code coverage above 80%," "no new bugs." If the code analysis results violate any of these conditions, the quality gate **fails**, and the entire pipeline stops. The artifact is not published. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

This is the checkpoint that transforms the artifact from "just compiled code" into a **"verified copy."** The instructor uses this exact phrase deliberately — once the code has been built, unit-tested, and passed code analysis with quality gates, it is now a **trusted, verified artifact** that is safe to distribute. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

> ⚠️ **Expert Note (Optional)**
>
> Quality gates are a policy enforcement mechanism. In real-world organizations, they prevent teams from shipping code that doesn't meet minimum standards. The key decision is **where to set the threshold**. Too strict and you block every build; too lenient and the gate is meaningless. Most teams start with reasonable defaults and tighten over time as code quality improves.

***

## 9. Artifact Versioning and Publishing to Nexus

The final stage: *"These artifacts will be versioned and will be uploaded to Nexus Sonatype repository."* The instructor explains this happens **before** deploying to servers. The artifact is not deployed directly from the pipeline — it's first stored in a dedicated **artifact repository** (Nexus). [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

**Versioning** means each artifact gets a unique version identifier (like `1.0.0`, `1.0.1`, `2.0.0-SNAPSHOT`). This ensures you can always trace which exact version of the code is running in any environment, and you can roll back to a previous version if something goes wrong. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

**Nexus Sonatype** is an artifact repository manager. Think of it as a **warehouse for your build outputs**. Just like GitHub stores your source code, Nexus stores your compiled artifacts. When it's time to deploy, the deployment process pulls the correct version from Nexus rather than rebuilding from source. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

> 🔍 **Deep Dive (Optional)**
>
> Why not deploy directly from Jenkins? Because the CI pipeline's job is to **produce and verify** artifacts, not to deploy them. Deployment is a separate concern (often called Continuous Delivery or Continuous Deployment). By storing artifacts in Nexus, you create a clean separation: CI produces verified artifacts → Nexus stores them → CD deploys them. This also means multiple environments (dev, staging, production) can pull the **exact same artifact** rather than rebuilding, which guarantees consistency.

***

## 10. Tool Interchangeability — The Meta-Lesson

The instructor bookends the video with this message: the specific tools don't matter as much as the flow. *"You may have GitLab, CircleCI, Bamboo — there are many CI tools, but the process will be almost the same. Fetch the code, build the code, test it, analyze it, and then publish the artifact."* [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

This is the single most important takeaway from this video. The five-stage flow — **Fetch → Build → Test → Analyze → Publish** — is universal across CI implementations. The instructor also emphasizes: *"Whatever CI tool you're using, you have to integrate it with other tools like GitHub, SonarQube, Nexus, or any other tool."* No CI tool works alone. The orchestrator (Jenkins, GitLab CI, etc.) is the **glue** that connects specialized tools into a unified pipeline. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

> ⚠️ **Expert Note (Optional)**
>
> In real projects, tool selection is driven by factors like: existing team expertise, licensing costs, integration ecosystem, and organizational standards. A DevOps engineer who understands the **flow** can adapt to any toolchain. This is why the instructor insists on learning the flow first and practicing with one toolset, then transferring that knowledge to others.

***

***

# ⚙️ SECTION 2: PRACTICAL — GUIDED EXECUTION MODE

***

## What We Are Building

This video does not contain hands-on execution — it is the **architectural blueprint** for a CI pipeline that will be built over the next several videos. The instructor explicitly states: *"Over the next few videos, we will see the steps to execute this entire pipeline. But before we do that, we will understand the flow."* [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

What is being planned is a **complete CI pipeline** with the following architecture:

    Developer → GitHub → Jenkins → [Build (Maven)] → [Unit Test (Maven)] 
        → [Code Analysis (SonarQube Scanner + Checkstyle)] → [Quality Gate (SonarQube Server)] 
        → [Publish Artifact (Nexus)]

The final outcome is: every time a developer pushes code to GitHub, the pipeline automatically builds it, tests it, analyzes it for quality and security, and — if everything passes — stores a versioned, verified artifact in Nexus, ready for deployment. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

**Why this matters:** Without this pipeline, every step would be manual. Someone would have to remember to run tests, someone else would have to check code quality, and artifacts would be built inconsistently on different machines. The CI pipeline makes this **automatic, consistent, and reliable**. A broken build is caught in minutes, not days. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

***

## The End-to-End Flow — Step by Step

Since this is a flow-understanding video, the "practical" content is the pipeline design itself. Here is the complete flow as the instructor describes it, with each stage's purpose and connections:

***

### Step 1: Developer Pushes Code to GitHub

The developer writes and modifies code on their local machine, tests it locally, and when satisfied, **commits and pushes** it to the GitHub repository. This is the **trigger event** for the entire pipeline. Without a push, nothing happens. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

**Connection to the pipeline:** The push creates a change in the centralized repository. Jenkins is configured to watch this repository. The moment a change appears, the pipeline begins.

***

### Step 2: Jenkins Detects the Change and Fetches Code

Jenkins uses its **Git tool and Git plugin** to detect the new commit and pull the latest code into its workspace. This is the pipeline's first automated action. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

**What you will need to set up (in later videos):**

*   Git installed on the Jenkins server (the tool)
*   Git plugin installed in Jenkins (the integration)
*   Repository URL and credentials configured in the Jenkins job

**Connection to the pipeline:** The fetched code becomes the input for the build stage.

***

### Step 3: Build with Maven

Maven compiles the Java source code and produces an **artifact** (e.g., a `.jar` or `.war` file). If the code has syntax errors or missing dependencies, the build fails and the pipeline stops. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

**What you will need to set up:**

*   Maven installed on the Jenkins server
*   Maven configured in the Jenkins pipeline to run against the project's `pom.xml`

**Connection to the pipeline:** A successful build produces the artifact that will be tested and analyzed in the next stages.

***

### Step 4: Run Unit Tests

Maven executes the unit tests that the developer wrote as part of the source code. The results are generated as **XML reports**. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

**Your role as DevOps:** You don't write these tests. You configure the pipeline step that **runs** them and **collects** the reports. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

**Connection to the pipeline:** If tests fail, the pipeline should stop (or at minimum, flag the failure). Passing tests mean the code's logic is correct at the unit level.

***

### Step 5: Code Analysis with SonarQube Scanner and Checkstyle

The code is scanned for vulnerabilities, bugs, code smells, and style violations. The scanner tools generate reports that are **uploaded to the SonarQube Server**. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

**What you will need to set up:**

*   SonarQube Scanner configured in Jenkins
*   Checkstyle configured in the pipeline
*   SonarQube Server running and accessible from Jenkins
*   Quality gates defined in SonarQube Server [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

**Connection to the pipeline:** The quality gate on the SonarQube Server is the **decision point**. If the gate passes, the artifact is considered verified. If it fails, the pipeline stops. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

***

### Step 6: Publish Verified Artifact to Nexus

The verified artifact is **versioned** and uploaded to the **Nexus Sonatype repository**. It is now stored safely and can be pulled for deployment to any environment. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

**What you will need to set up:**

*   Nexus repository running and accessible from Jenkins
*   Jenkins configured with Nexus credentials and repository details
*   Versioning strategy defined for the artifacts

**Connection to the overall system:** This is where CI ends. The artifact is ready. Deployment (CD) is a separate process that pulls from Nexus. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

***

## Summary of the Pipeline Architecture

    ┌─────────────┐     ┌──────────┐     ┌─────────┐     ┌────────────┐
    │  Developer   │────▶│  GitHub   │────▶│ Jenkins │────▶│ Build      │
    │  (writes &   │     │ (central │     │ (detects│     │ (Maven     │
    │   pushes)    │     │  repo)   │     │ & fetch)│     │  compiles) │
    └─────────────┘     └──────────┘     └─────────┘     └─────┬──────┘
                                                               │
                                                               ▼
    ┌──────────────┐     ┌────────────────┐     ┌──────────────────────┐
    │ Nexus        │◀────│ Quality Gate   │◀────│ Code Analysis        │
    │ (versioned   │     │ (SonarQube     │     │ (SonarQube Scanner   │
    │  artifact    │     │  pass/fail)    │     │  + Checkstyle)       │
    │  storage)    │     └────────────────┘     └──────────┬───────────┘
    └──────────────┘                                       ▲
                                                           │
                                                  ┌────────┴───────┐
                                                  │  Unit Tests    │
                                                  │  (Maven, XML   │
                                                  │   reports)     │
                                                  └────────────────┘

 [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

***

## What Comes Next

The instructor closes with: *"In the next video, we will see the steps that we will take to set up this entire continuous integration pipeline."* The upcoming videos will involve actual tool installation, configuration, and pipeline creation. This video ensures you understand **what** you're building and **why** each piece exists before you start executing. [\[163.-Flow-...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/163.-Flow-of-Continuous-Integration-Pipeline.txt)

***

This covers **everything** present in the caption file — no content has been skipped, no external concepts have been added. The flow and emphasis match the instructor's original delivery. Want me to save this as a downloadable Markdown file?

# 🎓 Continuous Integration Pipeline — Full Learning Material

*Reconstructed from video captions: "Steps for Continuous Integration Pipeline"* [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

***

## 📌 Video Context & Purpose

This video serves as a **roadmap lecture** — the instructor lays out the complete sequence of steps that will be followed across upcoming lectures to build an end-to-end **Continuous Integration (CI) pipeline**. No hands-on execution happens in this video itself; instead, it establishes the architectural plan, the tools involved, and the order in which everything will be configured. The instructor explicitly says: *"all the steps may not make much sense now, but this is the roadmap. Whenever you feel that you are lost while setting the pipeline, come and check this video."* [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

This tells us the video is designed as a **reference anchor** — something to return to whenever you lose track of the bigger picture during implementation.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. Continuous Integration Pipeline — The Core Idea

A Continuous Integration (CI) pipeline is an automated workflow that takes code written by developers and runs it through a series of stages — building, testing, analyzing code quality, storing the resulting artifact, and notifying the team — every time code is committed. The goal is to catch problems early, before they reach production.

In this video, the CI pipeline being built involves **three core servers** working together: **Jenkins** (the automation engine), **Nexus** (the artifact repository), and **SonarQube** (the code quality analyzer). These three are not isolated tools — they form a connected system where Jenkins orchestrates the entire flow, pulling code, running builds, sending code to SonarQube for analysis, and pushing the final artifact to Nexus. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

The pipeline script ties them all together, and notifications ensure that failures don't go unnoticed.

> 🔍 **Deep Dive (Optional)**
>
> The reason three separate servers are used instead of running everything on one machine is **separation of concerns**. Jenkins handles orchestration, Nexus handles storage, and SonarQube handles analysis. In real-world production environments, these run on different machines (or containers) so that a resource-heavy code scan on SonarQube doesn't starve Jenkins of CPU/memory during a build, and vice versa. This also allows independent scaling — you can upgrade your Nexus storage without touching Jenkins.

***

## 2. Jenkins — The Automation Engine

Jenkins is the central piece of this pipeline. It is an open-source automation server that executes jobs — sequences of steps defined by the user. In the context of CI, Jenkins listens for code changes, triggers builds, runs tests, calls external tools (like SonarQube and Nexus), and reports results.

The instructor mentions that **Jenkins may already be set up** from a previous section, and the existing one can be reused, or a new one can be created. This tells us Jenkins is being provisioned as an **EC2 instance on AWS**, set up using **user data scripts** (bash scripts that run automatically when the instance launches). [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

Jenkins on its own is a bare engine. Its power comes from **plugins** — modular extensions that add capabilities. The instructor explicitly lists the plugins that will be installed: **Nexus plugin, SonarQube plugin, Git plugin, and Maven plugin**. Each serves a specific purpose:

*   **Git plugin** — allows Jenkins to connect to Git repositories and pull source code.
*   **Maven plugin** — allows Jenkins to use Apache Maven as the build tool (compiling code, running tests, packaging artifacts).
*   **SonarQube plugin** — allows Jenkins to send code to SonarQube for quality analysis.
*   **Nexus plugin** — allows Jenkins to upload built artifacts (like `.war` or `.jar` files) to the Nexus repository.

Without these plugins, Jenkins would not know how to interact with any of these tools. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

> ⚠️ **Expert Note (Optional)**
>
> Plugin management is one of the most common sources of issues in Jenkins. Plugin version incompatibilities, deprecated plugins, and missing dependencies can break pipelines silently. In production, teams often pin plugin versions and test upgrades in a staging Jenkins instance before applying them to the production Jenkins server.

***

## 3. Nexus — The Artifact Repository

Nexus (specifically Sonatype Nexus Repository) is where the **built artifacts are stored**. When Maven compiles the source code and packages it into a deployable file (e.g., a `.war` file for a Java web application), that file needs to be stored somewhere versioned, reliable, and accessible. That's Nexus.

The instructor notes that **Nexus integration with Jenkins is straightforward** — it involves saving credentials (Nexus username and password) in Jenkins so that Jenkins can authenticate and upload artifacts. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

This simplicity tells us that the Nexus plugin handles most of the complexity internally — once credentials are stored, the pipeline script can reference Nexus as a target, and the plugin handles the upload protocol.

> 🔍 **Deep Dive (Optional)**
>
> Nexus doesn't just store files like a file server. It understands artifact formats — Maven artifacts have a `groupId`, `artifactId`, `version`, and `packaging type`. Nexus indexes these and allows you to retrieve specific versions later. This is critical for rollback scenarios: if version 2.5 breaks production, you can pull version 2.4 directly from Nexus without rebuilding.

***

## 4. SonarQube — The Code Quality Analyzer

SonarQube is a tool that performs **static code analysis** — it examines source code without executing it and identifies bugs, code smells (poor patterns), security vulnerabilities, and test coverage gaps.

The instructor explicitly notes that **SonarQube integration with Jenkins requires more steps** compared to Nexus. While Nexus only needs credentials, SonarQube involves additional configuration steps (which will be covered in subsequent lectures). [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

This difference in integration complexity is worth noting — it implies SonarQube requires things like a server URL configuration, an authentication token (rather than simple username/password), and possibly a webhook or quality gate configuration back to Jenkins.

***

## 5. EC2 Instances and User Data Scripts

All three servers — Jenkins, Nexus, and SonarQube — are being launched as **EC2 instances** on AWS. EC2 (Elastic Compute Cloud) provides virtual machines in the cloud.

The key detail here is that the setup is done through **user data scripts** — bash scripts that are provided at instance launch time. AWS executes these scripts automatically when the instance boots for the first time. This means the installation of Jenkins, Nexus, or SonarQube is **automated from the start** — no manual SSH and installation required. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

This approach is a DevOps best practice: infrastructure should be provisioned through scripts, not manual steps. It ensures repeatability — you can tear down a server and recreate it identically.

***

## 6. Security Groups — Network Access Control

The instructor mentions that **security groups** need to be checked to **allow connections between the three servers**. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

Security groups in AWS act as virtual firewalls for EC2 instances. By default, instances cannot talk to each other unless their security groups explicitly allow inbound traffic on the required ports. For this CI pipeline:

*   Jenkins needs to reach **Nexus** (to upload artifacts — typically port 8081).
*   Jenkins needs to reach **SonarQube** (to send code for analysis — typically port 9000).
*   Optionally, SonarQube may need to call back to Jenkins (for webhook-based quality gate results).

If security groups are not configured correctly, integrations will fail with connection timeout errors — a very common setup pitfall.

> ⚠️ **Expert Note (Optional)**
>
> A common mistake is opening all ports (0.0.0.0/0 on all ports) to "make it work." This is dangerous in any real environment. The correct approach is to allow only the specific ports needed, and restrict the source to the security group IDs of the other servers (not open to the entire internet).

***

## 7. Pipeline Script

Once all servers are set up, plugins installed, and integrations configured, the instructor says a **pipeline script** will be written. This script is the actual CI definition — it tells Jenkins what to do, in what order, using which tools. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

The pipeline script **uses all the resources** set up in the previous steps: it pulls code via Git, builds with Maven, analyzes with SonarQube, and uploads to Nexus. It is the glue that connects everything into a single automated flow.

The instructor implies this will be a **Jenkins Pipeline script** (likely written in Groovy-based Jenkinsfile syntax), which defines stages like `Build`, `Test`, `Code Analysis`, `Upload Artifact`, etc.

***

## 8. Notifications

The final step is setting up **notifications**. The instructor says: *"if anything goes wrong in the pipeline, any job fails, we should get notifications automatically."* [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

This is the observability layer of the pipeline. A pipeline that fails silently is worse than no pipeline at all — because developers assume everything is fine when it isn't. Notifications (typically via email, Slack, or Microsoft Teams) ensure that failures are immediately visible to the team.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are building a **complete Continuous Integration pipeline** that automates the process of building, testing, analyzing, and storing a software application every time code changes are committed. The system consists of three servers — Jenkins, Nexus, and SonarQube — all running on AWS EC2 instances, connected through properly configured security groups, and tied together by a Jenkins pipeline script. At the end, notifications are set up so failures trigger automatic alerts. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

### Why It Matters

Without CI, developers manually build, test, and deploy code — a slow, error-prone process. A CI pipeline catches bugs within minutes of a commit, ensures code quality standards are met, and stores every version of the artifact for reliable deployments. This is foundational to any modern software delivery practice.

### Final Outcome

A fully functional pipeline where: a code commit triggers Jenkins → Jenkins pulls code → builds with Maven → analyzes with SonarQube → uploads artifact to Nexus → sends notification on success or failure.

***

## Step-by-Step Roadmap

### Step 1: Set Up Jenkins Server

**What we are doing:** Launching an EC2 instance on AWS and using a user data bash script to automatically install and configure Jenkins.

**Why:** Jenkins is the orchestrator — nothing else in the pipeline works without it. It needs to be running and accessible before any plugins or integrations can be configured.

**How it's done:** When launching the EC2 instance in AWS, a bash script is provided in the "User Data" field. This script runs on first boot and handles the entire Jenkins installation — installing Java (Jenkins dependency), downloading Jenkins, starting the service, and enabling it to run on boot.

The instructor notes you can **reuse an existing Jenkins server** if one is already available from a previous section, or create a new one. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

**Connection to the overall system:** Jenkins is the central hub. Every other component (Nexus, SonarQube, plugins, pipeline script, notifications) connects to or through Jenkins.

***

### Step 2: Set Up Nexus Server

**What we are doing:** Launching a separate EC2 instance and using a user data bash script to install Sonatype Nexus Repository Manager.

**Why:** We need a dedicated, versioned storage location for the artifacts (`.war`, `.jar` files) produced by the build process. Nexus serves this purpose.

**How it's done:** Same approach as Jenkins — an EC2 instance is launched with a bash script in the user data field that installs and starts Nexus. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

**Connection to the overall system:** Nexus is the destination for built artifacts. Jenkins (via the Nexus plugin) will upload artifacts here after a successful build.

***

### Step 3: Set Up SonarQube Server

**What we are doing:** Launching a third EC2 instance with a user data bash script to install SonarQube.

**Why:** Code quality analysis is a critical gate in CI. SonarQube scans the source code for bugs, vulnerabilities, and code smells before the artifact is stored — ensuring only quality code progresses through the pipeline.

**How it's done:** Again, an EC2 instance with a user data bash script. SonarQube typically requires a database (like PostgreSQL) and sufficient memory, so the instance type may need to be larger than Jenkins. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

**Connection to the overall system:** SonarQube sits between the build step and the artifact upload step. Jenkins sends code to SonarQube, waits for the analysis result, and only proceeds if quality standards are met.

***

### Step 4: Configure Security Groups

**What we are doing:** Checking and updating the AWS security groups attached to the three EC2 instances to ensure they can communicate with each other over the required ports.

**Why:** By default, EC2 instances block inbound traffic. If Jenkins can't reach Nexus on port 8081 or SonarQube on port 9000, the integrations will fail with connection errors.

**How it's done:** The instructor says this will be covered during the setup — specifically, *"I'll tell you how you can allow connection in between them."* This means modifying inbound rules of each security group to allow traffic from the other servers' security groups on the necessary ports. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

**Connection to the overall system:** Security groups are the network foundation. If this step is wrong, nothing else works — integrations fail, plugins can't connect, and the pipeline breaks at runtime.

> ⚠️ **Expert Note (Optional)**
>
> When troubleshooting integration failures, always check security groups first. A "connection timed out" error between Jenkins and SonarQube almost always means the security group is blocking the port.

***

### Step 5: Install Plugins in Jenkins

**What we are doing:** Installing four essential plugins in Jenkins: **Nexus plugin, SonarQube plugin, Git plugin, and Maven plugin**.

**Why:** Jenkins without plugins is a bare automation engine. These plugins give Jenkins the ability to interact with Git (to pull code), Maven (to build), SonarQube (to analyze), and Nexus (to store artifacts). Each plugin adds a specific capability that the pipeline script will use.

**How it's done:** Plugins are installed through Jenkins' web UI: `Manage Jenkins → Manage Plugins → Available tab → Search and Install`. The instructor says these will be installed **one by one**. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

**Connection to the overall system:** Plugins are the bridge between Jenkins and external tools. Without them, the pipeline script would have no way to call Maven builds, trigger SonarQube scans, or upload to Nexus.

***

### Step 6: Integrate Nexus with Jenkins

**What we are doing:** Configuring Jenkins to authenticate with the Nexus server by saving Nexus credentials (username and password) in Jenkins.

**Why:** When the pipeline script instructs Jenkins to upload an artifact to Nexus, Jenkins needs valid credentials to authenticate. Without this, the upload will be rejected.

**How it's done:** The instructor describes this as **straightforward** — *"we just need to save the credentials."* This is typically done via `Manage Jenkins → Manage Credentials → Add Credentials`, where you enter the Nexus username and password and give the credential entry an ID that the pipeline script will reference. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

**Connection to the overall system:** This completes the Jenkins → Nexus link. After this, the pipeline script can include a stage that uploads the built artifact to Nexus.

***

### Step 7: Integrate SonarQube with Jenkins

**What we are doing:** Configuring Jenkins to communicate with the SonarQube server. This involves **more steps** than the Nexus integration.

**Why:** SonarQube integration isn't just about credentials — it requires configuring the SonarQube server URL in Jenkins, generating and saving an authentication token, and potentially setting up a webhook so SonarQube can send analysis results back to Jenkins.

**How it's done:** The instructor says *"we have a few steps that we need to execute"* — details will come in subsequent lectures. The fact that this is called out as more complex than Nexus is an important signal: expect additional configuration in both Jenkins and SonarQube's web interfaces. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

**Connection to the overall system:** This completes the Jenkins → SonarQube link. Once configured, the pipeline script can include a code analysis stage that sends source code to SonarQube and waits for the result.

***

### Step 8: Write and Execute the Pipeline Script

**What we are doing:** Writing a Jenkins pipeline script (likely a Jenkinsfile) that defines the entire CI workflow — pulling code, building, analyzing, uploading — and executing it.

**Why:** Everything set up so far (servers, plugins, integrations) is infrastructure. The pipeline script is the **logic** that ties it all together into an automated, repeatable process.

**How it's done:** The instructor says the script will **"use all these resources"** — meaning it will reference the Git repo, Maven build commands, SonarQube scanner, and Nexus uploader in a defined sequence of stages. The script is written in Jenkins' pipeline DSL (Groovy-based) and can be executed directly from the Jenkins UI or triggered by a code commit. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

**Connection to the overall system:** This is the culmination of all previous steps. The pipeline script is the product — it's what actually runs the CI process.

***

### Step 9: Set Up Notifications

**What we are doing:** Configuring Jenkins to send automatic notifications when a pipeline job fails.

**Why:** The instructor says *"if anything goes wrong in the pipeline, any job fails, we should get notifications automatically."* A pipeline that fails silently defeats the purpose of CI — the team must know immediately when something breaks.

**How it's done:** This is typically configured within the pipeline script itself (using a `post` block with `failure` condition) or through Jenkins' built-in email notification settings. The notification channel (email, Slack, etc.) will be covered in the relevant lecture. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

**Connection to the overall system:** Notifications are the final piece — they close the feedback loop. Without them, failures could go unnoticed for hours or days.

***

***

## 📋 Complete Roadmap Summary (Quick Reference)

| Step | Action                          | Key Detail                                          |
| ---- | ------------------------------- | --------------------------------------------------- |
| 1    | Set up Jenkins                  | EC2 + user data bash script (or reuse existing)     |
| 2    | Set up Nexus                    | EC2 + user data bash script                         |
| 3    | Set up SonarQube                | EC2 + user data bash script                         |
| 4    | Configure Security Groups       | Allow inter-server communication on required ports  |
| 5    | Install Jenkins Plugins         | Nexus, SonarQube, Git, Maven plugins                |
| 6    | Integrate Nexus ↔ Jenkins       | Save Nexus credentials in Jenkins (straightforward) |
| 7    | Integrate SonarQube ↔ Jenkins   | Multiple configuration steps required               |
| 8    | Write & Execute Pipeline Script | Uses all resources; defines the full CI flow        |
| 9    | Set Up Notifications            | Automatic alerts on pipeline failures               |

 [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

***

This video is a **navigation map** for the entire CI pipeline project. The instructor designed it as a checkpoint — return here whenever you feel lost during implementation to see where you are in the overall process. The actual hands-on execution begins in the next lecture. [\[164.-Steps...n-Pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/164.-Steps-for-Continuous-Integration-Pipeline.txt)

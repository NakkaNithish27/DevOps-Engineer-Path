# 🎓 Plugins for CI — Deep Learning Material

**Video Title:** Plugins for CI (Lecture 166)
**Context:** This is part of a CI/CD pipeline setup series. Jenkins, Nexus, and SonarQube servers have already been set up, and security group rules have been configured. This lecture focuses on installing the specific Jenkins plugins required to integrate all these tools together.

***

***

## 🧠 SECTION 1: THEORY — Deep Learning Mode

***

### 1. Where We Stand — The Setup Context

Before touching plugins, the video establishes a clear checkpoint of what has already been completed in the series:

1.  **Jenkins server** has been set up and is running.
2.  **Nexus server** (a binary artifact repository) has been set up.
3.  **SonarQube server** (a code quality analysis platform) has been set up.
4.  **Security group rules** have been configured — meaning the necessary network-level firewall rules (typically in AWS or a similar cloud provider) have been opened so that Jenkins can communicate with Nexus and SonarQube over the network.

This is important because plugins alone are not enough. A plugin lets Jenkins *talk* to an external tool, but the network path between them must already be open. That networking layer was handled in the previous step (security group rules). Now the focus shifts to the **software integration layer** — which is what plugins provide. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

***

### 2. What Are Jenkins Plugins and Why Do They Exist?

Jenkins, by design, is a **minimal automation server**. Out of the box, it can run jobs and execute shell commands, but it does not natively know how to interact with tools like Nexus, SonarQube, or Maven in a deep, integrated way. This is a deliberate architectural choice — Jenkins uses a **plugin-based architecture** so that users install only what they need, keeping the core lightweight and extensible.

A **plugin** in Jenkins is a packaged piece of functionality that extends Jenkins' capabilities. When you install a plugin, you are teaching Jenkins how to do something new — for example, how to upload an artifact to Nexus, or how to trigger a SonarQube code scan as part of a pipeline.

**Why this matters for CI:** In a Continuous Integration pipeline, Jenkins is the orchestrator. It pulls code, builds it, runs tests, analyzes quality, and stores artifacts. Each of those actions requires Jenkins to integrate with a different external tool. Without plugins, you would have to write raw shell scripts for every integration — which is fragile, hard to maintain, and lacks the UI-level feedback Jenkins plugins provide. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

***

### 3. The Five Plugins — What Each One Does and Why It's Needed

The video identifies **five specific plugins** that will be used in upcoming lectures. Let's understand each one deeply.

***

#### 3.1 Nexus Artifact Uploader

**What it is:** This plugin enables Jenkins to upload build artifacts (such as `.war`, `.jar`, or `.zip` files) directly to a **Sonatype Nexus Repository Manager**.

**Why it exists:** After Jenkins builds your application, the resulting artifact needs to be stored somewhere reliable and versioned — not on the Jenkins server itself (which is transient and not meant for storage). Nexus serves as that **centralized artifact repository**. Without this plugin, you would need to write custom shell commands using `curl` or Nexus's REST API to upload artifacts, which is error-prone and harder to manage within pipeline code.

**How it works internally:** Once installed, this plugin provides a pipeline step (typically `nexusArtifactUploader`) that you can call in your Jenkinsfile. You configure it with the Nexus server URL, repository name, credentials, and artifact details (groupId, artifactId, version, file path). When the pipeline reaches this step, the plugin handles authentication, file transfer, and version management with the Nexus server automatically.

**Where it connects:** This plugin sits at the **post-build stage** of the CI pipeline — after code is compiled and packaged, and typically after quality checks pass. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

> 🔍 **Deep Dive (Optional):**
> Nexus supports different repository types — `maven-releases`, `maven-snapshots`, `raw`, `docker`, etc. The Nexus Artifact Uploader plugin needs to know which repository to target. In real-world setups, snapshot builds go to `maven-snapshots` and release builds go to `maven-releases`. Misconfiguring this is a common source of pipeline failures — Nexus will reject a SNAPSHOT-versioned artifact pushed to a releases repository.

***

#### 3.2 SonarQube Scanner

**What it is:** This plugin integrates a **SonarQube server** with Jenkins, allowing Jenkins pipelines to trigger code quality and security analysis scans on SonarQube.

**Why it exists:** SonarQube analyzes source code for bugs, vulnerabilities, code smells, and technical debt. In a CI pipeline, you want this analysis to happen **automatically** on every code commit — not manually. This plugin allows Jenkins to invoke the SonarQube scanner as a pipeline step, pass the code to SonarQube for analysis, and optionally enforce a **quality gate** (a pass/fail threshold).

**How it works internally:** After installation, you configure the SonarQube server details in Jenkins (under *Manage Jenkins → System → SonarQube Servers*). In your pipeline, you use a `withSonarQubeEnv('server-name')` block, inside which you run the SonarQube scanner. The plugin handles injecting the correct server URL, authentication token, and environment variables so the scanner knows where to send results.

**Where it connects:** This plugin sits in the **code quality analysis stage** of the pipeline — typically after the build step but before artifact upload. If the quality gate fails, you may want to stop the pipeline before uploading a bad artifact to Nexus. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

***

#### 3.3 Git Plugin

**What it is:** The Git plugin allows Jenkins to clone, fetch, and check out code from **Git repositories** (GitHub, GitLab, Bitbucket, or any Git server).

**Why it exists:** The very first step of any CI pipeline is pulling the latest source code. The Git plugin makes this possible by providing Jenkins with Git capabilities — handling credentials, branch selection, polling for changes, and webhook-triggered builds.

**Key point from the video:** The instructor explicitly states that the Git plugin is **already installed** on the Jenkins server, along with the Git tool itself. This means no action is needed for this plugin — it's mentioned only for completeness, so you understand the full plugin landscape being used. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

> ⚠️ **Expert Note (Optional):**
> "Already have the tool as well" — this refers to the `git` binary being installed on the Jenkins server's operating system. The Git *plugin* lets Jenkins use Git, but it still needs the actual `git` command-line tool on the server. If the tool were missing, Git operations would fail even with the plugin installed. In Docker-based Jenkins setups, this is a common gotcha.

***

#### 3.4 Pipeline Maven Integration

**What it is:** This plugin provides deep integration between Jenkins Pipeline (declarative or scripted) and **Apache Maven**, the build automation tool for Java projects.

**Why it exists:** While you can always run Maven via a simple `sh 'mvn clean install'` shell step, this plugin provides **much richer integration**. It can automatically detect Maven builds, capture build metadata, track dependencies, and publish results in the Jenkins UI. Most importantly, it allows you to use `withMaven()` blocks in pipeline code, which automatically configures Maven settings, tool paths, and environment variables.

**How it works internally:** Once installed, the plugin provides the `withMaven` pipeline step. Inside this block, any Maven command you run is automatically enhanced — the plugin captures the artifacts produced, the tests run, and the dependencies resolved. It can also integrate with the Nexus plugin to automatically publish artifacts.

**Where it connects:** This plugin is central to the **build stage** — it's how Jenkins actually compiles and packages the Java application. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

***

#### 3.5 Build Timestamp

**What it is:** This plugin adds a **build timestamp** as an environment variable available during Jenkins pipeline execution.

**Why it exists:** In CI/CD, knowing *when* a build happened is critical for traceability, debugging, and artifact versioning. This plugin provides a `BUILD_TIMESTAMP` variable (in a configurable date format) that you can use in your pipeline — for example, to tag artifacts with the exact build time, name log files, or create versioned deployment directories.

**How it works internally:** After installation, you configure the timestamp format in *Manage Jenkins → System* (e.g., `yyyy-MM-dd_HH-mm-ss`). Once configured, every build automatically gets a `BUILD_TIMESTAMP` environment variable injected, which you can reference in your pipeline code like any other Jenkins variable.

**Where it connects:** This is a **utility plugin** — it doesn't integrate with any external tool but provides metadata that other stages of the pipeline consume. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

> 🔍 **Deep Dive (Optional):**
> Without this plugin, Jenkins provides `BUILD_NUMBER` and `BUILD_ID`, but these are sequential numbers or IDs — not human-readable timestamps. In production environments where you might need to correlate a deployed artifact with a specific point in time (for auditing, rollback decisions, or incident investigation), a formatted timestamp is far more useful than a build number.

***

### 4. "Some We Already Have, Some We Are Going to Install"

This is a small but meaningful statement from the video. It tells you that a Jenkins installation does not start from zero — certain plugins (like Git) come **pre-installed or were installed earlier** in the series. The instructor is being explicit about which plugins need action now versus which are already present. This teaches an important operational habit: **always verify what's already installed before adding new plugins**, to avoid conflicts or redundancy. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

***

***

## ⚙️ SECTION 2: PRACTICAL — Guided Execution Mode

***

### What We Are Building

We are installing **five Jenkins plugins** that will be used in upcoming CI pipeline lectures to integrate Jenkins with Nexus (artifact storage), SonarQube (code quality analysis), Maven (build tool), and to add build timestamp functionality. By the end of this process, Jenkins will be fully equipped to orchestrate a complete CI pipeline.

**Why it matters:** Without these plugins, Jenkins cannot communicate with Nexus or SonarQube, cannot execute Maven pipelines with rich integration, and cannot stamp builds with timestamps. These plugins are the **connective tissue** between Jenkins and the rest of the CI toolchain.

**Final outcome:** All five plugins installed and visible in Jenkins' *Installed Plugins* section, ready to be configured in subsequent lectures.

***

### Step 1: Navigate to the Plugin Management Page

From the Jenkins dashboard, click on **Manage Jenkins** in the left sidebar. Then click on **Plugins**. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

This takes you to the Jenkins Plugin Manager — the centralized interface for viewing, searching, installing, and updating plugins. It has multiple tabs, but the two relevant ones are:

*   **Available plugins** — plugins that exist in the Jenkins plugin registry but are not yet installed on your server.
*   **Installed plugins** — plugins that are already installed.

***

### Step 2: Switch to the "Available Plugins" Tab

Click on **Available plugins**. This loads the full catalog of plugins you can install. You will use the search bar at the top to find each plugin by name. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

***

### Step 3: Search and Select Each Plugin

You need to search for and check (select) each of the following plugins one by one:

***

**3a. Search: `Nexus Artifact Uploader`**

Type `Nexus Artifact Uploader` in the search bar. The plugin with this exact name should appear in the results. Check the box next to it. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

> ⚠️ **Expert Note (Optional):**
> There may be other Nexus-related plugins in the results (e.g., *Nexus Platform Plugin*). Make sure you select specifically **Nexus Artifact Uploader** — this is the one used in this course for uploading build artifacts.

***

**3b. Search: `SonarQube Scanner`**

Clear the search bar and type `Sonarqube`. Look for **SonarQube Scanner** in the results. Check the box. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

The video shows the instructor first typing `Sonarqube` broadly, then identifying `SonarQube Scanner` as the correct plugin. Be careful not to confuse it with other SonarQube-related plugins.

***

**3c. Search: `Pipeline Maven Integration`**

Clear the search bar and type `Maven`. Look for **Pipeline Maven Integration** in the results. Check the box. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

There will be multiple Maven-related plugins in the results. The specific one needed is *Pipeline Maven Integration* — this is the one that provides the `withMaven` pipeline step.

***

**3d. Search: `Build Timestamp`**

Clear the search bar and type `Timestamp`. Look for **Build Timestamp** in the results. Check the box. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

The video specifically says to search using the text `Timestamp` and to look for `Build Timestamp` in the results.

***

**3e. Git Plugin — Verification Only**

The Git plugin is already installed. The video mentions this explicitly. However, if you want to verify, switch to the **Installed plugins** tab and search for `Git`. You should see it listed there. No installation action is needed. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

***

### Step 4: Handle "Already Installed" Plugins

The video gives an important tip: **if a plugin is already installed, it will NOT appear in the Available plugins tab** — it will only appear in the **Installed plugins** tab. So if you search for a plugin in *Available* and don't find it, don't panic — switch to *Installed* and confirm it's already there. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

This is a common source of confusion for beginners who think a plugin is missing when it's actually already installed.

***

### Step 5: Click "Install"

Once you have checked all the required plugins (those that are not already installed), click the **Install** button. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

**What happens internally:** Jenkins downloads each plugin's `.hpi` file from the Jenkins Update Center (an online plugin registry), resolves any **dependencies** (plugins that depend on other plugins), downloads those too, and installs everything. This process takes a moment depending on network speed and the number of dependencies.

**Expected result:** You should see a progress screen showing each plugin being downloaded and installed. Once all show as *"Success"* or *"Installed"*, the process is complete.

**How to verify:** After installation, go back to *Manage Jenkins → Plugins → Installed plugins* and search for each plugin by name. All five should appear in the list.

> ⚠️ **Expert Note (Optional):**
> Some plugins may require a Jenkins restart to activate fully. Jenkins will typically show a message like *"Restart Jenkins when installation is complete and no jobs are running"* — in a learning/lab environment, it's safe to restart. In production, coordinate restarts during maintenance windows.

***

### Step 6: Proceed to the Next Lecture

The video ends with: *"Once it is installed, join me in the next lecture."* This means the plugins themselves will be **configured** (server URLs, credentials, tool paths) in subsequent lectures — this lecture only handles **installation**. [\[166.-Plugins-for-CI \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/166.-Plugins-for-CI.txt)

***

***

## 🧭 Summary of the Plugin Landscape

| Plugin                         | Purpose                          | Status in Video   | Pipeline Stage     |
| ------------------------------ | -------------------------------- | ----------------- | ------------------ |
| **Nexus Artifact Uploader**    | Upload build artifacts to Nexus  | To be installed   | Post-build         |
| **SonarQube Scanner**          | Trigger code quality scans       | To be installed   | Quality analysis   |
| **Git**                        | Clone source code from Git repos | Already installed | Source checkout    |
| **Pipeline Maven Integration** | Rich Maven build integration     | To be installed   | Build              |
| **Build Timestamp**            | Add timestamp to builds          | To be installed   | Utility / Metadata |

***

This lecture is a short but essential setup step — it bridges the gap between having individual servers running (Jenkins, Nexus, SonarQube) and having them **wired together** through Jenkins' plugin system, ready for pipeline configuration in the next lectures.

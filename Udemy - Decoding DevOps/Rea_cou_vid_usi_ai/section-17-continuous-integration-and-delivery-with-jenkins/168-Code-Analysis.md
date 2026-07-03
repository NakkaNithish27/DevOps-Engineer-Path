# 📘 Code Analysis — Deep Learning Material

*Reconstructed from video lecture: [168.-Code-Analysis.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt?EntityRepresentationId=fbdde800-b1eb-4039-9073-d5afa448c21f)* [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

### What Is Code Analysis?

Code analysis is the process of systematically examining your application's source code to identify potential issues, enforce best practices, and improve overall code quality. It is not about testing whether the application *works* (that's what unit tests do) — it is about testing whether the code itself is *written well*. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

Think of it this way: unit testing asks *"Does this code produce the correct output?"* Code analysis asks *"Is this code written safely, cleanly, and maintainably?"* These are fundamentally different questions, and both must be answered in a professional software pipeline.

Code analysis sits as a **gate** in your CI/CD pipeline. In the flow described in this lecture, the pipeline first fetches code from GitHub, builds it using Maven, executes unit test cases, and **then** performs code analysis as the next stage. This positioning is deliberate — there is no point analyzing code that doesn't even compile or pass basic tests. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

> 🔍 **Deep Dive (Optional)**
>
> Code analysis is broadly categorized into **static analysis** (examining code without executing it) and **dynamic analysis** (examining code during runtime). What this lecture covers — using tools like SonarQube and Checkstyle — falls squarely into **static analysis**. The source code is scanned as text/bytecode, pattern-matched against rulesets, and flagged for violations. No part of the application is actually *run* during this process.

***

### Why Code Analysis Matters

The lecture identifies several concrete reasons why code analysis is critical. Each of these maps to a real-world problem: [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

**1. Improving Code Quality.**
Code quality is not just about aesthetics. Poorly structured code is harder to debug, harder to extend, and more expensive to maintain. Code analysis enforces consistent quality across the entire codebase, regardless of which developer wrote which module. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

**2. Detecting Security Vulnerabilities.**
When developers do not follow best practices, they can inadvertently introduce security vulnerabilities — SQL injection points, hardcoded credentials, insecure deserialization, and so on. Hackers actively look for and exploit these weaknesses. Code analysis detects these vulnerabilities at a very early stage, before the application is anywhere near production. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

**3. Catching Shortcut-Driven Mistakes.**
Developers chasing deadlines will take shortcuts. This is a universal reality. These shortcuts — skipping null checks, ignoring edge cases, duplicating code blocks — will create issues later. Code analysis catches these early, when fixing them is cheap and fast. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

**4. Enforcing Consistent Coding Standards.**
In a team, different developers have different habits. Code analysis ensures everyone follows the same best practices and coding standards, making the codebase consistent and predictable. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

**5. Saving Time (Shift-Left Principle).**
Catching issues earlier in the development lifecycle is exponentially cheaper than catching them in production. A bug found during code analysis might take 10 minutes to fix; the same bug found in production could take days of debugging, hotfixes, and rollbacks. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

**6. Fitting Into Automated DevOps Workflows.**
Because code analysis is automated, it integrates seamlessly into CI/CD pipelines. There is no manual review gate — the pipeline runs analysis automatically on every build, every commit, every merge. This is essential for DevOps velocity. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

> ⚠️ **Expert Note**
>
> The lecture emphasizes that code analysis detects vulnerabilities that "will be used by hackers to exploit the application." In production environments, this is not hypothetical. Automated vulnerability scanners constantly probe public-facing applications. If your code has a known vulnerability pattern (e.g., an unparameterized SQL query), it *will* be found and exploited. Code analysis is a frontline defense.

***

### Code Analysis Tools Landscape

The lecture mentions several popular tools, each serving a specific purpose: [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

| Tool                    | Purpose                                                                          |
| ----------------------- | -------------------------------------------------------------------------------- |
| **SonarQube**           | Comprehensive code quality and security analysis platform (used in this lecture) |
| **ESLint**              | Linting tool for JavaScript and TypeScript                                       |
| **Checkstyle**          | Enforces Java coding standards and style rules (also used in this lecture)       |
| **PMD**                 | Detects common coding flaws (dead code, empty blocks, unnecessary objects, etc.) |
| **FindBugs / SpotBugs** | Finds potential bugs in Java bytecode                                            |

The lecture notes that many more tools exist, including enterprise-grade solutions. For this course section, **SonarQube** and **Checkstyle** are the tools being used. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

> 🔍 **Deep Dive (Optional)**
>
> SonarQube is not just a single-purpose scanner — it is a **platform**. It has its own server, its own dashboard, its own rule engine (called Quality Profiles), and its own pass/fail system (called **Quality Gates**). The lecture references quality gates as how SonarQube "detects issues." A quality gate is a set of threshold conditions (e.g., "no critical vulnerabilities," "code coverage above 80%," "no more than 5 code smells"). If the analyzed code violates any condition in the quality gate, the gate **fails**, and the pipeline can be configured to stop.

***

### Architecture: How Code Analysis Fits Into the Pipeline

The lecture describes a clear architectural flow: [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

After Maven executes unit testing, a **new stage** is added to the Jenkins pipeline that performs code analysis using the **SonarQube Scanner Tool**. This is directly analogous to how Maven works in the pipeline — just as you need the Maven tool and the Maven plugin installed in Jenkins, you need the **SonarQube CLI (Command-Line Interface) plugin** and the **SonarQube CLI Tool** installed in Jenkins. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

The scanner runs locally on the Jenkins agent, analyzes the code, and then **sends all the results to the SonarQube server**. The SonarQube server processes these results, displays them on its dashboard, and evaluates them against the configured **quality gates**. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

For this to work, **Jenkins must be integrated with the SonarQube server**. This integration has two parts:

1.  Adding the SonarQube Scanner Tool to Jenkins (so Jenkins can *run* the analysis)
2.  Configuring the SonarQube Server connection in Jenkins (so Jenkins knows *where to send* the results) [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

The lecture also foreshadows that in a later lecture, **webhooks** will be set up so that SonarQube can send the quality gate status *back* to Jenkins. This creates a two-way communication: Jenkins sends results to SonarQube, and SonarQube sends the pass/fail verdict back to Jenkins. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

> 🔍 **Deep Dive (Optional)**
>
> The reason Jenkins needs the SonarQube Scanner as a *tool* (not just a plugin) is because the scanner is an actual executable that runs during the build. The plugin provides Jenkins with the UI configuration and pipeline DSL integration (`withSonarQubeEnv`, etc.), but the *tool* is what actually performs the scan. This is the same pattern as Maven: the Maven plugin gives Jenkins the ability to invoke Maven, but the Maven tool is the actual `mvn` binary.

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

### What We Are Building

In this practical section, we are **preparing Jenkins to perform automated code analysis using SonarQube**. Specifically, we are doing two things: installing the SonarQube Scanner tool in Jenkins, and configuring Jenkins to communicate with an existing SonarQube server. We are also securing the network communication between the two servers using AWS Security Groups. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

By the end of this setup, Jenkins will have everything it needs to run code analysis as a pipeline stage, send the results to SonarQube, and (in a future lecture) receive the quality gate verdict back. The actual pipeline code is written in the next lecture — this lecture is purely about the integration and configuration groundwork.

***

### Step 1: Adding the SonarQube Scanner Tool in Jenkins

We need to install the SonarQube Scanner tool so that Jenkins has the binary available to execute code scans during pipeline runs. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

**Navigate to the tool configuration:**

1.  Go to **Manage Jenkins** → **Tools**
2.  Scroll down until you find **SonarQube Scanner Installations**

⚠️ There is a similarly named option — **SonarQube Scanner for MSBuild**. Do **not** use that one. MSBuild is for .NET projects. You need the standard **SonarQube Scanner Installations** section. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

3.  Click **Add SonarQube Scanner**

**Configure the tool:**

*   **Version**: Select `8.0.1.6346`
    *   The lecture explicitly states to stick to this version because it is **tested**. Using a different version might work, but introduces risk of compatibility issues with the pipeline code that will be written later. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

*   **Name**: Enter `sonar8.0`
    *   This name is critical. It is not just a label — this **exact name** will be referenced in the Jenkins pipeline code. If you name it differently, you must use that different name in your pipeline code. For consistency, use `sonar8.0`. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

4.  Click **Save**.

Jenkins will auto-install this tool version the first time a pipeline references it. At this point, the scanner tool is registered but has not yet been downloaded — that happens on first use.

***

### Step 2: Configuring the SonarQube Server Connection in Jenkins

Now we tell Jenkins *where* the SonarQube server is and *how* to authenticate with it. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

**Navigate to the server configuration:**

1.  Go to **Manage Jenkins** → **System**
2.  Scroll down to find the **SonarQube servers** section

**Configure the connection:**

3.  Check the box for **Environment Variables**
    *   This enables Jenkins to inject SonarQube-related environment variables (like the server URL and authentication token) into the build environment automatically when you use `withSonarQubeEnv()` in your pipeline code. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

4.  Click **Add SonarQube**

5.  **Name**: Enter `sonarserver`
    *   Again, stick to this exact name for consistency with the upcoming pipeline code. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

6.  **Server URL**: Enter `http://<private-IP-of-SonarQube-server>`

    This is the private IP address of the EC2 instance (or server) where SonarQube is running. You need to go to your cloud console (e.g., AWS EC2 dashboard), find the SonarQube server instance, and copy its **private IP address**. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

    **About the port:** SonarQube natively listens on **port 9000**. However, in this setup, there is an **NGINX reverse proxy** sitting in front of SonarQube, and NGINX listens on **port 80** (the default HTTP port). So you can either write `http://<private-IP>:80` or simply `http://<private-IP>` — omitting the port defaults to port 80. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

> 🔍 **Deep Dive (Optional)**
>
> The NGINX reverse proxy is significant. Without it, you'd need to expose port 9000 directly, which is a non-standard port and requires explicit security group rules. With NGINX in front, all traffic comes through the standard HTTP port 80, simplifying firewall rules and making the setup more conventional. NGINX receives the request on port 80 and internally forwards it to SonarQube on port 9000.

***

### Step 3: Generating an Authentication Token on SonarQube

Jenkins needs to authenticate with the SonarQube server to upload analysis results. This is done via a **token**, not a username/password. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

**On the SonarQube server dashboard:**

1.  Click your profile icon in the **top-right corner** → select **Account**
2.  Go to **My Account** → click the **Security** tab
3.  You will see a section for generating tokens

**Generate the token:**

*   **Token Name**: `Jenkins`
    *   This is just a label to help you remember what this token is used for. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)
*   **Type**: Select **User Token**
    *   A user token inherits the permissions of the user who generates it. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)
*   **Expires**: You have two choices:
    *   **30 days** — The token will stop working after 30 days, and you'll need to generate a new one and re-save it in Jenkins. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)
    *   **No expiration** — The token works indefinitely. Convenient, but less secure.
    *   The lecture chooses 30 days but notes the trade-off.

4.  Click **Generate**
5.  **Copy the token immediately** — it will only be displayed once. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

> ⚠️ **Expert Note**
>
> In production environments, token expiration policies are typically enforced. A 30-day token means you have a recurring maintenance task: every 30 days, generate a new token, update it in Jenkins credentials, and verify the pipeline still works. If you forget, your pipeline will silently fail at the code analysis stage. For learning environments, "no expiration" is simpler. For production, automate token rotation.

***

### Step 4: Saving the Token as a Jenkins Credential

Now we store the copied token securely inside Jenkins so that the SonarQube server configuration can reference it. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

**Back in Jenkins (Manage Jenkins → System → SonarQube servers section):**

1.  Next to the **Server authentication token** dropdown, click **Add** → select **Global**
2.  In the credential creation dialog:
    *   **Kind**: Select **Secret text**
        *   This is the correct credential type for a single token value (as opposed to username/password pairs). [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)
    *   **Secret**: Paste the token you copied from SonarQube
    *   **ID**: Enter `sonar token`
        *   This is the internal Jenkins identifier for this credential. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)
    *   **Description**: Enter `sonar token` (or any descriptive label)
3.  Click **Create**

**Critical step — Select the token:**

After creating the credential, you are returned to the SonarQube server configuration. The token dropdown will **not** automatically select your new credential. You **must manually select** the `sonar token` credential from the dropdown. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

4.  Select the token from the dropdown
5.  Click **Save**

> ⚠️ **Expert Note**
>
> Forgetting to select the token after creation is a very common mistake. Jenkins creates the credential but does not auto-apply it. If you save without selecting, the SonarQube integration will fail with authentication errors when the pipeline runs.

***

### Step 5: Configuring AWS Security Groups for Jenkins ↔ SonarQube Communication

Both Jenkins and SonarQube are running on separate servers (EC2 instances in AWS). For them to communicate, the **Security Groups** (AWS firewalls) must allow the correct traffic between them. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

#### 5a. SonarQube Server Security Group

Jenkins uploads code analysis results to the SonarQube server on **port 80** (through NGINX). Therefore, the SonarQube server's security group must allow inbound traffic on port 80. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

**Navigate to:** SonarQube Server → Security → Security Groups → **Edit Inbound Rules**

Configure:

| Port   | Source                     | Purpose                                                        |
| ------ | -------------------------- | -------------------------------------------------------------- |
| **80** | **Jenkins Security Group** | Allows Jenkins to upload analysis results to SonarQube         |
| **80** | **My IP**                  | Allows you to access the SonarQube dashboard from your browser |

The lecture explicitly warns: do **not** use "Anywhere" (0.0.0.0/0) as the source for port 80. While it works, it exposes your SonarQube dashboard to the entire internet. Instead, restrict access to only the Jenkins security group and your own IP address. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

Save the rules.

#### 5b. Jenkins Server Security Group

In a future lecture, **webhooks** will be configured so that SonarQube sends the quality gate status back to Jenkins. SonarQube will contact Jenkins on **port 8080** (Jenkins' default port). Therefore, the Jenkins security group must allow inbound traffic on port 8080 from SonarQube. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

**Navigate to:** Jenkins Server → Security → Security Groups → **Edit Inbound Rules**

Configure:

| Port     | Source                       | Purpose                                                                     |
| -------- | ---------------------------- | --------------------------------------------------------------------------- |
| **8080** | **SonarQube Security Group** | Allows SonarQube to send webhook callbacks (quality gate status) to Jenkins |

Save the rules. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

> 🔍 **Deep Dive (Optional)**
>
> Notice the asymmetry: Jenkins → SonarQube communicates on **port 80** (because NGINX fronts SonarQube), but SonarQube → Jenkins communicates on **port 8080** (Jenkins' native port, with no reverse proxy in front). This is a common pattern — reverse proxies are typically placed in front of servers that need public/browser access (like SonarQube's dashboard), while internal-only communication (like webhook callbacks) may go directly to the application port.

***

### Connection to the Overall System

At the end of this lecture, the integration groundwork is complete: [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

*   ✅ Jenkins has the **SonarQube Scanner tool** registered (ready to execute scans)
*   ✅ Jenkins knows the **SonarQube server URL** and has a valid **authentication token**
*   ✅ **Network rules** allow bidirectional communication between Jenkins and SonarQube

What remains (in the next lecture) is writing the **pipeline code** — the actual Jenkinsfile stage that invokes the scanner, runs the analysis, and uploads results to the SonarQube server. The configuration done in this lecture is referenced directly in that pipeline code (the tool name `sonar8.0`, the server name `sonarserver`), which is why naming consistency was emphasized throughout. [\[168.-Code-Analysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/168.-Code-Analysis.txt)

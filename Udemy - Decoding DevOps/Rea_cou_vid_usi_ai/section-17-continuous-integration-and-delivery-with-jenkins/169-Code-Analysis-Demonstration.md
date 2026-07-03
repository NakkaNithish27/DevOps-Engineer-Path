# 🎬 Code Analysis Demonstration — Deep Learning Material

**Video Title:** Code Analysis Demonstration
**Source:** Caption file from DevOps CI/CD pipeline course (Video #169)
**Resource Files:** [169. PAAC\_Checkstyle.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_Checkstyle.txt?EntityRepresentationId=dc3ebf57-6873-4334-8f34-c9d9b527833a) and [169. PAAC\_SonarCodeAnalysis.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_SonarCodeAnalysis.txt?EntityRepresentationId=996eecf8-0250-4c47-9d2a-4f79e75e6692)

This video walks through building a Jenkins pipeline that performs **Checkstyle code analysis**, then extends it to push all code analysis results to a **SonarQube server** for human-readable visualization. It covers pipeline scripting, Groovy-specific syntax, SonarQube scanner configuration, and real troubleshooting of a production failure — all within a continuous integration context using the **vprofile** Java project. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. Checkstyle — A Static Code Analysis Tool for Java

Checkstyle is a **static code analysis tool** specifically designed for Java projects. Its job is to examine your source code and check whether it follows a defined set of **coding standards and conventions** — things like naming conventions, code formatting, method length, import ordering, Javadoc comments, and structural patterns. It does not check whether your code *works*; it checks whether your code is *written properly* according to agreed-upon rules. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

In this video, Checkstyle is invoked through **Maven** using the command `mvn checkstyle:checkstyle`. This means Maven downloads the Checkstyle plugin (and its dependencies/binaries) automatically, then runs the analysis against the project source code. The output is an **XML file** — specifically `target/checkstyle-result.xml` — that contains every violation found. In the demonstration, it reported **641 errors** using Checkstyle version 9.3. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

The critical insight the instructor makes is this: the raw XML file is essentially **unreadable by humans**. He opens it in the Jenkins workspace browser and sarcastically asks "that's a beautiful view, isn't it? I mean, you can read everything. Only if you are a superhuman." The point is clear — generating analysis results is only half the job. You need a **dashboard** to interpret and present those results in a meaningful way. This is exactly where SonarQube comes in. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

> 🔍 **Deep Dive (Optional)**
>
> Checkstyle is "just one code analysis tool" — the instructor explicitly states there are **many** code analysis tools available. In a real pipeline, you might also use tools like PMD (for detecting common programming flaws), FindBugs/SpotBugs (for bug pattern detection), or OWASP Dependency Check (for security vulnerabilities in dependencies). All of these produce their own result files, and all of them can be pushed to SonarQube for centralized visualization. The pipeline pattern shown here — run a tool via Maven, capture the result file, then forward it to SonarQube — applies to all of them. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

## 2. SonarQube Server — The Code Quality Dashboard

SonarQube is a **centralized code quality management server**. It receives analysis results from various code analysis tools (Checkstyle, JaCoCo, JUnit, its own built-in analyzers, etc.), processes them, and presents them in a **human-readable dashboard** organized by project. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

The real-world problem it solves is straightforward: when your pipeline runs Checkstyle, unit tests, coverage analysis, and security scans, each tool produces its own report file in its own format (XML, JSON, etc.). No developer wants to read through thousands of lines of XML. SonarQube aggregates all these results into a single web interface where you can see at a glance: how many bugs exist, how many security vulnerabilities were found, how many code style violations there are, what your test coverage percentage is, and whether your code passes or fails the defined quality standards. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

In the demonstration, after the pipeline successfully pushes results to SonarQube, the dashboard for the **vprofile** project shows: **3 security issues**, **5,200 reliability issues**, and **25 security hotspots**. Despite these numbers, the overall status shows **"Pass"** — because the **Quality Gate** (discussed in the next lecture) was not configured to block on these specific thresholds. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

> ⚠️ **Expert Note (Optional)**
>
> The instructor mentions that the analysis log shows a **private IP** for the SonarQube result URL, which cannot be accessed from the browser — you need to use the **public IP** of the SonarQube server instead. This is a common gotcha in cloud-based setups (e.g., AWS EC2): the server internally knows itself by its private IP, but you access it externally via the public IP. Always use the public IP when navigating to the SonarQube dashboard from your browser. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

## 3. SonarQube Scanner — The CLI Bridge Between Pipeline and Server

The **SonarQube Scanner** (also called Sonar Scanner CLI) is the command-line tool that actually performs the scanning of source code and **pushes the results** to the SonarQube server. It is installed as a **tool in Jenkins** (in this case, named `sonar8.0` under Manage Jenkins → Tools → SonarQube Scanner installations). [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

The scanner is invoked in the pipeline via its binary path: `${scannerHome}/bin/sonar-scanner`, where `scannerHome` is a variable pointing to the installed tool's directory. Along with this command, you pass **parameters** (prefixed with `-D`) that tell the scanner what project this is, where the source code lives, and where to find the various analysis report files. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt), [\[169. PAAC_...deAnalysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_SonarCodeAnalysis.txt)

The parameters used in this video are:

| Parameter                                | Value                           | Purpose                                                     |
| ---------------------------------------- | ------------------------------- | ----------------------------------------------------------- |
| `-Dsonar.projectKey`                     | `vprofile`                      | Unique identifier for the project on SonarQube server       |
| `-Dsonar.projectName`                    | `vprofile`                      | Human-readable display name on the dashboard                |
| `-Dsonar.projectVersion`                 | `1.0`                           | Version label for tracking analysis over time               |
| `-Dsonar.sources`                        | `src/`                          | Path to the source code directory in the workspace          |
| `-Dsonar.java.binaries`                  | `target/classes`                | Path to compiled Java class files                           |
| `-Dsonar.junit.reportsPath`              | `target/surefire-reports`       | Path to JUnit test result reports (generated by `mvn test`) |
| `-Dsonar.coverage.jacoco.xmlReportPaths` | `target/site/jacoco/jacoco.xml` | Path to JaCoCo code coverage XML report                     |
| `-Dsonar.java.checkstyle.reportPaths`    | `target/checkstyle-result.xml`  | Path to Checkstyle result XML file                          |

 [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt), [\[169. PAAC_...deAnalysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_SonarCodeAnalysis.txt)

The instructor emphasizes: **you do not need to memorize these paths**. They are project-specific. The vprofile project uses `src/` for source code and `target/classes` for binaries, but another project might have different paths. What you need to understand is the **pattern**: when you scan code with any analysis tool, you need to tell the scanner where to find all the relevant result files so it can aggregate them and push everything to SonarQube. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

## 4. The `withSonarQubeEnv` Plugin — Connecting Jenkins to SonarQube

The `withSonarQubeEnv('sonarserver')` block is a Jenkins pipeline step provided by the **SonarQube plugin** for Jenkins. It wraps your scanner command and automatically injects the SonarQube server connection details (URL, authentication token, etc.) into the environment so the scanner knows *where* to send the results. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

The string inside the parentheses — `'sonarserver'` in this case — must **exactly match** the name you gave to the SonarQube server configuration in Jenkins (under Manage Jenkins → System → SonarQube servers). If the names don't match, the pipeline will fail because Jenkins won't know which server to connect to. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

Similarly, the tool reference `tool 'sonar8.0'` must exactly match the tool name configured under Manage Jenkins → Tools → SonarQube Scanner installations. The instructor explicitly navigates to both configuration screens in Jenkins to verify these names match. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

## 5. Groovy Scoping: `def`, `script`, and `environment` in Jenkins Pipelines

This is a **Groovy-specific** concept that directly affects how you write Jenkins pipeline scripts. The instructor encounters it while building the Sonar Code Analysis stage and explains the reasoning behind the final solution. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

The keyword `def` in Groovy declares a **local variable** — a variable whose scope is limited to the enclosing block (the nearest set of curly braces). In the initial version copied from documentation/AI, the variable `scannerHome` is declared as `def scannerHome = tool 'sonar8.0'` inside the stage. This is valid Groovy, but there is a catch: Jenkins Declarative Pipeline syntax has restrictions on where raw Groovy code can appear. If you want to use `def` inside a Declarative Pipeline, you must wrap it in a `script { }` block, which tells Jenkins "this is raw Groovy, execute it as-is." [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

However, the **best practice** shown in the video is to avoid `def` and `script` entirely by using the **`environment` section** instead. The `environment` block is a native Declarative Pipeline feature for defining variables. When placed inside a specific stage, the variables are **local to that stage** (not globally visible). When placed before the `stages` block (at the pipeline level), they become **global variables** accessible by all stages. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

The final solution uses:

```groovy
environment {
    scannerHome = tool 'sonar8.0'
}
```

placed inside the Sonar Code Analysis stage, making `scannerHome` a stage-local environment variable without needing `def` or `script`. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

> 🔍 **Deep Dive (Optional)**
>
> The distinction matters because Declarative Pipeline (which starts with `pipeline { }`) is intentionally more structured and restrictive than Scripted Pipeline (which starts with `node { }`). Declarative Pipeline expects specific sections (`agent`, `stages`, `steps`, `environment`, `post`, etc.) and does not allow arbitrary Groovy code outside of `script` blocks. This is a design choice — it makes pipelines more readable and maintainable at the cost of some flexibility. When you need raw Groovy (like `def`, `if/else`, loops), you either use a `script` block or find a Declarative equivalent. The `environment` section is the Declarative equivalent for variable declarations. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

## 6. Multi-Line Shell Commands in Jenkins Pipeline

When a shell command in a Jenkins pipeline is too long for a single line, you must use **triple single quotes** (`'''...'''`) to wrap it. A single-line command uses `sh 'command'` (single quotes), but a multi-line command uses `sh '''command line 1 \\ command line 2 \\ command line 3'''`. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

The instructor notes that the AI-generated example used triple *double* quotes, but triple *single* quotes also work. The backslash (`\\`) at the end of each line is a **line continuation character** in shell scripting — it tells the shell that the command continues on the next line. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt), [\[169. PAAC_...deAnalysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_SonarCodeAnalysis.txt)

***

## 7. Quality Gates (Preview)

The instructor briefly introduces **Quality Gates** at the end of the video. A Quality Gate is a set of **threshold conditions** defined on SonarQube that determine whether code analysis results are acceptable ("Pass") or unacceptable ("Fail"). For example, you might define a Quality Gate that fails if there are more than 0 critical security vulnerabilities, or if code coverage drops below 80%. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

In this demonstration, the default Quality Gate is in place and shows "Pass" despite 5,200+ reliability issues — because the default gate's thresholds do not block on those specific metrics. The instructor says "what does that mean? That will see in the next lecture" — indicating Quality Gate configuration is covered separately. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are building a **Jenkins CI/CD pipeline** that does three things in sequence: (1) fetches source code from GitHub, (2) builds it with Maven, (3) runs unit tests, (4) runs Checkstyle code analysis, and (5) scans the code with SonarQube Scanner and pushes all results (unit tests, code coverage, checkstyle violations) to a **SonarQube server dashboard**. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

This matters because in real-world software development, simply building and deploying code is not enough. You need automated quality checks that run on every build — catching bugs, security vulnerabilities, and code style violations *before* they reach production. The final outcome is a SonarQube dashboard showing a comprehensive quality report for the vprofile project. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

## Step 1: Adding the Checkstyle Analysis Stage to the Pipeline

The instructor starts with an existing pipeline script (from a previous lecture) that already has `Fetch code` and `Build` stages. He opens it in **Sublime Text** and makes two modifications. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

**First**, he moves the **Unit Test** stage to come *after* the Build stage. This is a logical ordering — you build first, then test. The Unit Test stage runs `mvn test`, which executes all unit tests in the project and generates test reports in `target/surefire-reports/`. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

**Second**, he copies the Unit Test stage block, pastes it below, and modifies it to create a new **Checkstyle Analysis** stage. The only changes are:

*   Stage name: changed from `'UNIT TEST'` to `'Checkstyle Analysis'`
*   Command: changed from `sh 'mvn test'` to `sh 'mvn checkstyle:checkstyle'`

 [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

The resulting pipeline at this point (matching [169. PAAC\_Checkstyle.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_Checkstyle.txt?EntityRepresentationId=dc3ebf57-6873-4334-8f34-c9d9b527833a)) looks like: [\[169. PAAC_Checkstyle \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_Checkstyle.txt)

```groovy
pipeline {
    agent any
    tools {
        maven "MAVEN3.9"
        jdk "JDK17"
    }
    stages {
        stage('Fetch code') {
            steps {
                git branch: 'electron', url: 'https://github.com/hkhcoder/vprofile-project.git'
            }
        }
        stage('Build') {
            steps {
                sh 'mvn install -DskipTests'
            }
            post {
                success {
                    echo 'Now Archiving it...'
                    archiveArtifacts artifacts: '**/target/*.war'
                }
            }
        }
        stage('UNIT TEST') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Checkstyle Analysis') {
            steps {
                sh 'mvn checkstyle:checkstyle'
            }
        }
    }
}
```

 [\[169. PAAC_Checkstyle \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_Checkstyle.txt)

The command `mvn checkstyle:checkstyle` tells Maven to execute the `checkstyle` goal from the `checkstyle` plugin. Maven automatically downloads the necessary Checkstyle binaries/dependencies if they are not already cached. The output is written to `target/checkstyle-result.xml`. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

> 🔍 **Deep Dive (Optional)**
>
> Notice the `git branch:` value is `'electron'` in the Checkstyle pipeline and `'atom'` in the final SonarQube pipeline. These are different branches of the same repository (`hkhcoder/vprofile-project`). The instructor likely switches branches between demonstrations. The branch name does not affect the pipeline structure — it only determines which version of the source code is fetched. [\[169. PAAC_Checkstyle \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_Checkstyle.txt), [\[169. PAAC_...deAnalysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_SonarCodeAnalysis.txt)

***

## Step 2: Creating and Running the Checkstyle Job in Jenkins

The instructor copies the entire pipeline script and goes to the **Jenkins dashboard**. He creates a new job: [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

1.  Click **New Item**
2.  Enter the job name: **`Checkstyle`**
3.  Select **Pipeline** as the job type
4.  Click **OK**
5.  Scroll down to the Pipeline section
6.  Paste the pipeline script into the script text area
7.  Click **Save**
8.  Click **Build Now**

He then clicks on **Stages** view to monitor progress and waits for completion. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

**Result:** The Checkstyle stage completes **successfully**. The console output shows:

*   Maven downloading Checkstyle dependencies (binaries required for execution)
*   **641 errors** reported by Checkstyle 9.3

 [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

## Step 3: Examining the Checkstyle Result File in the Workspace

After the build completes, the instructor navigates to the generated result file to demonstrate *why* a dashboard is needed: [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

1.  Go to the **Checkstyle** job page in Jenkins
2.  Click on the first build (Build #1)
3.  Click **Workspace**
4.  Click on the workspace path
5.  Navigate to the **`target`** folder
6.  Find **`checkstyle-result.xml`**
7.  Click **View**

The file opens in the browser, displaying raw XML — hundreds of lines of violation entries with file paths, line numbers, severity levels, and rule names. It is **technically complete** but practically useless for a human trying to understand the overall code quality picture. This is the instructor's key motivation for introducing SonarQube. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

While in the workspace, the instructor also points out other important directories that will be referenced later:

*   **`target/classes/`** — contains compiled Java `.class` files (needed by the sonar scanner as `sonar.java.binaries`)
*   **`target/surefire-reports/`** — contains JUnit test reports (needed as `sonar.junit.reportsPath`)

 [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

## Step 4: Researching the SonarQube Scanner Pipeline Syntax

The instructor searches Google for **"sonar scanner pipeline script"** and examines two sources: [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

**Source 1 — AI (Gemini):** Shows a stage structure with `withSonarQubeEnv`, the tool reference, and the shell command to execute the scanner. It also shows a Quality Gate stage (to be covered later). [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

**Source 2 — Official SonarQube Documentation ("Sonar Scanner for Jenkins"):** Shows the same pattern — stage definition, tool path, `withSonarQubeEnv` wrapping the scanner command, and the SonarQube server name reference. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

The instructor copies the documentation example into his pipeline script and begins modifying it. He also explicitly notes: "you can use any AI tool — GitHub Copilot, ChatGPT, or anything else — and generate the entire pipeline. But that is for later. First, you need to know how to do it yourself manually, one by one. Once you are good with that, then you can definitely use any AI assistant." [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

## Step 5: Building the Sonar Code Analysis Stage

This is the most complex part of the practical. The instructor builds the stage piece by piece, explaining each decision. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

### 5a. Setting the Stage Name

The copied template has a generic name. The instructor changes it to `'Sonar Code analysis'`. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

### 5b. Configuring the Scanner Tool Variable

The original code from documentation uses:

```groovy
def scannerHome = tool 'sonar8.0'
```

The instructor explains that `def` creates a **local variable** scoped to the current block. However, using `def` in a Declarative Pipeline requires wrapping it in a `script { }` block. Instead, the **best practice** is to use the `environment` section: [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

```groovy
environment {
    scannerHome = tool 'sonar8.0'
}
```

The tool name `'sonar8.0'` must **exactly match** the name configured in Jenkins. To verify: navigate to **Manage Jenkins → Tools**, scroll to **SonarQube Scanner installations**, and confirm the name is `sonar8.0` (or whatever you named it). [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

### 5c. Configuring the SonarQube Server Reference

The `withSonarQubeEnv('sonarserver')` block requires the server name to **exactly match** the configuration in Jenkins. To verify: navigate to **Manage Jenkins → System**, scroll to the **SonarQube servers** section, and confirm the name. In this case, the instructor had named it `'sonarserver'`. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

### 5d. Building the Scanner Command with Parameters

The instructor uses **ChatGPT** to generate the scanner command parameters. He asks it to provide the options for uploading Checkstyle results, JaCoCo results, project name, and other details to SonarQube. The AI generates a multi-line command with all necessary `-D` parameters. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

The instructor then customizes the values for the vprofile project:

```bash
${scannerHome}/bin/sonar-scanner \
    -Dsonar.projectKey=vprofile \
    -Dsonar.projectName=vprofile \
    -Dsonar.projectVersion=1.0 \
    -Dsonar.sources=src/ \
    -Dsonar.java.binaries=target/classes \
    -Dsonar.junit.reportsPath=target/surefire-reports \
    -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml \
    -Dsonar.java.checkstyle.reportPaths=target/checkstyle-result.xml
```

 [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt), [\[169. PAAC_...deAnalysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_SonarCodeAnalysis.txt)

Breaking down each parameter:

*   **`${scannerHome}/bin/sonar-scanner`** — The full path to the sonar-scanner executable. `${scannerHome}` resolves to the directory where Jenkins installed the SonarQube Scanner tool.
*   **`-Dsonar.projectKey=vprofile`** — The unique **identifier** for this project on SonarQube. Used internally to track the project across multiple analyses.
*   **`-Dsonar.projectName=vprofile`** — The **display name** shown on the SonarQube dashboard.
*   **`-Dsonar.projectVersion=1.0`** — Version label for this analysis run, useful for tracking quality trends over time.
*   **`-Dsonar.sources=src/`** — Tells the scanner where the **Java source code** lives in the workspace. The vprofile project has its Java code under the `src/` directory.
*   **`-Dsonar.java.binaries=target/classes`** — Points to the **compiled class files**. The scanner needs these for deeper analysis (e.g., detecting unused variables, dead code).
*   **`-Dsonar.junit.reportsPath=target/surefire-reports`** — Path to **JUnit test reports** generated by `mvn test`. Maven's Surefire plugin writes test results here by default.
*   **`-Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml`** — Path to the **JaCoCo code coverage report**. This tells SonarQube what percentage of your code is covered by tests.
*   **`-Dsonar.java.checkstyle.reportPaths=target/checkstyle-result.xml`** — Path to the **Checkstyle result file** we generated in the earlier stage. This is the same XML file that was unreadable in raw form.

 [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

### 5e. Wrapping the Command in `steps` and Using Triple Quotes

The instructor ensures the `withSonarQubeEnv` block is placed **inside** a `steps { }` block (required for every stage in Declarative Pipeline). The shell command itself is wrapped in **triple single quotes** (`'''...'''`) because it spans multiple lines. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

### 5f. The Final Pipeline Script

The complete pipeline (matching [169. PAAC\_SonarCodeAnalysis.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_SonarCodeAnalysis.txt?EntityRepresentationId=996eecf8-0250-4c47-9d2a-4f79e75e6692)): [\[169. PAAC_...deAnalysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_SonarCodeAnalysis.txt)

```groovy
pipeline {
    agent any
    tools {
        maven "MAVEN3.9"
        jdk "JDK17"
    }
    stages {
        stage('Fetch code') {
            steps {
                git branch: 'atom', url: 'https://github.com/hkhcoder/vprofile-project.git'
            }
        }
        stage('Build') {
            steps {
                sh 'mvn install -DskipTests'
            }
            post {
                success {
                    echo 'Now Archiving it...'
                    archiveArtifacts artifacts: '**/target/*.war'
                }
            }
        }
        stage('UNIT TEST') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Checkstyle Analysis') {
            steps {
                sh 'mvn checkstyle:checkstyle'
            }
        }
        stage('Sonar Code analysis') {
            environment {
                scannerHome = tool 'sonar8.0'
            }
            steps {
                withSonarQubeEnv('sonarserver') {
                    sh '''${scannerHome}/bin/sonar-scanner \
                        -Dsonar.projectKey=vprofile \
                        -Dsonar.projectName=vprofile \
                        -Dsonar.projectVersion=1.0 \
                        -Dsonar.sources=src/ \
                        -Dsonar.java.binaries=target/classes \
                        -Dsonar.junit.reportsPath=target/surefire-reports \
                        -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml \
                        -Dsonar.java.checkstyle.reportPaths=target/checkstyle-result.xml'''
                }
            }
        }
    }
}
```

 [\[169. PAAC_...deAnalysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_SonarCodeAnalysis.txt)

> ⚠️ **Expert Note (Optional)**
>
> Be very careful with **opening and closing curly braces**. The instructor explicitly warns about this. The nesting order is: `stage { }` → `steps { }` → `withSonarQubeEnv { }` → `sh '''...'''`. If any brace is mismatched, the pipeline will fail with a syntax error. The instructor suggests downloading the lecture resource file if the indentation becomes confusing while typing manually. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

## Step 6: Creating and Running the Code Analysis Job in Jenkins

The instructor creates a new Jenkins job for the full pipeline: [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

1.  Go to **New Item**
2.  Job name: **`Code Analysis`**
3.  Select **Pipeline**
4.  Click **OK**
5.  Scroll down, paste the complete pipeline script
6.  **Save** and click **Build Now**

He monitors the Stages view. The pipeline executes all five stages sequentially. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

## Step 7: Handling the 502 Bad Gateway Failure

The **first run fails**. The instructor investigates: [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

1.  Clicks on the failed **Sonar Code analysis** stage
2.  Sees a **502 Bad Gateway** error for the SonarQube server URL
3.  Opens the SonarQube **public IP** in the browser — same 502 error
4.  Waits — the SonarQube service had **restarted on its own** (a transient glitch)
5.  After a short while, SonarQube becomes accessible again from the browser
6.  He **reruns** the `Code Analysis` job

The rerun executes the **entire pipeline from scratch** (all five stages), not just the failed stage. This is default Jenkins behavior for Declarative Pipelines — there is no built-in "resume from failed stage" for this pipeline type. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

**Result:** The second run completes **successfully**. The console output at the end shows "analysis successful" with a result URL (using the private IP). [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

> ⚠️ **Expert Note (Optional)**
>
> A 502 Bad Gateway from SonarQube typically means the SonarQube web server (which runs behind a reverse proxy or directly on port 9000) is either starting up, ran out of memory, or crashed. In production environments, you should monitor SonarQube's health and allocate sufficient memory (the default Elasticsearch embedded in SonarQube is memory-hungry). A transient restart like this one is common on smaller instances (e.g., a t2.medium EC2 instance). [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

## Step 8: Verifying Results on the SonarQube Dashboard

After the successful build, the instructor navigates to the SonarQube dashboard: [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

1.  Open the **SonarQube public IP** in the browser
2.  Go to **Projects**
3.  Click on the project named **vprofile** (the name we set via `-Dsonar.projectName`)

The dashboard shows:

*   **3 Security Issues** — potential security vulnerabilities in the code
*   **5,200 Reliability Issues** — code bugs and reliability concerns
*   **25 Security Hotspots** — areas that need manual review for security implications
*   **Overall Status: Pass** — because the default Quality Gate does not block on these metrics

 [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

The instructor tells the viewer to "go through these errors and issues" independently, and says the next lecture will cover creating a **custom Quality Gate** that can enforce stricter thresholds and fail the pipeline if code quality is below standard. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt)

***

## 🔗 How Everything Connects

The full flow of this pipeline forms a **continuous inspection** loop:

    GitHub (source code)
        → Jenkins fetches code
            → Maven builds the project (mvn install -DskipTests)
                → Maven runs unit tests (mvn test) → generates surefire-reports + JaCoCo coverage
                    → Maven runs Checkstyle (mvn checkstyle:checkstyle) → generates checkstyle-result.xml
                        → SonarQube Scanner collects ALL results + scans source code
                            → Pushes everything to SonarQube Server
                                → Dashboard shows human-readable quality report
                                    → Quality Gate decides Pass/Fail (next lecture)

Every stage builds on the output of previous stages. The Build stage compiles classes needed by the scanner. The Unit Test stage generates reports needed by the scanner. The Checkstyle stage generates the XML file needed by the scanner. And the Sonar Code Analysis stage collects all of these and sends them to SonarQube for unified visualization. [\[169.-Code-...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.-Code-Analysis-Demonstration.txt), [\[169. PAAC_...deAnalysis \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/169.%20PAAC_SonarCodeAnalysis.txt)
